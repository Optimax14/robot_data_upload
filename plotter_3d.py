import plotly.graph_objects as go
import networkx as nx
import json
import numpy as np
from PIL import Image
import yaml
import cv2

# Color Palette 
# Color order MATTERS,
    # The order in which the categories are found in the graph.json will reflect
    # The colors that are assigned to each category
def get_color_palette():
    return [
        '#17becf',  # Light Blue
        '#ffbb78',  # Dark Orange
        '#c5b0d5',  # Light Purple
        '#e377c2',  # Darker shade of base chair color
        '#023020',  # Dark Green
        '#00008b',  # Dark Blue
        '#1f77b4',  # Blue
        '#2ca02c',  # Green
        '#FF3131',  # Red
        '#9467bd',  # Purple
        '#ff7f0e',  # Orange
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Olive
        '#17becf',  # Cyan
        '#ffbb78',  # Light Orange
        '#98df8a',  # Light Green
        '#ff9896',  # Light Red
        '#c5b0d5',  # Light Purple
        '#c49c94',  # Light Brown
        '#f7b6d2',  # Light Pink
        '#7f7f7f',  # Dark Gray
        '#e5cf0f',  # Dark Yellow
        '#00a2e8',  # Sky Blue
        '#e58931',  # Dark Orange
        '#a6d0b5'   # Light Teal
    ]

# Function to read graph JSON
# Replace with graph.json file
def read_graph_json(graph_json_path='graphs/graph3.json'):
    with open(graph_json_path, 'r') as file:
        return nx.node_link_graph(json.load(file))

# Function to calculate bounds for map
def calculate_bounds(coords):
    min_x, max_x = np.min(coords[:, 0]), np.max(coords[:, 0])
    min_y, max_y = np.min(coords[:, 1]), np.max(coords[:, 1])
    return min_x, max_x, min_y, max_y

# Function to get position for head nodes (spaced evenly)
def place_head_nodes(center_x, center_y, num_nodes, spacing):
    angles = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False)
    x_positions = center_x + spacing * np.cos(angles)
    y_positions = center_y + spacing * np.sin(angles)
    return x_positions, y_positions

# Function to add category nodes
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
            showlegend=False 
        ))

# Function to add a head node (included in the legend)
def add_head_node(fig, category, head_node, color):
    fig.add_trace(go.Scatter3d(
        x=[head_node[0]],
        y=[head_node[1]],
        z=[head_node[2]],
        mode='markers+text',
        marker=dict(size=10, color=color),
        text=[f"<b>{category.capitalize()}</b>"],
        textposition='top center',
        textfont=dict(size=30, family='Courier New', color='#000000'),
        name=f'{category.capitalize()}'
    ))

# Function to add connections (edges) between nodes
def add_connections(fig, head_node, detections, color, chair_head_node=None):
    for det in detections: 
        fig.add_trace(go.Scatter3d(
            x=[head_node[0], det[0]],
            y=[head_node[1], det[1]],
            z=[head_node[2], det[2]],
            mode='lines',
            line=dict(color=color, width=0.5),
            showlegend=False  
        ))
        

# Function to add child nodes 
# Only necessary if you have child nodes in graph
def add_child_nodes(fig, parent_node, children, color, child_z):
    for child in children:
        x_coords = child['pose'][0]
        y_coords = child['pose'][1]
        z_coords = child_z
        
        fig.add_trace(go.Scatter3d(
            x=[x_coords],
            y=[y_coords],
            z=[z_coords],
            mode='markers',
            marker=dict(size=5, color=color, symbol='diamond'),
            name=child['category'],
            showlegend=False  
        ))
        
        # Plot connection to parent node
        fig.add_trace(go.Scatter3d(
            x=[parent_node[0], x_coords],
            y=[parent_node[1], y_coords],
            z=[parent_node[2], z_coords],
            mode='lines',
            line=dict(color=color, width=0.5),
            showlegend=False 
        ))

# Funciton to get a connection between detections on level 2 and 3
def add_vertical_connections(fig, nodescord, category, color):
    for coord in nodescord[category]:
        fig.add_trace(go.Scatter3d(
            x=[coord[0], coord[0]],  
            y=[coord[1], coord[1]],  
            z=[2.5, 0.0],
            mode='lines',
            line=dict(color=color, width=0.5),
            showlegend=False   
        ))
            
                



with open('map.yaml', 'r') as file:
    map_metadata = yaml.safe_load(file)

resolution = map_metadata['resolution']
origin = map_metadata['origin']
image_path = "map.png"

map_image = Image.open(image_path).convert('L')
map_image = np.array(map_image)

image_height, image_width = map_image.shape

def pixels_to_world_coordinates(map_metadata, pixel_coords):
    pixel_x, pixel_y = pixel_coords
    world_x = pixel_x * map_metadata["resolution"] + map_metadata["origin"][0]
    world_y = (image_height - pixel_y) * map_metadata["resolution"] + map_metadata["origin"][1] + 1.7
    return [world_x, world_y, 0]


world_coords = []
nodescord = {}  
head_nodes = {}  

# Iterate through each pixel in the image
# Creates occupancy grid using the map_image
for y in range(image_height):
    for x in range(image_width):
        if map_image[y, x] != 0 and map_image[y, x] != 255:  # Plot only obstacles
            world_coord = pixels_to_world_coordinates(map_metadata, (x, y))
            world_coords.append(world_coord)

world_coords = np.array(world_coords)

# Get bounds for obstacles
min_x, max_x, min_y, max_y = calculate_bounds(world_coords)

# Calculate center coordinates of map
center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2

num_head_nodes = 0
spacing = 50  # Adjust as needed for spacing of head nodes

# Initialize graph and organize nodes by 
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

# Location of head nodes (Spaced out in a circle according to place_head_nodes function)
x_head, y_head = place_head_nodes(center_x, center_y, num_head_nodes, spacing)

for idx, category in enumerate(nodescord):
    head_nodes[category] = [x_head[idx], y_head[idx], 5]

for category in nodescord:
    nodescord[category] = np.array(nodescord[category])


fig = go.Figure()

# Add obstacle points (included in the legend)
fig.add_trace(go.Scatter3d(
    x=world_coords[:, 0],
    y=world_coords[:, 1],
    z=world_coords[:, 2],
    mode='markers',
    marker=dict(size=1, color='black'),
    name='Occupancy Map'  # Keep obstacles in the legend
))

colors = get_color_palette()

# Add category nodes, head nodes, and connections
for idx, category in enumerate(nodescord):
    color = colors[idx % len(colors)]
    add_head_node(fig, category, head_nodes[category], color)  # Adds head nodes 

    add_category_nodes(fig, category, color, 2.5, 'circle', nodescord) # Adds category detections on the 2nd level
    add_category_nodes(fig, category, color, 0.0, 'square', nodescord, 4) # Adds category detections on the 3rd level (occupancy map)
    
    add_connections(fig, head_nodes[category], nodescord[category], color)
    
    add_vertical_connections(fig, nodescord, category, color)  # Add vertical connections between z=2.5 and z=0.0 category detections (layer 2 and 3)

    # Add child nodes and connections
    # Uncomment following if you wish to plot child nodes 

    # for node, data in graph.nodes(data=True):
    #     if "children" in data and data["children"]:
    #         if data["category"] == category:
    #             child_color = color
    #             child_z = 0.0  # Lower Z level for child nodes
    #             parent_node = data["pose"]
    #             parent_node[2] = 2.5  # Parent nodes at a higher Z level
    #             add_child_nodes(fig, parent_node, data["children"], child_color, child_z)



# Customize axes labels
fig.update_layout(
    scene=dict(
        xaxis=dict(
            title='X (World)',  
            range=[min_x - 10, max_x + 10],
            visible=False,  
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title='Y (World)',  
            range=[min_y - 10, max_y + 10],
            visible=False,  
            showgrid=False,
            zeroline=False
        ),
        zaxis=dict(
            title='Z (World)',  
            visible=False,  
            showgrid=False,
            zeroline=False
        )
    )
)

fig.show()
