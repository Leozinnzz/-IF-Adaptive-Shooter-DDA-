import pygame
import random
from settings import WIDTH, HEIGHT

POWERUP_CONFIGS = {
    "coffee": { 
        "image_path": "src/assets/img/cafe.png", 
        "sound_path": "src/assets/sounds/powerup.wav",
        "size": (90, 90),
        "fallback_color": (0, 255, 0) 
    },
    #"auxilio": { 
        #"image_path": "src/assets/img/auxilio.png", 
        #"sound_path": "src/assets/sounds/powerup.wav",
        #"size": (80, 80),
        #"fallback_color": (255, 215, 0) 
    #}
}

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_type):
        super().__init__()
        self.type = power_type 
        self.config = POWERUP_CONFIGS.get(self.type, POWERUP_CONFIGS["coffee"])

        self.load_image()
        self.load_sound()

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = -40

        #hitbox do cafe
        self.mask = pygame.mask.from_surface(self.image)

        self.speed_y = 2

    def load_image(self):
        path = self.config.get("image_path")
        size = self.config.get("size", (40,40))
        fallback_color = self.config.get("fallback_color", (255, 255, 255))

        try: 
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
        except (pygame.error, FileNotFoundError): 
            self.image = pygame.Surface(size)
            self.image.fill(fallback_color)

    def load_sound(self):
        sound_path = self.config.get("sound_path")
        self.sound = None
        if sound_path:
            try:
                self.sound = pygame.mixer.Sound(sound_path)
                self.sound.set_volume(0.5)
            except (pygame.error, FileNotFoundError):
                self.sound = None

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()
