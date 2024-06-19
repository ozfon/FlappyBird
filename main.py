# Example file showing a basic pygame "game loop"
import pygame
from settings import Player, Floor, BotPipe, TopPipe, width, height, bg
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
running_time = 0
released = True
GameStarted = False
topSpacing = 100
botSpacing = -100
score = 0
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

p1 = Player()
floor = Floor()
rngNUM = random.randint(botSpacing, topSpacing)
botPipe = BotPipe(rngNUM)
topPipe = TopPipe(rngNUM)

all_spites_except_floor = pygame.sprite.Group()
pipes = pygame.sprite.Group()
collision_group = pygame.sprite.Group()

pipes.add(botPipe, topPipe)
collision_group.add(pipes, floor)
all_spites_except_floor.add(p1, pipes)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if  event.key == pygame.K_SPACE:
                released = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if botPipe.rect[0] == width - 6 * 50:
        rngNUM = random.randint(botSpacing, topSpacing)
        botPipe = BotPipe(rngNUM)
        topPipe = TopPipe(rngNUM)
        pipes.add(botPipe, topPipe)
        collision_group.add(botPipe, topPipe)
        all_spites_except_floor.add(botPipe, topPipe)

    x = 0
    while x <= width:
        screen.blit(bg, (x,0))
        x += bg.get_width()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if released:
            GameStarted = p1.jump()
            released = False

    p1.move()
    if GameStarted:
        pipes.update()

    for entity in all_spites_except_floor:
        screen.blit(entity.image, entity.rect)
    screen.blit(floor.image, floor.rect)

    for pipe in pipes:
        if pipe.rect[0] == 1280 - 189 * 6:
            score += 1
            break

    text_surface = my_font.render("Score: {}".format(score), False, (0,0,0))
    screen.blit(text_surface, (0,0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    if pygame.sprite.spritecollideany(p1, collision_group) or p1.rect[1] <= 0:
        p1.kill()
        running = False

    dt = clock.tick(60) / 1000 # limits FPS to 60
    p1.time += dt

pygame.quit()