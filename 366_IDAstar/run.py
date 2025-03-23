import pygame
import sys
from agent import Agent
from environment import Environment


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 200
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)
TASK_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
MOVEMENT_DELAY = 200  

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("IDA* Pathfinding Simulation")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent = Agent(environment, GRID_SIZE)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)

    button_rect = pygame.Rect(WINDOW_WIDTH + 50, WINDOW_HEIGHT // 2, 100, 50)
    simulation_started = False

    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not simulation_started and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    simulation_started = True
                    if environment.task_locations:
                        agent.find_nearest_task()

        screen.fill(BACKGROUND_COLOR)

        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        for (bx, by) in environment.barrier_locations:
            pygame.draw.rect(screen, BARRIER_COLOR, (bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            task_text = font.render(str(task_number), True, (255, 255, 255))
            screen.blit(task_text, task_rect.move(10, 10))

        all_sprites.draw(screen)

        status_x = WINDOW_WIDTH + 10
        screen.blit(font.render("Algorithm: IDA*", True, TEXT_COLOR), (status_x, 10))
        screen.blit(font.render(f"Tasks Completed: {agent.task_completed}", True, TEXT_COLOR), (status_x, 40))
        screen.blit(font.render(f"Position: {agent.position}", True, TEXT_COLOR), (status_x, 70))
        screen.blit(font.render(f"Completed Tasks: {agent.completed_tasks}", True, TEXT_COLOR), (status_x, 100))
        screen.blit(font.render(f"Total Path Cost: {agent.total_path_cost}", True, TEXT_COLOR), (status_x, 130))

       

        if not simulation_started:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
            screen.blit(font.render("Start", True, BUTTON_TEXT_COLOR), button_rect.move(35, 15))
        else:
            if pygame.time.get_ticks() - last_move_time > MOVEMENT_DELAY:
                if not agent.moving and environment.task_locations:
                    agent.find_nearest_task()
                elif agent.moving:
                    agent.move()
                last_move_time = pygame.time.get_ticks()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

