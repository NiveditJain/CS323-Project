import random
import numpy as np


def normal_generate(mu, sigma, times):
    number = np.random.normal(mu, sigma)

    while number <= 0 or abs(number - mu) > times * sigma:
        number = np.random.normal(mu, sigma)

    return round(number, 3)


def make_tree(n):
    tree = []
    prufer_sequence = []

    # generating a random prufer_sequence
    for _ in range(n - 2):
        prufer_sequence.append(random.randint(1, n))

    # converting prufer sequence to tree
    degree = [1] * (n + 1)

    for i in prufer_sequence:
        degree[i] = degree[i] + 1

    for element in prufer_sequence:
        for node in range(1, n + 1):
            if degree[node] == 1 and node != element:
                tree.append((element, node))
                degree[node] = degree[node] - 1
                degree[element] = degree[element] - 1
                break

    last = 0

    for i in range(1, n + 1):
        if degree[i] == 1:
            if last == 0:
                last = i
            else:
                tree.append((last, i))
                break

    return tree


def display(edges):
    import networkx
    import matplotlib.pyplot as plt

    graph = networkx.Graph()

    for edge in edges:
        graph.add_edge(edge[0], edge[1])

    networkx.draw(graph, with_labels=True)
    plt.show()


def assign_d1(tree, mu, sigma, times):
    new_tree = []

    for edge in tree:
        new_tree.append((edge[0], edge[1], normal_generate(mu, sigma, times)))

    return new_tree


def change_coding(n, tree):
    graph = []

    for _ in range(n + 1):
        graph.append(list())

    for edge in tree:
        graph[edge[0]].append([edge[1], edge[2]])
        graph[edge[1]].append([edge[0], edge[2]])

    return graph


def minPath(graph, n, start, end, max_dist):
    visited = [False] * (n + 1)
    distance = [max_dist] * (n + 1)

    visited[start] = True
    distance[start] = 0
    present = start

    while not visited[end]:
        for neighbour in graph[present]:
            if visited[neighbour[0]] == False and \
                    distance[neighbour[0]] > distance[present] + neighbour[1]:
                distance[neighbour[0]] = distance[present] + neighbour[1]

        next_val = max_dist

        for i in range(1, n+1):
            if visited[i] == False and distance[i] < next_val:
                present = i
                next_val = distance[i]

        visited[present] = True

    return round(distance[end], 3)


def maxPath(graph, n, start, end):
    visited = [False] * (n + 1)
    distance = [-1] * (n + 1)

    visited[start] = True
    distance[start] = 0
    present = start

    while not visited[end]:
        for neighbour in graph[present]:
            if visited[neighbour[0]] == False and \
                    distance[neighbour[0]] < distance[present] + neighbour[1]:
                distance[neighbour[0]] = distance[present] + neighbour[1]

        next_val = -1

        for i in range(1, n + 1):
            if visited[i] == False and distance[i] > next_val:
                present = i
                next_val = distance[i]

        visited[present] = True

    return round(distance[end], 3)


if __name__ == '__main__':
    tree = make_tree(4000)
    print(tree)
    graph = change_coding(4000, assign_d1(tree, 50, 10, 3))
    print(graph)
    print(minPath(graph, 4000, 1, 4000, 1000000000))
    print(maxPath(graph, 4000, 1, 4000))
