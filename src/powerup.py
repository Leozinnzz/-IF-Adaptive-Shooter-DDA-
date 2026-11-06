import pygame
import random
from settings import WIDTH, HEIGHT

POWERUP_CONFIGS = {
    "coffee": { 
        "image_path": "src/assets/img/powerups/cafe.png", 
        "sound_path": "src/assets/sounds/powerup.wav",
        "size": (90, 90),
        "fallback_color": (0, 255, 0) 
    },
    "ticket": { 
        "image_path": "src/assets/img/powerups/ticket.png", 
        "sound_path": "src/assets/sounds/powerup.wav",
        "size": (80, 80),
        "fallback_color": (255, 215, 0) 
    },
    "clock": { 
        "image_path": "src/assets/img/powerups/clock.png", 
        "sound_path": "src/assets/sounds/powerup.wav",
        "size": (80, 80),
        "fallback_color": (255, 215, 0) 
    },
    "shield": { 
        "image_path": "src/assets/img/powerups/shield.png", 
        "sound_path": "src/assets/sounds/powerup.wav",
        "size": (80, 80),
        "fallback_color": (255, 215, 0) 
    },
}

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_type):
        super().__init__()
        self.type = power_type 
        self.config = POWERUP_CONFIGS.get(self.type, POWERUP_CONFIGS["coffee"])

        self.load_image()

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

    def apply_effect(self, player, game_context, audio):
        sound_path = self.config.get("soudn_path", "src/assets/sounds/powerup.wav")
        audio.play_sound(sound_path, 0.4)

        if self.type == 'coffee': 
            player.apply_speed_boost(1.5) 
            game_context['score'] += 50 

        elif self.type == 'ticket': 
            game_context['sanity'] = min(100, game_context['sanity'] + 25)

        # 3. Clock -> Aula_vaga
        elif self.type == "clock":
            game_context['score'] += 300

        # 4. Escudo DP -> invulnerabilidade temporária
        elif self.type == "shield":
            player.activate_shield()
            game_context['score'] += 250



    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()
