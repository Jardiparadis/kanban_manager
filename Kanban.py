import pygame
from datetime import datetime
from Column import Column
from Task import *
from tkinter import *
from tkinter import messagebox
from enum import Enum

COLUMN_WIDTH = 200
COLUMN_HEADER_HEIGHT = 50
COLUMN_BODY_HEIGHT = 400
COLUMN_SPACES = 40
COLUMN_HEADER_FONT_SIZE = 24
COLUMN_BOTTOM_PADDING = 40

TASK_WIDTH = 180
TASK_HEIGHT = 80
TASK_SPACES = 10
TASK_FONT_SIZE = 22
TASK_LEFT_PADDING = 10
TASK_TOP_PADDING = 10
TASK_BACKGROUND_COLOR = pygame.Color(228, 228, 228)
TASK_LATE_BACKGROUND_COLOR = pygame.Color(241, 160, 160)

class Priority(Enum):
    Low = 1
    Medium = 2
    High = 3

class Status(Enum):
    Open = 1
    Develop = 2
    Waiting = 3
    Closed = 4


class Kanban:

    def __init__(self):
        default_task = Task("Title", "desc", "creator", "assignee", datetime.now(), theoric_completion_date=datetime(year=2010, day=20, month=2))
        default_task2 = Task("Title2", "desc2", "creator2", "assignee2", datetime.now())
        default_task3 = Task("Title3", "desc3", "creator3", "assignee3", datetime.now())
        default_task4 = Task("Title4", "desc4", "creator4", "assignee4", datetime.now())
        
        self.default_columns = [
            Column("Open", [default_task], pygame.Color(166, 237, 166), pygame.Color(217, 255, 211)),
            Column("Develop", [default_task2], pygame.Color(237, 193, 166), pygame.Color(255, 233, 211)),
            Column("Close", [default_task3, default_task4], pygame.Color(237, 166, 166), pygame.Color(255, 211, 211))
        ]
     
        self.screen = None
        self.column_left_start_pos = 20
        self.column_top_start_pos = 20
        self.tasks_rect: list[tuple[pygame.Rect, Task]] = []
        self.tasks = [] # list of ALL tasks
        self.moving_task_index = None
        self.old_column_index = None
        self.popup = None


    def save_changes(self, title, description, creator, assignee,
                 theoric_completion_date, completion_date, label):
        new_task = Task(
        title=title,
        description=description,
        creator=creator,
        assignee=assignee,
        creation_date=datetime.now(),
        theoric_completion_date=theoric_completion_date,
        completion_date=completion_date,
        label=label
    )

        # Choose the column to add the new task (e.g., Open column)
        self.default_columns[0].task_list.append(new_task)

        # Close the popup after saving changes
        self.popup.destroy()

    def show_popup(self):
        self.popup = Tk()
        self.popup.title("Modifier les valeurs")

        # Ajoutez des widgets pour chaque paramètre de la classe Task
        Label(self.popup, text="Titre").grid(row=0, column=0)
        title_entry = Entry(self.popup)
        title_entry.grid(row=0, column=1)

        Label(self.popup, text="Description").grid(row=1, column=0)
        description_entry = Entry(self.popup)
        description_entry.grid(row=1, column=1)

        Label(self.popup, text="Creator").grid(row=2, column=0)
        creator_entry = Entry(self.popup)
        creator_entry.grid(row=2, column=1)

        Label(self.popup, text="Assignee").grid(row=3, column=0)
        assignee_entry = Entry(self.popup)
        assignee_entry.grid(row=3, column=1)

        Label(self.popup, text="Completion date").grid(row=5, column=0)
        completion_date_entry = Entry(self.popup)
        completion_date_entry.grid(row=5, column=1)

        Label(self.popup, text="Label").grid(row=6, column=0)
        label_entry = Entry(self.popup)
        label_entry.grid(row=6, column=1)

        def save_changes():
        # Récupérez les valeurs saisies et appelez la méthode save_changes de Kanban
            new_title = title_entry.get()
            new_description = description_entry.get()
            new_creator = creator_entry.get()
            new_assignee = assignee_entry.get()
            new_theoric_completion_date = datetime.now()
            new_completion_date = completion_date_entry.get()
            new_label = label_entry.get()

            self.save_changes(new_title, new_description, new_creator, new_assignee,
                        new_theoric_completion_date, new_completion_date, new_label)

        save_button = Button(self.popup, text="Enregistrer", command=save_changes)
        save_button.grid(row=10, column=0, columnspan=2)

        self.popup.mainloop()

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
 
    def list_all_tasks(self):
        for column in self.default_columns:
            for task in column.task_list:
                self.tasks.append(task)
        return self.tasks

    def render_columns(self):
        left_pos = self.column_left_start_pos
        top_pos = self.column_top_start_pos
        for column in self.default_columns:
            column_header_rect = pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT)
            pygame.draw.rect(self.screen, column.header_color, column_header_rect)
            column_body_height = len(column.task_list) * (TASK_HEIGHT + TASK_TOP_PADDING) + COLUMN_BOTTOM_PADDING
            col_rect = pygame.draw.rect(self.screen, column.body_color,
                             pygame.Rect(left_pos, top_pos + COLUMN_HEADER_HEIGHT, COLUMN_WIDTH, column_body_height))
            column.rect = col_rect
            self.display_text_in_rectangle(column_header_rect, column.title, COLUMN_HEADER_FONT_SIZE)
            self.render_tasks(column.task_list, left_pos, top_pos + COLUMN_HEADER_HEIGHT)
            left_pos += COLUMN_WIDTH + COLUMN_SPACES

    def render_tasks(self, tasks, left_pos, top_pos):
        for task in tasks:
            background_color = self.get_task_color(task)
            task_rect_left_pos = left_pos + TASK_LEFT_PADDING
            task_rect_top_pos = top_pos + TASK_TOP_PADDING
            task_rect = pygame.Rect(task_rect_left_pos, task_rect_top_pos, TASK_WIDTH, TASK_HEIGHT)
            pygame.draw.rect(self.screen, background_color, task_rect)
            self.tasks_rect.append((task_rect, task))
            self.display_text_in_rectangle(task_rect, task.title, TASK_FONT_SIZE)
            top_pos += TASK_HEIGHT + TASK_SPACES
            if task.moving is False:
                task.rect = task_rect

    def show_task_in_popup(self, task_rect):
        Tk().wm_withdraw()  # hide main TK window, we only want popup
        popup_content = ("Description: " + task_rect[1].description +
                         "\nAssignee: " + task_rect[1].assignee +
                         "\nDate created: " + task_rect[1].creation_date.strftime("%d/%m/%Y") +
                         "\nDate due: " + task_rect[1].theoric_completion_date +
                         "\nCreator: " + task_rect[1].creator)
        messagebox.showinfo(task_rect[1].title, popup_content)

    # Drag & Drop
    def handle_mouse_event(self, event):
        # clic gauche
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.take_drag_and_drop(event) 
        # relachement du clic
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.release_drag_and_drop(event)
            if event.button == 3:
                pos = pygame.mouse.get_pos()
                for task_rect in self.tasks_rect:
                    if pygame.Rect.collidepoint(task_rect[0], pos):
                        self.show_task_in_popup(task_rect)
        # mouvement du curseur
        if event.type == pygame.MOUSEMOTION:
            self.hold_drag_and_drop(event)

    def take_drag_and_drop(self, event):
        self.list_all_tasks() # fill self.tasks with all task
        for num, task in enumerate(self.tasks):
            if task.rect.collidepoint(event.pos):
                self.moving_task_index = num
                task.moving = True  

    def hold_drag_and_drop(self, event):
        if self.moving_task_index is not None:
            self.tasks[self.moving_task_index].rect.move_ip(event.rel)
            self.print_moving_task()

    def release_drag_and_drop(self,event):
        if self.moving_task_index:
            for column in self.default_columns:
                if column.rect.collidepoint(event.pos):
                    # On supprime notre tache de l'ancienne colonne
                    old_column_index =  self.get_column_index(self.tasks[self.moving_task_index])
                    self.default_columns[old_column_index].task_list.remove(self.tasks[self.moving_task_index])
                    # Et on la rajoute a la nouvelle
                    column.task_list.append(self.tasks[self.moving_task_index])
            self.tasks[self.moving_task_index].moving = False
            self.moving_task_index = None

    """
    Get the column index of a task
    """
    def get_column_index(self, task):
        for index, col in enumerate(self.default_columns):
            if task in col.task_list:
                return index
        return index

    def get_task_color(self, task):
        background_color = pygame.Color(228, 228, 228)
        if task.theoric_completion_date is not None \
                and (datetime.timestamp(task.theoric_completion_date) - datetime.timestamp(datetime.now()) < 0):
            background_color = pygame.Color(241, 160, 160)
        return background_color

    def print_moving_task(self):
        if self.moving_task_index is not None:
            current_task = self.tasks[self.moving_task_index]
            background_color = self.get_task_color(current_task)
            pygame.draw.rect(self.screen, background_color, current_task.rect)
            self.display_text_in_rectangle(self.tasks[self.moving_task_index].rect, current_task.title, TASK_FONT_SIZE)

    def start_ui(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                self.handle_mouse_event(event)
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
            self.print_moving_task()

            # Ajoutez un bouton
            button_rect = pygame.Rect(30, 10, 150, 30)
            pygame.draw.rect(self.screen, pygame.Color(0, 128, 255), button_rect)
            font = pygame.font.SysFont(None, 24)
            button_text = font.render("Modifier Valeurs", True, pygame.Color(255, 255, 255))
            self.screen.blit(button_text, (40, 10))

            # Vérifiez si le bouton est cliqué
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:  # 0 correspond au clic gauche
                    self.show_popup()

            pygame.display.flip()
            clock.tick(60)