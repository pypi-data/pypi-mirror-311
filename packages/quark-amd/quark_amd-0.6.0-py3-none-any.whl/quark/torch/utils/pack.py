#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from typing import Optional, TypeVar
import torch

T = TypeVar('T', bound='PackMethod')


class PackMethod:

    def __init__(self, qscheme: Optional[str], dtype: str) -> None:
        self.qscheme = qscheme
        self.dtype = dtype

    def pack(self, to_pack: torch.Tensor, reorder: bool) -> torch.Tensor:
        return to_pack

    def unpack(self, to_unpack: torch.Tensor, reorder: bool) -> torch.Tensor:
        return to_unpack

    def transpose(self, tensor: torch.Tensor) -> torch.Tensor:
        return tensor


class Pack_4_bits(PackMethod):

    def __init__(self, qscheme: Optional[str], dtype: str) -> None:
        super().__init__(qscheme, dtype)

    def pack(self, to_pack: torch.Tensor, reorder: bool = True) -> torch.Tensor:
        if to_pack.ndim > 2:
            raise ValueError("Pack: Only supports tensors with dimensions not greater than 2.")
        if self.qscheme == "per_group":
            to_pack = to_pack.t().contiguous()

        if reorder:
            order_map = [0, 2, 4, 6, 1, 3, 5, 7]
        else:
            order_map = [0, 1, 2, 3, 4, 5, 6, 7]
        pack_num = 8
        if to_pack.ndim == 2:
            packed = torch.zeros(to_pack.shape[0],
                                 to_pack.shape[1] // pack_num,
                                 dtype=torch.int32,
                                 device=to_pack.device)
            new_c = to_pack.shape[1] // pack_num
            for c in range(new_c):
                for i in range(pack_num):
                    # Use -3 as an example, high_position is 11111111,cause bit_or generate errors, so we can't use int4 directly
                    packed_col = to_pack[:, c * pack_num + order_map[i]]
                    if self.dtype == "int4":
                        packed_col = packed_col & 0x0F
                    packed[:, c] = torch.bitwise_or(packed[:, c], torch.bitwise_left_shift(packed_col, i * 4))
        else:
            packed = torch.zeros(to_pack.shape[0] // pack_num, dtype=torch.int32, device=to_pack.device)
            new_c = to_pack.shape[0] // pack_num
            for c in range(new_c):
                for i in range(pack_num):
                    # Use -3 as an example, high_position is 11111111,cause bit_or generate errors, so we can't use int4 directly
                    packed_col = to_pack[c * pack_num + order_map[i]]
                    if self.dtype == "int4":
                        packed_col = packed_col & 0x0F
                    packed[c] = torch.bitwise_or(packed[c], torch.bitwise_left_shift(packed_col, i * 4))

        return packed

    def unpack(self, to_unpack: torch.Tensor, reorder: bool = True) -> torch.Tensor:
        if to_unpack.ndim > 2:
            raise ValueError("Unpack: Only supports tensors with dimensions not greater than 2.")

        shifts = torch.tensor([0, 4, 8, 12, 16, 20, 24, 28], device=to_unpack.device)
        ORDER = [0, 4, 1, 5, 2, 6, 3, 7]
        if to_unpack.ndim == 2:
            unpacked = (to_unpack.unsqueeze(-1) >> shifts.view(1, 1, -1)).view(to_unpack.shape[0], -1).to(torch.int8)
            if reorder:
                order_tensor = torch.arange(
                    unpacked.shape[-1],
                    dtype=torch.int32,
                    device=unpacked.device,
                )
                order_tensor = order_tensor.view(-1, 8)
                order_tensor = order_tensor[:, ORDER].view(-1)
                unpacked = unpacked[:, order_tensor]

        elif to_unpack.ndim == 1:
            unpacked = (to_unpack.unsqueeze(-1) >> shifts.view(1, -1)).view(-1).to(torch.int8)
            if reorder:
                order_tensor = torch.arange(
                    unpacked.shape[-1],
                    dtype=torch.int32,
                    device=unpacked.device,
                )
                order_tensor = order_tensor.view(-1, 8)
                order_tensor = order_tensor[:, ORDER].view(-1)
                unpacked = unpacked[order_tensor]

        unpacked &= 0b1111
        # Use -3 as an example, we have to restore 00001101 to 11111101, so we can check the fourth digit of the unzipped number,
        # and if the fourth digit == 1 it proves that the number is negative
        if self.dtype == "int4":
            mask = (unpacked & 0x08).bool()
            unpacked[mask] = unpacked[mask] | 0xF0

        if self.qscheme == "per_group":
            unpacked = unpacked.t().contiguous()

        return unpacked

    def transpose(self, tensor: torch.Tensor) -> torch.Tensor:
        if tensor.ndim > 2:
            raise ValueError("Only supports tensors with dimensions not greater than 2.")
        if self.qscheme == "per_group":
            tensor = tensor.t().contiguous()
        return tensor


class Pack_8_bits(PackMethod):

    def __init__(self, qscheme: Optional[str], dtype: str) -> None:
        super().__init__(qscheme, dtype)

    def pack(self, to_pack: torch.Tensor, reorder: bool) -> torch.Tensor:
        if self.dtype == "uint8":
            return to_pack.to(torch.uint8).contiguous()
        else:
            return to_pack.to(torch.int8).contiguous()

    def unpack(self, to_unpack: torch.Tensor, reorder: bool) -> torch.Tensor:
        return to_unpack.to(torch.int32).contiguous()


def create_pack_method(qscheme: Optional[str], dtype: str) -> PackMethod:
    if dtype == "int4" or dtype == "uint4":
        return Pack_4_bits(qscheme, dtype)
    elif dtype == "int8" or dtype == "uint8":
        return Pack_8_bits(qscheme, dtype)
    else:
        return PackMethod(qscheme, dtype)
