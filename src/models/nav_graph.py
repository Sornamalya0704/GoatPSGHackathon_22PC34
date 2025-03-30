import json
import logging

class NavigationGraph:
    def __init__(self, graph_file):
        self.file_path = graph_file
        with open(graph_file, "r") as f:
            self.graph_data = json.load(f)
        self.vertices = self.graph_data.get("vertices", []) 
        self.lanes = self.graph_data.get("lanes", [])
        self.load_graph()  # Loading data from JSON
        logging.info("Navigation Graph initialized.")

    def load_graph(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

                #Extracting level1 from the JSON structure
                level_data = data.get("levels", {}).get("level1", {})
                
                #Assign extracted vertices and lanes
                self.vertices = level_data.get("vertices", [])
                self.lanes = level_data.get("lanes", [])

                if not self.vertices or not self.lanes:
                    logging.error("Error: Graph file does not contain valid vertices/lanes.")

        except FileNotFoundError:
            logging.error(f"Navigation graph file {self.file_path} not found.")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON file: {self.file_path}")

    def get_vertices(self):
        return self.vertices  #Returning the list of vertices.

    def get_lanes(self):
        return self.lanes  #Returns the list of lanes.

