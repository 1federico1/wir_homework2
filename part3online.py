import csv
import os
import sys
import part1 as p1


def from_file_to_map(file):
    map = {}
    input_file = open(file, 'r')
    data = csv.reader(input_file, delimiter='\t')
    for line in data:
        key = int(line[0])
        map[key] = float(line[1])
    return map


def aggregate_pageranks():
    scan_user_pref_vector = 0
    result = {}
    for map in maps:
        for movie in maps[map]:
            try:
                result[movie] += maps[map][movie] * user_preferences_vector[scan_user_pref_vector]
            except KeyError:  # this is for the first time the result map is accessed
                result[movie] = maps[map][movie] * user_preferences_vector[scan_user_pref_vector]
            except IndexError:
                raise IndexError('User preferences vector has to be of five elements')
        scan_user_pref_vector += 1
    return result


def parse_input_vector():
    try:
        user_preferences_vector = ([int(value) for value in user_input.split('_')])
        return user_preferences_vector
    except ValueError:
        raise ValueError('Bad written user preferences vector')


if __name__ == '__main__':
    user_input = sys.argv[1]
    user_preferences_vector = parse_input_vector()
    graph = p1.read_file(p1.movie_file)
    cont = 1
    os.chdir('datasets')
    directory = os.listdir('.')
    files = [file for file in directory if file.startswith('input')]
    files.sort()
    maps = {}

    for file in files:
        maps[cont] = from_file_to_map(file)
        cont += 1

    norm_user_preferences_vector = sum(user_preferences_vector)
    result = aggregate_pageranks()

    for movie in result:
        result[movie] /= norm_user_preferences_vector

    for movie in sorted(result, key=result.get, reverse=True):
        print(movie, result[movie])
