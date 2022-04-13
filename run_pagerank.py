import matplotlib.pyplot as plt
# from pygraphml import GraphMLParser
# from pygraphml import Graph
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

# parser = GraphMLParser()
print("before read")
g = nx.read_graphml("users_clean.graphml")
print("after read")
pr = nx.pagerank(g)

sorted_pr = {k: v for k, v in sorted(pr.items(), key=lambda item: item[1])}

TOP_HOW_MANY = 100

count = 1
hateful = 0
normal = 0
other = 0
hateful_bar_graph = [0]

for item in sorted_pr:
  if users[item] == "other":
    continue
  else:
    if count > 25:
      hateful_bar_graph.append(1)
      count = 1
    if users[item] == "hateful":
      hateful_bar_graph[-1] += 1
      count += 1
    elif users[item] == "normal":
      count += 1

normal_bar_graph = [(25 - i) for i in hateful_bar_graph]

for item in sorted_pr:
  if users[item] == "other":
    other += 1
  elif users[item] == "normal":
    normal += 1
  elif users[item] == "hateful":
    hateful += 1

print("Number of hateful users in this dataset: " + str(hateful))
print("Number of normal users in this dataset: " + str(normal))
print("Number of unlabelled users in this dataset: " + str(other))

percent_hateful = (hateful) / (normal + hateful)
margin = math.sqrt(percent_hateful * (1 - percent_hateful) / (normal + hateful)) * 1.96

print("Percent hateful: " + str(100 * percent_hateful))
print("Confidence Interval : " + str(percent_hateful - margin) + " , " + str(percent_hateful + margin))

x_axis = np.arange(len(hateful_bar_graph))
hateful_bar_graph = [(i / 25) * 100 for i in hateful_bar_graph]
normal_bar_graph = [(j / 25) * 100 for j in normal_bar_graph]

plt.bar(x_axis - 0.2, hateful_bar_graph, width=0.4, label = "Hateful")
plt.bar(x_axis + 0.2, normal_bar_graph, width=0.4, label = "Normal")

# plt.xticks(x_axis, x_percentiles)
plt.legend()
plt.show()

