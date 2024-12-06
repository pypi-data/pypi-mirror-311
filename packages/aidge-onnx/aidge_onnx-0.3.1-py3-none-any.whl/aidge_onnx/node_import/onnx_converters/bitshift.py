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

@auto_register_import("bitshift")
def import_bitshift(onnx_node:onnx.NodeProto, input_nodes:List[Tuple[aidge_core.Node, int]], opset=None) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    node_name = onnx_node.output[0]
    attrs = {attr.name : attr for attr in onnx_node.attribute}
    onnx_attr_default: dict = {}
    direction = None
    
    if 'direction' in attrs:
        onnx_attr_default['direction'] = attrs['direction']
        del attrs['direction']
   
    if(len(attrs) > 0):
        print(f"Warning: Attribute {attrs.keys()} is not supported for operator bitshift.")
        return None
   
    string_direction_onnx = onnx_attr_default['direction'].s.decode('utf-8')
    if(string_direction_onnx == "RIGHT"):
        direction  = aidge_core.BitShiftOp.BitShiftDirection.Right
    elif(string_direction_onnx == "LEFT"):
        direction  = aidge_core.BitShiftOp.BitShiftDirection.Left
    else:
        print(f"Warning: Unable to parse shift direction <{string_direction_onnx}> for operator bitshift")
        return None
    My_op = aidge_core.BitShiftOp(direction)
    print(f"- {node_name} ({onnx_node.op_type})")
    return aidge_core.Node(My_op,name=node_name)
