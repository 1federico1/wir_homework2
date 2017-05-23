import csv
import os
import sys
import part1 as p1
import part3offline as p3offline


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


def aggregate_pagerank(pr_vector, user_preferences_vector, norm_user_preferences_vector):
    cont = 0
    result = 0.
    while cont < len(pr_vector):
        try:
            result += pr_vector[cont] * user_preferences_vector[cont]
            cont += 1
        except IndexError:
            raise IndexError('User preferences vector has to be of five elements')
    return result / norm_user_preferences_vector


if __name__ == '__main__':
    p3offline.pageranks()
    user_input = sys.argv[1]
    try:
        user_preferences_vector = ([int(value) for value in user_input.split('_')])
    except ValueError:
        raise ValueError('Bad written user preferences vector')
    graph = p1.read_file(p1.movie_file)
    cont = 1
    os.chdir('datasets')
    directory = os.listdir('.')
    files = [file for file in directory if file.startswith('input')]
    files.sort()
    maps = {}
    result = {}

    for file in files:
        maps[cont] = from_file_to_map(file)
        cont += 1

    norm_user_preferences_vector = sum(user_preferences_vector)

    for movie in graph:
        pr_vector = pageranks_values(movie, maps)
        final_output = aggregate_pagerank(pr_vector, user_preferences_vector, norm_user_preferences_vector)
        result[movie] = final_output

    for movie in sorted(result, key=result.get, reverse=True):
        print(movie, result[movie])

        # sum = 0.
        # for movie in result:
        #     sum += result[movie]
        # print(sum)
