from collections import deque
import csv

__author__ = 'Derek'

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def make_graph(edges, node_index_one=0, node_index_two=1):
    G = {}
    for edge in edges: make_link(G, edge[node_index_one], edge[node_index_two])
    return G

def clustering_coefficient(G,v=None):
    if not v:
        return sum([clustering_coefficient(G, v_x) for v_x in G.keys()]) / len(G)
    neighbors = G[v].keys()
    if len(neighbors) == 1: return -1.0
    links = 0
    for w in neighbors:
        for u in neighbors:
            if u in G[w]: links += 0.5
    return 2.0*links/(len(neighbors)*(len(neighbors)-1))

def read_graph(filename, node_index_one=0, node_index_two=1):
    """Reads a graph from the given file if the file is in tsv format"""
    tsv = csv.reader(open(filename), delimiter='\t')
    return make_graph(tsv, node_index_one, node_index_two)

def centrality(G, v):
    path_lengths = path_length(G, v, None)
    return float(sum(path_lengths.values())) / len(path_lengths)

def path(G, v1, v2):
    path_from_start = {}
    open_list = deque([v1])
    path_from_start[v1] = [v1]
    while len(open_list) > 0:
        current = open_list.popleft()
        for neighbor in G[current].keys():
            if neighbor not in path_from_start:
                path_from_start[neighbor] = path_from_start[current] + [neighbor]
                if neighbor == v2: return path_from_start[neighbor]
                open_list.append(neighbor)
    return path_from_start

def path_length(G, v1, v2):
    path_from_start = {}
    open_list = deque([v1])
    path_from_start[v1] = 0
    while len(open_list) > 0:
        current = open_list.popleft()
        for neighbor in G[current].keys():
            if neighbor not in path_from_start:
                path_from_start[neighbor] = path_from_start[current] + 1
                if neighbor == v2: return path_from_start[neighbor]
                open_list.append(neighbor)
    return path_from_start