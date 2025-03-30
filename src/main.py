import tkinter as tk
from gui.fleet_gui import FleetGUI
from controllers.fleet_manager import FleetManager
from models.nav_graph import NavigationGraph
import logging
import os

# Initialize logging activity
os.makedirs("./src/logs", exist_ok=True)  
logging.basicConfig(filename='./src/logs/fleet_logs.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting Fleet Management System...")
    
    graph_file = os.path.abspath("./data/nav_graph_1.json")  

    try:
        # Loading the navigation graph
        graph = NavigationGraph(graph_file)

        if not graph.vertices or not graph.lanes:
            logging.error("Navigation graph loaded but contains no data.")
            print("Error: Navigation graph contains no data.")
            return

        FleetManager(graph)
        
        # Initialize of Tkinter GUI
        root = tk.Tk()
        root.geometry("900x700")  
        root.title("Fleet Management System")
        print(graph.get_vertices())
        print(graph.get_lanes())
        app = FleetGUI(root, graph_file)
    
        
        logging.info("Fleet Management System started successfully.")
        
        # Run the application
        root.mainloop()
    
    except FileNotFoundError:
        logging.error(f"Error: Navigation graph file {graph_file} not found.")
        print(f"Error: Navigation graph file {graph_file} not found.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
