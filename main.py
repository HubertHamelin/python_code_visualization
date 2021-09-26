from visualize import format_pycg_json_to_pandas_df, explore_code, pandas_df_to_nx_graph, draw_nx_graph


if __name__ == '__main__':

    # Explore the code of a specific package and generate a json file with the results of the analysis
    entry_point = ['./main.py', './visualize.py']
    package = None
    output = 'cg.json'
    graph_output = None
    explore_code(entry_point, package, output, graph_output)

    # Produce a pandas dataframe from the json file
    with open('cg.json', 'r') as myfile:
        data = myfile.read()
        dataframe = format_pycg_json_to_pandas_df(data)

        # Generate the graph
        nx_graph = pandas_df_to_nx_graph(dataframe)
        draw_nx_graph(nx_graph)
