import pygame
from Column import Column
from Task import Task
from datetime import datetime

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

        default_task = Task("Title", "desc", "creator", "assignee", datetime.now)
        default_task2 = Task("Title2", "desc2", "creator2", "assignee2", datetime.now)
        
        self.default_columns = [
            #Column("Open", ["Create column", "Create task"], pygame.Color(166, 237, 166), pygame.Color(217, 255, 211)),
            #Column("Develop", ["aa"], pygame.Color(237, 193, 166), pygame.Color(255, 233, 211)),
            #Column("Close", ["c'est ok", "oui"], pygame.Color(237, 166, 166), pygame.Color(255, 211, 211))
            Column("Open", [default_task, default_task], pygame.Color(166, 237, 166), pygame.Color(217, 255, 211)),
            Column("Develop", [default_task], pygame.Color(237, 193, 166), pygame.Color(255, 233, 211)),
            Column("Close", [default_task, default_task2], pygame.Color(237, 166, 166), pygame.Color(255, 211, 211))
        ]
        self.screen = None
        self.column_left_start_pos = 20
        self.column_top_start_pos = 20
        self.tasks = [] # list of ALL tasks
        self.index_moving_task = None

    def list_all_tasks(self):
        for column in self.default_columns:
            for task in column.task_list:
                self.tasks.append(task)
        return self.tasks

    def render_columns(self):
        left_pos = self.column_left_start_pos
        top_pos = self.column_top_start_pos
        for column in self.default_columns:
            pygame.draw.rect(self.screen, column.header_color,
                             pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT))
            #pygame.draw.rect(self.screen, "red",
            #                 pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT))
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
            if task.moving == False:
                task.rect = task_rect

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

    # Drag & Drop
    def handleMouseEvent(self, event):
        # clic gauche
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.list_all_tasks() # fill self.tasks with all task
                for num, task in enumerate(self.tasks):
                    if task.rect.collidepoint(event.pos):
                        self.index_moving_task = num
                        task.moving = True   

        # relachement du clic
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.tasks[self.index_moving_task].moving = False
                self.index_moving_task = None

                #if col.collidepoint(event.pos):
                    #print("collide")
    
        # souris bouge
        if event.type == pygame.MOUSEMOTION:
            if self.index_moving_task != None:
                self.tasks[self.index_moving_task].rect.move_ip(event.rel)
                self.print_moving_task()

    def print_moving_task(self):
        if self.index_moving_task != None:
            pygame.draw.rect(self.screen, pygame.Color(228, 228, 228), self.tasks[self.index_moving_task].rect)

    def start_ui(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        
        while True:
        

            for event in pygame.event.get():
                self.handleMouseEvent(event)

                if event.type == pygame.QUIT:
                    return pygame.quit()
            self.screen.fill(pygame.Color(241, 241, 241))

            self.render_columns()
            self.print_moving_task()
            pygame.display.flip()
            clock.tick(60)
