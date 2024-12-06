#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
import torch
from torch.fx import GraphModule, Node
# from torch.nn.utils.fusion import fuse_conv_bn_weights
from quark.torch.quantization.graph.torch_utils import is_conv2d_node, is_batchnorm2d_node
from quark.torch.quantization.graph.torch_utils import BATCHNORM_OPS_WO_TRAIN
from quark.torch.quantization.graph.optimization.utils import get_param_and_del_attr, is_all_nodes_save_parameters
from quark.torch.quantization.graph.optimization.utils import replace_ops_module_name_suffix
from quark.torch.quantization.nn.modules.quantize_conv_bn_fused import QuantizedConvBatchNorm2d
from quark.torch.quantization.config.config import QuantizationConfig
from quark.torch.quantization.graph.processor.processor_utils import _is_skip_quant_node
from quark.shares.utils.log import ScreenLogger

logger = ScreenLogger(__name__)


def replace_conv2dbn_quantizedconv_module(m: GraphModule) -> None:
    '''
    replace [ops.aten.conv2d -> ops.aten.cudnn_batch_norm] to QuantizedConvBatchNorm2d(QAT)
    ops.aten.conv2d:
        args: (Tensor input, Tensor weight, Tensor? bias=None, int[2] stride=1, int[2] padding=0, int[2] dilation=1, int groups=1)
        required: [input, weight]
        optional: [bias=None, stride=[1,1], padding=[0,0], dilation=[1,1], groups=1]
    cudnn_batch_norm:
        args: (Tensor input, Tensor weight, Tensor? bias, Tensor? running_mean, Tensor? running_var, bool training, float exponential_average_factor, float epsilon) -> (Tensor, Tensor, Tensor, Tensor)
        required: [input, weight]
        optional: [bias, running_mean, running_var, training]
    '''
    device = [module for module in m.parameters()][0].device  # cpu/gpu
    count_replace_num = 0  # used for track
    recognized_but_not_optimized = 0
    for n in m.graph.nodes:
        if not is_batchnorm2d_node(n):
            continue
        bn_node = n
        maybe_conv_node = bn_node.args[0]
        if not is_conv2d_node(maybe_conv_node):
            continue
        conv_node = maybe_conv_node

        # because we want to delete conv_node, need to check whether other nodes use this conv_node
        if len(conv_node.users) > 1:
            recognized_but_not_optimized += 1
            logger.warning("Conv Node: {} have multi users, skip replace to QuantizedConvBatchNorm2d.".format(
                conv_node.name))
            continue
        # get param
        conv_weight_node = conv_node.args[1]
        conv_bias_node = conv_node.args[2] if len(conv_node.args) > 2 else None

        to_delete_node = [bn_node, conv_node, conv_weight_node]  # need to care order
        if conv_bias_node is not None:
            to_delete_node.append(conv_bias_node)

        skip_quant = True if any(_is_skip_quant_node(node) for node in to_delete_node) else False

        bn_w_node = bn_node.args[1]
        bn_b_node = bn_node.args[2]
        bn_rm_node = bn_node.args[3]
        bn_rv_node = bn_node.args[4]
        to_delete_node += [bn_w_node, bn_b_node, bn_rm_node, bn_rv_node]

        # pre check if conv's weight/bias bn'weight/bias is not parameters, we skip replace
        need_check_node = [conv_weight_node] if conv_bias_node is None else [conv_weight_node, conv_bias_node]
        need_check_node += [bn_w_node, bn_b_node]
        if (not all(isinstance(item, Node)
                    for item in need_check_node)) or (not is_all_nodes_save_parameters(m, need_check_node)):
            logger.warning(
                "Skip replace node: {} and {} to QuantizedConvBatchNorm2d, bacause not all args (Nodes): {} save Parameters."
                .format(conv_node.name, bn_node.name, need_check_node))

            recognized_but_not_optimized += 1
            continue

        # conv and bn param
        conv_weight = get_param_and_del_attr(m, conv_weight_node)
        conv_bias = get_param_and_del_attr(m, conv_bias_node) if conv_bias_node else None
        assert conv_weight is not None

        # init QuantizedConvBatchNorm2d
        # weight shape: out_channel, in_channel/group, kernel_size_0, kernel_size_1
        # conv_node.target._schema.arguments: ['input', 'weight', 'bias', 'stride', 'padding', 'dilation', 'groups']

        conv_groups = conv_node.args[6] if len(
            conv_node.args) >= 7 else conv_node.target._schema.arguments[6].default_value
        conv_out_channels = conv_weight.shape[0]
        conv_in_channels = conv_weight.shape[1] * conv_groups
        conv_kernel_size = conv_weight.shape[2]
        conv_stride = conv_node.args[3] if len(
            conv_node.args) >= 4 else conv_node.target._schema.arguments[3].default_value
        conv_padding = conv_node.args[4] if len(
            conv_node.args) >= 5 else conv_node.target._schema.arguments[4].default_value
        conv_dilation = conv_node.args[5] if len(
            conv_node.args) >= 6 else conv_node.target._schema.arguments[5].default_value

        conv_padding_mode = 'zeros'  # NOTE can not get from graph

        bn_w = get_param_and_del_attr(m, bn_w_node)
        bn_b = get_param_and_del_attr(m, bn_b_node)
        bn_run_m = get_param_and_del_attr(m, bn_rm_node)
        bn_run_v = get_param_and_del_attr(m, bn_rv_node)
        assert isinstance(bn_w, torch.nn.Parameter)
        assert isinstance(bn_b, torch.nn.Parameter)
        # Different ops.aten operations for BN have different function arguments.
        bn_momentum = bn_node.args[5] if bn_node.target in BATCHNORM_OPS_WO_TRAIN else bn_node.args[6]
        bn_eps = bn_node.args[6] if bn_node.target in BATCHNORM_OPS_WO_TRAIN else bn_node.args[7]
        # bn_training = bn_node.args[5]  # not used

        conv_module = QuantizedConvBatchNorm2d(
            conv_in_channels,
            conv_out_channels,
            conv_kernel_size,
            conv_stride,
            conv_padding,
            conv_dilation,
            conv_groups,
            conv_bias_node is not None,  # if bn's running mean is not None, must fold to conv's bias
            conv_padding_mode,
            bn_eps,
            bn_momentum,
            False,
            QuantizationConfig()).to(device=device)
        conv_module.weight = conv_weight
        conv_module.bias = conv_bias
        conv_module.bn.weight = bn_w
        conv_module.bn.bias = bn_b
        conv_module.bn.running_mean = bn_run_m
        conv_module.bn.running_var = bn_run_v
        conv_module.bn.num_batches_tracked = torch.tensor(0,
                                                          device=device) if conv_weight is not None else torch.tensor(0)
        conv_module.bn.momentum = bn_momentum
        conv_module.bn.eps = bn_eps

        input_activation_node = conv_node.args[0]
        convbn_name = conv_node.name + replace_ops_module_name_suffix[type(conv_module)]
        setattr(m, convbn_name, conv_module)
        with m.graph.inserting_after(input_activation_node):
            convbn_node = m.graph.create_node('call_module', convbn_name, (input_activation_node, ), {})
            convbn_node.meta["val"] = conv_node.meta["val"]
            convbn_node.meta["skip_quant"] = skip_quant
            bn_node.next.replace_all_uses_with(convbn_node)
            for next_node in bn_node.users:
                to_delete_node.insert(0, next_node)
        [m.graph.erase_node(node) for node in to_delete_node]
        count_replace_num += 1
    logger.info("Totally replace op.conv2d->op.bn to {} count:\t{}, found but skip: {}".format(
        QuantizedConvBatchNorm2d.__name__, count_replace_num, recognized_but_not_optimized))
    m.graph.eliminate_dead_code()
    m.recompile()
    return
