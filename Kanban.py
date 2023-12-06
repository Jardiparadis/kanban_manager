import pygame

COLUMN_WIDTH = 200
COLUMN_HEADER_HEIGHT = 50
COLUMN_BODY_HEIGHT = 400
COLUMN_SPACES = 40


class Kanban:
    def __init__(self):
        self.default_columns = ["Open", "Develop", "Close"]
        self.screen = None
        self.column_left_start_pos = 20
        self.column_top_start_pos = 20
        pass

    def render_columns(self):
        left_pos = self.column_left_start_pos
        top_pos = self.column_top_start_pos
        for column in self.default_columns:
            pygame.draw.rect(self.screen, pygame.Color(224, 224, 224),
                             pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT))
            pygame.draw.rect(self.screen, pygame.Color(204, 204, 204),
                             pygame.Rect(left_pos, top_pos + COLUMN_HEADER_HEIGHT, COLUMN_WIDTH, COLUMN_BODY_HEIGHT))
            font = pygame.font.SysFont(None, 24)
            img = font.render(column, True, pygame.Color(39, 39, 39))
            self.screen.blit(img, (left_pos + 10, top_pos + 15))
            left_pos += COLUMN_WIDTH + COLUMN_SPACES

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

            pygame.display.flip()
            clock.tick(60)
