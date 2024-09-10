import plotly.graph_objects as go
import networkx as nx
import json
import numpy as np
from PIL import Image
import yaml

# Function to read the color palette from a file
def read_color_palette(palette_path='color_palette.yaml'):
    with open(palette_path, 'r') as file:
        data = yaml.safe_load(file)
        return data['colors']

# Function to read graph JSON
def read_graph_json(graph_json_path='graph_updated.json'):
    with open(graph_json_path, 'r') as file:
        return nx.node_link_graph(json.load(file))

# Function to calculate bounds
def calculate_bounds(coords):
    min_x, max_x = np.min(coords[:, 0]), np.max(coords[:, 0])
    min_y, max_y = np.min(coords[:, 1]), np.max(coords[:, 1])
    return min_x, max_x, min_y, max_y

# Function to place head nodes
def place_head_nodes(center_x, center_y, num_nodes, spacing):
    angles = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False)
    x_positions = center_x + spacing * np.cos(angles)
    y_positions = center_y + spacing * np.sin(angles)
    return x_positions, y_positions

# Function to add category nodes (no legend entry)
def add_category_nodes(fig, category, color, z_value, symbol, nodescord, size=3):
    if category in nodescord and len(nodescord[category]) > 0:
        x_coords = nodescord[category][:, 0]
        y_coords = nodescord[category][:, 1]
        z_coords = np.full_like(nodescord[category][:, 2], z_value)
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers',
            marker=dict(size=size, color=color, symbol=symbol),
            showlegend=False  # Disable legend for category nodes
        ))

# Function to add a head node (included in the legend)
def add_head_node(fig, category, head_node, color):
    fig.add_trace(go.Scatter3d(
        x=[head_node[0]],
        y=[head_node[1]],
        z=[head_node[2]],
        mode='markers+text',
        marker=dict(size=10, color=color),
        text=[category.capitalize()],
        textposition='top center',
        name=f'{category.capitalize()} Head'
    ))

# Function to add connections (no legend entry)
def add_connections(fig, head_node, detections, color):
    for det in detections:
        fig.add_trace(go.Scatter3d(
            x=[head_node[0], det[0]],
            y=[head_node[1], det[1]],
            z=[head_node[2], det[2]],
            mode='lines',
            line=dict(color=color, width=1),
            showlegend=False  # Disable legend for connections
        ))

# Function to add child nodes (no legend entry)
def add_child_nodes(fig, parent_node, children, color, child_z):
    for child in children:
        x_coords = child['pose'][0]
        y_coords = child['pose'][1]
        z_coords = child_z
        
        # Plot child nodes
        fig.add_trace(go.Scatter3d(
            x=[x_coords],
            y=[y_coords],
            z=[z_coords],
            mode='markers',
            marker=dict(size=5, color=color, symbol='diamond'),
            name=child['category'],
            showlegend=False  # Disable legend for child nodes
        ))
        
        # Plot connection to parent node
        fig.add_trace(go.Scatter3d(
            x=[parent_node[0], x_coords],
            y=[parent_node[1], y_coords],
            z=[parent_node[2], z_coords],
            mode='lines',
            line=dict(color=color, width=1),
            showlegend=False  # Disable legend for connections
        ))

# Load map metadata from the map.yaml file
with open('map.yaml', 'r') as file:
    map_metadata = yaml.safe_load(file)

resolution = map_metadata['resolution']
origin = map_metadata['origin']
image_path = "map.png"

# Load the grayscale map image using PIL
map_image = Image.open(image_path).convert('L')
map_image = np.array(map_image)

# Get the height and width of the image
image_height, image_width = map_image.shape

# Convert pixel coordinates to world coordinates
def pixels_to_world_coordinates(map_metadata, pixel_coords):
    pixel_x, pixel_y = pixel_coords
    world_x = pixel_x * map_metadata["resolution"] + map_metadata["origin"][0]
    world_y = (image_height - pixel_y) * map_metadata["resolution"] + map_metadata["origin"][1]
    return [world_x, world_y, 0]

# Create lists to hold the world coordinates for obstacles
world_coords = []
nodescord = {}  # Dictionary to hold nodes by category
head_nodes = {}  # Head nodes for class names

# Iterate through each pixel in the image
for y in range(image_height):
    for x in range(image_width):
        if map_image[y, x] != 0 and map_image[y, x] != 255:  # Plot only obstacles
            world_coord = pixels_to_world_coordinates(map_metadata, (x, y))
            world_coords.append(world_coord)

# Convert to numpy array for easier manipulation
world_coords = np.array(world_coords)

# Get bounds for obstacles
min_x, max_x, min_y, max_y = calculate_bounds(world_coords)

# Calculate center coordinates
center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2

# Determine spacing
num_head_nodes = 0
spacing = 30  # Adjust as needed for spacing

# Load color palette
colors = read_color_palette()

# Initialize graph and organize nodes by category
graph = read_graph_json()
for node, data in graph.nodes(data=True):
    category = data["category"]
    if category not in nodescord:
        nodescord[category] = []
        head_nodes[category] = None
        num_head_nodes += 1
    
    pose = data["pose"]
    pose[2] = 2.5  # Shift detections to lower Z level
    pose[0], pose[1] = pose[0], -pose[1]
    nodescord[category].append(pose)

# Place head nodes
x_head, y_head = place_head_nodes(center_x, center_y, num_head_nodes, spacing)

# Set head node positions
for idx, category in enumerate(nodescord):
    head_nodes[category] = [x_head[idx], y_head[idx], 5]

# Convert lists to numpy arrays
for category in nodescord:
    nodescord[category] = np.array(nodescord[category])

# Plotting with Plotly
fig = go.Figure()

# Add obstacle points (included in the legend)
fig.add_trace(go.Scatter3d(
    x=world_coords[:, 0],
    y=world_coords[:, 1],
    z=world_coords[:, 2],
    mode='markers',
    marker=dict(size=1, color='black'),
    name='Obstacles'  # Keep obstacles in the legend
))

# Add category nodes, head nodes, and connections
for idx, category in enumerate(nodescord):
    color = colors[idx % len(colors)]
    add_category_nodes(fig, category, color, 2.5, 'circle', nodescord)
    add_head_node(fig, category, head_nodes[category], color)  # Keep head nodes in the legend
    add_connections(fig, head_nodes[category], nodescord[category], color)

    # Add child nodes and connections
    for node, data in graph.nodes(data=True):
        if "children" in data and data["children"]:
            if data["category"] == category:
                child_color = color
                child_z = 0.0  # Lower Z level for child nodes
                parent_node = data["pose"]
                parent_node[2] = 2.5  # Parent nodes at a higher Z level
                add_child_nodes(fig, parent_node, data["children"], child_color, child_z)

# Customize axes labels
fig.update_layout(
    scene=dict(
        xaxis_title='X (World)',
        yaxis_title='Y (World)',
        zaxis_title='Z (World)',
        xaxis=dict(range=[min_x - 10, max_x + 10]),
        yaxis=dict(range=[min_y - 10, max_y + 10])
    )
)

fig.show()
