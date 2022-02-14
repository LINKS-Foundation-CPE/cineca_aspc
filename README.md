# Optimal graph colouring with Neutral Atoms - CINECA 18th Advanced School on Parallel Computing

## Maximum Independent Set (MIS) tutorial 
[MIS jupiter notebook](https://github.com/LINKS-Foundation-CPE/cineca_aspc/blob/main/UD-mis/UD-mis.ipynb) tutorial provides the basic tools to implement MIS problems through the [Pulser](https://pulser.readthedocs.io/) library, leveraging the Rydberg Blockade effect. Furthermore, it highlights the effect of the optimization approach to make the optimal solutions more likely to be measured.

## Graph coloring (GC) tutorial
[GC jupiter notebook](https://github.com/LINKS-Foundation-CPE/cineca_aspc/blob/main/iterative_mis/GC_iterativeMIS.ipynb) tutorial concerns GC problems solutions through iterative MIS problem solution, exploiting [Pulser](https://pulser.readthedocs.io/) software. It presents two different approaches:
- Greedy-itMIS approach: solve iteratively MIS problem and assign one color at a time
- BB-itMIS: Branch&Bound (BB) approach to explore multiple MIS solutions and find better coloring. It exploits [PyBnB](https://pypi.org/project/pybnb/) library to model the BB exploration.



