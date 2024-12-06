#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from typing import Dict, List

from tqdm import tqdm
import torch
import torch.nn as nn
from quark.torch.quantization.nn.modules.quantize_linear import QuantLinear
from quark.torch.export.config.config import JsonExporterConfig
from quark.torch.export.nn.modules.export_operator import ExportLinear, ExportOperator
from quark.torch.quantization.utils import set_op_by_name, get_op_by_name
from quark.torch.export.utils import find_patterns_groups
from quark.shares.utils.log import ScreenLogger

logger = ScreenLogger(__name__)


class ModelPostProcessor:

    def __init__(self, model: nn.Module, export_config: JsonExporterConfig, custom_mode: str,
                 output_quant: bool) -> None:
        self._model = model
        self._config = export_config
        self.custom_mode = custom_mode
        self.output_quant = output_quant
        self._name_module_map: Dict[str, nn.Module] = {}

    @property
    def model(self) -> nn.Module:
        return self._model

    def process(self) -> nn.Module:
        logger.info("Model post process start.")

        logger.info("Simplifying quantized operators...")
        reorder = True if self._config.pack_method == "reorder" else False
        named_modules = dict(self._model.named_modules(remove_duplicate=False))
        for name, module in tqdm(named_modules.items()):
            if isinstance(module, QuantLinear):
                self._name_module_map[name] = module
                export_linear = ExportLinear(module, reorder, self.custom_mode)
                set_op_by_name(self._model, name, export_linear)

        if self._config.weight_merge_groups and len(self._config.weight_merge_groups) > 0:
            self._virtual_merge_weight_matrix()

        if (self._config.kv_cache_group is not None) and (len(self._config.kv_cache_group) > 0):
            self._insert_kv_scale()

        if self._config.weight_format == "real_quantized":
            logger.info("Doing real quantization for operators...")
            named_modules = dict(self._model.named_modules(remove_duplicate=False))
            for name, module in tqdm(named_modules.items()):
                if isinstance(module, ExportOperator):
                    module.to_quantized_weight()
                    module.to_quantized_bias()
                    # For int4/uint4 per_group quantization, the scale need to be transposed.
                    # In this maybe_to_transposed_scales function, the scales of int4/uint4 per_group
                    # quantization are transposed while the others remain the original shape.
                    module.maybe_to_transposed_scales()
                    module.to_packed_zero_point()

        named_modules = dict(self._model.named_modules(remove_duplicate=False))
        has_dbrx_experts = any(module.__class__.__name__ == "DbrxExperts_" for module in named_modules.values())
        if has_dbrx_experts:
            self._merge_params_for_DbrxExperts()

        logger.info("Model post process end")
        return self._model

    def reset(self) -> nn.Module:
        if hasattr(self, "name_dbrxexperts_map"):
            for name, module in self.name_dbrxexperts_map.items():
                set_op_by_name(self._model, name, module)

        logger.info("Resetting model to frozen model...")
        for name, module in self._name_module_map.items():
            set_op_by_name(self._model, name, module)
        return self._model

    def _virtual_merge_weight_matrix(self) -> None:
        named_modules = dict(self._model.named_modules(remove_duplicate=False))
        names = list(named_modules.keys())
        merge_groups = find_patterns_groups(self._config.weight_merge_groups, names)

        for merge_group in merge_groups:
            module_merge_group = [get_op_by_name(self._model, name) for name in merge_group]
            self._merge_scaling_factor(module_merge_group)

    def _merge_scaling_factor(self, module_group: List[nn.Module]) -> None:
        weight_quant_or_not = all(getattr(module, "weight_qspec", None) is not None for module in module_group)
        if not weight_quant_or_not:
            return
        static_quant_or_not = all(module.weight_qspec.is_dynamic is False for module in module_group)
        if not static_quant_or_not:
            return
        per_tensor_or_not = all(module.weight_qspec.qscheme.name == "per_tensor" for module in module_group)
        if not per_tensor_or_not:
            return
        zero_point_or_not = all(
            (hasattr(module, "weight_zero_point") and module.weight_zero_point is not None) for module in module_group)
        if zero_point_or_not:
            symmetric_quant_or_not = all(torch.all(module.weight_zero_point == 0) for module in module_group)
            if not symmetric_quant_or_not:
                return

        weight_scale_list = [module.weight_scales for module in module_group]

        group_weight_scale = torch.stack(weight_scale_list, ).max(dim=0).values

        for module in module_group:
            module.weight_scales = group_weight_scale.cpu().clone()

        output_quant_or_not = all(getattr(module, "output_qspec", None) is not None for module in module_group)
        if not output_quant_or_not:
            return
        static_quant_or_not = all(module.output_qspec.is_dynamic is False for module in module_group)
        if not static_quant_or_not:
            return
        per_tensor_or_not = all(module.output_qspec.qscheme.name == "per_tensor" for module in module_group)
        if not per_tensor_or_not:
            return
        zero_point_or_not = all(
            (hasattr(module, "output_zero_point") and module.output_zero_point is not None) for module in module_group)
        if zero_point_or_not:
            symmetric_quant_or_not = all(torch.all(module.output_zero_point == 0) for module in module_group)
            if not symmetric_quant_or_not:
                return

        output_scale_list = [module.output_scale for module in module_group]

        group_output_scale = torch.stack(output_scale_list, ).max(dim=0).values

        for module in module_group:
            module.output_scale.data = group_output_scale.cpu().clone()

    def _insert_kv_scale(self) -> None:
        named_modules = dict(self._model.named_modules(remove_duplicate=False))
        names = list(named_modules.keys())
        kv_groups = find_patterns_groups([self._config.kv_cache_group], names)

        for kv_group in kv_groups:
            kv_modules = [get_op_by_name(self._model, name) for name in kv_group]
            self._build_kv_scale(kv_group, kv_modules)

    def _build_kv_scale(self, module_names: List[str], module_group: List[nn.Module]) -> None:
        output_quant_or_not = all(getattr(module, "output_qspec", None) is not None for module in module_group)
        if not output_quant_or_not:
            return
        static_quant_or_not = all(module.output_qspec.is_dynamic is False for module in module_group)
        if not static_quant_or_not:
            return
        per_tensor_or_not = all(module.output_qspec.qscheme.name == "per_tensor" for module in module_group)
        if not per_tensor_or_not:
            return
        zero_point_or_not = all(
            (hasattr(module, "output_zero_point") and module.output_zero_point is not None) for module in module_group)
        if zero_point_or_not:
            symmetric_quant_or_not = all(torch.all(module.output_zero_point == 0) for module in module_group)
            if not symmetric_quant_or_not:
                return

        output_scale_list = [module.output_scale for module in module_group]
        kv_scale = torch.stack(output_scale_list, ).max(dim=0).values
        if self.output_quant is False:
            for module in module_group:
                del module.output_scale

        parent_module_name = ".".join(module_names[0].split(".")[:-1])
        parent_module = get_op_by_name(self._model, parent_module_name)
        parent_module.kv_scale = torch.nn.Parameter(kv_scale, requires_grad=False)

    def _merge_params_for_DbrxExperts(self) -> None:
        named_modules = dict(self._model.named_modules(remove_duplicate=False))
        self.name_dbrxexperts_map: Dict[str, nn.Module] = {}
        for name, module in tqdm(named_modules.items()):
            if module.__class__.__name__ == "DbrxExperts_":
                export_experts = torch.nn.Module()
                export_experts.mlp = torch.nn.Module()

                w1_weight_tensors = [expert.w1.weight for expert in module.mlp]
                w1_weight_concat = torch.cat(w1_weight_tensors)
                export_experts.mlp.w1_weight = torch.nn.Parameter(w1_weight_concat, requires_grad=False)

                if hasattr(module.mlp[0].w1, "weight_scale"):
                    w1_weight_scale_tensors = [expert.w1.weight_scale for expert in module.mlp]
                    w1_weight_scale_concat = torch.stack(w1_weight_scale_tensors)
                    export_experts.mlp.w1_weight_scale = torch.nn.Parameter(w1_weight_scale_concat, requires_grad=False)

                if hasattr(module.mlp[0].w1, "input_scale"):
                    w1_input_scale_tensors = [expert.w1.input_scale for expert in module.mlp]
                    w1_input_scale_concat = torch.stack(w1_input_scale_tensors)
                    export_experts.mlp.w1_input_scale = torch.nn.Parameter(w1_input_scale_concat, requires_grad=False)

                if hasattr(module.mlp[0].w1, "output_scale"):
                    w1_output_scale_tensors = [expert.w1.output_scale for expert in module.mlp]
                    w1_output_scale_concat = torch.stack(w1_output_scale_tensors)
                    export_experts.mlp.w1_output_scale = torch.nn.Parameter(w1_output_scale_concat, requires_grad=False)

                v1_weight_tensors = [expert.v1.weight for expert in module.mlp]
                v1_weight_concat = torch.cat(v1_weight_tensors)
                export_experts.mlp.v1_weight = torch.nn.Parameter(v1_weight_concat, requires_grad=False)

                if hasattr(module.mlp[0].v1, "weight_scale"):
                    v1_weight_scale_tensors = [expert.v1.weight_scale for expert in module.mlp]
                    v1_weight_scale_concat = torch.stack(v1_weight_scale_tensors)
                    export_experts.mlp.v1_weight_scale = torch.nn.Parameter(v1_weight_scale_concat, requires_grad=False)

                if hasattr(module.mlp[0].v1, "input_scale"):
                    v1_input_scale_tensors = [expert.v1.input_scale for expert in module.mlp]
                    v1_input_scale_concat = torch.stack(v1_input_scale_tensors)
                    export_experts.mlp.v1_input_scale = torch.nn.Parameter(v1_input_scale_concat, requires_grad=False)

                if hasattr(module.mlp[0].v1, "output_scale"):
                    v1_output_scale_tensors = [expert.v1.output_scale for expert in module.mlp]
                    v1_output_scale_concat = torch.stack(v1_output_scale_tensors)
                    export_experts.mlp.v1_output_scale = torch.nn.Parameter(v1_output_scale_concat, requires_grad=False)

                # transpose w2.weight back when exporting dbrx model
                w2_weight_tensors = [expert.w2.weight.t() for expert in module.mlp]
                w2_weight_concat = torch.cat(w2_weight_tensors)
                export_experts.mlp.w2_weight = torch.nn.Parameter(w2_weight_concat, requires_grad=False)

                if hasattr(module.mlp[0].w2, "weight_scale"):
                    w2_weight_scale_tensors = [expert.w2.weight_scale for expert in module.mlp]
                    w2_weight_scale_concat = torch.stack(w2_weight_scale_tensors)
                    export_experts.mlp.w2_weight_scale = torch.nn.Parameter(w2_weight_scale_concat, requires_grad=False)

                if hasattr(module.mlp[0].w2, "input_scale"):
                    w2_input_scale_tensors = [expert.w2.input_scale for expert in module.mlp]
                    w2_input_scale_concat = torch.stack(w2_input_scale_tensors)
                    export_experts.mlp.w2_input_scale = torch.nn.Parameter(w2_input_scale_concat, requires_grad=False)

                if hasattr(module.mlp[0].w2, "output_scale"):
                    w2_output_scale_tensors = [expert.w2.output_scale for expert in module.mlp]
                    w2_output_scale_concat = torch.stack(w2_output_scale_tensors)
                    export_experts.mlp.w2_output_scale = torch.nn.Parameter(w2_output_scale_concat, requires_grad=False)
                set_op_by_name(self._model, name, export_experts)
                self.name_dbrxexperts_map[name] = module
