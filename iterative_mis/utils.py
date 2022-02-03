import networkx as nx
from pulser.devices import Chadoq2
from scipy.spatial import distance_matrix
import numpy as np

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