import networkx as nx
from iterative_mis.visualize_graph import *
from iterative_mis.utils import *
from iterative_mis.MIS_kernel import PulserMISSolver


num_vertexes = 7    
G = nx.read_gpickle("graphs_dataset/G_{}.gpickle".format(num_vertexes))
G = plot_initial_graph_nx(G, num_vertexes)
rabi_freq, blockade_radius = compute_rydberg(G)
print(f'Blockade Radius {blockade_radius:.2f} μm')
plot_initial_graph_pulser(G, blockade_radius)

coloring =  dict.fromkeys(G.nodes(), -1)
num_colors = 0
orig_G = G.copy()
plot_sol(coloring, orig_G, -1)
while len(G.nodes())> 0:   
    if len(G.edges())>0: 
        # there are still conflict to be solved
        pulser_MIS_solver = PulserMISSolver(G)
        solutions = pulser_MIS_solver.solve_Pulser()
        num_sol = len(solutions)     
        print('Found {} solutions'.format(num_sol))       
        for sol in range(num_sol):  
            x = solutions[sol]      
            if is_MIS(x, G):
                # the solution is indipendent and maximal
                H, MIS_set = compute_subgraph(x, G)
                print(f'Solution at position {sol}')
                break
        G=H
        print(G.nodes)
    else:
        # the same color can be assigned to all the remaining nodes 
        MIS_set=G.nodes()
        G = G.subgraph([])
    num_colors+=1
    # update the coloring
    for graph_node in MIS_set:
        coloring[graph_node]=num_colors 
    plot_sol(coloring.copy(), orig_G, num_colors)
        
print('Iterative MIS solved with {} colors'.format(num_colors)) 