import datetime
import pygame
from Column import Column
from Task import Task

COLUMN_WIDTH = 200
COLUMN_HEADER_HEIGHT = 50
COLUMN_BODY_HEIGHT = 400
COLUMN_SPACES = 40
COLUMN_HEADER_FONT_SIZE = 24

TASK_WIDTH = 180
TASK_HEIGHT = 80
TASK_SPACES = 10
TASK_FONT_SIZE = 22
TASK_LEFT_PADDING = 10
TASK_TOP_PADDING = 10


class Kanban:
    def __init__(self):
        task = Task("Title", "description", "moi", "lui", datetime.datetime.now())
        self.default_columns = [
            Column("Open", [task], pygame.Color(166, 237, 166), pygame.Color(217, 255, 211)),
            Column("Develop", [], pygame.Color(237, 193, 166), pygame.Color(255, 233, 211)),
            Column("Close", [], pygame.Color(237, 166, 166), pygame.Color(255, 211, 211))
        ]
        self.screen = None
        self.column_left_start_pos = 20
        self.column_top_start_pos = 20
        self.tasks_rect: list[tuple[pygame.Rect, Task]] = []

    def render_columns(self):
        left_pos = self.column_left_start_pos
        top_pos = self.column_top_start_pos
        for column in self.default_columns:
            pygame.draw.rect(self.screen, column.header_color,
                             pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT))
            pygame.draw.rect(self.screen, column.body_color,
                             pygame.Rect(left_pos, top_pos + COLUMN_HEADER_HEIGHT, COLUMN_WIDTH, COLUMN_BODY_HEIGHT))
            font = pygame.font.SysFont(None, COLUMN_HEADER_FONT_SIZE)
            img = font.render(column.title, True, pygame.Color(39, 39, 39))
            self.screen.blit(img, (left_pos + 10, top_pos + 15))
            self.render_tasks(column.task_list, left_pos, top_pos + COLUMN_HEADER_HEIGHT)
            left_pos += COLUMN_WIDTH + COLUMN_SPACES

    def render_tasks(self, tasks, left_pos, top_pos):
        for task in tasks:
            task_rect_left_pos = left_pos + TASK_LEFT_PADDING
            task_rect_top_pos = top_pos + TASK_TOP_PADDING
            task_rect = pygame.Rect(task_rect_left_pos, task_rect_top_pos, TASK_WIDTH, TASK_HEIGHT)
            pygame.draw.rect(self.screen, pygame.Color(228, 228, 228), task_rect)
            self.tasks_rect.append((task_rect, task))

            # Text
            font = pygame.font.SysFont(None, TASK_FONT_SIZE)
            task_text = font.render(task.title, True, pygame.Color(39, 39, 39))
            task_text_width, task_text_height = task_text.get_size()
            task_text_rect = task_text.get_rect(
                topleft=(
                    task_rect_left_pos + (task_rect.size[0] / 2) - (task_text_width / 2),
                    (task_rect_top_pos + (task_rect.size[1] / 2) - (task_text_height / 2))
                )
            )
            self.screen.blit(task_text, task_text_rect)
            top_pos += TASK_HEIGHT + TASK_SPACES

    def start_ui(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for task_rect in self.tasks_rect:
                        if pygame.Rect.collidepoint(task_rect[0], pos):
                            print(task_rect[1])

            self.tasks_rect.clear()
            self.screen.fill(pygame.Color(241, 241, 241))
            self.render_columns()

            pygame.display.flip()
            clock.tick(60)
