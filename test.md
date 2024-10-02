Hierarchical Semantic Mapping with Graphs and Occupancy Maps
This project visualizes a hierarchical semantic map using a graph representation. The graph data is provided in a JSON format, and an occupancy map is represented using a grayscale image. The visualization is generated using Plotly in a 3D space, displaying both the semantic information from the graph and the occupancy map from the image.

Table of Contents
Dependencies
Installation
Usage
Description
License
Dependencies
This project requires the following Python libraries:

Plotly: For interactive 3D plotting and visualizations.
NetworkX: For handling graph data structures.
Numpy: For numerical operations on arrays.
Pillow (PIL): For image processing and loading occupancy maps.
PyYAML: For parsing metadata from YAML files.
You can install the required dependencies using pip:

bash
Copy code
pip install plotly networkx numpy pillow pyyaml
Detailed Dependency Breakdown:
Plotly: This is used to create 3D scatter plots for graph nodes, edges, and occupancy map points.
NetworkX: This handles the graph structures, which are provided in a JSON format. It allows the graph to be loaded and manipulated efficiently.
Numpy: Used for efficient array manipulations, especially in calculating coordinates and distances.
Pillow (PIL): Required to load the occupancy map image in grayscale format.
PyYAML: This library is used to load metadata from the YAML file associated with the map.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/hierarchical-semantic-mapping.git
Navigate to the project directory:

bash
Copy code
cd hierarchical-semantic-mapping
Install the required Python dependencies:

bash
Copy code
pip install -r requirements.txt
Alternatively, install dependencies individually as mentioned above.

Usage
Ensure you have the following input files:

graph.json: The graph file containing nodes and edges with category and position information.
map.yaml: Metadata file for the map, including resolution and origin.
map.png: Grayscale image representing the occupancy map.
Run the script to generate the 3D visualization:

bash
Copy code
python your_script.py
The output will be an interactive 3D plot visualizing the graph and map data.

Example Input Files:
graph.json: Contains graph nodes and their connections.
map.png: A PNG image representing the occupancy map (grayscale).
map.yaml: Metadata file containing map resolution and origin details.
Description
This project creates a 3D visualization that shows:

Nodes: Each node represents an entity (such as a category or object), plotted in a 3D space.
Edges: Connections between nodes representing relationships between them.
Occupancy Map: The background map, represented as a 2D occupancy grid, is displayed alongside the graph nodes to show the real-world environment context.
Key Functions:
read_graph_json: Loads the graph structure from a JSON file.
calculate_bounds: Calculates the bounds for positioning elements on the map.
place_head_nodes: Positions the category nodes in a circular manner.
add_category_nodes, add_head_node, add_connections: These functions build the plot, adding nodes, head nodes, and connections between them.
pixels_to_world_coordinates: Converts pixel coordinates from the image to world coordinates based on the map metadata.
License
This project is licensed under the MIT License - see the LICENSE file for details.
