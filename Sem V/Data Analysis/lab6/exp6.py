import networkx as nx
import matplotlib.pyplot as plt

friends = ['Aryan', 'Rohit', 'Shikhar', 'Virat', 'Shreyas', 'Rishabh', 'Hardik', 'Ishant', 'Umesh', 'Rahul']
edges = [('Aryan', 'Rohit'), ('Aryan', 'Shikhar'), ('Rohit', 'Virat'), ('Shikhar', 'Shreyas'), ('Shreyas', 'Rishabh'), ('Rishabh', 'Hardik'), ('Hardik', 'Ishant'), ('Ishant', 'Umesh'), ('Umesh', 'Rahul'), ('Rahul', 'Aryan'), ('Virat', 'Hardik'), ('Rohit', 'Ishant')]

G = nx.Graph()
G.add_nodes_from(friends)
G.add_edges_from(edges)

print(G.nodes())
print(G.edges())

#graph

plt.figure(figsize=(6, 6))
nx.draw(G, with_labels=True, node_color='skyblue', font_weight='bold', font_size=10, node_size=1500)
plt.show()

#exporting to csv

import pandas as pd
df_edges = pd.DataFrame(list(G.edges()), columns = ['node1', 'node2'])
df_edges.to_csv('edges.csv', index=False)

df_nodes = pd.DataFrame(list(G.nodes()), columns = ['node'])
df_nodes.to_csv('nodes.csv', index=False)

df_imported_edges = pd.read_csv('edges.csv')
G_imported = nx.from_pandas_edgelist(df_imported_edges, 'node1', 'node2')

print("Nodes:", G_imported.nodes(data=True))
print("Edges:", G_imported.edges(data=True))

plt.figure(figsize=(6, 6))
nx.draw(G_imported, with_labels=True, node_color='skyblue', font_weight='bold', font_size=10, node_size=1500)
plt.show()

#analysis of the community

# Basic graph properties
print("Number of nodes:", G_imported.number_of_nodes())
print("Number of edges:", G_imported.number_of_edges())

# Degree centrality
degrees = dict(G_imported.degree())
print("\nDegree Centrality:", degrees)

betweenness = nx.betweenness_centrality(G_imported, normalized=False)
print("\nBetweenness Centrality:", betweenness)
betweenness = nx.betweenness_centrality(G_imported)
print("Normalized Betweenness Centrality:")
for node, value in betweenness.items():
    print(f"{node}: {value:.4f}") #round upto 4 decimals


# Closeness centrality
e_betwenness = nx.edge_betweenness_centrality(G_imported,normalized=False)
print("\nEdge Betweenness Centrality:", e_betwenness)
e_betwenness = nx.edge_betweenness_centrality(G_imported)
print("Normalized Edge Betweenness Centrality:")
for edge, value in e_betwenness.items():
    print(f"{edge}: {value:.4f}")

# Community detection (Girvan-Newman)

communities = nx.algorithms.community.girvan_newman(G_imported)
try:
    top_level_communities = next(communities)
    print("\nCommunities after 1 step:", top_level_communities)


    top_level_communities = next(communities)
    print("\nCommunities after 2 steps:", top_level_communities)


    top_level_communities = next(communities)
    print("\nCommunities after 3 steps:", top_level_communities)


    top_level_communities = next(communities)
    print("\nCommunities after 4 steps:", top_level_communities)


    top_level_communities = next(communities)
    print("\nCommunities after 5 steps:", top_level_communities)


except StopIteration:
  print('No more splits are possible!')


