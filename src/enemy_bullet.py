import pygame 
from settings import WIDTH, HEIGHT 

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

    # Cria uma superfície simples para o projétil o qual eu vou subistituir depois pela pixel art
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y


        self.mask = pygame.mask.from_surface(self.image)
        self.speed_y = 6 

    def update(self):
        self.rect.y += self.speed_y


        if self.rect.top > HEIGHT:
            self.kill()