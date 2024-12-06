#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
"""Quark Exporting API for PyTorch."""

from __future__ import annotations
import json
import tempfile
from pathlib import Path
from typing import Union, List, Dict, Tuple, Optional, Any
import dataclasses
from tqdm import tqdm
from quark.torch.quantization.utils import set_op_by_name, get_op_by_name
from quark.torch.export.config.quant_config import QuantConfig
from quark.torch.export.main_import.pretrained_config import PretrainedConfig
from quark.torch.export.main_import.safetensors_loader import SafetensorsLoader
from quark.torch.export.main_export.quant_config_parser import get_quant_config
from quark.torch.export.nn.modules.import_operator import ImportLinear

import torch
import torch.nn as nn
from safetensors.torch import save_file
from transformers import AutoTokenizer

from quark.torch.export.config.config import JsonExporterConfig
from quark.torch.quantization.tensor_quantize import ScaledFakeQuantize
from quark.torch.quantization.config.config import Config
from quark.torch.quantization.config.type import QuantizationMode
from quark.torch.export.config.config import ExporterConfig
from quark.torch.export.json_export.builder.llm_info_builder import create_llm_builder
from quark.torch.export.json_export.builder.native_model_info_builder import NativeModelInfoBuilder
from quark.torch.export.json_export.utils.utils import split_model_info
from quark.torch.export.json_export.converter.llm_info_converter import LLMInfoConverter
from quark.torch.export.main_export.model_post_process import ModelPostProcessor
from quark.torch.export.main_export.quant_config_parser import QuantConfigParser
from quark.shares.utils.log import ScreenLogger, log_errors

__all__ = ["ModelExporter", "save_params", "import_model_info"]

logger = ScreenLogger(__name__)


class ModelExporter:
    """
    Provides an API for exporting quantized Pytorch deep learning models.
    This class converts the quantized model to json-safetensors files or onnx graph, and saves to export_dir.

    Args:
        config (ExporterConfig): Configuration object containing settings for exporting.
        export_dir (Union[Path, str]): The target export directory. This could be a string or a pathlib.Path(string) object.
    """

    def __init__(self, config: ExporterConfig, export_dir: Union[Path, str] = tempfile.gettempdir()) -> None:
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.config = config

    def export_model_info(self,
                          model: nn.Module,
                          model_type: str = "",
                          model_dtype: torch.dtype = torch.float16,
                          quant_config: Optional[Config] = None,
                          export_type: Optional[str] = None,
                          tokenizer: AutoTokenizer = None,
                          custom_mode: str = "quark") -> None:
        """
        This function aims to export json and safetensors files of the quantized Pytorch model.

        The model's network architecture or configuration is stored in the json file, and parameters including weight, bias, scale, and zero_point are stored in the safetensors file.

        Parameters:
            model (torch.nn.Module): The quantized model to be exported.
            model_type (str): The type of the model, e.g. gpt2, gptj, llama or gptnext.
            model_dtype (torch.dtype): The weight data type of the quantized model. Default is torch.float16.
            quant_config (Optional[Config]): Configuration object containing settings for quantization. Default is None.
            export_type (Optional[str]): The specific format in which the JSON and safetensors files are stored. Default is None. The file list of the default exporting format is the same as the original HuggingFace file list. On the basis of these files, add quantization information into them. If set to 'vllm-adopt', the exported files are customized for the VLLM compiler. This option is going to be deprecated soon.
            custom_mode (str): Whether to export the quantization config and model in a custom format expected by some downstream library. Possible options:
                - `"quark"`: standard quark format. This is the default and recommended format that should be favored.
                - `"awq"`: targets AutoAWQ library.
                - `"fp8"`: targets vLLM-compatible fp8 models.

        Returns:
            None
        **Examples**:

            .. code-block:: python

                # default exporting:
                export_path = "./output_dir"
                from quark.torch import ModelExporter
                from quark.torch.export.config.config import ExporterConfig, JsonExporterConfig, OnnxExporterConfig
                NO_MERGE_REALQ_CONFIG = JsonExporterConfig(weight_format="real_quantized",
                                                           pack_method="reorder")
                export_config = ExporterConfig(json_export_config=NO_MERGE_REALQ_CONFIG, onnx_export_config=OnnxExporterConfig())
                exporter = ModelExporter(config=export_config, export_dir=export_path)
                exporter.export_model_info(model, quant_config=quant_config)

            .. code-block:: python

                # vllm adopted exporting:
                export_path = "./output_dir"
                from quark.torch import ModelExporter
                from quark.torch.export.config.config import ExporterConfig, JsonExporterConfig, OnnxExporterConfig
                NO_MERGE_REALQ_CONFIG = JsonExporterConfig(weight_format="real_quantized",
                                                           pack_method="reorder")
                export_config = ExporterConfig(json_export_config=NO_MERGE_REALQ_CONFIG, onnx_export_config=OnnxExporterConfig())
                exporter = ModelExporter(config=export_config, export_dir=export_path)
                exporter.export_model_info(model, model_type=model_type, model_dtype=model_dtype, export_type="vllm-adopt")

        Note:
            Currently, default exporting format supports large language models(LLM) in HuggingFace.
            If set to 'vllm-adopt', supported quantization types include fp8, int4_per_group, and w4a8_per_group, and supported models include Llama2-7b, Llama2-13b, Llama2-70b, and Llama3-8b.
        """
        if custom_mode not in ["quark", "fp8", "awq"]:
            raise ValueError(
                f"The supported values for `custom_mode` are {['quark', 'fp8', 'awq', 'auto']} but custom_mode={custom_mode} was provided. Please check your code or open an issue in Quark repository."
            )

        if export_type == "vllm-adopt":
            if model_type == "":
                raise ValueError("model_type should not be empty when exporting vllm-adopt files")
            self._export_vllm_adopt_info(model, model_type, model_dtype)
        else:
            if quant_config is None:
                raise ValueError("quant_config should not be None when exporting default format files")
            self._export_quark_model_info(model, quant_config, tokenizer=tokenizer, custom_mode=custom_mode)

    def _export_vllm_adopt_info(self,
                                model: nn.Module,
                                model_type: str,
                                model_dtype: torch.dtype = torch.float16) -> None:
        logger.info("Start exporting VLLM adopted quantized model ...")
        params_dict: Dict[str, torch.Tensor] = {}

        llm_builder = create_llm_builder(model=model,
                                         model_type=model_type,
                                         model_dtype=model_dtype,
                                         config=self.config.json_export_config)
        model_info = llm_builder.build_model_info()
        info = dataclasses.asdict(model_info)
        split_model_info(info, params_dict)
        converter = LLMInfoConverter(info, params_dict, config=self.config.json_export_config)
        info = converter.convert()

        json_path = self.export_dir / f"{model_type}.json"
        with open(json_path, "w") as f:
            json.dump(info, f, indent=4)

        # handle tensors shared
        data_ptr_list: List[str] = []
        for key, value in params_dict.items():
            if str(value.data_ptr()) in data_ptr_list:
                params_dict[key] = value.clone()
            else:
                data_ptr_list.append(str(value.data_ptr()))

        params_path = self.export_dir / f"{model_type}.safetensors"
        save_file(params_dict, params_path)

        logger.info("VLLM adopted quantized model exported to {} and {} successfully.".format(json_path, params_path))

    def _export_quark_model_info(self,
                                 model: nn.Module,
                                 quant_config: Config,
                                 tokenizer: AutoTokenizer = None,
                                 custom_mode: str = "quark") -> None:
        logger.info("Start exporting json-safetensors quantized model ...")

        quark_quant_config = quant_config.to_dict()
        quantization_config_dict = {}

        config_parser = QuantConfigParser(quant_config, self.config.json_export_config)
        if custom_mode != "quark":
            # Some quantization methods (fp8, awq) might be used in external libraries directly. Quark's `Config` is parsed
            # to detect whether we may add custom keys in the config.json `quantization_config` to make loading quark models
            # in external libraries easier.
            custom_config, inferred_custom_mode = config_parser.get_custom_config()

            if inferred_custom_mode != custom_mode:
                raise ValueError(
                    f"Requested to export the model in the custom mode `{custom_mode}`, but the quantization config used does not appear to match with this `custom_mode`. If using `custom_mode='awq'` or `custom_mode='fp8'`, please make sure the quantization config is well defined to match these custom modes. Alternatively, please use `custom_mode='quark'` or open an issue in Quark repository."
                )

            # This custom_config might be empty.
            if len(custom_config) > 0:
                quantization_config_dict.update(custom_config)
            else:
                quantization_config_dict.update(quark_quant_config)
        else:
            _, inferred_custom_mode = config_parser.get_custom_config()

            if inferred_custom_mode != "quark":
                logger.info(
                    f"The quantized model is being exported in `ModelExporter.export_model_info` with the default `custom_mode='quark'`, which uses the standard format to export quark. However, the `Config` used also matches with the custom_mode `'{inferred_custom_mode}'`, which is not recommended but may temporarily facilitate usage in some downstream libraries. If you would like to use this custom export, please use `ModelExporter.export_model_info(..., custom_mode='{inferred_custom_mode}')`."
                )

            quark_quant_config["export"] = dataclasses.asdict(self.config.json_export_config)
            quantization_config_dict.update(quark_quant_config)

        model.config.update({"quantization_config": quantization_config_dict})

        # Map `QuantLinear` (fake quantization) to `ExportLinear` ("real" quantization, where weights have low precision).
        processor = ModelPostProcessor(model,
                                       self.config.json_export_config,
                                       custom_mode=custom_mode,
                                       output_quant=quant_config.global_quant_config.output_tensors is not None)
        model = processor.process()

        model.save_pretrained(self.export_dir)

        if tokenizer is None and getattr(model.config, "_name_or_path", None):
            try:
                tokenizer = AutoTokenizer.from_pretrained(model.config._name_or_path, trust_remote_code=True)
            except Exception as e:
                logger.warning(f"An error occurred when loading tokenizer: {e}")
        if tokenizer is not None:
            tokenizer.save_pretrained(self.export_dir)
        else:
            logger.warning(
                "Tokenizer is None when exporting Quark model information, so there will not be a tokenizer file in the export directory."
            )

        model.config.__dict__.pop("quantization_config")
        model = processor.reset()
        logger.info("Json-safetensors quantized model exported to {} successfully.".format(self.export_dir))

    def export_onnx_model(self,
                          model: nn.Module,
                          input_args: Union[torch.Tensor, Tuple[float]],
                          input_names: List[str] = [],
                          output_names: List[str] = [],
                          verbose: bool = False,
                          opset_version: Optional[int] = None,
                          do_constant_folding: bool = True,
                          operator_export_type: torch.onnx.OperatorExportTypes = torch.onnx.OperatorExportTypes.ONNX,
                          uint4_int4_flag: bool = False) -> None:
        """
        This function aims to export onnx graph of the quantized Pytorch model.

        Parameters:
            model (torch.nn.Module): The quantized model to be exported.
            input_args (Union[torch.Tensor, Tuple[float]]): Example inputs for this quantized model.
            input_names (List[str]): Names to assign to the input nodes of the onnx graph, in order. Default is empty list.
            output_names (List[str]): Names to assign to the output nodes of the onnx graph, in order. Default is empty list.
            verbose (bool): Flag to control showing verbose log or no. Default is False
            opset_version (Optional[int]): The version of the default (ai.onnx) opset to target. If not set, it will be valued the latest version that is stable for the current version of PyTorch.
            do_constant_folding (bool): Apply the constant-folding optimization. Default is False
            operator_export_type (torch.onnx.OperatorExportTypes): Export operator type in onnx graph. The choices include OperatorExportTypes.ONNX, OperatorExportTypes.ONNX_FALLTHROUGH, OperatorExportTypes.ONNX_ATEN and OperatorExportTypes.ONNX_ATEN_FALLBACK. Default is OperatorExportTypes.ONNX.
            uint4_int4_flag (bool): Flag to indicate uint4/int4 quantized model or not. Default is False.

        Returns:
            None

        **Examples**:

            .. code-block:: python

                from quark.torch import ModelExporter
                from quark.torch.export.config.config import ExporterConfig, JsonExporterConfig
                export_config = ExporterConfig(json_export_config=JsonExporterConfig())
                exporter = ModelExporter(config=export_config, export_dir=export_path)
                exporter.export_onnx_model(model, input_args)

        Note:
            Mix quantization of int4/uint4 and int8/uint8 is not supported currently.
            In other words, if the model contains both quantized nodes of uint4/int4 and uint8/int8, this function cannot be used to export the ONNX graph.
        """
        from quark.torch.export.onnx import convert_model_to_uint4_int4
        logger.info("Start exporting quantized onnx model ...")

        for module in model.modules():
            if isinstance(module, ScaledFakeQuantize):
                module.disable_observer()
                module.enable_fake_quant()
        onnx_path = str(self.export_dir / "quark_model.onnx")
        torch.onnx.export(model.eval(),
                          input_args,
                          onnx_path,
                          verbose=verbose,
                          input_names=input_names,
                          output_names=output_names,
                          opset_version=opset_version,
                          do_constant_folding=do_constant_folding,
                          operator_export_type=operator_export_type)
        if uint4_int4_flag:
            convert_model_to_uint4_int4(onnx_path)
        else:
            logger.info("Quantized onnx model exported to {} successfully.".format(onnx_path))

    def export_gguf_model(self, model: nn.Module, tokenizer_path: Union[str, Path], model_type: str) -> None:
        """
        This function aims to export gguf file of the quantized Pytorch model.

        Parameters:
            model (torch.nn.Module): The quantized model to be exported.
            tokenizer_path (Union[str, Path]): Tokenizer needs to be encoded into gguf model. This argument specifies the directory path of tokenizer which contains tokenizer.json, tokenizer_config.json and/or tokenizer.model
            model_type (str): The type of the model, e.g. gpt2, gptj, llama or gptnext.

        Returns:
            None

        **Examples**:

            .. code-block:: python

                from quark.torch import ModelExporter
                from quark.torch.export.config.config import ExporterConfig, JsonExporterConfig
                export_config = ExporterConfig(json_export_config=JsonExporterConfig())
                exporter = ModelExporter(config=export_config, export_dir=export_path)
                exporter.export_gguf_model(model, tokenizer_path, model_type)

        Note:
            Currently, only support asymetric int4 per_group weight-only quantization, and the group_size must be 32.
            Supported models include Llama2-7b, Llama2-13b, Llama2-70b, and Llama3-8b.
        """

        logger.info("Start exporting gguf quantized model ...")

        save_params(model, model_type, export_dir=self.export_dir)

        json_path = self.export_dir / f"{model_type}.json"
        params_path = self.export_dir / f"{model_type}.safetensors"
        gguf_path = self.export_dir / f"{model_type}.gguf"
        from quark.torch.export.gguf_export.api import convert_exported_model_to_gguf
        convert_exported_model_to_gguf(model_type, json_path, params_path, tokenizer_path, gguf_path)

        if json_path.exists():
            json_path.unlink()
        if params_path.exists():
            params_path.unlink()

        logger.info("GGUF quantized model exported to {} successfully.".format(gguf_path))

    def export_model_info_from_gguf(self, model: nn.Module, gguf_path: str, model_type: str) -> None:

        logger.info("Start exporting quantized model from gguf model ...")

        params_dict: Dict[str, torch.Tensor] = {}
        builder = NativeModelInfoBuilder(model=model, config=self.config.json_export_config)
        info = builder.build_model_info(params_dict)
        from quark.torch.export.gguf_export.api import insert_quant_info_from_gguf
        info, params_dict = insert_quant_info_from_gguf(model_type, info, params_dict, gguf_path)
        json_path = self.export_dir / f"{model_type}_from_gguf.json"
        with open(json_path, "w") as f:
            json.dump(info, f, indent=4)

        # handle tensors shared
        data_ptr_list: List[str] = []
        for key, value in params_dict.items():
            if str(value.data_ptr()) in data_ptr_list:
                params_dict[key] = value.clone()
            else:
                data_ptr_list.append(str(value.data_ptr()))

        params_path = self.export_dir / f"{model_type}_from_gguf.safetensors"
        save_file(params_dict, params_path)

        logger.info("Exported quantized model from gguf model to {} successfully.".format(self.export_dir))


def save_params(model: nn.Module,
                model_type: str,
                args: Optional[Tuple[Any, ...]] = None,
                kwargs: Optional[Dict[str, Any]] = None,
                export_dir: Union[Path, str] = tempfile.gettempdir(),
                quant_mode: QuantizationMode = QuantizationMode.eager_mode) -> None:
    """
    Save the network architecture or configurations and parameters of the quantized model.
    For eager mode quantization, the model's configurations are stored in json file, and parameters including weight, bias, scale, and zero_point are stored in safetensors file.
    For fx_graph mode quantization, the model's network architecture and parameters are stored in pth file.

    Parameters:
        model (torch.nn.Module): The quantized model to be saved.
        model_type (str): The type of the model, e.g. gpt2, gptj, llama or gptnext.
        args (Optional[Tuple[Any, ...]]): Example tuple inputs for this quantized model. Only available for fx_graph mode quantization. Default is None.
        kwargs (Optional[Dict[str, Any]]): Example dict inputs for this quantized model. Only available for fx_graph mode quantization. Default is None.
        export_dir (Union[Path, str]): The target export directory. This could be a string or a pathlib.Path(string) object.
        quant_mode (QuantizationMode): The quantization mode. The choice includes "QuantizationMode.eager_mode" and "QuantizationMode.fx_graph_mode". Default is "QuantizationMode.eager_mode".

    Returns:
        None

    **Examples**:

        .. code-block:: python

            # eager mode:
            from quark.torch import save_params
            save_params(model, model_type=model_type, export_dir="./save_dir")

        .. code-block:: python

            # fx_graph mode:
            from quark.torch.export.api import save_params
            save_params(model,
                        model_type=model_type,
                        args=example_inputs,
                        export_dir="./save_dir",
                        quant_mode=QuantizationMode.fx_graph_mode)
    """
    logger.info("Start saving parameters of quantized model ...")
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    if quant_mode is QuantizationMode.eager_mode:
        params_dict: Dict[str, torch.Tensor] = {}
        builder = NativeModelInfoBuilder(model=model, config=JsonExporterConfig())
        info = builder.build_model_info(params_dict)

        json_path = export_dir / f"{model_type}.json"
        with open(json_path, "w") as f:
            json.dump(info, f, indent=4)

        # handle tensors shared
        data_ptr_list: List[str] = []
        for key, value in params_dict.items():
            if str(value.data_ptr()) in data_ptr_list:
                params_dict[key] = value.clone()
            else:
                data_ptr_list.append(str(value.data_ptr()))

        params_path = export_dir / f"{model_type}.safetensors"
        save_file(params_dict, params_path)
    elif quant_mode is QuantizationMode.fx_graph_mode:
        if args is None:
            raise ValueError("args should not be None when saving fx_graph_mode quantized model")
        model_file_path = export_dir / f"{model_type}_quantized.pth"
        exported_model = torch.export.export(model, args, kwargs=kwargs)
        torch.export.save(exported_model, model_file_path)

    logger.info("Parameters of quantized model saved to {} successfully.".format(export_dir))


@log_errors
def import_model_info(model: nn.Module, model_info_dir: Union[Path, str]) -> nn.Module:
    """
    Instantiate a quantized large language model(LLM) from quark's json-safetensors exporting files.
    The json-safetensors files are exported using "export_model_info" API of ModelExporter class.

    Parameters:
        model (torch.nn.Module): The original HuggingFace large language model.
        model_info_dir (Union[Path, str]): The directory in which the quantized model files are stored.

    Returns:
        nn.Module: The reloaded quantized version of the input model. In this model, the weights of the quantized operators are stored in the real_quantized format.

    **Examples**:

        .. code-block:: python

            from quark.torch import import_model_info
            safetensors_model_dir = "./output_dir/json-safetensors"
            model = import_model_info(model, model_info_dir=safetensors_model_dir)

    Note:
        This function only supports large language models(LLM) of HuggingFace, and does not support dynamic quantized models for now.
    """
    logger.info("Start importing json-safetensors quantized model ...")

    model_config = PretrainedConfig(pretrained_dir=model_info_dir)

    if model_config.quantization_config is None:
        logger.info("This is a non-quantized model")
        return model

    quantization_config = model_config.quantization_config
    custom_mode = quantization_config["quant_method"]

    safetensors_loader = SafetensorsLoader(pretrained_dir=model_info_dir, custom_mode=custom_mode)

    logger.info("Start converting quantized ops")
    for op_name in tqdm(safetensors_loader.ops_name):
        float_module = get_op_by_name(model, op_name)

        op_type = type(float_module)
        quantized, weight_qconfig, bias_qconfig, input_qconfig, output_qconfig = get_quant_config(
            quantization_config, op_type, op_name)
        # quantized, weight_qconfig, bias_qconfig, input_qconfig, output_qconfig = False, None, None, None, None
        if quantized is True and op_type in [nn.Linear]:
            device = float_module.weight.device
            import_module = ImportLinear.from_float(float_module,
                                                    reorder=False if model_config.pack_method == "order" else True,
                                                    quant_algo=model_config.quant_method)  # type: ignore

            if weight_qconfig is not None and len(weight_qconfig) > 0:
                qweight = safetensors_loader.get_tensor(op_name, tensor_type="qweight")
                if qweight is None:
                    raise ValueError(f"Quantized weight of {op_name} does not exist")
                import_module.weight.data = qweight.to(device)

                weight_scale = safetensors_loader.get_tensor(op_name, tensor_type="weight_scale")
                if weight_scale is None:
                    raise ValueError(f"Quantized weight scale of {op_name} does not exist")
                import_module.weight_scale = weight_scale.to(device)

                weight_zero_point = safetensors_loader.get_tensor(op_name, tensor_type="weight_zero_point")
                import_module.weight_zero_point = weight_zero_point.to(  # type: ignore[assignment]
                    device) if weight_zero_point is not None else None

                import_module.weight_qconfig = QuantConfig.from_dict(weight_qconfig)  # type: ignore[assignment]
            else:
                weight_data = safetensors_loader.get_tensor(op_name, tensor_type="weight")
                import_module.weight.data = weight_data.to(device)  # type: ignore[union-attr]

            if bias_qconfig is not None and len(bias_qconfig) > 0 and hasattr(float_module,
                                                                              "bias") and float_module.bias is not None:
                bias_data = safetensors_loader.get_tensor(op_name, tensor_type="bias")
                if bias_data is None:
                    raise ValueError(f"Quantized bias of {op_name} does not exist")
                import_module.bias.data = bias_data.to(device)

                bias_scale = safetensors_loader.get_tensor(op_name, tensor_type="bias_scale")
                if bias_scale is None:
                    raise ValueError(f"Quantized bias scale of {op_name} does not exist")
                import_module.bias_scale = bias_scale.to(device)

                bias_zero_point = safetensors_loader.get_tensor(op_name, tensor_type="bias_zero_point")
                import_module.bias_zero_point = bias_zero_point.to(
                    device) if bias_zero_point is not None else None  # type: ignore[assignment]

                import_module.bias_qconfig = QuantConfig.from_dict(bias_qconfig)  # type: ignore[assignment]
            elif hasattr(float_module, "bias") and float_module.bias is not None:
                bias_data = safetensors_loader.get_tensor(op_name, tensor_type="bias")
                import_module.bias.data = bias_data.to(device)  # type: ignore[union-attr]

            if input_qconfig is not None and len(input_qconfig) > 0:
                input_scale = safetensors_loader.get_tensor(op_name, tensor_type="input_scale")
                if input_scale is None:
                    raise ValueError(f"Quantized input scale of {op_name} does not exist")
                import_module.input_scale = input_scale.to(device)

                input_zero_point = safetensors_loader.get_tensor(op_name, tensor_type="input_zero_point")
                import_module.input_zero_point = input_zero_point.to(
                    device) if input_zero_point is not None else None  # type: ignore[assignment]

                import_module.input_qconfig = QuantConfig.from_dict(input_qconfig)  # type: ignore[assignment]
            if output_qconfig is not None and len(output_qconfig) > 0:
                output_scale = safetensors_loader.get_tensor(op_name, tensor_type="output_scale")
                if output_scale is not None:
                    import_module.output_scale = output_scale.to(device)

                    output_zero_point = safetensors_loader.get_tensor(op_name, tensor_type="output_zero_point")
                    import_module.output_zero_point = output_zero_point.to(  # type: ignore[assignment]
                        device) if output_zero_point is not None else None

                    import_module.output_qconfig = QuantConfig.from_dict(output_qconfig)  # type: ignore[assignment]
            set_op_by_name(model, op_name, import_module)
        else:
            weight_data = safetensors_loader.get_tensor(op_name, tensor_type="weight")
            if weight_data is not None:
                float_module.weight.data = weight_data.to(float_module.weight.device)

            bias_data = safetensors_loader.get_tensor(op_name, tensor_type="bias")
            if hasattr(float_module, "bias") and float_module.bias is not None and bias_data is not None:
                float_module.bias.data = bias_data.to(float_module.bias.device)

    logger.info("Converting quantized ops end")

    logger.info("Json-safetensors quantized model imported successfully.")
    return model
