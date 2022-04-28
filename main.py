import networkx as nx
import matplotlib.pyplot as plt

# Global variable for routes
routes = []

# Create a drawgraph function


def drawgraph(graph):
    G = nx.Graph()
    for city in graph:
        adjacency = list(graph[city].keys())
        distances = list(graph[city].values())
        for index in range(len(adjacency)):
            G.add_edge(city, adjacency[index], weight=distances[index])
    # pos = nx.nx_agraph.graphviz_layout(G)
    pos = nx.spring_layout(G, scale=100)
    nx.draw_networkx(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 9)
    plt.show()


# Find the available paths
def find_paths(node, cities, path, distance):
    # add the starting city to the path
    path.append(node)
    # Calculate the length of path from starting city
    if len(path) > 1:
        distance += cities[path[-2]][node]

    # If path contains all cities and is not a dead end, add path from last to first city and return.
    # This means path is completed, salesman has visited all cities once and can return to starting city
    if (len(cities) == len(path)) and (path[0] in cities[path[-1]]):
        path.append(path[0])
        distance += cities[path[-2]][path[0]]
        print(path, distance)
        routes.append([distance, path])
        return
    # Create path to unvisited cities
    for city in cities:
        if (city not in path) and (node in cities[city]):
            find_paths(city, dict(cities), list(path), distance)


# permutation example!
# 4 total cities
# Time complexity = (n-1)!
# 1*3*2*1
complete_graph = {
    'Spokane': {'Jakarta': 86, 'Kathmandu': 178,  'Seoul': 91},
    'Jakarta': {'Spokane': 86, 'Seoul': 107, 'Kathmandu': 123},
    'Kathmandu': {'Spokane': 178, 'Jakarta': 123, 'Seoul': 170},
    'Seoul': {'Spokane': 195, 'Jakarta': 107, 'Kathmandu': 210}
}


# permutation example with no complete graph
# Technically, this will still run in (n-1)!
# But since it is not a complete graph, there are only some available paths
# Hence total path < (n-1)!
cities = {
    'Spokane': {'Seoul': 195, 'Jakarta': 86, 'Kathmandu': 178, 'Berlin': 180, 'Beijing': 91},
    'Jakarta': {'Spokane': 86, 'Seoul': 107, 'Hanoi': 171, 'Kathmandu': 123},
    'Kathmandu': {'Spokane': 178, 'Jakarta': 123, 'Hanoi': 170},
    'Seoul': {'Spokane': 195, 'Jakarta': 107, 'Hanoi': 210, 'Boston': 210, 'Singapore': 135, 'Taiwan': 64},
    'Hanoi': {'Seoul': 210, 'Jakarta': 171, 'Kathmandu': 170, 'Singapore': 230, 'Boston': 230},
    'Boston': {'Hanoi': 230, 'Seoul': 210, 'Singapore': 85},
    'Singapore': {'Boston': 85, 'Hanoi': 230, 'Seoul': 135, 'Taiwan': 67},
    'Taiwan': {'Singapore': 67, 'Seoul': 64, 'Berlin': 191},
    'Berlin': {'Taiwan': 191, 'Spokane': 180, 'Beijing': 85, 'Tokyo': 91},
    'Tokyo': {'Berlin': 91, 'Beijing': 120},
    'Beijing': {'Berlin': 120, 'Tokyo': 85, 'Spokane': 91}
}

drawgraph(complete_graph)
drawgraph(cities)

find_paths('Jakarta', complete_graph, [], 0)
routes.sort()

if len(routes) != 0:
    print("Shortest route: ", routes[0][0], routes[0][1])
else:
    print("No possible route can be found!")
