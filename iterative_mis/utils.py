import networkx as nx
from pulser.devices import Chadoq2
from scipy.spatial import distance_matrix
import numpy as np
import matplotlib.pyplot as plt

def compute_rydberg(G):
    pos_list =[]
    for n in G.nodes():
        pos_list.append(G._node[n]['pos'])
    pos=np.array(pos_list) 
    # find the rydberg blockade radius
    dist_matrix = distance_matrix(pos, pos)
    A = nx.to_numpy_matrix(G)
    blockade_radius = dist_matrix[A==1].max() 
    rabi_freq = Chadoq2.rabi_from_blockade(blockade_radius)
    return rabi_freq, blockade_radius

def _check_maximal(A, x):
    not_selected_nodes = np.where(x == 0)[0]
    maximal_set = True
    for node in not_selected_nodes:
        x_copy = x.copy()
        x_copy[node]=1
        if x_copy.T@A@x_copy==0:
            maximal_set = False
            break
    return maximal_set

def is_MIS(x,G):
    A = nx.to_numpy_matrix(G)
    num_conflicts = int(x.T@A@x)
    maximal_set = _check_maximal(A, x)
    is_MIS = (num_conflicts == 0 and maximal_set)
    return is_MIS

def compute_subgraph(x, G):
    MIS_set = []
    node_set = list(G.nodes())
    for node in range(len(x)):
        if x[node] == 1:
            MIS_set.append(node_set[node])
    remaining_nodes = set(node_set).difference(set(MIS_set))
    H = G.subgraph(remaining_nodes)    
    return H, MIS_set

