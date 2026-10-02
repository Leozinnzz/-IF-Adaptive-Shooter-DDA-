import pygame 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()

        self.image = pygame.Surface((40, 40)) 
        self.image.fill((255, 140, 0))

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.frame_counter = 0
        self.lifetime = 15 # tempo da explosao
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.lifetime:
            self.kill()