import csv
import pprint as pp
import part1

category_file = "datasets/category_movies.txt"
path = "datasets/movie_graph.txt"

if __name__ == '__main__':
    graph = part1.read_file(path)
    input_file = open(category_file, 'r')
    data = input_file.readlines()
    input_file.close()
    categories = csv.reader(data, delimiter='\t')
    map = {}
    cont = 1
    online_input = open('datasets/online_input.txt', 'w')

    for category in categories:
        results = []
        results = [int(i) for i in category]
        map[cont] = results
        current_graph = graph.subgraph(map[cont])
        current_graph = part1.normalize_graph(current_graph)
        cont += 1
        teleporting_dist = part1.compute_teleporting_distribution(current_graph)
        pr_vector = part1.compute_page_rank(current_graph, teleporting_dist)
        for node in pr_vector:
            online_input.write(str(node) + "\t{0}".format(pr_vector[node]) + "\t")
        online_input.write("\n")
    online_input.close()
