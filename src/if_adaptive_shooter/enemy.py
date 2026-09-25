import pygame
import random
from settings import WIDTH, HEIGHT, RED

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        try:
            self.image = pygame.image.load("assets/img/sintaxe_corrompida.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (200, 200))
        except pygame.error:
            # Fallback caso a imagem falhe
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 60, 60)) 
        
        # O rect deve ficar DEPOIS do try/except para garantir que existe sempre!
        self.rect = self.image.get_rect()
        
        # OPCIONAL: Se a imagem de 128x128 deixar a hitbox grande demais, 
        # podes redimensionar o rect para a colisão ficar mais justa:
        # self.rect = pygame.Rect(0, 0, 80, 80) 
        
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(50, WIDTH - 50)
