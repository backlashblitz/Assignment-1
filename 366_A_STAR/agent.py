# agent.py
import pygame
import heapq

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  
        self.moving = False  
        self.total_path_cost = 0  

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
        shortest_path = None
        for task_position in self.environment.task_locations.keys():
            path = self.a_star_search(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        if shortest_path:
            self.path = shortest_path[1:]  
            self.moving = True

    def a_star_search(self, target):
       
        start = tuple(self.position)
        goal = target
        open_list = []
        heapq.heappush(open_list, (0, start))  
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)
            
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(*current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
        return None  

    def reconstruct_path(self, came_from, current):
        
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def manhattan_distance(self, pos1, pos2):
       
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, x, y):
       
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
