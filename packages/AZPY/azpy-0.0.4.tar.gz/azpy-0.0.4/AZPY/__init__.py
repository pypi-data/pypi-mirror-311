import networkx as nx
import numpy as np

def resistance_distance(G, n, R):
    # چاپ مقاومت بین گره‌ها
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            print(f'R({i},{j})={nx.resistance_distance(G, i, j)*R:.3f}')
    
    # محاسبه مجموع کل مقاومت‌ها
    total = sum(nx.resistance_distance(G, i, j)*R 
                for i in range(1, n+1) 
                for j in range(i+1, n+1))
    
    # چاپ و بازگرداندن مجموع کل
    print(f'\nans =\n\n{total:.3f}')
    return total

__all__ = ['resistance_distance']
