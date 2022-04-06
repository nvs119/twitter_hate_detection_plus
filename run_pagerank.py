import matplotlib.pyplot as plt
# from pygraphml import GraphMLParser
# from pygraphml import Graph
import networkx as nx
import numpy as np
import csv

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

count = 0
hateful = 0
normal = 0
avg_hateful = 0
avg_normal = 0
hateful_ranks = []
normal_ranks = []

hateful_bar_graph = [0, 0, 0, 0]
normal_bar_graph = [0, 0, 0, 0]

for item in sorted_pr:
    if users[item] == "other":
        continue
    else:
        print(item, sorted_pr[item])
        print(item, users[item])
        if users[item] == "hateful":
            hateful += 1
            avg_hateful += count
            hateful_ranks.append(count)
            if (count / TOP_HOW_MANY) >= 0.75:
                hateful_bar_graph[3] += 1
            elif (count / TOP_HOW_MANY) >= 0.5:
                hateful_bar_graph[2] += 1
            elif (count / TOP_HOW_MANY) >= 0.25:
                hateful_bar_graph[1] += 1
            else:
                hateful_bar_graph[0] += 1
        elif users[item] == "normal":
            normal += 1
            avg_normal += count
            normal_ranks.append(count)
            if (count / TOP_HOW_MANY) >= 0.75:
                normal_bar_graph[3] += 1
            elif (count / TOP_HOW_MANY) >= 0.5:
                normal_bar_graph[2] += 1
            elif (count / TOP_HOW_MANY) >= 0.25:
                normal_bar_graph[1] += 1
            else:
                normal_bar_graph[0] += 1
        count += 1
    if count == TOP_HOW_MANY:
        break

print("Number of top " + str(TOP_HOW_MANY) + " infuential users that are hateful: " + str(hateful))
print("Number of top " + str(TOP_HOW_MANY) + " influential users that are normal: " + str(normal))

# is this a good metric to have? when there are roughly 9x more normal users
# than hateful?
# print("Average pagerank of a top 100 hateful user: " + str(avg_hateful / hateful))
# print("Average pagerank of a top 100 normal user: " + str(avg_normal / normal))

# line graph
# plot normal users by page rank
# plot hateful users by page rank
x_percentiles = ["top 25%", "25% - 50%", "50% - 75%", "75% - 100%"]
x_axis = np.arange(len(x_percentiles))
hateful_bar_graph = [(i / hateful) * 100 for i in hateful_bar_graph]
normal_bar_graph = [(j / normal) * 100 for j in normal_bar_graph]

plt.bar(x_axis - 0.2, hateful_bar_graph, width=0.4, label = "Hateful")
plt.bar(x_axis + 0.2, normal_bar_graph, width=0.4, label = "Normal")

plt.xticks(x_axis, x_percentiles)
plt.legend()
plt.show()

