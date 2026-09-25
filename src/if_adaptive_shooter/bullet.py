import pygame
from settings import HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Um retângulo pequeno e brilhante (ex: cor amarela laser)
        self.image = pygame.Surface((5, 12))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        
        # O tiro nasce na posição central do topo da nave do jogador
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10  # Velocidade negativa para subir no ecrã

    def update(self):
        self.rect.y += self.speed_y
        # Se o tiro sair do tela pelo topo, é destruído da memória
        if self.rect.bottom < 0:
            self.kill()