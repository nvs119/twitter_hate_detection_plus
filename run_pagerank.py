import matplotlib
# from pygraphml import GraphMLParser
# from pygraphml import Graph
import networkx as nx
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

count = 0
hateful = 0
normal = 0
avg_hateful = 0
avg_normal = 0
for item in sorted_pr:
    if users[item] == "other":
        continue
    else:
        print(item, sorted_pr[item])
        print(item, users[item])
        if users[item] == "hateful":
            hateful += 1
            avg_hateful += count
        elif users[item] == "normal":
            normal += 1
            avg_normal += count
        count += 1
    if count == 100:
        break

print("Number of top 100 infuential users that are hateful: " + str(hateful))
print("Number of top 100 influential users that are normal: " + str(normal))

# is this a good metric to have? when there are roughly 9x more normal users
# than hateful?
print("Average pagerank of a top 100 hateful user: " + str(avg_hateful / hateful))
print("Average pagerank of a top 100 normal user: " + str(avg_normal / normal))

