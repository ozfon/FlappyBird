import pygame
import os

width = 1280
height = 720

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.vel = 0
        self.acc = 0
        self.image = pygame.image.load(os.path.join('images','bird2.png'))
        self.rect = self.image.get_rect()
        self.rect.move_ip(150, height/2-self.image.get_size()[0]/2)

    def jump(self):
        self.time = 0
        self.vel = -50
        self.acc = 90
        self.image = pygame.image.load(os.path.join('images','bird3.png'))
        self.image = pygame.transform.rotate(self.image, 18)
        return True

    def move(self):
        dx = self.vel*self.time + self.acc*self.time**2
        self.rect.move_ip(0, dx) 
        if dx > 0:
            self.image = pygame.image.load(os.path.join('images','bird1.png'))
            self.image = pygame.transform.rotate(self.image, -18)

bg = pygame.image.load(os.path.join('images','bg.png'))
bg = pygame.transform.scale(bg, (bg.get_width(), height))

class Floor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('images','base.png'))
        self.image = pygame.transform.scale(self.image, (width, self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.move_ip(0, height-self.image.get_height())
        self.floorHeight = self.image.get_rect()[0]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, rngNUM):
        super().__init__()
        self.rngNUM = rngNUM

    def update(self):
        self.rect.move_ip(-6, 0)

    def move(self):
        self.rect.move_ip(0, self.rngNUM)

class BotPipe(Pipe):
    def __init__(self, rngNUM):
        super().__init__(rngNUM)
        self.image = pygame.image.load(os.path.join('images','pipe.png'))
        self.rect = self.image.get_rect()
        self.rect.move_ip(width, height - self.image.get_rect()[3])
        super().move()

class TopPipe(Pipe, pygame.sprite.Sprite):
    def __init__(self, rngNUM):
        super().__init__(rngNUM)
        self.image = pygame.image.load(os.path.join('images','pipe.png'))
        self.rect = self.image.get_rect()
        self.rect.move_ip(width, -100)
        self.image = pygame.transform.rotate(self.image, 180)
        super().move()