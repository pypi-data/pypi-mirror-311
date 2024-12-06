#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import quark.torch.kernel  # noqa

from typing import Optional
import torch
from torch import nn
from quark.torch.quantization.config.type import Dtype
from quark.torch.quantization.config.config import QuantizationSpec
from quark.torch.quantization.nn.modules.quantize_linear import QuantLinear
from quark.torch.quantization.nn.modules.quantize_conv import QuantConv2d
from quark.torch.quantization.nn.modules.mixin import QuantMixin
from quark.shares.utils.log import ScreenLogger
from quark.torch.utils.pack import create_pack_method

logger = ScreenLogger(__name__)

__all__ = ["ExportLinear", "ExportConv2d"]

INT_QUANT_DTYPES = [Dtype.int2, Dtype.int4, Dtype.uint4, Dtype.int8, Dtype.uint8]
AWQ_QUANT_DTYPES = [Dtype.int4, Dtype.uint4, Dtype.int8, Dtype.uint8]


class ExportOperator(nn.Module):

    def init_quant_info(self,
                        quant_module: QuantMixin,
                        reorder: bool = True,
                        custom_mode: Optional[str] = None) -> None:
        if quant_module.weight_qspec is not None and quant_module.weight_quantizer is not None and quant_module.weight_qspec.is_dynamic is False:
            if custom_mode == "awq":
                self.scales = torch.nn.Parameter(quant_module.weight_quantizer.scale.to(torch.float),
                                                 requires_grad=False)
            else:
                self.weight_scale = torch.nn.Parameter(quant_module.weight_quantizer.scale.to(torch.float),
                                                       requires_grad=False)
            if quant_module.weight_qspec.dtype in INT_QUANT_DTYPES:
                self.weight_zero_point = torch.nn.Parameter(quant_module.weight_quantizer.zero_point.to(torch.int),
                                                            requires_grad=False)

            self.weight_quant_min = getattr(quant_module.weight_quantizer, 'quant_min', None)
            self.weight_quant_max = getattr(quant_module.weight_quantizer, 'quant_max', None)

        if quant_module.input_qspec is not None and quant_module.input_quantizer is not None and quant_module.input_qspec.is_dynamic is False:
            self.input_scale = torch.nn.Parameter(quant_module.input_quantizer.scale.to(torch.float),
                                                  requires_grad=False)
            if quant_module.input_qspec.dtype in INT_QUANT_DTYPES:
                self.input_zero_point = torch.nn.Parameter(quant_module.input_quantizer.zero_point.to(torch.int),
                                                           requires_grad=False)

            self.input_quant_min = getattr(quant_module.input_quantizer, 'quant_min', None)
            self.input_quant_max = getattr(quant_module.input_quantizer, 'quant_max', None)

        if quant_module.output_qspec is not None and quant_module.output_quantizer is not None and quant_module.output_qspec.is_dynamic is False:
            self.output_scale = torch.nn.Parameter(quant_module.output_quantizer.scale.to(torch.float),
                                                   requires_grad=False)
            if quant_module.output_qspec.dtype in INT_QUANT_DTYPES:
                self.output_zero_point = torch.nn.Parameter(quant_module.output_quantizer.zero_point.to(torch.int),
                                                            requires_grad=False)

            self.output_quant_min = getattr(quant_module.output_quantizer, 'quant_min', None)
            self.output_quant_max = getattr(quant_module.output_quantizer, 'quant_max', None)

        if quant_module.bias_qspec is not None and quant_module.bias_quantizer is not None and quant_module.bias_qspec.is_dynamic is False:
            self.bias_scale = torch.nn.Parameter(quant_module.bias_quantizer.scale.to(torch.float), requires_grad=False)
            if quant_module.bias_qspec.dtype in INT_QUANT_DTYPES:
                self.bias_zero_point = torch.nn.Parameter(quant_module.bias_quantizer.zero_point.to(torch.int),
                                                          requires_grad=False)

            self.bias_quant_min = getattr(quant_module.bias_quantizer, 'quant_min', None)
            self.bias_quant_max = getattr(quant_module.bias_quantizer, 'quant_max', None)

        self._custom_mode = custom_mode
        self._input_qspec = quant_module.input_qspec
        self._output_qspec = quant_module.output_qspec
        self._weight_qspec = quant_module.weight_qspec
        self._bias_qspec = quant_module.bias_qspec
        self._reorder = reorder

        # self.to_quantized_weight()
        # self.to_quantized_bias()

    @property
    def input_qspec(self) -> Optional[QuantizationSpec]:
        return self._input_qspec

    @property
    def output_qspec(self) -> Optional[QuantizationSpec]:
        return self._output_qspec

    @property
    def weight_qspec(self) -> Optional[QuantizationSpec]:
        return self._weight_qspec

    @property
    def bias_qspec(self) -> Optional[QuantizationSpec]:
        return self._bias_qspec

    @property
    def custom_mode(self) -> Optional[str]:
        return self._custom_mode

    @property
    def weight_scales(self) -> Optional[torch.nn.Parameter]:
        if self.weight_qspec is None:
            return None
        elif self.custom_mode == "awq":
            return self.scales
        else:
            return self.weight_scale

    @weight_scales.setter
    def weight_scales(self, data: torch.Tensor) -> None:
        if self.custom_mode == "awq":
            self.scales.data = data
        else:
            self.weight_scale.data = data

    def to_quantized_weight(self) -> None:
        if (not hasattr(self, "weight")) or (self.weight is None):
            # logger.warning("There is no weight in this module, could not get quantized weight")
            return
        if self.weight_qspec is None:
            # logger.warning("There is no weight quantization info in this module, could not get quantized weight")
            return
        if self.weight_qspec.is_dynamic is not False:
            return

        dtype = self.weight_qspec.dtype.value
        ch_axis = self.weight_qspec.ch_axis
        group_size = self.weight_qspec.group_size
        round_method = getattr(self.weight_qspec.round_method, "value", None)
        qscheme_str_name = getattr(self.weight_qspec.qscheme, "value", None)

        quant_min = self.weight_quant_min
        quant_max = self.weight_quant_max
        scale = self.weight_scales
        zero_point = getattr(self, "weight_zero_point", None)

        res = quark.torch.kernel.real_quantize(  # type: ignore[attr-defined]
            dtype, self.weight if self.weight is None else self.weight.cpu(), scale if scale is None else scale.cpu(),
            zero_point if zero_point is None else zero_point.cpu(), ch_axis, group_size, quant_min, quant_max,
            round_method, qscheme_str_name)
        weight_pack = create_pack_method(qscheme_str_name, self.weight_qspec.dtype.value)
        res = weight_pack.pack(res, self._reorder)
        assert isinstance(res, torch.Tensor)

        if self._custom_mode == "awq":
            self.qweight = torch.nn.Parameter(res, requires_grad=False)
            del self.weight
        else:
            self.weight.data = res.data

    def to_quantized_bias(self) -> None:
        if (not hasattr(self, "bias")) or (self.bias is None):
            # logger.warning("There is no bias in this module, could not get quantized bias")
            return
        if self.bias_qspec is None:
            # logger.warning("There is no bias quantization info in this module, could not get quantized bias")
            return
        if self.bias_qspec.is_dynamic is not False:
            return

        dtype = self.bias_qspec.dtype.value
        ch_axis = self.bias_qspec.ch_axis
        group_size = self.bias_qspec.group_size
        round_method = getattr(self.bias_qspec.round_method, "value", None)
        qscheme_str_name = getattr(self.bias_qspec.qscheme, "value", None)

        quant_min = self.bias_quant_min
        quant_max = self.bias_quant_max
        scale = self.bias_scale
        zero_point = getattr(self, "bias_zero_point", None)
        res = quark.torch.kernel.real_quantize(  # type: ignore[attr-defined]
            dtype, self.bias, scale, zero_point, ch_axis, group_size, quant_min, quant_max, round_method,
            qscheme_str_name)
        assert isinstance(res, torch.Tensor)
        bias_pack = create_pack_method(qscheme_str_name, self.bias_qspec.dtype.value)
        res = bias_pack.pack(res, self._reorder)
        self.bias.data = res.data

    def maybe_to_transposed_scales(self) -> None:

        def scale_transpose(quantization_spec: QuantizationSpec, scales: torch.nn.Parameter) -> None:
            qscheme_str_name = getattr(quantization_spec.qscheme, "value", None)
            if getattr(quantization_spec.dtype, "value", None) is not None:
                pack_method = create_pack_method(qscheme_str_name, quantization_spec.dtype.value)
                scales.data = pack_method.transpose(scales.data)

        if self.weight_scales is not None and self.weight_qspec is not None:
            scale_transpose(self.weight_qspec, self.weight_scales)

        if hasattr(self, "bias_scale") and self.bias_qspec is not None:
            scale_transpose(self.bias_qspec, self.bias_scale)

        if hasattr(self, "input_scale") and self.input_qspec is not None:
            scale_transpose(self.input_qspec, self.input_scale)

        if hasattr(self, "output_scale") and self.output_qspec is not None:
            scale_transpose(self.output_qspec, self.output_scale)

    def to_packed_zero_point(self) -> None:
        if hasattr(self, "weight_zero_point") and self.weight_qspec and hasattr(self.weight_qspec, "dtype"):
            qscheme_str_name = getattr(self.weight_qspec.qscheme, "value", None)
            weight_zero_point_pack = create_pack_method(qscheme_str_name, self.weight_qspec.dtype.value)
            if self.custom_mode == "awq":
                self.qzeros = nn.Parameter(weight_zero_point_pack.pack(self.weight_zero_point, self._reorder),
                                           requires_grad=False)
                del self.weight_zero_point
            else:
                self.weight_zero_point = nn.Parameter(weight_zero_point_pack.pack(self.weight_zero_point,
                                                                                  self._reorder),
                                                      requires_grad=False)

        if hasattr(self, "bias_zero_point") and self.bias_qspec and hasattr(self.bias_qspec, "dtype"):
            qscheme_str_name = getattr(self.bias_qspec.qscheme, "value", None)
            bias_zero_point_pack = create_pack_method(qscheme_str_name, self.bias_qspec.dtype.value)
            self.bias_zero_point = nn.Parameter(bias_zero_point_pack.pack(self.bias_zero_point, self._reorder),
                                                requires_grad=False)

        if hasattr(self, "input_zero_point") and self.input_qspec and hasattr(self.input_qspec, "dtype"):
            qscheme_str_name = getattr(self.input_qspec.qscheme, "value", None)
            input_zero_point_pack = create_pack_method(qscheme_str_name, self.input_qspec.dtype.value)
            self.input_zero_point = nn.Parameter(input_zero_point_pack.pack(self.input_zero_point, self._reorder),
                                                 requires_grad=False)

        if hasattr(self, "output_zero_point") and self.output_qspec and hasattr(self.output_qspec, "dtype"):
            qscheme_str_name = getattr(self.output_qspec.qscheme, "value", None)
            output_zero_point_pack = create_pack_method(qscheme_str_name, self.output_qspec.dtype.value)
            self.output_zero_point = nn.Parameter(output_zero_point_pack.pack(self.output_zero_point, self._reorder),
                                                  requires_grad=False)


class ExportLinear(nn.Linear, ExportOperator):
    """Exporting version of nn.Linear

    """

    def __init__(self, quant_linear: QuantLinear, reorder: bool = True, custom_mode: Optional[str] = None) -> None:
        bias = False if (quant_linear.bias is None) else True
        super(ExportLinear, self).__init__(quant_linear.in_features, quant_linear.out_features, bias)
        self.weight.data = quant_linear.weight.data
        self.weight.requires_grad_(False)
        if quant_linear.bias is not None:
            self.bias.data = quant_linear.bias.data
            self.bias.requires_grad_(False)
        self.init_quant_info(quant_linear, reorder, custom_mode)

    # In the original __init__ function of torch.nn.Linear,
    # the reset_parameters function is called, which takes up a lot of time.
    # This is the reason why inplace ops replacement is slow.
    # Therefore, overload this function in this class to skip the parameter
    # allocation operation, reducing the time of inplace ops replacement.
    def reset_parameters(self) -> None:
        pass


class ExportConv2d(nn.Conv2d, ExportOperator):
    """Exporting version of nn.Conv2d

    """

    def __init__(self, quant_conv2d: QuantConv2d, reorder: bool = True, custom_mode: Optional[str] = None) -> None:
        bias = False if (quant_conv2d.bias is None) else True
        super(ExportConv2d, self).__init__(
            quant_conv2d.in_channels,
            quant_conv2d.out_channels,
            quant_conv2d.kernel_size,  # type: ignore
            quant_conv2d.stride,  # type: ignore
            quant_conv2d.padding,  # type: ignore
            quant_conv2d.dilation,  # type: ignore
            quant_conv2d.groups,
            bias,
            quant_conv2d.padding_mode)
        self.weight.data = quant_conv2d.weight.data
        self.weight.requires_grad_(False)
        if quant_conv2d.bias is not None and self.bias is not None:
            self.bias.data = quant_conv2d.bias.data
            self.bias.requires_grad_(False)
        self.init_quant_info(quant_conv2d, reorder, custom_mode)
