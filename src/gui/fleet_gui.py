import tkinter as tk
from tkinter import messagebox, Menu
from models.nav_graph import NavigationGraph
from controllers.fleet_manager import FleetManager
from controllers.traffic_manager import TrafficManager

class FleetGUI:
    def __init__(self, root, graph_file):
        self.root = root
        self.root.title("Fleet Management System")
        self.center_window(800, 600)
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        self.graph = NavigationGraph(graph_file)
        self.fleet_manager = FleetManager(self.graph)
        self.traffic_manager = TrafficManager(self.graph)
        
        self.robots = {}  # Store robot visuals
        self.selected_robot = None
        self.task_menu = None
        self.load_graph()
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)  # Right-click to assign task
        self.update_gui()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_graph(self):
        if not self.graph.vertices:
            print("ERROR: No vertices found in graph!")
            messagebox.showerror("Error", "Graph data is empty. Check nav_graph.json.")
            return

        for vertex in self.graph.vertices:
            x, y = self.transform_coords(vertex[0], vertex[1])
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue", tags=f"vertex_{vertex[2]['name']}")
            self.canvas.create_text(x+10, y, text=vertex[2]['name'], anchor=tk.W)
        
        for lane in self.graph.lanes:
            x1, y1 = self.transform_coords(self.graph.vertices[lane[0]][0], self.graph.vertices[lane[0]][1])
            x2, y2 = self.transform_coords(self.graph.vertices[lane[1]][0], self.graph.vertices[lane[1]][1])
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

    def transform_coords(self, lat, lon):
        return int(400 + lat * 50), int(300 + lon * -50)
    
    def on_canvas_click(self, event):
        for vertex in self.graph.vertices:
            x, y = self.transform_coords(vertex[0], vertex[1])
            if abs(event.x - x) < 10 and abs(event.y - y) < 10:
                self.spawn_robot(vertex[2]['name'], x, y)
                return

        for robot_id, robot in self.robots.items():
            x1, y1, x2, y2 = self.canvas.coords(robot["oval"])
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_robot = robot_id
                print(f"Robot {robot_id} selected")
                return

    def on_right_click(self, event):
        if not self.selected_robot:
            return
        for vertex in self.graph.vertices:
            x, y = self.transform_coords(vertex[0], vertex[1])
            if abs(event.x - x) < 100 and abs(event.y - y) < 100:
                self.show_task_menu(event.x, event.y, self.selected_robot, vertex[2]['name'])
                return
    
    def show_task_menu(self, x, y, robot_id, destination):
        if self.task_menu:
            self.task_menu.destroy()
        
        self.task_menu = Menu(self.root, tearoff=0)
        self.task_menu.add_command(label="Move", command=lambda: self.assign_task(robot_id, destination))
        self.task_menu.add_command(label="Wait")
        self.task_menu.add_command(label="Charge")
        self.task_menu.add_command(label="Complete task")
        self.task_menu.post(x, y)

    def spawn_robot(self, location, x, y):
        if any(robot["position"] == location for robot in self.robots.values()):
            messagebox.showinfo("Sorry","A Robot is already there ..")
            return
        
        robot_id = len(self.robots) + 1
        color = self.get_robot_color("idle")
        self.fleet_manager.add_robot(robot_id, location)
        
        self.robots[robot_id] = {
            "oval": self.canvas.create_oval(x-8, y-8, x+8, y+8, fill=color, tags=f"robot_{robot_id}"),
            "status": "idle",
            "position": location,
            "text": self.canvas.create_text(x, y-12, text=str(robot_id), fill="black")
        }
        print(f"Spawned Robot {robot_id} at ({x}, {y})")

    def assign_task(self, robot_id, destination):
        success, path = self.fleet_manager.assign_task(robot_id, destination)
        if success:
            print(f"Robot {robot_id} assigned path: {path}")
            self.robots[robot_id]["path"] = path  # Store path in robot dict
            self.move_robot(robot_id)  # Start moving robot
        else:
            messagebox.showerror("Error", "Path assignment failed.")
    
    def move_robot(self, robot_id):
        if robot_id not in self.robots:
            return

        robot = self.robots[robot_id]
    
        if "path" not in robot or not robot["path"]:
            print(f"Robot {robot_id} reached destination.")
            robot["status"] = "task complete"
            return

        # Get the next position in the path
        next_position = robot["path"].pop(0)
        x, y = self.transform_coords(next_position[0], next_position[1])

        # Move the robot
        self.canvas.coords(robot["oval"], x-8, y-8, x+8, y+8)
        self.canvas.coords(robot["text"], x, y-12)
        robot["position"] = next_position
        robot["status"] = "moving"

        # Continue moving until path is empty
        self.root.after(500, lambda: self.move_robot(robot_id))


    def update_gui(self):
        for robot_id, robot in self.robots.items():
            fleet_robot = self.fleet_manager.robots.get(robot_id)
            if not fleet_robot:
                continue

            if fleet_robot.has_reached_destination():
                robot["status"] = "task complete"
                print(f"Robot {robot_id} reached destination.")

            next_position = fleet_robot.get_next_move()
            if next_position:
                x, y = self.transform_coords(next_position[0], next_position[1])
                self.canvas.coords(robot["oval"], x-8, y-8, x+8, y+8)
                self.canvas.coords(robot["text"], x, y-12)
                robot["status"] = "moving"
                robot["position"] = next_position
                print(f"Robot {robot_id} moved to {next_position}")

            color = self.get_robot_color(robot["status"])
            self.canvas.itemconfig(robot["oval"], fill=color)

        self.root.after(100, self.update_gui)

    def get_robot_color(self, status):
        status_colors = {
            "idle": "pink",
            "moving": "green",
            "waiting": "orange",
            "charging": "blue",
            "task complete": "gray"
        }
        return status_colors.get(status, "black")

if __name__ == "__main__":
    root = tk.Tk()
    app = FleetGUI(root, "nav_graph_1.json")
    root.mainloop()
