import part1
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


def filter_results(pr_vector, user_ratings):
    result = {}
    for movie in pr_vector:
        if movie not in user_ratings:
            result[movie] = pr_vector[movie]
    for value in sorted(result, key=result.get, reverse=True):
        print(value, result[value])

def compute_bias(rating, user_ratings):
    sum_of_ratings = 0.
    for movie in user_ratings:
        sum_of_ratings += user_ratings[movie]
    return rating / sum_of_ratings

def compute_teleporting_vector(graph, user_ratings):
    teleporting_vector = {}
    for node in graph:
        if(node in user_ratings):
            teleporting_vector[node] = compute_bias(user_ratings[node], user_ratings)
        else:
            teleporting_vector[node] = 0.

    return teleporting_vector


if __name__ == '__main__':
    user_ratings = read_ratings(ratings_file, 1683)
    graph = part1.read_file(movie_file)
    norm_graph = part1.normalize_graph(graph)
    teleporting_vector = compute_teleporting_vector(norm_graph, user_ratings)
    pr_vector = part1.compute_page_rank(norm_graph, teleporting_vector)
    filter_results(pr_vector, user_ratings)
    # page_rank = reader.compute_page_rank(ratings_file)
