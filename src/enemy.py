import pygame
import random
from settings import WIDTH, HEIGHT, RED

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        try:
            self.image = pygame.image.load("src/assets/img/sintaxe_corrompida.png").convert_alpha()
            # print(self.image.get_bounding_rect()) eu descobri como achar quantos bits ocupa
            self.image = pygame.transform.scale(self.image, (100, 100))
        except pygame.error:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 60, 60)) 

        #definir a posição inicial do rect
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-100, -40)

        # encontra a hitbox do jogo
        pixel_rect = self.image.get_bounding_rect() 
        self.hitbox = pixel_rect.copy() 
        self.hitbox.center = self.rect.center

        self.speed_y = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(50, WIDTH - 50)

        self.hitbox.center = self.rect.center