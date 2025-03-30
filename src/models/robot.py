import logging
from utils import helpers 

class Robot:
    def __init__(self, robot_id, start_vertex):
        self.robot_id = robot_id
        self.current_position = start_vertex
        self.destination = None
        self.path = []
        self.status = "idle"
        logging.info(f"Robot {self.robot_id} initialized at vertex {self.current_position}")

    def assign_task(self, destination, path):
        self.destination = destination
        self.path = path
        self.status = "moving"
        logging.info(f"Robot {self.robot_id} assigned task to {self.destination} via {self.path}")
    
    def update_position(self):
        if self.path:
            self.current_position = self.path.pop(0)
            logging.info(f"Robot {self.robot_id} moved to {self.current_position}")
            if not self.path:
                self.status = "idle"
                logging.info(f"Robot {self.robot_id} reached destination {self.destination}")

    def get_status(self):
        return {
            "id": self.robot_id,
            "position": self.current_position,
            "destination": self.destination,
            "status": self.status
        }
