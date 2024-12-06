"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
import aidge_core
import numpy as np
from collections import defaultdict
import colorama

from onnx import numpy_helper
import onnx
from .node_import import ONNX_NODE_CONVERTER_, generic
from .utils import onnx_to_aidge_model_names

def load_onnx(filename: str, verbose: bool = False):
    """Load an ONNX file and convert it into a :py:class:`aidge_core.GraphView`.

    :param filename: Path to the ONNX file to load
    :type filename: str
    :param verbose: If ``True``, display information on the terminal, default=False
    :type verbose: bool, optional
    :returns: Aidge :py:class:`aidge_core.GraphView` corresponding to the ONNX model described by the onnx file  ``filename``
    :rtype: :py:class:`aidge_core.GraphView`
    """
    if verbose : print(f"Loading ONNX {filename}")

    # Load the ONNX model
    model = onnx.load(filename)
    return _load_onnx2graphview(model, verbose)

def has_native_coverage(graph: aidge_core.GraphView):
    """Check if a graph view is supported with only native Aidge operators
    (meaning no GenericOperator)

    :param graph: Graph view
    :type graph: aidge_core.GraphView
    :returns: True if there is no GenericOperator in the graph
    :rtype: bool
    """
    for node in graph.get_nodes():
        if isinstance(node.get_operator(), aidge_core.GenericOperatorOp):
            return False
    return True

def native_coverage_report(graph: aidge_core.GraphView):
    """Report Aidge native operators support for a graph view

    :param graph: Graph view
    :type graph: aidge_core.GraphView
    """
    if len(graph.get_nodes()) == 0:
        print("GraphView is empty!")
        return

    native_node_types = defaultdict(int)
    generic_node_types = defaultdict(int)

    for node in graph.get_nodes():
        if isinstance(node.get_operator(), aidge_core.GenericOperatorOp):
            generic_node_types[node.type()] += 1
        else:
            native_node_types[node.type()] += 1

    nb_native_nodes = sum(native_node_types.values())
    nb_generic_nodes = sum(generic_node_types.values())

    print(f"Native operators: {nb_native_nodes} ({len(native_node_types)} types)")
    for op, nb in sorted(native_node_types.items()):
        print(f"- {op}: {nb}")
    print(f"Generic operators: {nb_generic_nodes} ({len(generic_node_types)} types)")
    for op, nb in sorted(generic_node_types.items()):
        print(f"- {op}: {nb}")
    print(f"Native types coverage: {100 * len(native_node_types) / (len(native_node_types) + len(generic_node_types)):.1f}% ({len(native_node_types)}/{len(native_node_types) + len(generic_node_types)})")
    print(f"Native operators coverage: {100 * nb_native_nodes / (nb_native_nodes + nb_generic_nodes):.1f}% ({nb_native_nodes}/{nb_native_nodes + nb_generic_nodes})")

    return (native_node_types, generic_node_types)

def _load_onnx2graphview(model:onnx.ModelProto, verbose:bool = False):
    """Transform an ONNX graph to an Aidge GraphView

    :param model: ONNX graph
    :type model: onnx.ModelProto
    :param verbose: If ``True``, display information on the terminal, default=False
    :type verbose: bool, optional
    :returns: Aidge :py:class:`aidge_core.GraphView` corresponding to the ONNX model described by the onnx ``model``
    :rtype: :py:class:`aidge_core.GraphView`
    """
    opset: int = None
    if hasattr(model, 'opset_import'):
        domains =  {domain.domain : domain.version for domain in model.opset_import}
    else:
        raise RuntimeError("Cannot retieve opset version from ONNX model.")
    if verbose:
        print(f"ONNX metadata:" \
            f"\n\t- Producer name: {model.producer_name}" \
            f"\n\t- Producer version: {model.producer_version}"\
            f"\n\t- Opset version: {opset}")
    node_inputs = {} # Key : node name, Value : list of tuple [input objects, their outputIdx] ordered by inputIdx
    model_producers = {} # Key : producer name, Value : producer object
    model_nodes = {} # Key : producer name, Value : node object
    graph: aidge_core.GraphView = aidge_core.GraphView()

    # Clean model if some issues in the model
    # might affect Aidge in the next steps
    model: onnx.ModelProto = onnx_to_aidge_model_names(model)

    if verbose : print(f"\nGetting Initializers\n====================")
    for i in model.graph.initializer:
        values = numpy_helper.to_array(i)
        if verbose : print(f"- Initializer  : {i.name} : {list(values.shape)}")
        model_producers[i.name] = aidge_core.Producer(aidge_core.Tensor(values) if values.shape != () else aidge_core.Tensor(np.array([values.item()])), i.name)

    if verbose : print(f"\nProcessing Nodes\n================")

    # Get the nodes
    # Associate the ONNX nodes with Aidge Node if possible
    for onnx_node in model.graph.node:
        node_name = onnx_node.output[0] # Do not use onnx_node.name as it is not a mandatory value
        node_inputs[node_name] = [None]*len(onnx_node.input)
        # There can be multiple opsets in a given model, each ones attached to a given domain
        # Each nodes are attached to a given opset via a domain name.
        # more on how opset work here : http://onnx.ai/sklearn-onnx/auto_tutorial/plot_cbegin_opset.html
        node_opset = domains[onnx_node.domain]

        # Adding producers to the list of inputs
        for input_idx, input_node in enumerate(onnx_node.input):
            if input_node in model_producers:
                node_inputs[node_name][input_idx] = (model_producers[input_node], 0)

        try:
            model_nodes[node_name] = ONNX_NODE_CONVERTER_[onnx_node.op_type.lower()](onnx_node, node_inputs[node_name], node_opset)
        except Exception as e:
            print(colorama.Fore.YELLOW + f"Warning: an error occured when trying to load node {node_name} of type {onnx_node.op_type.lower()}.")
            print(f"Loading node using a generic operator.")
            print(f"Please report this issue at https://gitlab.eclipse.org/eclipse/aidge/aidge_onnx")
            print(f"by providing your ONNX model and the following error:")
            print(f"ONNX_NODE_CONVERTER_ returned: {e}")
            print(colorama.Style.RESET_ALL)
            model_nodes[node_name] = None

        # If None, the node type exists but could not be converted (for instance because unsupported attribute) => fall back to generic
        if model_nodes[node_name] is None:
            model_nodes[node_name] = generic.import_generic(onnx_node, node_inputs[node_name], opset)

    # Collect all outputs in the graph
    node_outputs = {}
    for onnx_node in model.graph.node:
        node_name = onnx_node.output[0] # Do not use onnx_node.name as it is not a mandatory value
        for output_idx, output in enumerate(onnx_node.output):
            node_outputs[output] = (model_nodes[node_name], output_idx)

    # Add nodes to the node_inputs dict
    for onnx_node in model.graph.node:
        node_name = onnx_node.output[0] # Do not use onnx_node.name as it is not a mandatory value
        for input_idx, input_node_name in enumerate(onnx_node.input):
            if input_node_name in node_outputs and input_node_name not in model_producers:
                node_inputs[node_name][input_idx] = node_outputs[input_node_name]

    if verbose : print(f"\nConnecting Nodes\n================")
    # Link every inputs
    for name, inputs in node_inputs.items():
        for input_idx, input_node in enumerate(inputs):
            if input_node is None:
                # TODO : proper handle of input nodes.
                if verbose : print(f"Warning: Node {name} misses input #{input_idx}. If it is not an input node of the graph, there is an error!")
            else:
                input_node[0].add_child(model_nodes[name], input_node[1], input_idx)
                graph.add(input_node[0]) # Add input nodes to the graph
        graph.add(model_nodes[name])
        if verbose : print(f"{name} added")

    # Set graph outputs
    graph_outputs = []
    for output in model.graph.output:
        graph_outputs.append(node_outputs[output.name])
    graph.set_ordered_outputs(graph_outputs)

    return graph
