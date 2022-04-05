import matplotlib
# from pygraphml import GraphMLParser
# from pygraphml import Graph
import networkx as nx

import os
import sys

# parser = GraphMLParser()
print("before read")
g = nx.read_graphml("users_clean.graphml")
print("after read")
pr = nx.pagerank(g)

sorted_pr = {k: v for k, v in sorted(pr.items(), key=lambda item: item[1])}

count = 0
for item in sorted_pr:
    print(item, sorted_pr[item])
    count += 1
    if count == 20:
        break

