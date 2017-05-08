import networkx as nx
import pprint as pp
import csv

path = "datasets/movie_graph.txt"
result = nx.Graph()
alpha = 0.15
epsilon = 10 ** -6


def load_graph():
    input_file = open(path, 'r')
    data = input_file.readlines()
    input_file.close()
    graph = csv.reader(data, delimiter='\t')
    for adjacency_list in graph:
        result.add_node(int(adjacency_list[0]))
        result.add_edge(int(adjacency_list[0]), int(adjacency_list[1]), weight=int(adjacency_list[2]))
    return result


def create_pagerank_vector(graph):
    page_rank_vector = {}
    num_nodes = graph.number_of_nodes()
    initial_pr_value = 1. / num_nodes
    for node_id in range(1, num_nodes + 1):
        page_rank_vector[node_id] = initial_pr_value
    return page_rank_vector


def norm_weights(graph):
    sum = {}
    for node_j in graph:
        sum[node_j] = 0
        for node_i in graph[node_j]:
            sum[node_j] += get_weight(graph, node_i, node_j)
    result = nx.Graph()

    for node_j in graph:
        dict_result = {}
        for node_i in graph[node_j]:
            result.add_node(node_j)
            norm = get_weight(graph, node_i, node_j) / sum[node_j]
            dict_result[node_i] = norm
            print(node_i, dict_result[node_i])
            result.add_edge(node_j, node_i, weight=dict_result[node_i])
            break
    return result


def pagerank_single_iteration(graph, pagerank_vector):
    next_page_rank_vector = {}
    sum_of_all_partial_values = 0.

    node_degree = {}
    for node_j in graph.nodes():
        node_degree[node_j] = len(graph[node_j])

    sum = {}
    for node_j in graph.nodes():
        sum[node_j] = 0
        for node_i in graph[node_j]:
            sum[node_j] += get_weight(graph, node_j, node_i)

    for node_j in graph.nodes():
        next_page_rank_vector[node_j] = 0.
        for node_i in graph[node_j]:
            degree_node_i = node_degree[node_j]
            weight_norm = get_weight(graph, node_j, node_i) / sum[node_j]
            next_page_rank_vector[node_j] += (1. - alpha) * pagerank_vector[node_j] * weight_norm / degree_node_i
        sum_of_all_partial_values += next_page_rank_vector[node_j]

        leaked_pr = 1. - sum_of_all_partial_values

        num_nodes = graph.number_of_nodes()

        fraction_of_leaked_pr_to_give_each_node = leaked_pr / num_nodes

        for node_j in next_page_rank_vector:
            next_page_rank_vector[node_j] = next_page_rank_vector[node_j] + fraction_of_leaked_pr_to_give_each_node

    return next_page_rank_vector


def get_weight(graph, node_i, node_j):
    return graph[node_i][node_j]['weight']

    # next_page_rank_vector = {}
    # sum_of_all_partial_values = 0.
    # for node_j in graph.nodes():
    #     next_page_rank_vector[node_j] = 0.
    #     for node_i in graph[node_j]:
    #         out_degree_node_i = graph.out_degree(node_i)
    #         next_page_rank_vector[node_j] += ((1. - alpha) * pagerank_vector[node_i]) * \
    #                                          (graph[node_i][node_j]['weight'] / out_degree_node_i)
    #
    #     sum_of_all_partial_values += next_page_rank_vector[node_j]
    #
    # leaked_pr = 1 - sum_of_all_partial_values
    # num_nodes = graph.number_of_nodes()
    # fraction_of_leaked_pr_to_give_each_node = leaked_pr / num_nodes
    #
    # for node_j in next_page_rank_vector:
    #     next_page_rank_vector[node_j] = next_page_rank_vector[node_j] + fraction_of_leaked_pr_to_give_each_node
    #
    # return next_page_rank_vector


def compute_distance(vector_1, vector_2):
    distance = 0.
    for node in vector_1.keys():
        distance += abs(vector_1[node] - vector_2[node])
    return distance


def compute_page_rank(graph):
    previous_page_rank_vector = create_pagerank_vector(graph)
    iterations = 1
    convergence = False
    page_rank_vector = {}
    while not convergence:
        print("iteration #" + str(iterations))
        page_rank_vector = pagerank_single_iteration(graph, previous_page_rank_vector)
        iterations += 1
        dist = compute_distance(previous_page_rank_vector, page_rank_vector)
        print(dist, epsilon)
        if dist <= epsilon:
            convergence = True
            print("Convergence")
        previous_page_rank_vector = page_rank_vector
    return page_rank_vector


if __name__ == '__main__':
    print("computing graph")
    result_graph = load_graph()
    # norm_graph = norm_weights(result_graph)
    # print(norm_graph[1])
    pr_vector = create_pagerank_vector(result_graph)
    # pagerank_single_iteration(result_graph, pr_vector)
    # print(result_graph[1])
    # print("normalizing weights")
    # normalize_graph(result_graph)
    # print(result_graph[1])
    # for key in result_graph:
    #     for inner_key in result_graph[key]:
    #         print(result_graph[key][inner_key]['weight'])
    #         break
    #     break
    damping_factor = 1 - alpha
    # realpr = nx.pagerank(result_graph, alpha=damping_factor, tol=epsilon)
    print("computing page rank vector")
    pp.pprint(nx.pagerank(result_graph, alpha=damping_factor, tol=epsilon))
    mypr = compute_page_rank(result_graph)
    # print(distance(mypr, realpr))
    pp.pprint(mypr)
    totalsum = 0.
    for val in mypr:
        totalsum += mypr[val]
    print(totalsum)
