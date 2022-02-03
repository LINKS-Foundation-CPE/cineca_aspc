import networkx as nx
import matplotlib.pyplot as plt
from pulser import Register


def plot_initial_graph_nx(G, num_vertexes):
    mapping = dict(zip(G, range(1, num_vertexes+1)))
    G = nx.relabel_nodes(G, mapping)
    nx.drawing.nx_pylab.draw(G, pos=dict(G.nodes(data='pos')), with_labels=True)  
    plt.show()
    return G

def plot_initial_graph_pulser(G, rydberg_blockade_radius):
    qubits={}
    for n in G.nodes():
        qubits[n]=G._node[n]['pos']
    reg = Register(qubits)
    reg.draw(blockade_radius=rydberg_blockade_radius, draw_graph=True,  draw_half_radius=True)