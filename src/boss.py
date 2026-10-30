import pygame as py 
import settings 
from enemy_bullet import EnemyBullet

BOSS_CONFIGS = {
    "ITERATOR-01": {
        "image_path": "src/assets/img/ITERATOR-01.png",
        "size_scale": (0.15, 0.15), 
        "max_health": 1000,
        "fallback_color": (255, 0, 255), 
    }, 
    "SEGMENTATION": {
        "image_path": "src/assets/img/SEGMENTATION.png",
        "size_scale": (0.15, 0.15), 
        "max_health": 1000,
        "fallback_color": (255, 0, 255), 
    },
}

class Boss(py.sprite.Sprite):
    def __init__(self, boss_type="ITERATOR-01"):
        super().__init__()
        self.boss_type = boss_type 
        self.config = BOSS_CONFIGS.get(self.boss_type, BOSS_CONFIGS["ITERATOR-01"]) 

        self.load_image_dynamic()

        self.rect = self.image.get_rect()
        self.rect.centerx = settings.WIDTH // 2
        self.rect.y = -self.rect.height

        self.mask = py.mask.from_surface(self.image)

        self.max_health = self.config["max_health"]
        self.health = self.max_health
        self.speed_x = 3 

        self.state = "ENTRANCE"

        self.is_flashing = False 
        self.flash_timer = 0 
        self.flash_duration = 10 

        # Temporizador de tiro do Boss
        self.shoot_timer = 0
        self.shoot_interval = 45

    def load_image_dynamic(self):
        boss_width = max(100, int(settings.WIDTH * self.config["size_scale"][0]))
        boss_height = max(100, int(settings.HEIGHT * self.config["size_scale"][1]))
        
        path = self.config.get("image_path")
        fallback_color = self.config.get("fallback_color", settings.RED)

        try: 
            self.original_image = py.image.load(path).convert_alpha()
            self.original_image = py.transform.scale(self.original_image, (boss_width, boss_height))
            self.image = self.original_image
        except (py.error, FileNotFoundError):
            self.original_image = py.Surface((boss_width, boss_height))
            self.original_image.fill(fallback_color)
            self.image = self.original_image

    def resize(self):
        centerx = self.rect.centerx
        y = self.rect.y
        self.load_image_dynamic()
        self.rect = self.image.get_rect(centerx=centerx, y=y)
        self.mask = py.mask.from_surface(self.image)

    def hit(self):
        if not self.is_flashing: 
            self.is_flashing = True
            self.flash_timer = 0

            self.flash_image = self.original_image.copy()
            self.flash_image.fill((100, 100, 100), special_flags=py.BLEND_RGBA_MULT)
            self.image = self.flash_image

    def update(self, enemy_group, enemy_bullet_group):
        if self.is_flashing: 
            self.flash_timer += 1
            if self.flash_timer > self.flash_duration:
                self.is_flashing = False
                self.image = self.original_image

        if self.state == "ENTRANCE":
            self.rect.y += 2
            if self.rect.top >= int(settings.HEIGHT * 0.08):
                self.state = "FIGHT"
                
        elif self.state == "FIGHT":
            self.rect.x += self.speed_x
            if self.rect.left <= 20 or self.rect.right >= settings.WIDTH - 20:
                self.speed_x *= -1

            # Lógica de disparo do Boss
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                self.shoot_pattern(enemy_bullet_group)

    def shoot_pattern(self, enemy_bullet_group):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        enemy_bullet_group.add(bullet)

    def draw_health_bar(self, surface):
        bar_width = int(settings.WIDTH * 0.6)
        bar_height = 18
        bar_x = (settings.WIDTH - bar_width) // 2
        bar_y = 20
        
        fill = max(0, (self.health / self.max_health) * bar_width)
        
        outline_rect = py.Rect(bar_x, bar_y, bar_width, bar_height)
        fill_rect = py.Rect(bar_x, bar_y, fill, bar_height)
        
        py.draw.rect(surface, (50, 50, 50), outline_rect)
        py.draw.rect(surface, (255, 0, 0), fill_rect)
        py.draw.rect(surface, (255, 255, 255), outline_rect, 2)