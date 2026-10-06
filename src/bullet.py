import pygame 
from settings import HEIGHT
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Carrega a imagem única do tiro e redimensiona
        bullet = pygame.image.load("src/assets/img/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(bullet, (50, 50))

        #redimensiona a imagem e centraliza ela
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Hitbox precisa baseada nos pixels reais da imagem
        pixel_rect = self.image.get_bounding_rect()
        self.hitbox = pixel_rect.copy()
        self.hitbox.center = self.rect.center

        self.speed_y = -10  

    def update(self):
        # Movimento vertical ativo
        self.rect.y += self.speed_y

        # Ajuste em tempo real da hitbox para acompanhar o movimento
        self.hitbox.center = self.rect.center
        
        # remove o tiro se ele sair da tela 
        if self.rect.bottom < 0:
            self.kill()