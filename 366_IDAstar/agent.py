import pygame
from collections import deque
import math

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting position
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  # Path for movement
        self.moving = False
        self.explored_nodes = []  # For visualization
        self.total_path_cost = 0  # Total movement cost


    def move(self):
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.total_path_cost += 1
            self.check_task_completion()
        else:
            self.moving = False

    def check_task_completion(self):
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def find_nearest_task(self):
        nearest_task = None
        best_path = None
        for task_position in self.environment.task_locations.keys():
            path = self.ida_star(task_position)
            if path:
                if not best_path or len(path) < len(best_path):
                    best_path = path
                    nearest_task = task_position
        if best_path:
            self.path = best_path[1:]
            self.moving = True

    def ida_star(self, goal):
        start = tuple(self.position)
        threshold = self.heuristic(start, goal)

        while True:
            self.explored_nodes.clear()
            temp_path = []
            result = self.search(start, goal, 0, threshold, temp_path)
            if isinstance(result, list):
                return result  # Found solution path
            if result == float("inf"):
                return None  # No solution
            threshold = result  # Increase threshold

    def search(self, node, goal, g, threshold, path):
        f = g + self.heuristic(node, goal)
        if f > threshold:
            return f
        if node == goal:
            return path + [node]

        self.explored_nodes.append(node)
        min_cost = float("inf")
        for neighbor in self.get_neighbors(*node):
            if neighbor not in path:
                path.append(neighbor)
                result = self.search(neighbor, goal, g + 1, threshold, path)
                if isinstance(result, list):
                    return result  # Solution found
                if result < min_cost:
                    min_cost = result
                path.pop()
        return min_cost

    def heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])  # Manhattan distance

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors