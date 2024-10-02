# Hierarchical 3D Graph Representation for Semantic Mapping

This project visualizes a hierarchical semantic map using a graph representation. Using Plotly it visualizes a given graph and map into a 3D representation.

## Dependencies

This project requires the following Python libraries:

- **Plotly**: For interactive 3D plotting and visualizations.
- **NetworkX**: For handling graph data structures.
- **NumPy**: For numerical operations on arrays.
- **Pillow (PIL)**: For image processing and loading occupancy maps.
- **PyYAML**: For parsing metadata from YAML files.

You can install the required dependencies using pip:

```bash
pip install plotly==5.23.0 networkx==3.3 numpy==1.26.4 pillow==10.0.0 pyyaml==6.0.2
```
Make sure you have Python verion 3.12 or higher.


## Usage

### Ensure you have the following input files:

1. **graph.json**: The graph file containing detection data (Object Pose,Robot Pose, Category, ID)
2. **map.yaml**: Metadata file for the map, including:
   - `resolution`: The resolution of the map in meters per pixel.
   - `origin`: The coordinates of the origin point on the map.
3. **map.png**: A grayscale image representing the occupancy map.

Make sure the `graph.json`, `map.yaml`, and `map.png` files are in the project directory or provide the appropriate paths in the script.

### Running the script

To generate the 3D visualization, follow these steps:

1. Ensure you have installed all necessary dependencies as described in the Dependencies section.

2. Modify the code to read from the correct names of the input files. 
   
3. Run the Python script to visualize the hierarchical semantic map:

   ```bash
   python plotter_3d.py
   ```

