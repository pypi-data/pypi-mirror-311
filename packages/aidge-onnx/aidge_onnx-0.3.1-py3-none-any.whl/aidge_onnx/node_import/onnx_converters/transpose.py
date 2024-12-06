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

@auto_register_import("transpose")
def import_transpose(onnx_node:onnx.NodeProto, input_nodes:List[Tuple[aidge_core.Node, int]], opset=None) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    onnx_attrs = get_node_attributes(onnx_node, opset)
    transpose_attrs : dict = {"output_dims_order" : [], "name" : node_name}

    if 'perm' in onnx_attrs:
        transpose_attrs["output_dims_order"] = onnx_attrs['perm']
        del onnx_attrs['perm']
    else:
        Log.warn("Warning: Operator 'Transpose' must have 'perm' attribute. This node will be filled by a GenericOperator.")
        return None

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'Transpose' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    transpose_node = aidge_core.Transpose(**transpose_attrs)
    Log.notice(f"- {node_name} ({onnx_node.op_type})")
    return transpose_node
