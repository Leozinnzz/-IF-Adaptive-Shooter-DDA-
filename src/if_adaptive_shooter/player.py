import pygame
from settings import WIDTH, HEIGHT, IF_GREEN
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        try: 
            # 1. Carrega a imagem e redimensiona para 40x40 pixels
            self.image = pygame.image.load("assets/img/Roteador.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (128, 128))
        except pygame.error:
            # 2. Fallback de segurança caso a imagem não seja encontrada
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 60, 60)) # Vermelho de erro
            
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30
        self.speed = 6

    def update(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed
        # Movimento Vertical (Cima / Baixo ou W / S)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        # Retorna um tiro disparado a partir do topo central da nave
        return Bullet(self.rect.centerx, self.rect.top)