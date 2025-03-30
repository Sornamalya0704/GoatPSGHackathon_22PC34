import logging
from models.robot import Robot
from controllers.traffic_manager import TrafficManager

class FleetManager:
    def __init__(self, graph):
        self.graph = graph
        self.robots = {}
        self.traffic_manager = TrafficManager(self.graph)
        logging.info("Fleet Manager initialized.")

    def add_robot(self, robot_id, start_position):
        if robot_id in self.robots:
            logging.warning(f"Robot {robot_id} already exists!")
            return False
        
        self.robots[robot_id] = Robot(robot_id, start_position)
        logging.info(f"Robot {robot_id} added at position {start_position}.")
        return True

    def assign_task(self, robot_id, destination):
        if robot_id not in self.robots:
            logging.error(f"Robot {robot_id} not found.")
            return False
        
        robot = self.robots[robot_id]
        path = self.graph.find_shortest_path(robot.position, destination)

        if not path:
            logging.error(f"No path found for Robot {robot_id} from {robot.position} to {destination}.")
            return False
        
        if self.traffic_manager.is_path_occupied(path):
            logging.warning(f"Path {path} is occupied. Robot {robot_id} will retry.")
            return False
        
        robot.set_path(path)
        logging.info(f"Robot {robot_id} assigned task to {destination} via {path}.")
        return True

    def update_fleet(self):
        for robot_id, robot in self.robots.items():
            if robot.has_reached_destination():
                logging.info(f"Robot {robot_id} reached its destination.")
                continue
            
            next_position = robot.get_next_move()
            if next_position and self.traffic_manager.can_move(robot.position, next_position):
                self.traffic_manager.update_traffic(robot.position, next_position)
                robot.move()
                logging.info(f"Robot {robot_id} moved to {robot.position}.")
            else:
                logging.warning(f"Robot {robot_id} waiting due to traffic.")
