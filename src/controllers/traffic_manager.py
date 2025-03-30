import logging

class TrafficManager:
    def __init__(self, graph):
        self.graph = graph
        self.occupied_lanes = set()
        self.robot_positions = {}  # {robot_id: (current_vertex, next_vertex)}
        logging.info(" Traffic Manager initialized.")

    def request_lane(self, robot_id, start, end):
        #Handles lane requests, ensuring no collision occurs.
        if (start, end) in self.occupied_lanes or (end, start) in self.occupied_lanes:
            logging.warning(f"Robot {robot_id} waiting: lane {start} -> {end} occupied.")
            return False  # Lane occupied
        
        self.occupied_lanes.add((start, end))
        self.robot_positions[robot_id] = (start, end)
        logging.info(f"Robot {robot_id} moving on lane {start} -> {end}.")
        return True

    def release_lane(self, robot_id):
        #Releases lane once robot moves forward.
        if robot_id in self.robot_positions:
            lane = self.robot_positions.pop(robot_id)
            self.occupied_lanes.discard(lane)
            logging.info(f"Robot {robot_id} released lane {lane}.")

    def is_path_occupied(self, path):
        #Check if any part of the path is occupied.
        return any((path[i], path[i+1]) in self.occupied_lanes for i in range(len(path) - 1))

    def can_move(self, start, end):
        #Check if the lane is free for movement.
        return not self.is_lane_occupied(start, end)

    def update_traffic(self, start, end):
        #Update traffic to show movement.
        self.occupied_lanes.discard((start, end))
        self.occupied_lanes.add((end, start))
