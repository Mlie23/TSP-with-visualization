import networkx as nx
import matplotlib.pyplot as plt
import timeit 
import tkinter as tk
from PIL import Image,ImageTk

# Global variable for routes
routes = []
count = True
# Create a drawgraph function
def drawK5(graph):
    if count == True:
        plt.figure(1)
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

def drawK6(graph):
    plt.figure(2)
    Y = nx.Graph()
    for city in graph:
        adjacency = list(graph[city].keys())
        distances = list(graph[city].values())
        for index in range(len(adjacency)):
            Y.add_edge(city, adjacency[index], weight=distances[index])
    # pos = nx.nx_agraph.graphviz_layout(G)
    pos = nx.spring_layout(Y, scale=100)
    nx.draw_networkx(Y, pos)
    labels = nx.get_edge_attributes(Y, 'weight')
    nx.draw_networkx_edge_labels(Y, pos, edge_labels=labels)
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 9)
    plt.show()

def shortest_paths(graph,starting,txtfile):
    start = timeit.default_timer()
    find_paths(starting, graph, [], 0)
    stop = timeit.default_timer()
    f = open(txtfile, "w")
    f.write("Time taken: " +str(stop-start)+"\n")
    routes.sort()
    if len(routes) != 0:
        path = ""
        for i in ((routes[0][1])):
            path = path+i+"-"
        path= path[:-1]
        f.write("Shortest route: "+ str(routes[0][0])+"\n"+ "Path: "+path)
    else:
        f.write("No possible route can be found!")
    f.close()

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
five_cg = {
    'Spokane': {'Jakarta': 86, 'Kathmandu': 178,  'Seoul': 195,'Tokyo':100},
    'Jakarta': {'Spokane': 86, 'Seoul': 107, 'Kathmandu': 123,'Tokyo':100},
    'Kathmandu': {'Spokane': 178, 'Jakarta': 123, 'Seoul': 170,'Tokyo':100},
    'Seoul': {'Spokane': 195, 'Jakarta': 107, 'Kathmandu': 170,'Tokyo':100},
    'Tokyo':{'Jakarta': 100, 'Kathmandu': 100,  'Seoul': 100,'Spokane':100}
}


six_cg = {
    'Spokane': {'Jakarta': 86, 'Kathmandu': 178,  'Seoul': 195,'Tokyo':121,'Singapore':210},
    'Jakarta': {'Spokane': 86, 'Seoul': 107, 'Kathmandu': 123,'Tokyo':99,'Singapore':50},
    'Kathmandu': {'Spokane': 178, 'Jakarta': 123, 'Seoul': 170,'Tokyo':140,'Singapore':177},
    'Seoul': {'Spokane': 195, 'Jakarta': 107, 'Kathmandu': 210,'Tokyo':120,'Singapore':195},
    'Tokyo':{'Jakarta': 99, 'Kathmandu': 140,  'Seoul': 120,'Spokane':121,'Singapore':89},
    'Singapore':{'Jakarta': 50, 'Kathmandu': 177,  'Seoul': 195,'Tokyo':89,'Spokane':210}
}
shortest_paths(five_cg,"Spokane","K5.txt")
routes = []
shortest_paths(six_cg,"Spokane","K6.txt")
# permutation example with no complete graph
# Technically, this will still run in (n-1)!
# But since it is not a complete graph, there are only some available paths
# Hence total path < (n-1)!
# cities = {
#     'Spokane': {'Seoul': 195, 'Jakarta': 86, 'Kathmandu': 178, 'Berlin': 180, 'Beijing': 91},
#     'Jakarta': {'Spokane': 86, 'Seoul': 107, 'Hanoi': 171, 'Kathmandu': 123},
#     'Kathmandu': {'Spokane': 178, 'Jakarta': 123, 'Hanoi': 170},
#     'Seoul': {'Spokane': 195, 'Jakarta': 107, 'Hanoi': 210, 'Boston': 210, 'Singapore': 135, 'Taiwan': 64},
#     'Hanoi': {'Seoul': 210, 'Jakarta': 171, 'Kathmandu': 170, 'Singapore': 230, 'Boston': 230},
#     'Boston': {'Hanoi': 230, 'Seoul': 210, 'Singapore': 85},
#     'Singapore': {'Boston': 85, 'Hanoi': 230, 'Seoul': 135, 'Taiwan': 67},
#     'Taiwan': {'Singapore': 67, 'Seoul': 64, 'Berlin': 191},
#     'Berlin': {'Taiwan': 191, 'Spokane': 180, 'Beijing': 85, 'Tokyo': 91},
#     'Tokyo': {'Berlin': 91, 'Beijing': 120},
#     'Beijing': {'Berlin': 120, 'Tokyo': 85, 'Spokane': 91}
# }
root = tk.Tk()
canvas = tk.Canvas(root,width=700,height=500)
canvas.grid(columnspan=3,rowspan=3)
logo = Image.open("logo.PNG")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.grid(column=1,row=0)
title = tk.Label(root,text="TSP visualization with Brute Force Algorithm  ©Michael Lie-2022")
title.grid(columnspan=3,column=1,row=3)

instructions = tk.Label(root, text="Select different K(n) graph", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)
#browse button
K5 = tk.StringVar()
K5_btn = tk.Button(root, textvariable=K5, command=lambda:drawK5(five_cg), font="Raleway", bg="#20bebe", fg="white", height=2, width=10)
K5.set("K5")
K5_btn.place(x=275,y=430)
K6 = tk.StringVar()
K6_btn = tk.Button(root, textvariable=K6, command=lambda:drawK6(six_cg), font="Raleway", bg="#20bebe", fg="white", height=2, width=10)
K6.set("K6")
K6_btn.place(x=375,y=430)

root.mainloop(0)

# drawgraph(five_cg)





