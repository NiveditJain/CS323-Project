import random
import numpy as np
import pickle

Graph = {}

def get_line():
    line = input()
    while(line[0] == '/'):
        line = input()
    return line.strip()


def random_normal_generator(mu, sigma, times = 3):
    number = np.random.normal(mu, sigma)

    while number <=0 or abs(number - mu) > times * sigma:
        number = np.random.normal(mu, sigma)

    return round(number, 2)


def prufer_sequence(size):
    sequence = []
    for i in range(size):
        sequence.append(random.randint(1, size + 2))
    return sequence


def add_edge(i,j,distance):
    global Graph

    if i in Graph.keys():
        Graph[i].append([j, distance])
    else:
        Graph[i] = [[j, distance]]

    if j in Graph.keys():
        Graph[j].append([i, distance])
    else:
        Graph[j] = [[i, distance]]


def make_tree(size, mu, sigma):

    degree = [1] * (size + 1)

    prufer = prufer_sequence(size - 2)
    for i in prufer:
        degree[i] = degree[i] + 1

    for i in prufer:
        for j in range(1, size + 1):
            if degree[j] == 1 and i != j:
        
                add_edge(i, j, random_normal_generator(mu, sigma))

                degree[i] = degree[i] - 1
                degree[j] = degree[j] - 1

                break
    
    last = None

    for i in range(1, size + 1):
        if degree[i] == 1:
            if last is None:
                last = i
                degree[i] = degree[i] - 1
            else:
                add_edge(last, i, random_normal_generator(mu, sigma))
                degree[i] = degree[i] - 1
                break


def min_path(source, destination):
    global Graph

    max_dist = 0

    for key in Graph.keys():
        for node in Graph[key]:
            if node[1] > max_dist:
                max_dist = node[1]

    visited = [False] * (len(Graph.keys()) + 1)
    distance = [(max_dist + 1) * len(Graph.keys())] * (len(Graph.keys()) + 1)

    visited[source] = True
    distance[source] = 0
    
    while visited[destination] == False:

        for nbour in Graph[source]:
            if visited[nbour[0]] == False and \
                distance[nbour[0]] > distance[source] + nbour[1]:
                distance[nbour[0]] = distance[source] + nbour[1]

        temp = (max_dist + 1) * len(Graph.keys())

        for i in Graph.keys():
            if visited[i] == False and distance[i] < temp:
                source = i
                temp = distance[i]

        visited[source] = True

    return distance[destination]


def max_path(source, destination):
    global Graph

    visited = [False] * (len(Graph.keys()) + 1)
    distance = [0] * (len(Graph.keys()) + 1)

    visited[source] = True
    distance[source] = 0
    
    while visited[destination] == False:

        for nbour in Graph[source]:
            if visited[nbour[0]] == False and \
                distance[nbour[0]] < distance[source] + nbour[1]:
                distance[nbour[0]] = distance[source] + nbour[1]

        temp = 0

        for i in Graph.keys():
            if visited[i] == False and distance[i] > temp:
                source = i
                temp = distance[i]

        visited[source] = True

    return distance[destination]


def check_edge(i, j):
    global Graph

    for temp in Graph[i]:
        if temp[0] == j:
            return True
    
    return False


def connect_metros(cities, alpha):

    for i in cities:
        for j in cities:
            source = i
            destination = j

            if source != destination:
                if not check_edge(source, destination):
                    lower_bound = (1 - alpha) * min_path(source, destination)
                    upper_bound = (1 + alpha) * max_path(source, destination)
                    add_edge(source, destination, round(np.random.uniform(lower_bound, upper_bound), 2))


def connection_number(max_number):
    if max_number/4 < 1:
        raise Exception("Number of non-metros too less to model")

    number = np.random.normal(max_number/2, max_number/4)
    number = int(number)

    while(number<1 or number>max_number):
        number = np.random.normal(max_number/2, max_number/4)
        number = int(number)

    return number


def connect_cities(metros, nonmetros):

    temp_nonmetos = nonmetros.copy()
    
    for source in metros:
        random.shuffle(temp_nonmetos)
        destinations = temp_nonmetos[:connection_number(len(temp_nonmetos))]

        for destination in destinations:

            if source != destination:
                if not check_edge(source, destination):
                    lower_bound = (1 - alpha) * min_path(source, destination)
                    upper_bound = (1 + alpha) * max_path(source, destination)
                    add_edge(source, destination, round(np.random.uniform(lower_bound, upper_bound), 2))
    

def add_time(souce, destination, time):
    global Graph

    for neighbour in Graph[souce]:
        if neighbour[0] == destination:
            neighbour.append(time)

    for neighbour in Graph[destination]:
        if neighbour[0] == souce:
            neighbour.append(time)


def assign_time(mu, sigma, c):
    global Graph

    for souce in Graph.keys():
        for destination in Graph[souce]:
            if len(destination) == 2:
                denum = c * (max(len(Graph[souce]), len(Graph[destination[0]]))) + random_normal_generator(mu, sigma)
                add_time(souce, destination[0], round(destination[1]/denum, 2))


number_of_cities = int(get_line())

mu1 = int(get_line())

sigma1 = int(get_line())

make_tree(number_of_cities, mu1, sigma1)

number_of_metros = int(get_line())

number_of_remotes = int(get_line())
number_of_non_metros = number_of_cities - number_of_metros - number_of_remotes

alpha = float(get_line())

cities = []
for i in range(1, number_of_cities + 1):
    cities.append(i)
random.shuffle(cities)

metro_cities = cities[:number_of_metros]
non_meto_cities = cities[number_of_metros:number_of_metros+number_of_non_metros]
remote_cities = cities[number_of_metros+number_of_non_metros:]

connect_metros(metro_cities, alpha)
connect_cities(metro_cities, non_meto_cities)

mu2 = int(get_line())

sigma2 = int(get_line())

c = int(get_line())

assign_time(mu2, sigma2, c)

with open('map.pickle', 'wb') as file:
    pickle.dump(Graph, file)

print("map crated : ", Graph)
print("Saved file in python pickle formal as map.pickle")
