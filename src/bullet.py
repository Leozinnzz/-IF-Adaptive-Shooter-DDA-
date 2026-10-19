import pygame 
from settings import HEIGHT
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Carrega a imagem única do tiro e redimensiona
        bullet = pygame.image.load("src/assets/img/bullet_purple.png").convert_alpha()
        self.image = pygame.transform.scale(bullet, (40, 40))

        #redimensiona a imagem e centraliza ela
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Hitbox pixel perfect
        self.mask = pygame.mask.from_surface(self.image)

        self.speed_y = -10  

    def update(self):
        # Movimento vertical ativo
        self.rect.y += self.speed_y

        # remove o tiro se ele sair da tela 
        if self.rect.bottom < 0:
            self.kill()