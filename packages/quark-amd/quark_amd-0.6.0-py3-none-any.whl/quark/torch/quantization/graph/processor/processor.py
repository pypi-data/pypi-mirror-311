#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
import types
import torch.fx
from torch.fx import Node
from typing import Callable, Optional, List, Dict
from quark.torch.quantization.config.config import QuantizationConfig, Config
# Graph
from quark.torch.quantization.graph.optimization.replace_linear_to_qtlinear import replace_linear_qtlinear
from quark.torch.quantization.graph.optimization.replace_conv2d_to_qtconv2d import replace_conv2d_qtconv2d
from quark.torch.quantization.graph.optimization.replace_conv_bn_to_qt_model import replace_conv2dbn_quantizedconv_module
from quark.torch.quantization.graph.optimization.replace_convtranspose2d_to_qtconvtranspose2d import replace_convtranspose2d_qtconvtranspose2d
from quark.torch.quantization.graph.optimization.modify_reshape_param import modify_reshape_param
from quark.torch.quantization.graph.processor.insert_quantizer import insert_quantizer
from quark.torch.quantization.graph.processor.processor_utils import _convert_scalars_to_attrs
from quark.torch.quantization.graph.processor.processor_utils import OP_TO_ANNOTATOR
from quark.torch.quantization.graph.processor.processor_utils import propagate_annotation
from quark.torch.quantization.graph.torch_utils import allow_exported_model_train_eval
from torch.ao.quantization.pt2e.utils import _get_tensor_constant_from_node
from quark.torch.quantization.graph.torch_utils import LINEAR_OPS, CONV1D_OPS, CONV2D_OPS, BATCHNORM_OPS
from quark.torch.quantization.nn.modules.quantize_conv_bn_fused import QuantizedConvBatchNorm2d
# from quark.torch.quantization.graph.optimization.remove_dropout_node import RemoveDropoutNode
from quark.shares.utils.log import DebugLogger, ScreenLogger
# from torch.ao.quantization.pt2e.utils import _get_node_name_to_scope
in_place_replace_ops = DebugLogger(name="in_place_replace_ops")
logger = ScreenLogger(__name__)

STATIC_OPS = [
    "quantized_convbn_act",  # include [QuantLinear, QuantizedConvBatchNorm2d, QuantConv2d, QuantConvTranspose2d]
    "convlike_act",
    "add_act",
    'quantized_convbn_wo_act',  # include [QuantLinear, QuantizedConvBatchNorm2d, QuantConv2d, QuantConvTranspose2d]
    "convlike",
    "avg_pool2d",  # include torch.nn.{Adaptive}AvgPool2d, F.{adaptive_}avg_pool2d
    "max_pool2d",
    "element_arithmetic",  # elementary arithmetic: addition(+), subtraction(-), multiplication(*), division(/).
    'mean',
    'sum',  # the sum of all elements in input tensor.
    # activation
    'hardtanh',
    'relu_act',  # nn.{ReLU, ReLU6}, functional.{relu, relu6}
    'sigmoid',
    'softmax',
    # concat
    'cat',
    # shape
    'shape_change',  # ops.aten.(reshpe, permute,unsqueeze,squeeze)
]


def _share_weight_check(model: torch.fx.GraphModule) -> List[str]:
    '''
    In some models, like coat_tiny(in TIMM), some components may used over one time.
    This causes the parsed graph to contain multi conv/linear/bn use shared weight/bias.
    This function will pick out the names of the operations that used shared weights/biases.
    '''
    skip_op_list = []
    # The parameters' names are always weight and bias, and are positioned in indexes 1 and 2.
    need_check_opeartion = LINEAR_OPS + CONV1D_OPS + CONV2D_OPS + BATCHNORM_OPS
    param_name_count: Dict[str, int] = {}
    node_param_list: Dict[str, List[str]] = {}
    for n in model.graph.nodes:
        if n.op != "call_function" or n.target not in need_check_opeartion:
            continue

        opeartion_node = n
        # using index 1 to fetch weight is effective for linear, conv2d, batch_norm
        weight_node = opeartion_node.args[1]
        # using index 2 to fetch bias is effective for linear, conv2d, batch_norm
        bias_node = opeartion_node.args[2] if len(opeartion_node.args) > 2 else None
        node_param_list[opeartion_node.name] = []
        if isinstance(weight_node, Node) and weight_node.op == "get_attr" and isinstance(
                _get_tensor_constant_from_node(weight_node, model),  # type: ignore [no-untyped-call]
                torch.nn.Parameter):
            weight_name = weight_node.target
            param_name_count[
                weight_name] = 1 if weight_name not in param_name_count else param_name_count[weight_name] + 1
            node_param_list[opeartion_node.name].append(weight_name)
        if bias_node is not None and isinstance(bias_node, Node) and bias_node.op == "get_attr" and isinstance(
                _get_tensor_constant_from_node(bias_node, model), torch.nn.Parameter):  # type: ignore [no-untyped-call]
            bias_name = bias_node.target
            param_name_count[bias_name] = 1 if bias_name not in param_name_count else param_name_count[bias_name] + 1
            node_param_list[opeartion_node.name].append(bias_name)

    for node_name, params_name_list in node_param_list.items():
        for param_name in params_name_list:
            if param_name_count[param_name] > 1:
                skip_op_list.append(node_name)
                break

    return skip_op_list


def _quant_optimize(model: torch.fx.GraphModule) -> torch.fx.GraphModule:
    '''
        using QuantizedConvBatchNorm2d can let training process more stable and quantizer more easily,
        [ops.aten.conv2d -> ops.aten.cudnn_batch_norm] -> QuantizedConvBatchNorm2d
        '''
    # because we replace [ops.aten.linear, ops.aten.conv2d, ops.aten.batch_norm] to quantizedModel
    # We need to pre-check to avoid share weights occasions.
    # 0: Check whether contain share weights occasion, if contain, we will skip replacement
    skip_op_name = _share_weight_check(model=model)
    if len(skip_op_name) > 0:
        logger.warning("In this model, total {} opeartions have shared parameters, skip model optimatition".format(
            len(skip_op_name)))
        return model

    # 1: [ops.aten.conv2d -> ops.aten.cudnn_batch_norm] -> QuantizedConvBatchNorm2d/QuantizedConv2d
    # TODO further refin 1.if CLE etc. con + bn -> qconv 2. IF NO FOLD: conv + vn -> QuantizedConvBatchNorm2d
    replace_conv2dbn_quantizedconv_module(model)
    # 2: [ops.aten.linear] -> QuantLinear
    replace_linear_qtlinear(model)
    # 3: [ops.aten.conv2d] -> QuantConv2d
    replace_conv2d_qtconv2d(model)
    # 4: [ops.aten.conv_transpose2d] -> QuantConvTranspose2d
    replace_convtranspose2d_qtconvtranspose2d(model)
    # 5 change ops.aten,reshape param
    modify_reshape_param(model)
    return model


def transform_for_annotation(model: torch.fx.GraphModule) -> torch.fx.GraphModule:
    '''Prepare before annotation, for both PTQ and QAT'''
    model = _convert_scalars_to_attrs(model)
    return model


def _annotate_all_static_patterns(
    model: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> torch.fx.GraphModule:
    if quantization_config is None:
        return model

    # TODO future annoate by configuration rather fixed order in STATIC_OPS
    for op in STATIC_OPS:
        OP_TO_ANNOTATOR[op](model, quantization_config, filter_fn)
    return model


def _annotate_for_static_quant_config(model: torch.fx.GraphModule, config: Config) -> torch.fx.GraphModule:
    # TODO haoliang refine [layer_type_quant_config]
    # layer_type_list = list(config.layer_type_quant_config.keys())
    # layer_name_list = list(config.layer_quant_config.keys())

    _annotate_all_static_patterns(model, config.global_quant_config, None)
    return model


def annotate(model: torch.fx.GraphModule, config: Config) -> torch.fx.GraphModule:
    model = _annotate_for_static_quant_config(model, config)
    propagate_annotation(model)
    return model


def freeze_model(model: torch.fx.GraphModule) -> torch.fx.GraphModule:
    '''
    After quantization, we need to export model (e.g onnx, torch.export),
    we regard the users will not need further calibration, training, optimization.
    '''
    # 1 if find QuantizedConvBatchNorm2d, then merge bn to conv, let the forward like a naive conv
    for module in model.modules():
        if isinstance(module, QuantizedConvBatchNorm2d):
            module.merge_bn_to_conv()
    # 2 if find dropout layer, delete them
    # model = RemoveDropoutNode().apply(model)
    logger.info('Freeze quantized torch.fx.GraphModule ')
    return model


def _mask_op_with_no_grad_no_quant(model: torch.fx.GraphModule) -> List[str]:
    # TODO haoliang this is a temponary func, hope to use QuantStub and DeQuantStub
    # NOTE this is tempory func and may be changed in the future.
    '''
    For assuming that the operations that no need grad will not be quantized
    e.g:
        op0 = **
        _set_grad_enabled_1 = torch._C._set_grad_enabled(False)
        op1 = **
        op2 = **
        _set_grad_enabled_1 = torch._C._set_grad_enabled(True)
        op3 = **
    Tha above eample we will not intend to quant op1 & op2, so we mark op1 & op2 not to quant.
    '''
    skip_quant = False
    skip_quant_node_name = []
    for node in model.graph.nodes:
        if node.op == 'call_function' and node.target == torch._C._set_grad_enabled:
            if node.args[0] is False:
                skip_quant = True
            elif node.args[0] is True:
                skip_quant = False
        node.meta['skip_quant'] = skip_quant if skip_quant else node.meta['skip_quant']
        if skip_quant:
            skip_quant_node_name.append(node.name)
    return skip_quant_node_name


def _mask_op_by_start_end_name_to_skip_quant(model: torch.fx.GraphModule, start_end_node: Optional[List[str]],
                                             exclude_st_end_pair: Optional[List[List[str]]]) -> List[str]:
    # TODO haoliang this is a temponary func, hope to use QuantStub and DeQuantStub
    # NOTE this is a tempory func, in the future will be replaced by QuantStub() etc.
    ''' # Step0: All Nodes default set to quantiable.
        # Step1: Node among the start_end_node will set to not to quant.
        # Step2: Nodes among Nodes pairs(exclude_st_end_pair) will reactivate to quantiable.
    e.g:
        model: node0->node1->node2->node3->node4->node5->node6->node7->node8->node9
        start_end_node: [node1, node8]
        exclude_st_end_pair: [[node1, node3], [node5, node7]]

        model: node0(qt)->node1(qt)->node2(qt)->node3(qt)->node4(no qt)->
                    node5(qt)->node6(qt)->node7(qt)->node8(no qt)->node9(qt)
    '''
    # Step0 + Step1
    if isinstance(start_end_node, list):
        assert len(start_end_node) in [
            0, 2
        ], "Must assign start & end Node name (two str) or set to None, but size is:{}".format(len(start_end_node))
    st_n_name, end_n_name = start_end_node if isinstance(start_end_node, list) and len(start_end_node) else (None, None)
    skip_quant = False
    for node in model.graph.nodes:
        if st_n_name is not None and node.name == st_n_name:
            skip_quant = True
        elif end_n_name is not None and node.name == end_n_name:
            node.meta['skip_quant'] = skip_quant
            skip_quant = False
            continue
        node.meta['skip_quant'] = skip_quant

    # Step2.1: first loop init node between [start_end_node[0], start_end_node[0]] set to skip
    # ckeck whether (1) each pair in exclude_st_end_pair among in start_end_node (2) each pair have no overlap
    bound_list = []  # nodes need to be quantized
    if isinstance(exclude_st_end_pair, list):
        for each_pair in exclude_st_end_pair:
            assert len(each_pair) == 2, "start and end node must be pair"
            start_node, end_node = each_pair
            need_collect_qt_node = False
            for node in model.graph.nodes:
                if node.name == start_node:
                    need_collect_qt_node = True
                elif node.name == end_node:
                    bound_list.append(node.name)
                    need_collect_qt_node = False
                    continue
                if need_collect_qt_node:
                    bound_list.append(node.name)

    # Step2.2: set meta info that all nodes that need quantize
    for node in model.graph.nodes:
        if node.name in bound_list:
            node.meta['skip_quant'] = False

    # collect all skip node
    skip_quant_node = []
    for node in model.graph.nodes:
        if node.meta['skip_quant'] is True:
            skip_quant_node.append(node.name)
    return skip_quant_node


def mark_no_need_quant_node(model: torch.fx.GraphModule, config: Config) -> List[str]:
    # 0. mask node by start and end node
    if len(config.exclude) and len(config.exclude) % 2 == 0:
        start_end_node = [config.exclude[0], config.exclude[1]]
        exclude_start_end = [list(pair) for pair in zip(config.exclude[2::2], config.exclude[3::2])]
    else:
        start_end_node, exclude_start_end = None, None
    masked_node = _mask_op_by_start_end_name_to_skip_quant(model, start_end_node, exclude_start_end)
    # 1. start from grad_enabled(False) and end with grad_enabled(False)
    skip_quant_name = _mask_op_with_no_grad_no_quant(model=model)
    return masked_node + skip_quant_name


def prepare_quant_model(model: torch.fx.GraphModule, config: Config) -> torch.fx.GraphModule:
    original_graph_meta = model.meta
    # node_name_to_scope = _get_node_name_to_scope(model)
    # optimize before annotation
    # NOTE: this is a tempory func, future will use QuantStub()
    skip_quant_node_name = mark_no_need_quant_node(model=model, config=config)
    # TODO haoliang optimize check e.g(1. one param/tensor share over one time 2.)
    model = _quant_optimize(model)
    model = transform_for_annotation(model)
    annotate(model, config)
    # inset the quantizer
    model = insert_quantizer(model)
    model.meta.update(original_graph_meta)
    model.freeze_model = types.MethodType(freeze_model, model)  # type: ignore [assignment]
    return allow_exported_model_train_eval(model)
