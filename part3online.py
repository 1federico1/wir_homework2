path = "datasets/movie_graph.txt"
import part1
import pprint as pp
import csv
import os


def compute_page_rank_movie(map, movie):
    list_of_page_ranks = []
    for vector in map:
        if (movie in vector):
            list_of_page_ranks.append(vector[movie])
        else:
            list_of_page_ranks.append(0.)

    return list_of_page_ranks


def from_file_to_map(file):
    map = {}
    input_file = open(file, 'r')
    data = csv.reader(input_file, delimiter='\t')
    for line in data:
        key = int(line[0])
        map[key] = float(line[1])
    return map


def pageranks_values(movie, maps):
    vector = []
    for map in maps:
        if movie in maps[map]:
            vector.append(maps[map][movie])
        else:
            vector.append(0.)
    return vector


if __name__ == '__main__':
    user_preferences_vector = [3, 4, 0, 2, 1]
    graph = part1.read_file(path)
    cont = 1
    os.chdir('datasets')
    directory = os.listdir()
    files = [file for file in directory if file.startswith('input')]
    files.sort()
    maps = {}

    for file in files:
        maps[cont] = from_file_to_map(file)
        cont += 1

    for movie in graph:
        pr_vector = pageranks_values(movie, maps)
        print(movie, pr_vector)

        # for movie in norm_graph:
        #     page_rank_movie_vector = compute_page_rank_movie(map, movie);
        #     print (movie, weight)
