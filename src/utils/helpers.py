import math

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def find_nearest_vertex(position, vertices):
    min_distance = float('inf')
    nearest_vertex = None
    for i, vertex in enumerate(vertices):
        distance = calculate_distance(position, vertex)
        if distance < min_distance:
            min_distance = distance
            nearest_vertex = i
    return nearest_vertex

def log_event(message):
    with open("fleet_logs.txt", "a") as log_file:
        log_file.write(message + "\n")
