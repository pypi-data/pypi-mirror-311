#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import fnmatch
from typing import List, Optional


def find_patterns_groups(patterns: Optional[List[List[str]]], layer_names: List[str]) -> List[List[str]]:
    pattern_groups: List[List[str]] = []
    if patterns is None:
        return pattern_groups
    for pattern in patterns:
        pattern0 = pattern[0]
        for key in layer_names:
            if fnmatch.fnmatch(key, pattern0):
                word0 = pattern0.replace("*", "")
                key_list = [key]
                for other in pattern[1:]:
                    other_word = other.replace("*", "")
                    other_key = key.replace(word0, other_word)
                    if other_key in layer_names:
                        key_list.append(other_key)
                if key_list and len(key_list) > 0:
                    pattern_groups.append(key_list)
    return pattern_groups
