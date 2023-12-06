import datetime
import pygame
from Column import Column
from Task import Task
from tkinter import *
from tkinter import messagebox


COLUMN_WIDTH = 200
COLUMN_HEADER_HEIGHT = 50
COLUMN_BODY_HEIGHT = 400
COLUMN_SPACES = 40
COLUMN_HEADER_FONT_SIZE = 24
COLUMN_BOTTOM_PADDING = 20

TASK_WIDTH = 180
TASK_HEIGHT = 80
TASK_SPACES = 10
TASK_FONT_SIZE = 22
TASK_LEFT_PADDING = 10
TASK_TOP_PADDING = 10


class Kanban:
    def __init__(self):
        task = Task("Title task", "Description task", "moi", "lui", datetime.datetime.now())
        self.default_columns = [
            Column("Open", [task, task], pygame.Color(166, 237, 166), pygame.Color(217, 255, 211)),
            Column("Develop", [], pygame.Color(237, 193, 166), pygame.Color(255, 233, 211)),
            Column("Close", [], pygame.Color(237, 166, 166), pygame.Color(255, 211, 211))
        ]
        self.screen = None
        self.column_left_start_pos = 20
        self.column_top_start_pos = 20
        self.tasks_rect: list[tuple[pygame.Rect, Task]] = []

    def display_text_in_rectangle(self, rect_container: pygame.Rect, text, font_size):
        font = pygame.font.SysFont(None, font_size)
        rendered_text = font.render(text, True, pygame.Color(39, 39, 39))
        rendered_text_width, rendered_text_height = rendered_text.get_size()
        rendered_text_rect = rendered_text.get_rect(
            topleft=(
                rect_container.topleft[0] + (rect_container.size[0] / 2) - (rendered_text_width / 2),
                (rect_container.topleft[1] + (rect_container.size[1] / 2) - (rendered_text_height / 2))
            )
        )
        self.screen.blit(rendered_text, rendered_text_rect)

    def render_columns(self):
        left_pos = self.column_left_start_pos
        top_pos = self.column_top_start_pos
        for column in self.default_columns:
            column_header_rect = pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT)
            pygame.draw.rect(self.screen, column.header_color, column_header_rect)
            column_body_height = len(column.task_list) * (TASK_HEIGHT + TASK_TOP_PADDING) + COLUMN_BOTTOM_PADDING
            pygame.draw.rect(self.screen, column.body_color,
                             pygame.Rect(left_pos, top_pos + COLUMN_HEADER_HEIGHT, COLUMN_WIDTH, column_body_height))
            self.display_text_in_rectangle(column_header_rect, column.title, COLUMN_HEADER_FONT_SIZE)
            self.render_tasks(column.task_list, left_pos, top_pos + COLUMN_HEADER_HEIGHT)
            left_pos += COLUMN_WIDTH + COLUMN_SPACES

    def render_tasks(self, tasks, left_pos, top_pos):
        for task in tasks:
            task_rect_left_pos = left_pos + TASK_LEFT_PADDING
            task_rect_top_pos = top_pos + TASK_TOP_PADDING
            task_rect = pygame.Rect(task_rect_left_pos, task_rect_top_pos, TASK_WIDTH, TASK_HEIGHT)
            pygame.draw.rect(self.screen, pygame.Color(228, 228, 228), task_rect)
            self.tasks_rect.append((task_rect, task))
            self.display_text_in_rectangle(task_rect, task.title, TASK_FONT_SIZE)
            top_pos += TASK_HEIGHT + TASK_SPACES

    def show_task_in_popup(self, task_rect):
        Tk().wm_withdraw()  # hide main TK window, we only want popup
        popup_content = ("Description: " + task_rect[1].description +
                         "\nAssignee: " + task_rect[1].assignee +
                         "\nDate created: " + task_rect[1].creation_date.strftime("%d/%m/%Y") +
                         "\nDate due: " + task_rect[1].theoric_completion_date +
                         "\nCreator: " + task_rect[1].creator)
        messagebox.showinfo(task_rect[1].title, popup_content)

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
                            self.show_task_in_popup(task_rect)

            self.tasks_rect.clear()
            self.screen.fill(pygame.Color(241, 241, 241))
            self.render_columns()

            pygame.display.flip()
            clock.tick(60)
