import csv
import part1 as p1

category_file = "datasets/category_movies.txt"


def read_categories_file():
    input_file = open(category_file, 'r')
    data = input_file.readlines()
    input_file.close()
    return csv.reader(data, delimiter='\t')


def compute_teleporting_probability(graph, category):
    teleporting_distribution = {}
    for node in graph:
        if node in category:
            teleporting_distribution[node] = 1. / len(category)
        else:
            teleporting_distribution[node] = 0.
    return teleporting_distribution


def compute_pageranks_for_categories(categories, cont, graph, map, temp_map):
    for category in categories:
        results = [int(i) for i in category]
        map[cont] = results
        # current_graph = graph.subgraph(map[cont])
        # current_graph = p1.normalize_graph(current_graph)
        # teleporting_dist = p1.compute_teleporting_distribution(current_graph)
        teleporting_dist = compute_teleporting_probability(graph, map[cont])
        temp_map[cont] = p1.compute_page_rank(graph, teleporting_dist)
        cont += 1


def write_pageranks_to_files(file_cont, temp_map):
    for map in temp_map:
        output_file = open('datasets/input_' + str(file_cont) + '.txt', 'w')
        for node in temp_map[map]:
            output_file.write("{}".format(node) + "\t{}".format(temp_map[map][node]) + "\n")
        output_file.close()
        file_cont += 1


def pageranks():
    graph = p1.read_file(p1.movie_file)
    graph = p1.normalize_graph(graph)

    categories = read_categories_file()
    map = {}
    temp_map = {}
    cont = 1
    file_cont = 1

    compute_pageranks_for_categories(categories, cont, graph, map, temp_map)

    write_pageranks_to_files(file_cont, temp_map)



    # if __name__ == '__main__':
    # pageranks()
