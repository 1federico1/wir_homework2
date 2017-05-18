path = "datasets/movie_graph.txt"
import part1
import pprint as pp
import csv



# def compute_list_of_categories(movie, category_file):
#     movie_categories = []
#     for category in category_file:
#         if str(movie) in category_file[category]:
#             movie_categories.append(1)
#         else:
#             movie_categories.append(0)
#     return movie_categories

def compute_page_rank_movie(map, movie):
    list_of_page_ranks = []
    for vector in map:
        if(movie in vector):
            list_of_page_ranks.append(vector[movie])
        else:
            list_of_page_ranks.append(0.)

    return list_of_page_ranks


# def compute_weight(list_of_categories, user_preferences_vector):
#     total = 0.
#     weight = 0.
#     cont = 0
#     for preference in user_preferences_vector:
#         total += preference
#     while cont < len(user_preferences_vector):
#         weight += user_preferences_vector[cont] * list_of_categories[cont]
#         cont += 1
#     return weight / total

def from_file_to_map(file):
    map = {}
    input_file = open(file, 'r')
    data = csv.reader(input_file, delimiter = '\t')
    for line in data:
        key = int(line[0])
        map[key] = float(line[1])
    return map

def pageranks_values(movie, maps):
    vector = []
    for map in maps:
        if movie in map:
            vector.append(map[movie])
        else:
            vector.append(0.)
    pp.pprint(vector)
    return vector


if __name__ == '__main__':
    user_preferences_vector = [3, 4, 0, 2, 1]
    graph = part1.read_file(path)
    norm_graph = part1.normalize_graph(graph)
    cont = 1
    files = ['datasets/input_1.txt', 'datasets/input_2.txt', 'datasets/input_3.txt', 'datasets/input_4.txt', 'datasets/input_5.txt']
    maps = {}

    for file in files:
        maps[cont] = from_file_to_map(file)
        cont+=1

    for movie in norm_graph:
        movie_pr_vector = pageranks_values(movie, maps)
        break




    # for movie in norm_graph:
    #     page_rank_movie_vector = compute_page_rank_movie(map, movie);
    #     print (movie, weight)

