####### Graph Building using data from Arnes.gml ########
import networkx as nx
import time
import random
import math
import numpy as np
import pandas as pd

from math import radians, cos, sin, asin, sqrt
from collections import defaultdict

####### Data collection, cleaning, and handling corner cases #######


def build_graph(k, graph, final_data):
    lat = nx.get_node_attributes(graph, "Latitude")
    lon = nx.get_node_attributes(graph, "Longitude")

    # Remove bad nodes from 'graph'
    for node in list(graph.nodes):
        # removing nodes
        # (a) with undefined latitude or longitude
        # (b) that are isolated
        check_bad_node = lat.get(node) == None or lon.get(
            node) == None or nx.is_isolate(graph, node)
        if check_bad_node == True:
            graph.remove_node(node)

    def dist_between_nodes(node_1, node_2):
        '''Compute distance between any 2 nodes of 'graph' using Haversine formula

        Args:
            node_1 (int): The first among the 2 graph nodes 
            node_2 (int): The second among the 2 graph nodes 

        Returns:
            dist: distanct between the two nodes
        '''
        lat_1 = radians(lat.get(node_1))
        lat_2 = radians(lat.get(node_2))
        lon_1 = radians(lon.get(node_1))
        lon_2 = radians(lon.get(node_2))

        # Applying Haversine formula
        dlon = lon_2 - lon_1
        dlat = lat_2 - lat_1
        a = sin(dlat/2)**2 + cos(lat_1)*cos(lat_2)*sin(dlon/2)**2
        c = 2*asin(sqrt(a))

        # Mean radius of Earth
        R = 6371.009
        dist = c*R

        return dist

    # Assigning weights (based on distance) to the edges of the graph
    for node in list(graph.nodes):
        for neighbor in list(graph.neighbors(node)):
            graph[node][neighbor]['weight'] = dist_between_nodes(
                node, neighbor)

    # Removing edges with no weights assigned
    for edge in list(graph.edges):
        if 'weight' not in graph.edges[edge] == False:
            graph.remove_edge(edge[0], edge[1])

    print(nx.info(graph))
    n = nx.number_of_nodes(graph)

    ####### Graph building and Controllers' Cluster formation #######

    # Store the graph as an adjacency list
    adj_list = []
    for i in range(0, n):
        adj_list.append([])

    for edge in graph.edges:
        i, j = edge
        adj_list[i].append(j)
        adj_list[j].append(i)

    # Random sampling for controller index selection
    controllers = random.sample(range(0, n), k)

    # List of lists represents index of switches in particular controller
    # e.g. [[s1,s2],[s3,s4],[s5]] controller distribution set
    lol = []
    for i in range(0, k):
        lol.append([])

    # Controllers set
    # Keeping copies for Greedy approach and Q-learning
    controllers_Q = list(controllers)
    controllers_G = list(controllers)
    print("\nControllers: \n{}\n".format(controllers))

    def BFS(queue, adj_list, listx):
        '''Performs a breadth first search in the graph
        '''
        while queue:
            p = queue.pop(0)
            u, w = p
            for v in adj_list[u]:
                if listx[v] == math.inf:
                    listx[v] = w + 1
                    queue.append((v, w + 1))
        return listx

    index = 0
    for j in range(0, k):
        listx = n*[math.inf]
        listx[controllers[index]] = 0
        queue = []
        queue.append((controllers[index], 0))
        listx = BFS(queue, adj_list, listx)
        lol[j] = listx
        index += 1

    transpose_list = np.transpose(lol).tolist()
    minumum_pos = []

    for x in transpose_list:
        min_ele = n+5
        for i in range(0, len(x)):
            if x[i] < min_ele:
                min_ele = x[i]
        ts = []
        for i in range(0, len(x)):
            if(x[i] == min_ele):
                ts.append(i)
        minumum_pos.append(random.choice(ts))

    final = []
    controller_sets = []
    for i in range(0, k):
        controller_sets.append([])

    for i in range(0, n):
        final.append((i, controllers[minumum_pos[i]]))
        controller_sets[minumum_pos[i]].append(i)

    print('Cluster set for each controller: \n{}\n'.format(controller_sets))
    controller_maps = {}
    index = 0

    for controller_set in controller_sets:
        switch_array, controller = [], controllers[index]
        for switch in controller_set:
            if switch != controller:
                switch_array.append(switch)
        controller_maps[controller] = switch_array
        index += 1

    print('Cluster map for each controller: \n{}\n'.format(controller_maps))

    def floyd_warshall(graph):
        d = defaultdict(set)
        cnt = defaultdict(set)
        inf = float('inf')

        # Initialising distance between all nodes as infinity
        for node1 in graph.nodes:
            for node2 in graph.nodes:
                d[(node1, node2)] = inf
                cnt[(node1, node2)] = inf

        # Changing the distance between adjacent nodes
        for edge in graph.edges:
            # Undirected graph
            d[(edge[0], edge[1])] = graph.edges[edge]['weight']
            d[(edge[1], edge[0])] = graph.edges[edge]['weight']
            cnt[(edge[0], edge[1])] = 1
            cnt[(edge[1], edge[0])] = 1

        for node in graph.nodes:
            d[(node, node)] = 0
            cnt[(node, node)] = 0

        # Updating the matrix
        for node1 in graph.nodes:
            for node2 in graph.nodes:
                for node3 in graph.nodes:
                    if d[(node2, node3)] > d[(node2, node1)] + d[(node1, node3)]:
                        d[(node2, node3)] = d[(node2, node1)] + d[(node1, node3)]
                        d[(node3, node2)] = d[(node2, node3)]
                        cnt[(node2, node3)] = cnt[(node2, node1)] + \
                            cnt[(node1, node3)]
                        cnt[(node3, node2)] = cnt[(node2, node3)]

        return [d, cnt]

    [dist, hop_count] = floyd_warshall(graph)

    print('Having used Floyd Warshall algorithm, we obtain the following - (i) Dist and (ii) Hop Count')
    print(dist)
    print(hop_count)

    # Keeping another copy of the controller set for Greedy approach
    controller_sets_G = list(controller_sets)
    print(controller_sets_G)

    # Keeping another copy of the controller set for Q-learning
    controller_sets_Q = list(controller_sets)
    print(controller_sets_Q)

    load_array = []  # Array of maps, with each node mapped to a load
    for i in final_data.index:
        Load = dict(final_data.loc[i])
        load_array.append(Load)

    print(load_array)
    return controllers_Q, controller_sets_Q, controller_sets_G, load_array
