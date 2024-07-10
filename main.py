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
    node_id = int(node_id)  # Ensure node_id is treated as an integer
    G.add_node(node_id, label=node_label, mitre_attack=mitre_attack)

# Add edges to the graph with attributes
for edge in edges_data[1:]:  # Skip the header
    source, target, edge_attack, edge_mediation, edge_mediation_boolean = edge
    source = int(source)  # Ensure source is treated as an integer
    target = int(target)  # Ensure target is treated as an integer
    G.add_edge(source, target, edge_attack=edge_attack, edge_mediation=edge_mediation, edge_mediation_boolean=edge_mediation_boolean)

# Function to create positions for nodes based on node_id and tree_level
def create_positions(nodes_data):
    pos = {}
    level_node_ids = {}
    
    for node in nodes_data[1:]:  # Skip the header
        node_id, _, _ = node
        node_id = int(node_id)  # Ensure node_id is treated as an integer
        level = node_id // 100
        
        if level not in level_node_ids:
            level_node_ids[level] = []
        
        level_node_ids[level].append(node_id)
    
    for level, node_ids in level_node_ids.items():
        count = len(node_ids)
        if count == 1:
            pos[node_ids[0]] = (level, 0)
        else:
            mid = count // 2
            for i, node_id in enumerate(node_ids):
                pos[node_id] = (level, (i - mid) if count % 2 != 0 else (i - mid + 0.5))
    
    return pos

# Create node positions
pos = create_positions(nodes_data)
labels = {node: f"{attr['label']}\nMITRE ATT&CK: {attr['mitre_attack']}" for node, attr in G.nodes(data=True)}
edge_labels = {(source, target): f"Attack: {attr['edge_attack']}\nMediation: {attr['edge_mediation']}\nMediated: {attr['edge_mediation_boolean']}"
               for source, target, attr in G.edges(data=True)}

# Draw the graph
plt.figure(figsize=(14, 8))
nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=8, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8, rotate=False)

plt.title("Mars Outpost Attack Path Tree")
plt.show()
