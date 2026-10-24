import pygame 
from settings import WIDTH, HEIGHT


BULLET_CONFIGS = {
    "red_orb": {
        "image_path": "src/assets/img/red_orb.png",
        "size": (25, 25),
        "fallback_color": (255, 0, 0)      # Vermelho se a imagem falhar
    },
    "blue_orb": {
        "image_path": "src/assets/img/blue_orb.png",
        "size": (25, 25),
        "fallback_color": (0, 0, 255)      # Azul se a imagem falhar
    },
    "green_orb": {
        "image_path": "src/assets/img/green_orb.png",
        "size": (25, 25),
        "fallback_color": (0, 255, 0)      # Verde se a imagem falhar
    }
}

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_type="red_orb"):
        super().__init__()
        self.type = bullet_type
        self.config = BULLET_CONFIGS.get(self.type, BULLET_CONFIGS["red_orb"])

        self.load_image()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

        self.mask = pygame.mask.from_surface(self.image)
        self.speed_y = 6

    def load_image(self):
        path = self.config.get("image_path")
        size = self.config.get("size", (25, 25))
        fallback_color = self.config.get("fallback_color", (255, 0, 0))
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface(size)
            self.image.fill(fallback_color)

        
    def update(self):
        self.rect.y += self.speed_y


        if self.rect.top > HEIGHT:
            self.kill()