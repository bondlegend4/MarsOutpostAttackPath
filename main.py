import ezodf
import networkx as nx
import matplotlib.pyplot as plt

# Load the .ods file
doc = ezodf.opendoc("Mars Outpost Attack Path.ods")

# Extract the Nodes and Edges sheets
nodes_sheet = doc.sheets["Nodes"]
edges_sheet = doc.sheets["Edges"]

# Function to extract data from a sheet
def extract_data(sheet):
    data = []
    for row in sheet.rows():
        data.append([cell.value for cell in row])
    return data

# Extract nodes and edges data
nodes_data = extract_data(nodes_sheet)
edges_data = extract_data(edges_sheet)

# Create a graph
G = nx.DiGraph()

# Add nodes to the graph
for node in nodes_data[1:]:  # Skip the header
    node_id, node_label, mitre_attack = node[0], node[1], node[2]
    G.add_node(node_id, label=node_label, mitre_attack=mitre_attack)

# Add edges to the graph with attributes
for edge in edges_data[1:]:  # Skip the header
    source, target, edge_attack, edge_mediation, edge_mediation_boolean = edge
    G.add_edge(source, target, edge_attack=edge_attack, edge_mediation=edge_mediation, edge_mediation_boolean=edge_mediation_boolean)

# Draw the graph
pos = nx.spring_layout(G)  # Layout for visualization
labels = {node: f"{attr['label']}\nMITRE ATT&CK: {attr['mitre_attack']}" for node, attr in G.nodes(data=True)}
edge_labels = {(source, target): f"Attack: {attr['edge_attack']}\nMediation: {attr['edge_mediation']}\nMediated: {attr['edge_mediation_boolean']}"
               for source, target, attr in G.edges(data=True)}

plt.figure(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', rotate=False)

plt.title("Mars Outpost Attack Path Tree")
plt.show()