import pygame
from settings import WIDTH, HEIGHT, IF_GREEN
from bullet import Bullet
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try: 
            self.image = pygame.image.load("src/assets/img/DP-02 Delta.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 146))
        except pygame.error:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 60, 60)) 

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30

        #Hitbox pixel perfect 
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 6

    def update(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < settings.WIDTH:
            self.rect.x += self.speed
        # Movimento Vertical (Cima / Baixo ou W / S)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < settings.HEIGHT:
            self.rect.y += self.speed


    def shoot(self): 
        return Bullet(self.rect.centerx, self.rect.top)