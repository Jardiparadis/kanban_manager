import pygame

COLUMN_WIDTH = 200
COLUMN_HEADER_HEIGHT = 50
COLUMN_BODY_HEIGHT = 400
COLUMN_SPACES = 40


def render_columns(screen):
    columns_list = ["oui", "non", "peut-être"]
    left_pos = 20
    top_pos = 20
    for column in columns_list:
        pygame.draw.rect(screen, pygame.Color(224, 224, 224),
                         pygame.Rect(left_pos, top_pos, COLUMN_WIDTH, COLUMN_HEADER_HEIGHT))
        pygame.draw.rect(screen, pygame.Color(204, 204, 204),
                         pygame.Rect(left_pos, top_pos + COLUMN_HEADER_HEIGHT, COLUMN_WIDTH, COLUMN_BODY_HEIGHT))
        font = pygame.font.SysFont(None, 24)
        img = font.render(column, True, pygame.Color(39, 39, 39))
        screen.blit(img, (left_pos + 10, top_pos + 15))
        left_pos += COLUMN_WIDTH + COLUMN_SPACES


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color(241, 241, 241))

    # RENDER YOUR GAME HERE
    render_columns(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
