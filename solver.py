import matplotlib.pyplot as plt
import networkx as nx

def get_line():
    line = input()
    while(line[0] == '/'):
        line = input()
    return line.strip()

solutions = []

def dfs(depth, max_depth, present_node, destination, path, parcels, delivered, edges_traveled):
    global Graph

    if depth > max_depth:
        return

    if present_node == destination:
        solutions.append((path, parcels, delivered))

    for neighbour in Graph[present_node]:
        if (neighbour[0], present_node) not in edges_traveled \
            and (present_node, neighbour[0]) not in edges_traveled:

            temp_delivered = []
            for parcel in parcels:
                if parcel[0] == neighbour[0]:
                    temp_delivered.append(parcel)

            dfs(depth+1, max_depth, neighbour[0], destination, path + [neighbour], parcels, delivered + temp_delivered,edges_traveled + [(neighbour[0], present_node)])


def get_cost(path, parcels, delivered):
    global c1, c2, c3, m, Ts, Ls
    time = 0
    distance = 0
    for node in path:
        distance = distance + node[1]
        time = time + node[2]
    
    cost = c1 * distance + c2 * (len(parcels) * Ls + len(delivered) * Ts + time)
    
    for parcel in delivered:
        cost = cost - c3 * parcel[3]

    cost = cost + m * (len(parcels) - len(delivered))
    
    return cost


def get_best():
    global solutions
    
    if len(solutions) == 0:
        return

    best_cost = get_cost(solutions[0][0], solutions[0][1], solutions[0][2])
    best_solution = solutions[0]

    for i in range(1, len(solutions)):
        cost = get_cost(solutions[i][0], solutions[i][1], solutions[i][2])
        if cost < best_cost:
            best_cost = cost
            best_solution = solutions[i]

    return best_solution


def display(path, start):

    optimal_path = list()
    prev = start

    for node in path:
        optimal_path.append((prev, node[0]))
        prev = node[0]
   
    g = nx.DiGraph()
    
    for i in optimal_path:
        g.add_edge(i[0], i[1], weigth = 5)
    
    nx.draw(g, with_labels=True) 
    plt.show()


Vv = int(get_line())

Vm = int(get_line())

c1 = int(get_line())

c2 = int(get_line())

c3 = int(get_line())

Ts = int(get_line())

Ls = int(get_line())

m = int(get_line())

num_edges = int(get_line())

Graph = {}

for i in range(num_edges):
    data = get_line().split(',')
    
    if data[0] in Graph.keys():
        Graph[data[0]].append((data[1], int(data[2]), int(data[3])))
    else:
        Graph[data[0]] = [(data[1], int(data[2]), int(data[3]))]

    if data[1] in Graph.keys():
        Graph[data[1]].append((data[0], int(data[2]), int(data[3])))
    else:
        Graph[data[1]] = [(data[0], int(data[2]), int(data[3]))]

stepSize = int(get_line())

epochs = int(get_line())

num_of_parcels = int(get_line())

parcels = []

for i in range(num_of_parcels):
    data = get_line().split(',')
    parcels.append((data[0], int(data[1]), int(data[2]), int(data[3])))

start = get_line()

end = get_line()

for epoch in range(1,epochs+1):
    print(f"running epoch{epoch}, best solution found : ", end="")
    
    parcel_set = []

    for bit_mask in range(pow(2,num_of_parcels)):
        for i in range(num_of_parcels):
            if ((bit_mask & (1<<i)) > 0):
                parcel_set.append(parcels[i])

        temp_volume = 0
        temp_mass = 0

        for parcel in parcel_set:
            temp_mass = temp_mass + parcel[1]
            temp_volume = temp_volume + parcel[2]

        if temp_mass <= Vm and temp_volume <=Vv:
            dfs(0, epoch*stepSize, 'A', 'C', [], parcel_set, [], [])
        parcel_set = []
    
    best_solution = get_best()
    if best_solution == None:
        print("no goal state found")
    else:
        print("path ->", best_solution[0], "  parcels delivered ->", best_solution[1])

display(best_solution[0], start)
