#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import os
import sys
import torch
from typing import Dict, Any, Tuple, Optional
import torch.nn.functional as F
from quark.onnx.operators.custom_ops import get_library_path
import platform

library_path = os.path.split(get_library_path())[0]
if library_path not in sys.path:
    sys.path.append(library_path)
try:
    import libvai_custom_op_cuda as custom_torch_ops_cuda  # type: ignore
except Exception:
    custom_torch_ops_cuda = None
try:
    if platform.system().lower() == 'windows':
        import vai_custom_op as custom_torch_ops  # type: ignore
    else:
        import libvai_custom_op as custom_torch_ops  # type: ignore

except Exception:
    custom_torch_ops = None


class BFPQuantDequantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: torch.autograd.Function, tensor: torch.Tensor, bit_width: int, block_size: int, rounding_mode: int,
                kernel_version: int) -> Any:
        if tensor.device.type == 'cuda':
            return custom_torch_ops_cuda.bfp(tensor, bit_width, block_size, rounding_mode, kernel_version)
        else:
            return custom_torch_ops.bfp(tensor, bit_width, block_size, rounding_mode, kernel_version)

    @staticmethod  # type: ignore
    def backward(ctx: torch.autograd.Function,
                 grad_output: torch.Tensor) -> Tuple[Optional[torch.Tensor], None, None, None, None, None]:
        grad_input = grad_output.clone()
        return grad_input, None, None, None, None, None


class BFPPrimeQuantDequantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: torch.autograd.Function, tensor: torch.Tensor, bit_width: int, block_size: int,
                sub_block_size: int, sub_block_shift_bits: int, rounding_mode: int) -> Any:
        if tensor.device.type == 'cuda':
            return custom_torch_ops_cuda.bfp_prime(tensor, bit_width, block_size, sub_block_size, sub_block_shift_bits,
                                                   rounding_mode)
        else:
            return custom_torch_ops.bfp_prime(tensor, bit_width, block_size, sub_block_size, sub_block_shift_bits,
                                              rounding_mode)

    @staticmethod  # type: ignore
    def backward(ctx: torch.autograd.Function,
                 grad_output: torch.Tensor) -> Tuple[Optional[torch.Tensor], None, None, None, None, None]:
        grad_input = grad_output.clone()
        return grad_input, None, None, None, None, None


bfp_quant_dequant_func = BFPQuantDequantFunction.apply
bfp_prime_quant_dequant_func = BFPPrimeQuantDequantFunction.apply

# Do not use the common function to replace the autograd function, otherwise it may cause
# "RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn"
# because Torch cannot automatically derive the gradient of the BFP kernel


class BFPQuantizer(torch.nn.Module):
    """ A quantizer has a similar behavior as BFPFixNeuron
    """

    def __init__(self, attrs: Dict[str, Any]) -> None:
        super().__init__()

        self.bfp_method = attrs['bfp_method'] if 'bfp_method' in attrs else 'to_bfp'
        self.axis = attrs['axis'] if 'axis' in attrs else 1
        self.bit_width = attrs['bit_width'] if 'bit_width' in attrs else 16
        self.block_size = attrs['block_size'] if 'block_size' in attrs else 8
        self.sub_block_size = attrs['sub_block_size'] if 'sub_block_size' in attrs else 2
        self.sub_block_shift_bits = attrs['sub_block_shift_bits'] if 'sub_block_shift_bits' in attrs else 2
        self.rounding_mode = attrs['rounding_mode'] if 'rounding_mode' in attrs else 0
        self.convert_to_bfloat_before_bfp = attrs[
            'convert_to_bfloat_before_bfp'] if 'convert_to_bfloat_before_bfp' in attrs else 0
        self.use_compiler_version_cpu_kernel = attrs[
            'use_compiler_version_cpu_kernel'] if 'use_compiler_version_cpu_kernel' in attrs else 0

        # This flag is used to be compatiable with QDQQuantizer
        # For BFP, it's always false
        self.q_folded = False

    def quantize(self, tensor: torch.Tensor) -> torch.Tensor:
        # This function is used to be compatiable with QDQQuantizer
        # For BFP, do not support quantizing a tensor to a bfp tensor yet
        return tensor

    def dequantize(self, tensor: torch.Tensor) -> torch.Tensor:
        # This function is used to be compatiable with QDQQuantizer
        # For BFP, do not support dequantizing a bfp tensor to a float tensor yet
        return tensor

    def quantize_dequantize(self, tensor: torch.Tensor) -> Any:
        if self.bfp_method == 'to_bfp':
            return bfp_quant_dequant_func(tensor, self.bit_width, self.block_size, self.rounding_mode,
                                          self.use_compiler_version_cpu_kernel)
        else:
            return bfp_prime_quant_dequant_func(tensor, self.bit_width, self.block_size, self.sub_block_size,
                                                self.sub_block_shift_bits, self.rounding_mode)

    def forward(self, tensor: torch.Tensor) -> Any:
        # Do nothing for scalar
        if tensor.numel() <= 1:
            return tensor

        # Convert the tensor to bfloat16 before converting to bfp
        if self.convert_to_bfloat_before_bfp == 1:
            bfloat16_tensor = tensor.to(dtype=torch.bfloat16)
            transformed_tensor = bfloat16_tensor.to(dtype=torch.float32)
        else:
            transformed_tensor = tensor

        # Transpose the target axis to the last dimension
        if tensor.dim() > 1 and (self.axis != tensor.dim() - 1 and self.axis != -1):
            transformed_tensor = transformed_tensor.transpose(self.axis, tensor.dim() - 1)

        # Pad the last dimension to make sure it could be divisible by integers
        origin_size = transformed_tensor.shape[-1]
        remainder = origin_size % self.block_size
        pad_size = 0 if remainder == 0 else self.block_size - remainder

        if pad_size > 0:
            transformed_tensor = F.pad(transformed_tensor, (0, pad_size), mode='constant', value=0)

        # Call quant-dequant
        out_tensor = self.quantize_dequantize(transformed_tensor)

        # Remove the padded data
        if pad_size > 0:
            out_tensor = out_tensor[..., :origin_size]

        # Transpose the axis back
        if tensor.dim() > 1 and (self.axis != tensor.dim() - 1 and self.axis != -1):
            out_tensor = out_tensor.transpose(self.axis, tensor.dim() - 1)

        return out_tensor
