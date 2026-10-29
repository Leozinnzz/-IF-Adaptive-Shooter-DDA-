import pygame
import settings
from bullet import Bullet


PLAYER_CONFIGS = {
    "IF-01 Alpha": {
        "image_path": "src/assets/img/IF-01 Alpha.png",
        "size_scale": (0.05, 0.18),
        "fallback_color": (0, 255, 0)
    },
    "DP-02 Delta": {
        "image_path": "src/assets/img/DP-02 Delta.png", 
        "size_scale": (0.05, 0.18),
        "fallback_color": (0, 100, 255)
    }
}

class Player(pygame.sprite.Sprite):
    def __init__(self, ship_type="IF-01 Alpha"):
        super().__init__()
        self.ship_type = ship_type
        self.config = PLAYER_CONFIGS.get(self.ship_type, PLAYER_CONFIGS["IF-01 Alpha"])
        
        self.load_image_dynamic()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = settings.WIDTH // 2
        self.rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05)

        #Hitbox pixel perfect 
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 6

    def load_image_dynamic(self):
        player_width = max(50, int(settings.WIDTH * self.config["size_scale"][0]))
        player_height = max(50, int(settings.HEIGHT * self.config["size_scale"][1]))
        path = self.config.get("image_path") 
        fallback_color = self.config.get("fallback_color", settings.WHITE) 

        #tratamento de exeção 
        try: 
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (player_width, player_height))
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((player_width, player_height))
            self.image.fill(fallback_color)

    def resize(self):
        centerx = self.rect.centerx
        bottom = self.rect.bottom

        self.load_image_dynamic()
        self.rect = self.image.get_rect()

        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.rect.clamp_ip(pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

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