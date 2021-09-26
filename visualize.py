import json
import networkx as nx
import pandas as pd
from pyvis.network import Network
from pycg.pycg import CallGraphGenerator
from pycg import formats
from pycg.utils.constants import CALL_GRAPH_OP


def format_pycg_json_to_pandas_df(json_file):
    file_content_dictionary = json.loads(json_file)
    relations_array = []
    for key in file_content_dictionary:
        source_node = key
        destination_nodes = file_content_dictionary[key]
        for destination_node in destination_nodes:
            relations_array.append([source_node, destination_node])
    dataframe = pd.DataFrame(relations_array, columns=["source_node", 'destination_node'])
    return dataframe


def explore_code(entry_point, package, _output, graph_output):
    cg = CallGraphGenerator(entry_point, package, -1, CALL_GRAPH_OP)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()
    with open(_output, "w+") as f:
        f.write(json.dumps(output))


def pandas_df_to_nx_graph(dataframe):
    nx_graph = nx.from_pandas_edgelist(dataframe, source='source_node', target='destination_node')
    # Todo: directed graph, colored types (functions, classes, imports...), node size proportional to its edges number
    for node in nx_graph.nodes:
        nx_graph.nodes[node]['size'] = nx_graph.degree[node]
    nx_graph.to_directed()
    return nx_graph


def draw_nx_graph(nx_graph):
    net = Network(notebook=True)
    net.from_nx(nx_graph)
    net.show("example.html")
