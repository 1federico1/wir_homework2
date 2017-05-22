import csv
import part1 as p1

category_file = "datasets/category_movies.txt"
path = "datasets/movie_graph.txt"


def pageranks():
    graph = p1.read_file(path)
    input_file = open(category_file, 'r')
    data = input_file.readlines()
    input_file.close()
    categories = csv.reader(data, delimiter='\t')
    map = {}
    temp_map = {}
    cont = 1
    file_cont = 1

    for category in categories:
        results = [int(i) for i in category]
        map[cont] = results
        current_graph = graph.subgraph(map[cont])
        current_graph = p1.normalize_graph(current_graph)
        teleporting_dist = p1.compute_teleporting_distribution(current_graph)
        temp_map[cont] = p1.compute_page_rank(current_graph, teleporting_dist)
        cont += 1

    for map in temp_map:
        output_file = open('datasets/input_' + str(file_cont) + '.txt', 'w')
        for node in temp_map[map]:
            output_file.write("{}".format(node) + "\t{}".format(temp_map[map][node]) + "\n")
        output_file.close()
        file_cont += 1


if __name__ == '__main__':
    pageranks()
