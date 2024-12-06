#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import os
import unittest
from typing import Any, Union, Optional

from .import_utils import is_torch_available

if is_torch_available():  # pragma: no cover
    # Set env var CUDA_VISIBLE_DEVICES="" to force cpu-mode
    import torch

    torch_device: Optional[Union[str, torch.device]] = None
    if "QUARK_TEST_DEVICE" in os.environ:
        torch_device = os.environ["QUARK_TEST_DEVICE"]

        if torch_device == "cuda" and not torch.cuda.is_available():
            raise ValueError(
                f"QUARK_TEST_DEVICE={torch_device}, but CUDA is unavailable. Please double-check your testing environment."
            )

        try:
            # try creating device to see if provided device is valid
            torch_device = torch.device(torch_device)
        except RuntimeError as e:
            raise RuntimeError(
                f"Unknown testing device specified by environment variable `TRANSFORMERS_TEST_DEVICE`: {torch_device}"
            ) from e
    elif torch.cuda.is_available():
        torch_device = torch.device("cuda")
    else:
        torch_device = torch.device("cpu")
else:  # pragma: no cover
    torch_device = None


def require_torch_gpu(test_case: Any) -> Any:  # pragma: no cover
    """Decorator marking a test that requires CUDA and PyTorch."""
    return unittest.skipUnless(
        isinstance(torch_device, torch.device) and torch_device.type == "cuda", "test requires CUDA")(test_case)
