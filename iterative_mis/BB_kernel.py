import pybnb
import numpy as np
import networkx as nx
from iterative_mis.utils import compute_LB, compute_obj, compute_UB, fingerprint
from iterative_mis.MIS_kernel import PulserMISSolver
from iterative_mis.utils import is_MIS
import matplotlib.pyplot as plt

class BBQ_MIS(pybnb.Problem):
    
    def __init__(self, G):
        self.G = G 
        self.orig_G = G.copy()     
        self.x = np.zeros((len(G.nodes),1))
        _, LB, _ = compute_LB(self.x, self.G)
        self.colors_used = 0
        self.edges = len(G.edges())
        self.fingerprints=set([])        
        self.lower_bound= LB
        self.child_story={0:-1}
        coloring =  dict.fromkeys(G.nodes(), -1)
        obj, coloring = compute_obj(G, self.colors_used, coloring)
        self.obj = obj
        self.coloring = coloring
        

    def sense(self):
        return pybnb.minimize

    def objective(self):             
        return self.obj

    def bound(self):
        # lower bound on the objective function
        return self.lower_bound

    def save_state(self, node, x=None, colors_used=None, lower_bound=None, H=None, obj=None, coloring=None, child_story=None):
        if x is None:
            # root node initialization
            node.state = (self.x, self.colors_used, self.G, self.edges, self.coloring, self.child_story)
        else:
            num_edges = len(H.edges())
            node.state = (x, colors_used, H, num_edges, coloring, child_story)
            node.objective = obj
            node.bound = lower_bound
            UB = compute_UB(H)
            node.queue_priority = -UB*num_edges          
                      
    def load_state(self, node):
        (self.x, self.colors_used, self.G, self.edges, self.coloring, self.child_story) = node.state
        self.obj = node.objective
        self.lower_bound = node.bound

    def branch(self):
        pulser_MIS_solver = PulserMISSolver(self.G)
        solutions = pulser_MIS_solver.solve_Pulser()
        num_colors_child = self.colors_used+1
        num_sol = len(solutions)
        child_num=0                    
        for sol in range(num_sol): 
            child_story=self.child_story.copy()
            child_story[num_colors_child]=child_num+1
            coloring_dict = self.coloring.copy() 
            x = solutions[sol]      
            if is_MIS(x, self.G):                                
                H, LB, MIS_set = compute_LB(x, self.G)
                for graph_node in MIS_set:
                    coloring_dict[graph_node]=num_colors_child                
                fp = fingerprint(H.nodes())                
                if fp not in self.fingerprints and len(H.nodes())>0:
                    child_num+=1
                    # avoid symmetries in BB
                    child = pybnb.Node()
                    obj, coloring_dict = compute_obj(H, num_colors_child, coloring_dict)
                    # self.plot_sol(coloring_dict.copy(), num_colors_child,child_num)
                    child_bound = num_colors_child+LB
                    self.save_state(child, x, num_colors_child, child_bound, H, obj, coloring_dict, child_story)
                    self.fingerprints.add(fp)
                    yield child
                    
    def plot_sol(self, coloring, num_colors):
        cmap=plt.get_cmap('tab10')
        new_cmap = [(1,1,1)]+list(cmap.colors)
        # represent the iterative coloring
        for col in range(1, num_colors+1):
            coloring_copy = {}
            for key, val in coloring.items():
                if val <= col:
                    coloring_copy[key]=new_cmap[val]
                else:
                    coloring_copy[key]=new_cmap[0]
        
        f = plt.figure()
        nx.draw(self.orig_G, pos=dict(self.orig_G.nodes(data='pos')), node_color=list(coloring_copy.values()), with_labels=True, node_size=500,
                font_weight="bold", node_shape="o", ax=f.add_subplot(111))            
        ax= plt.gca()
        ax.collections[0].set_edgecolor("#000000")
        plt.tight_layout()
        plt.show() 