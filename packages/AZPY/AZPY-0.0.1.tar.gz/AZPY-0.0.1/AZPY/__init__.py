import numpy as np
import networkx as nx

def resistance_distance(G, n, R):
   for i in range(1, n+1):
       for j in range(i+1, n+1):
           print(f'R({i},{j})={nx.resistance_distance(G, i, j)*R:.3f}\n')
   total = sum(nx.resistance_distance(G, i, j)*R 
              for i in range(1, n+1) 
              for j in range(i+1, n+1))
   
   return (print(f'ans =\n\n{total:.3f}\n'f'\nans =\n\n{total:.3f}'))   