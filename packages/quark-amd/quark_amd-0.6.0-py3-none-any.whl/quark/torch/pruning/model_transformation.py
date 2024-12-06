#
# Copyright (C) 2024, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import torch
import torch.nn as nn
import numpy as np
from typing import List, Optional, Tuple
from quark.torch.algorithm.utils.utils import clear_memory
from quark.torch.pruning.config import Config
from quark.torch.quantization.utils import set_op_by_name, get_op_by_name
from quark.shares.utils.log import ScreenLogger

logger = ScreenLogger(__name__)


def process_model_pruning(
    model: nn.Module,
    config: Config,
    is_accelerate: Optional[bool],
) -> nn.Module:

    logger.info("Pruning model start.")
    before_pruning_parameters = sum(p.numel() for p in model.parameters())

    device_map = {"": model.device}
    if is_accelerate:
        device_map = model.hf_device_map

    model = model.half().cpu()
    clear_memory()

    pruned_model, pruned_intermediate_size = model_pruning_on_cpu(model, config)

    if config.algo_config is not None and hasattr(config.algo_config, 'mlp_intermediate_size_name'):
        pruned_model.config.__setattr__(config.algo_config.mlp_intermediate_size_name, pruned_intermediate_size)

    del model
    clear_memory()

    after_pruning_parameters = sum(p.numel() for p in pruned_model.parameters())
    logger.info("#Param before pruning: {}, #Param after pruning: {}, Pruning Ratio = {:.4f}%".format(
        before_pruning_parameters, after_pruning_parameters,
        100.0 * after_pruning_parameters / before_pruning_parameters))
    logger.info("Pruning model end.")

    if len(device_map) == 1 and "" in device_map.keys():
        pruned_model = pruned_model.to(device_map[""])
    else:
        for name, module in pruned_model.named_modules(remove_duplicate=False):
            if name in device_map:
                module.to(torch.device(device_map[name])) if isinstance(device_map[name], int) else pruned_model.to(
                    device_map[name])

    return pruned_model


def prune_weights_tool(weights: torch.Tensor, bias: torch.Tensor,
                       mask: List[bool]) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Weight pruning tool that removes weights based on the given mask.

    Parameters:
    weights: np.ndarray - The weight tensor
    bias: np.ndarray - The bias tensor
    mask: List[bool] - A boolean mask indicating which weights to keep

    Returns:
    np.ndarray - The pruned weight tensor
    """

    mask = np.array(mask).astype(bool)  # Ensure the mask is of boolean type

    indices_to_keep = np.where(~mask)[0]  # Find the indices to keep

    if weights.shape[0] == len(mask):
        pruned_weights = weights.T[:, indices_to_keep].T  # Transpose and prune
    elif weights.shape[0] == len(mask) * 2:  # For chatglm3
        pruned_weights = weights.T[:, np.concatenate((indices_to_keep, indices_to_keep))].T  # Transpose and prune
    elif weights.shape[1] == len(mask):
        pruned_weights = weights[:, indices_to_keep]  # Directly prune
    else:
        raise ValueError(
            f"The shape of the weight tensor {weights.shape} does not match the shape of the mask {mask.shape}")

    if bias is not None and bias.shape[0] == len(mask):
        pruned_bias = bias[indices_to_keep]
    else:
        pruned_bias = bias

    return pruned_weights, pruned_bias


def prune_layer(layer: nn.Module, zero_input_channels: List[bool]) -> nn.Module:
    if isinstance(layer, nn.Linear):
        with torch.no_grad():
            weight = layer.weight.data.clone()

            bias = layer.bias.data.clone() if layer.bias is not None else None

            pruned_weights, pruned_bias = prune_weights_tool(weight, bias, zero_input_channels)

            pruned_layer = nn.Linear(pruned_weights.shape[1], pruned_weights.shape[0], bias=(bias is not None))
            pruned_layer.weight.data = pruned_weights.contiguous()
            if bias is not None:
                pruned_layer.bias.data = pruned_bias
            return pruned_layer

    return layer


def model_pruning_on_cpu(model: nn.Module, config: Config) -> Tuple[nn.Module, int]:

    if config.algo_config is not None and hasattr(config.algo_config, 'mlp_pruning_modules') and hasattr(
            config.algo_config, 'mlp_pruning_ratio') and hasattr(config.algo_config, 'mlp_intermediate_size_name'):
        mlp_pruning_module = config.algo_config.mlp_pruning_modules[0]

        pruned_size = int((1 - config.algo_config.mlp_pruning_ratio) *
                          model.config.__getattribute__(config.algo_config.mlp_intermediate_size_name))
    else:
        raise ValueError("Algorithm configuration is not set.")

    for name, module in model.named_modules():

        if mlp_pruning_module in name:

            weights = module.weight.data.cpu().numpy()
            zero_input_channels = np.all(weights == 0, axis=0)

            original_input_channel = weights.shape[1]
            remove_input_channel = sum(zero_input_channels)

            current_pruned_size = int(original_input_channel - remove_input_channel)

            # adjust for opt since opt's activation is relu
            if current_pruned_size < pruned_size:
                diff = pruned_size - current_pruned_size
                for i in range(len(zero_input_channels)):
                    if zero_input_channels[i] is True:
                        zero_input_channels[i] = False
                        diff -= 1
                    if diff == 0:
                        break

            logger.info(
                f"Start pruning layer {name}, original input channel: {original_input_channel} --> pruned input channel {pruned_size}"
            )

            pruned_layer = prune_layer(module, zero_input_channels)

            set_op_by_name(model, name, pruned_layer)

            if config.algo_config is not None and hasattr(config.algo_config, 'mlp_scaling_layers'):
                for prev_name in config.algo_config.mlp_scaling_layers[mlp_pruning_module]:

                    prev_module_name = name.replace(mlp_pruning_module, prev_name)

                    prev_pruned_module = prune_layer(get_op_by_name(model, prev_module_name), zero_input_channels)

                    logger.info(
                        f"Start pruning prev_layer {prev_module_name}, original out channel: {original_input_channel} --> pruned out channel {pruned_size}"
                    )

                    set_op_by_name(model, prev_module_name, prev_pruned_module)

    return model, pruned_size
