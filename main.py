# Example file showing a basic pygame "game loop"
import os
import sys
import neat
import neat.config
import neat.population
import pygame
from settings import birdToPipeCollision, Birds, Floor, BotPipe, TopPipe, width, height, bg
import random

generation = 0
highscore = 0

def main(genomes, config):
    pygame.init()

    global generation, highscore
    generation += 1

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    topSpacing = 100
    botSpacing = -100
    score = 0

    pygame.font.init()
    my_font = pygame.font.SysFont('Times New Roman', 30)

    birds = []
    ge = []
    nets = []
    distanceToPipes = []
    textSurfaces = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Birds())
        g.fitness = 0
        ge.append(g)


    floor1 = Floor(0)
    floor2 = Floor(width)
    floors = [floor1, floor2]

    rngNUM = random.randint(botSpacing, topSpacing)
    botPipe = BotPipe(rngNUM)
    topPipe = TopPipe(rngNUM)

    topPipes = [topPipe]
    botPipes = [botPipe]

    all_spites_except_floor = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    collision_group = pygame.sprite.Group()

    pipes.add(botPipe, topPipe)
    collision_group.add(pipes, floor1, floor2)
    all_spites_except_floor.add(pipes)
    for bird in birds:
        all_spites_except_floor.add(bird)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if  event.key == pygame.K_SPACE:
                    released = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()

        if len(birds) == 0:
            running =False
            break
        
        if topPipes[len(topPipes)-1].rect[0] <= 970 and not topPipes[len(topPipes)-1].addPipe:
            topPipes[len(topPipes)-1].addPipe = True
            rngNUM = random.randint(botSpacing, topSpacing)
            botPipe = BotPipe(rngNUM)
            topPipe = TopPipe(rngNUM)
            pipes.add(botPipe, topPipe)
            collision_group.add(botPipe, topPipe)
            all_spites_except_floor.add(botPipe, topPipe)
            topPipes.append(topPipe)
            botPipes.append(botPipe)

        x = 0
        while x <= width:
            screen.blit(bg, (x,0))
            x += bg.get_width()

        distanceToPipes.clear()
        for pipe in topPipes:
            distanceToPipes.append(pipe.rect[0] - birds[0].rect[0])

        minPosDistance = sys.maxsize
        for x, distance in enumerate(distanceToPipes):
            if distance > 0 and distance < minPosDistance:
                minPosDistance = distance
                pipeindex = x

        for x, bird in enumerate(birds):
            bird.move()
            bird.draw_border(screen)
            ge[x].fitness += 1/60

            output = nets[x].activate((bird.rect[1], 
                                       abs(bird.rect[1] - topPipes[pipeindex].rect[1] - topPipes[pipeindex].rect[3]),
                                       abs(bird.rect[1] - botPipes[pipeindex].rect[1])))

            if output[0] > 0.5 and bird.time > 0.2:
                bird.jump()

        pipes.update()

        for _ in all_spites_except_floor:
            screen.blit(_.image, _.rect)
        for _ in floors:
            _.move()
            screen.blit(_.image, _.rect)

        for _ in topPipes:
            if _.rect[0] + _.image.get_width() < 0:
                topPipes.remove(_)
                pipes.remove(_)
            for bird in birds:
                if bird.rect[0] > _.rect[0] + _.rect[2]:
                    if not _.passed:
                        score += 1
                        if score > highscore:
                            highscore = score
                        for g in ge:
                            g.fitness += 5
                        _.passed = True
                if _.passed:
                    break
            _.draw_border(screen)   
        
        for _ in botPipes:
            if _.rect[0] + _.image.get_width() < 0:
                botPipes.remove(_)
                pipes.remove(_)
            _.draw_border(screen)   

        textSurfaces.clear()
        textSurfaces.append(my_font.render("Score: {}".format(score), False, (0,0,0)))
        textSurfaces.append(my_font.render("Highscore: {}".format(highscore), False, (0,0,0)))
        textSurfaces.append(my_font.render("Generation: {}".format(generation), False, (0,0,0)))


        for x, textSurface in enumerate(textSurfaces):
            screen.blit(textSurface, (width-textSurface.get_width(),x * 30))

        pygame.display.flip()

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if birdToPipeCollision(bird, pipe):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    bird.kill()

        for x, bird in enumerate(birds):
            if bird.rect[1] < 0 or bird.rect[1] + bird.rect[3] > floor1.top:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                bird.kill()

        dt = clock.tick(60) / 1000 # limits FPS to 60
        for bird in birds:
            bird.time += dt

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 100)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run(config_path)