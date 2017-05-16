category_file = "datasets/category_movies.txt"
path = "datasets/movie_graph.txt"
import part1

import csv


# def compute_bias():



def compute_list_of_categories(movie, category_file):
    movie_categories = []
    for category in category_file:
        if str(movie) in category_file[category]:
            movie_categories.append(1)
        else:
            movie_categories.append(0)
    return movie_categories


def compute_weight(list_of_categories, user_preferences_vector):
    total = 0.
    weight = 0.
    cont = 0
    for preference in user_preferences_vector:
        total += preference
    while cont < len(user_preferences_vector):
        weight += user_preferences_vector[cont] * list_of_categories[cont]
        cont += 1
    return weight / total



if __name__ == '__main__':
    user_preferences_vector = [3, 4, 0, 2, 1]
    input_file = open(category_file, 'r')
    data = input_file.readlines()
    input_file.close()
    categories = csv.reader(data, delimiter='\t')
    graph = part1.read_file(path)
    norm_graph = part1.normalize_graph(graph)
    map = {}
    cont = 1

    for category in categories:
        map[cont] = category
        cont+=1


    for movie in norm_graph:
        list_of_categories = compute_list_of_categories(movie, map)
        weight = compute_weight(list_of_categories, user_preferences_vector)
        print (movie, weight)

