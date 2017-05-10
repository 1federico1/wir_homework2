import part1
import pprint as pp
import csv

ratings_file = "datasets/user_movie_rating.txt"
movie_file = "datasets/movie_graph.txt"


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





def pagerank_single_iteration(graph, pagerank_vector, user_ratings):
    next_page_rank_vector = {}
    sum_of_all_partial_values = 0.
    num_nodes = graph.number_of_nodes()
    for node in graph:
        next_page_rank_vector[node] = part1.compute_porting_probability(node, graph,next_page_rank_vector,
                                                                      pagerank_vector)
        sum_of_all_partial_values+= next_page_rank_vector[node]
    fraction_of_leaked_pr_to_give_each_node = part1.compute_teleporting_probability(num_nodes,sum_of_all_partial_values)
    for node in next_page_rank_vector:
        bias =0.
        if node in user_ratings:
            bias = compute_bias(user_ratings[node],user_ratings)
        next_page_rank_vector[node] = next_page_rank_vector[node] + fraction_of_leaked_pr_to_give_each_node * bias


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

def compute_bias(rating, user_ratings):
    sum_of_ratings = 0
    for movie in user_ratings:
        sum_of_ratings += user_ratings[movie]
    return rating / sum_of_ratings


if __name__ == '__main__':
    user_ratings = read_ratings(ratings_file, 1683)
    pr_vector = compute_page_rank(movie_file, user_ratings)
    filter_results(pr_vector, user_ratings)
    # page_rank = reader.compute_page_rank(ratings_file)
