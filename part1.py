import networkx as nx
import pprint as pp
import csv

path = "datasets/movie_graph.txt"
# path = "datasets/test_graph.txt"
result = nx.DiGraph()
alpha = .15
epsilon = 10 ** -6


def read_file(path):
    input_file = open(path, 'r')
    data = input_file.readlines()
    input_file.close()
    graph = csv.reader(data, delimiter='\t')
    for adjacency_list in graph:
        result.add_node(int(adjacency_list[0]))
        result.add_edge(int(adjacency_list[0]), int(adjacency_list[1]), weight=int(adjacency_list[2]))
        result.add_edge(int(adjacency_list[1]), int(adjacency_list[0]), weight=int(adjacency_list[2]))
    return result


def create_pagerank_vector(graph):
    page_rank_vector = {}
    num_nodes = graph.number_of_nodes()
    initial_pr_value = 1. / num_nodes
    for node_id in range(1, num_nodes + 1):
        page_rank_vector[node_id] = initial_pr_value
    return page_rank_vector


def pagerank_single_iteration(graph, pagerank_vector):
    next_page_rank_vector = {}
    sum_of_all_partial_values = 0.
    num_nodes = graph.number_of_nodes()
    for node in graph.nodes():
        next_page_rank_vector[node] = compute_porting_probability(node, graph, next_page_rank_vector, pagerank_vector)
        sum_of_all_partial_values += next_page_rank_vector[node]

    fraction_of_leaked_pr_to_give_each_node = compute_teleporting_probability(num_nodes, sum_of_all_partial_values)

    for node_k in next_page_rank_vector:
        next_page_rank_vector[node_k] = next_page_rank_vector[node_k] + fraction_of_leaked_pr_to_give_each_node

    return next_page_rank_vector


def compute_total_weights(graph):
    total_weights = {}
    for node in graph.nodes():
        total = compute_total_weight_for_node(graph, node)
        total_weights[node] = total
    return total_weights


def normalize_graph(graph):
    for node in graph:
        sum_of_weights = 0.
        for adjacent in graph[node]:
            sum_of_weights += get_weight(graph, node, adjacent)
        for adjacent in graph[node]:
            graph[node][adjacent]['weight'] = get_weight(graph, node, adjacent) / sum_of_weights
    return graph


def compute_porting_probability(node, graph, next_page_rank_vector, pagerank_vector):
    # total_weight = compute_total_weight_for_node(graph, node)
    next_page_rank_vector[node] = 0.
    for node_i in graph[node]:
        weight = get_weight(graph, node_i, node)
        next_page_rank_vector[node] += (1 - alpha) * pagerank_vector[node_i] * weight

    return next_page_rank_vector[node]


def compute_teleporting_probability(num_nodes, sum_of_all_partial_values):
    leaked_pr = 1. - sum_of_all_partial_values
    fraction_of_leaked_pr_to_give_each_node = leaked_pr / num_nodes
    return fraction_of_leaked_pr_to_give_each_node



def compute_total_weight_for_node(graph, node):
    total_weight = 0.
    for node_i in graph[node]:
        total_weight += get_weight(graph, node, node_i)
    return total_weight


def get_weight(graph, node_j, node_i):
    return graph[node_j][node_i]['weight']


def compute_distance(vector_1, vector_2):
    distance = 0.
    for node in vector_1:
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
    result_graph = read_file(path)
    print("computing page rank vector")
    result_graph = normalize_graph(result_graph)
    mypr = compute_page_rank(result_graph)
    print("my page rank:")

    for node in sorted(mypr, key=mypr.get, reverse=True):
        print(node, mypr[node])

    totalsum = 0.
    for val in mypr:
        totalsum += mypr[val]
    print(totalsum)
