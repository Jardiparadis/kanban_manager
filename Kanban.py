import pygame
from Column import Column
from enum import Enum
from tkinter import *
from Task import *
import datetime

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
        self.default_columns = [
            Column("Open", ["Create column", "Create task"], pygame.Color(166, 237, 166), pygame.Color(217, 255, 211)),
            Column("Develop", ["aa"], pygame.Color(237, 193, 166), pygame.Color(255, 233, 211)),
            Column("Close", ["c'est ok", "oui"], pygame.Color(237, 166, 166), pygame.Color(255, 211, 211))
        ]
        self.screen = None
        self.column_left_start_pos = 40
        self.column_top_start_pos = 40
    
    task_instance = Task(title="Exemple", description="Description de l'exemple",
                     creator="Créateur initial", assignee="Assigné initial",
                     creation_date="Date de création initiale")
    
    def show_popup(self):
        popup = Tk()
        popup.title("Modifier les valeurs")

        # Ajoutez des widgets pour chaque paramètre de la classe Task
        Label(popup, text="Titre").grid(row=0, column=0)
        title_entry = Entry(popup)
        title_entry.grid(row=0, column=1)

        Label(popup, text="Description").grid(row=1, column=0)
        description_entry = Entry(popup)
        description_entry.grid(row=1, column=1)

        Label(popup, text="Creator").grid(row=2, column=0)
        creator_entry = Entry(popup)
        creator_entry.grid(row=2, column=1)

        Label(popup, text="Assignee").grid(row=3, column=0)
        assignee_entry = Entry(popup)
        assignee_entry.grid(row=3, column=1)

        Label(popup, text="Theoric Completion Date").grid(row=5, column=0)
        theoric_completion_date_entry = Entry(popup)
        theoric_completion_date_entry.grid(row=5, column=1)

        Label(popup, text="Completion date").grid(row=6, column=0)
        completion_date_entry = Entry(popup)
        completion_date_entry.grid(row=6, column=1)

        Label(popup, text="Label").grid(row=7, column=0)
        label_entry = Entry(popup)
        label_entry.grid(row=7, column=1)

        Label(popup, text="Priority").grid(row=8, column=0)
        priority_entry = Entry(popup)
        priority_entry.grid(row=8, column=1)

        Label(popup, text="Status").grid(row=9, column=0)
        status_entry = Entry(popup)
        status_entry.grid(row=9, column=1)

        def save_changes():
            # Récupérez les valeurs saisies et mettez à jour votre instance de Task
            new_title = title_entry.get()
            new_description = description_entry.get()
            new_creator = creator_entry.get()
            new_assignee = assignee_entry.get()
            new_creation_date = datetime.datetime.now()
            new_theoric_completion_date = theoric_completion_date_entry.get()
            new_completion_date = completion_date_entry.get()
            new_label = label_entry.get()
            new_priority = priority_entry.get()
            new_status = status_entry.get()
            
            #Mettre à jour l'instance de Task avec les nouvelles valeurs
            self.task_instance.update_task(new_title, new_description, new_creator, new_assignee,
                                new_creation_date, new_theoric_completion_date,
                                 new_completion_date, new_label, new_priority, new_status)
            
            print(self.task_instance.title)
            print(self.task_instance.description)

            popup.destroy()  # Fermez le popup après avoir enregistré les modifications

            # Ajoutez un bouton pour enregistrer les modifications
        save_button = Button(popup, text="Enregistrer", command=save_changes)
        save_button.grid(row=10, column=0, columnspan=2)

        popup.mainloop()

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

            # Text
            font = pygame.font.SysFont(None, TASK_FONT_SIZE)
            task_text = font.render(task, True, pygame.Color(39, 39, 39))
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
                
            self.screen.fill(pygame.Color(241, 241, 241))
            self.render_columns()

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
