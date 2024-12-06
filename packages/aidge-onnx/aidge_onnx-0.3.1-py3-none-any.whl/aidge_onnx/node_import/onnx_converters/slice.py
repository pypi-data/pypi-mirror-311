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

@auto_register_import("slice")
def import_slice(onnx_node:onnx.NodeProto, input_nodes:List[Tuple[aidge_core.Node, int]], opset=None) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    onnx_attrs = get_node_attributes(onnx_node, opset)
    slice_attrs: dict = {"name" : node_name}

    if opset < 10:
        for key in ('starts','ends','axes'):
            if key in onnx_attrs:
                slice_attrs[key] = onnx_attrs[key]
                del onnx_attrs[key]
    elif opset in (10,11,13):#in opsets superior to 10, attributes are moved to inputs
        for ite,ele in enumerate(('starts','ends','axes','steps'), start=1):
            if input_nodes[ite] is not None:
                slice_attrs[ele] = input_nodes[ite][0].get_operator().get_output(input_nodes[ite][1])

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'Slice' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    slice_node = aidge_core.Slice(**slice_attrs)
    Log.notice(f"- {node_name} ({onnx_node.op_type})")
    return slice_node
