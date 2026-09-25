import pygame
import random
from settings import WIDTH, HEIGHT

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_type):
        super().__init__()
        self.type = power_type  # 'coffee' or 'auxilio'
        
        if self.type == 'coffee':
            try: 
                # Confere se o ficheiro se chama exatamente 'Cafe.png' ou 'cafe.png'
                self.image = pygame.image.load("assets/img/Cafe.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (128, 128))
            except pygame.error:
                self.image = pygame.Surface((40, 40))
                self.image.fill((0, 255, 0))  
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 215, 0))  # Gold
            
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = -40
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()