import pygame
import os
import random

width = 1280
height = 720

class Birds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.red = random.randint(0,255)
        self.green = random.randint(0,255)
        self.blue = random.randint(0,255)
        self.time = 0
        self.vel = -50
        self.acc = 90
        self.image = pygame.image.load(os.path.join('images','bird2.png'))
        self.rect = self.image.get_rect()
        self.rect.move_ip(150, height/2-self.image.get_size()[0]/2)

    def jump(self):
        self.time = 0
        self.image = pygame.image.load(os.path.join('images','bird3.png'))
        self.image = pygame.transform.rotate(self.image, 18)
        self.rect = pygame.Rect(self.rect[0], self.rect[1], self.image.get_width(), self.image.get_height())

    def move(self):
        dx = self.vel*self.time + self.acc*self.time**2
        self.rect.move_ip(0, dx) 
        if dx > 0:
            self.image = pygame.image.load(os.path.join('images','bird1.png'))
            self.image = pygame.transform.rotate(self.image, -18)
            self.rect = pygame.Rect(self.rect[0], self.rect[1], self.image.get_width(), self.image.get_height())

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def draw_border(self, screen):
        pygame.draw.rect(screen, (self.red, self.green, self.blue), self.rect, width=1)

bg = pygame.image.load(os.path.join('images','bg.png'))
bg = pygame.transform.scale(bg, (bg.get_width(), height))

class Floor(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load(os.path.join('images','base.png'))
        self.image = pygame.transform.scale(self.image, (width, self.image.get_height()))
        self.top = height-self.image.get_height() 
        self.rect = pygame.Rect(x, self.top, self.image.get_width(), self.image.get_height())

    def move(self):
        self.rect.move_ip(-6, 0)
        if self.rect[0] <= -width:
            self.rect.move_ip(2*width, 0)

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        self.rect.move_ip(-6, 0)

    def move(self, rngNUM):
        self.rect.move_ip(0, rngNUM)
    
    def draw_border(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect, width=1)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
class BotPipe(Pipe):
    def __init__(self, rngNUM):
        super().__init__()
        self.image = pygame.image.load(os.path.join('images','pipe.png'))
        self.rect = self.image.get_rect()
        self.rect.move_ip(width, height - self.image.get_rect()[3])
        super().move(rngNUM)

class TopPipe(Pipe):
    def __init__(self, rngNUM):
        self.passed = False
        self.addPipe = False
        super().__init__()
        self.image = pygame.image.load(os.path.join('images','pipe.png'))
        self.rect = self.image.get_rect()
        self.rect.move_ip(width, -100)
        self.image = pygame.transform.flip(self.image, False, True)
        super().move(rngNUM)

def birdToPipeCollision(bird, pipe):
    bird_mask = bird.get_mask()
    pipe_mask = pipe.get_mask()

    offset = (pipe.rect[0] - bird.rect[0], pipe.rect[1] - bird.rect[1])

    point = bird_mask.overlap(pipe_mask, offset)

    if point:
        return True
    
    return False