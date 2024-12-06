#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from __future__ import annotations
import quark.torch.kernel  # noqa
from typing import Optional
import torch
from torch import nn
from quark.torch.utils.pack import create_pack_method
from quark.torch.export.config.quant_config import QuantConfig


class ImportOperator(nn.Module):

    def init_quant_info(self,
                        weight_qconfig: Optional[QuantConfig] = None,
                        weight_scale: Optional[torch.Tensor] = None,
                        weight_zero_point: Optional[torch.Tensor] = None,
                        bias_qconfig: Optional[QuantConfig] = None,
                        bias_scale: Optional[torch.Tensor] = None,
                        bias_zero_point: Optional[torch.Tensor] = None,
                        input_qconfig: Optional[QuantConfig] = None,
                        input_scale: Optional[torch.Tensor] = None,
                        input_zero_point: Optional[torch.Tensor] = None,
                        output_qconfig: Optional[QuantConfig] = None,
                        output_scale: Optional[torch.Tensor] = None,
                        output_zero_point: Optional[torch.Tensor] = None,
                        reorder: bool = True,
                        quant_algo: str = "quark") -> None:
        self.weight_qconfig = weight_qconfig
        self.weight_scale = weight_scale
        self.weight_zero_point = weight_zero_point
        self.bias_qconfig = bias_qconfig
        self.bias_scale = bias_scale
        self.bias_zero_point = bias_zero_point
        self.input_qconfig = input_qconfig
        self.input_scale = input_scale
        self.input_zero_point = input_zero_point
        self.output_qconfig = output_qconfig
        self.output_scale = output_scale
        self.output_zero_point = output_zero_point
        self.reorder = reorder
        self.quant_algo = quant_algo
        self.weight_has_dequantized = False
        self.bias_has_dequantized = False
        self.input_has_unpacked = False
        self.output_has_unpacked = False

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        dtype = input.dtype
        if self.weight_qconfig is not None and self.weight_has_dequantized is False:
            pack_method = create_pack_method(qscheme=self.weight_qconfig.qscheme, dtype=self.weight_qconfig.dtype)
            self.weight.data = pack_method.unpack(self.weight.data, self.reorder)
            if self.weight_scale is None:
                raise ValueError("Weight_scale should not be None if the weight tensor is quantized")
            self.weight_scale = pack_method.transpose(self.weight_scale)
            self.weight_zero_point = None if self.weight_zero_point is None else pack_method.unpack(
                self.weight_zero_point, self.reorder)
            self.weight.data = quark.torch.kernel.dequantize(  # type: ignore[attr-defined]
                self.weight_qconfig.dtype, self.weight.data, self.weight_scale, self.weight_zero_point,
                self.weight_qconfig.ch_axis, self.weight_qconfig.group_size, self.weight_qconfig.qscheme).to(dtype)
            self.weight_has_dequantized = True

        if self.bias is not None and self.bias_qconfig is not None and self.bias_has_dequantized is False:
            pack_method = create_pack_method(qscheme=self.bias_qconfig.qscheme, dtype=self.bias_qconfig.dtype)
            self.bias.data = pack_method.unpack(self.bias.data, self.reorder)
            if self.bias_scale is None:
                raise ValueError("Bias_scale should not be None if the bias tensor is quantized")
            self.bias_scale = pack_method.transpose(self.bias_scale)
            self.bias_zero_point = None if self.bias_zero_point is None else pack_method.unpack(
                self.bias_zero_point, self.reorder)
            self.bias.data = quark.torch.kernel.dequantize(  # type: ignore[attr-defined]
                self.bias_qconfig.dtype, self.bias.data, self.bias_scale, self.bias_zero_point,
                self.bias_qconfig.ch_axis, self.bias_qconfig.group_size, self.bias_qconfig.qscheme).to(dtype)
            self.bias_has_dequantized = True

        if self.input_qconfig is not None:
            pack_method = create_pack_method(qscheme=self.input_qconfig.qscheme, dtype=self.input_qconfig.dtype)
            if self.input_has_unpacked is False:
                self.input_zero_point = None if self.input_zero_point is None else pack_method.unpack(
                    self.input_zero_point, self.reorder)
                if self.input_scale is None:
                    raise ValueError("Input_scale should not be None if the input tensor is quantized")
                self.input_scale = pack_method.transpose(self.input_scale)
                self.input_has_unpacked = True
            input = quark.torch.kernel.scaled_fake_quantize(  # type: ignore[attr-defined]
                self.input_qconfig.dtype, input, self.input_scale, self.input_zero_point, self.input_qconfig.ch_axis,
                self.input_qconfig.group_size, self.input_qconfig.quant_min, self.input_qconfig.quant_max,
                self.input_qconfig.round_method, self.input_qconfig.qscheme, None).to(dtype)

        output = self.func_method(input)

        if self.output_qconfig is not None:
            pack_method = create_pack_method(qscheme=self.output_qconfig.qscheme, dtype=self.output_qconfig.dtype)
            if self.output_has_unpacked is False:
                self.output_zero_point = None if self.output_zero_point is None else pack_method.unpack(
                    self.output_zero_point, self.reorder)
                if self.output_scale is None:
                    raise ValueError("Output_scale should not be None if the output tensor is quantized")
                self.output_scale = pack_method.transpose(self.output_scale)
                self.output_has_unpacked = True
            output = quark.torch.kernel.scaled_fake_quantize(  # type: ignore[attr-defined]
                self.output_qconfig.dtype, output, self.output_scale, self.output_zero_point,
                self.output_qconfig.ch_axis, self.output_qconfig.group_size, self.output_qconfig.quant_min,
                self.output_qconfig.quant_max, self.output_qconfig.round_method, self.output_qconfig.qscheme,
                None).to(dtype)
        return output

    def func_method(self, input: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError("This method should be overridden by subclasses")


class ImportLinear(nn.Linear, ImportOperator):

    def __init__(self,
                 in_features: int,
                 out_features: int,
                 device: torch.device,
                 bias: bool,
                 weight_qconfig: Optional[QuantConfig] = None,
                 weight_scale: Optional[torch.Tensor] = None,
                 weight_zero_point: Optional[torch.Tensor] = None,
                 bias_qconfig: Optional[QuantConfig] = None,
                 bias_scale: Optional[torch.Tensor] = None,
                 bias_zero_point: Optional[torch.Tensor] = None,
                 input_qconfig: Optional[QuantConfig] = None,
                 input_scale: Optional[torch.Tensor] = None,
                 input_zero_point: Optional[torch.Tensor] = None,
                 output_qconfig: Optional[QuantConfig] = None,
                 output_scale: Optional[torch.Tensor] = None,
                 output_zero_point: Optional[torch.Tensor] = None,
                 reorder: bool = True,
                 quant_algo: str = "quark"):
        super(ImportLinear, self).__init__(in_features, out_features, bias)
        self.device = device
        self.init_quant_info(weight_qconfig=weight_qconfig,
                             weight_scale=weight_scale,
                             weight_zero_point=weight_zero_point,
                             bias_qconfig=bias_qconfig,
                             bias_scale=bias_scale,
                             bias_zero_point=bias_zero_point,
                             input_qconfig=input_qconfig,
                             input_scale=input_scale,
                             input_zero_point=input_zero_point,
                             output_qconfig=output_qconfig,
                             output_scale=output_scale,
                             output_zero_point=output_zero_point,
                             reorder=reorder,
                             quant_algo=quant_algo)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return ImportOperator.forward(self, input)

    # In the original __init__ function of torch.nn.Linear,
    # the reset_parameters function is called, which takes up a lot of time.
    # This is the reason why inplace ops replacement is slow.
    # Therefore, overload this function in this class to skip the parameter
    # allocation operation, reducing the time of inplace ops replacement.
    def reset_parameters(self) -> None:
        pass

    def func_method(self, input: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.linear(input, self.weight, self.bias)

    @classmethod
    def from_float(cls, float_module: nn.Module, reorder: bool = True, quant_algo: str = "quark") -> nn.Linear:
        bias = False if float_module.bias is None else True
        import_linear = cls(in_features=float_module.in_features,
                            out_features=float_module.out_features,
                            device=float_module.weight.device,
                            bias=bias,
                            reorder=reorder,
                            quant_algo=quant_algo)

        import_linear.weight = float_module.weight
        import_linear.weight.requires_grad_(False)

        import_linear.bias = float_module.bias
        if import_linear.bias is not None:
            import_linear.bias.requires_grad_(False)
        return import_linear
