import part1 as part1
import pprint as pp
import csv
import sys


def read_ratings(path, user_id):
    input_file = open(path, 'r')
    data = input_file.readlines()
    input_file.close()
    ratings = csv.reader(data, delimiter='\t')
    result = {}
    for line in ratings:
        if line[0] == str(user_id):
            result[int(line[1])] = int(line[2])
    return result


def compute_alpha(rating, user_ratings):
    sum_of_ratings = 0
    for movie in user_ratings:
        sum_of_ratings += user_ratings[movie]
    result = rating / sum_of_ratings
    return result


def pagerank_single_iteration(graph, pagerank_vector, user_ratings):
    next_page_rank_vector = {}
    sum_of_all_partial_values = 0.
    num_nodes = graph.number_of_nodes()
    node_degree = {}

    for node_j in graph.nodes():
        node_degree[node_j] = len(graph[node_j])

    total_weight = {}
    for node_j in graph.nodes():
        total_weight[node_j] = 0
        for node_i in graph[node_j]:
            total_weight[node_j] += part1.get_weight(graph, node_j, node_i)

    for node_j in graph.nodes():
        next_page_rank_vector[node_j] = 0.

        for node_i in graph[node_j]:
            degree_node_i = graph.degree(node_i)
            weight = (part1.get_weight(graph, node_j, node_i))
            weight_norm = weight / total_weight[node_j]
            if node_j in user_ratings:
                alpha = compute_alpha(user_ratings[node_j], user_ratings)
            else:
                alpha = 0.
            num = (1. - alpha) * (pagerank_vector[node_j]) * weight_norm
            next_page_rank_vector[node_j] += num / degree_node_i
        sum_of_all_partial_values += next_page_rank_vector[node_j]

    leaked_pr = 1. - sum_of_all_partial_values

    fraction_of_leaked_pr_to_give_each_node = leaked_pr / num_nodes

    for node_k in next_page_rank_vector:
        next_page_rank_vector[node_k] = next_page_rank_vector[node_k] + fraction_of_leaked_pr_to_give_each_node
    return next_page_rank_vector


def compute_page_rank(path, user_ratings):
    graph = part1.read_file(path)
    previous_page_rank_vector = part1.create_pagerank_vector(graph)
    iterations = 1
    convergence = False
    page_rank_vector = {}
    while not convergence:
        print("iteration #" + str(iterations))
        page_rank_vector = pagerank_single_iteration(graph, previous_page_rank_vector, user_ratings)
        iterations += 1
        dist = part1.compute_distance(previous_page_rank_vector, page_rank_vector)
        print(dist, part1.epsilon)
        if dist <= part1.epsilon:
            convergence = True
            print("Convergence")
        previous_page_rank_vector = page_rank_vector
    return page_rank_vector


def filter_results(pr_vector, user_ratings):
    result = {}
    for movie in pr_vector:
        if movie not in user_ratings:
            result[movie] = pr_vector[movie]
    for value in sorted(result, key=result.get, reverse=True):
        print(value, result[value])


if __name__ == '__main__':
    user_ratings = read_ratings(sys.argv[2], sys.argv[3])
    pr_vector = compute_page_rank(sys.argv[1], user_ratings)
    # pp.pprint(pr_vector)
    filter_results(pr_vector, user_ratings)
    # page_rank = reader.compute_page_rank(ratings_file)
