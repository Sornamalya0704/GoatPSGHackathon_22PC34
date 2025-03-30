import math

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def find_nearest_node(point, graph):
    """Finds the nearest node in the graph to a given (x, y) coordinate."""
    min_distance = float('inf')
    nearest_node = None

    for node in graph.vertices:
        dist = calculate_distance((node[0], node[1]), point)
        if dist < min_distance:
            min_distance = dist
            nearest_node = node[2]['name']

    return nearest_node
