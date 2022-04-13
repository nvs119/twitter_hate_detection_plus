import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import csv
import math

import os
import sys

# open csv
users_csv = open("users_neighborhood_anon.csv")
csvreader = csv.reader(users_csv)

# extract header fields
fields = []
fields = next(csvreader)

# extract rows of users
users = {}
for row in csvreader:
  users[row[0]] = row[1]

print("before read")
g = nx.read_graphml("users_clean.graphml")
print("after read")
pr = nx.pagerank(g)

count = 0
hateful_nodes = []
normal_nodes = []
for node in list(g.nodes):
    if users[node] == "hateful":
        hateful_nodes.append(node)
    elif users[node] == "normal":
        normal_nodes.append(node)

hateful_subgraph = g.subgraph(hateful_nodes)
normal_subgraph = g.subgraph(normal_nodes)

print("Reciprocity of normal nodes: " + str(nx.reciprocity(normal_subgraph)))
print("Reciprocity of hateful nodes: " + str(nx.reciprocity(hateful_subgraph)))