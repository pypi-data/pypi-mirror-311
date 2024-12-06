"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
from typing import List, Tuple

import aidge_core
import onnx
from aidge_onnx.node_import import auto_register_import
from aidge_onnx.utils import get_node_attributes

from aidge_core import Log
from aidge_onnx.utils import warn_unsupported_attr

@auto_register_import("gemm")
def import_gemm(onnx_node:onnx.NodeProto, input_nodes:List[Tuple[aidge_core.Node, int]], opset=None) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    onnx_attrs = get_node_attributes(onnx_node, opset)
    gemm_attrs = {'transA':0,'transB':1,'alpha':1.0,'beta':1.0}

    for attr_name,attr_exp_value in gemm_attrs.items():
        if onnx_attrs[attr_name] != attr_exp_value:
            warn_unsupported_attr(attr_name,'Gemm',opset,onnx_attrs[attr_name])
            return None
        del onnx_attrs[attr_name]

    if opset < 7 and 'broadcast' in onnx_attrs:
        warn_unsupported_attr("broadcast","Gemm",opset,onnx_attrs["broadcast"])
        return None

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'Gemm' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    # nb_outputs = input_nodes[1][0].get_operator().get_output(input_nodes[1][1]).dims()[0]
    # nb_inputs = input_nodes[1][0].get_operator().get_output(input_nodes[1][1]).dims()[1]

    fc_node = aidge_core.Node(aidge_core.FCOp(), name=node_name)
    Log.notice(f"- {node_name} ({onnx_node.op_type})")
    return fc_node
