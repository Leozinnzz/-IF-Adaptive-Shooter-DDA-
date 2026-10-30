import pygame
import random
from enemy_bullet import EnemyBullet
import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type

        # Dicionario dos caminhos das pixel arts
        self.image_paths = {
            "bug": "src/assets/img/bug.png",
            "drone_sintaxe": "src/assets/img/drone_sintaxe.png", 
            "AND_corrompido": "src/assets/img/AND_corrompido.png",
            "NOT_corrompido": "src/assets/img/NOT_corrompido.png",
            "OR_corrompido": "src/assets/img/OR_corrompido.png"
        }
        #tipo de projetil do inimigo
        bullet_map = {
            "drone_sintaxe": "green_orb",
            "AND_corrompido": "blue_orb",
            "NOT_corrompido": "blue_orb",
            "OR_corrompido": "red_orb"
        }
        
        self.bullet_type = bullet_map.get(self.enemy_type, "red_orb")

        self.load_image_dynamic()

        self.rect = self.image.get_rect()


        self.rect.x = random.randint(50, settings.WIDTH - 50)
        self.rect.y = random.randint(-150, -40)

        self.mask = pygame.mask.from_surface(self.image)
        self.speed_y = 2

        #efeito de impacto
        self.is_flashing = False 
        self.flash_timer = 0
        self.flash_duration = 10

        #disparo do inimigo
        self.can_shoot = False
        self.shoot_timer = 0
        self.shoot_interval = 0

        if enemy_type == "bug":
            self.speed_y = random.randint(3,5)
            self.max_health = 100
            self.can_shoot = False 
        elif enemy_type == "drone_sintaxe":
            self.speed_y = random.randint(2,4)
            self.max_health = 150
            self.can_shoot = True
            self.shoot_interval = 120
            self.shoot_timer = random.randint(0, 60)
        elif enemy_type == "OR_corrompido":
            self.speed_y = random.randint(2,2)
            self.max_health = 400
            self.can_shoot = True
            self.shoot_interval = 120
            self.shoot_timer = random.randint(0, 30)
        else:
            self.max_health = 200
            self.speed_y = random.randint(1,3)
            self.can_shoot = True
            self.shoot_interval = 90 
            self.shoot_timer = random.randint(0, 30)
        
        self.health = self.max_health

    def load_image_dynamic(self):
        enemy_size = max(50, int(settings.WIDTH * 0.05))
        path = self.image_paths.get(self.enemy_type, "")

        try:
            self.original_image = pygame.image.load(path).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (enemy_size, enemy_size))
            self.image = self.original_image
        except (pygame.error, FileNotFoundError):
            self.original_image = pygame.Surface((enemy_size, enemy_size))
            self.original_image.fill(settings.RED)
            self.image = self.original_image

    def reset_state(self):
        self.rect.y = random.randint(-100, -40)
        self.rect.x = random.randint(0, settings.WIDTH - self.rect.width)
        
        self.health = self.max_health
        
        if hasattr(self, 'is_flashing'):
            self.is_flashing = False
            self.image = self.original_image

    def resize(self):
        self.load_image_dynamic()
        self.mask = pygame.mask.from_surface(self.image)


    def draw_health_bar(self, surface):
            if self.health < self.max_health:
                bar_width = self.rect.width     
                bar_height = 5 
                fill = (self.health / self.max_health) * bar_width 

                bar_x = self.rect.x
                bar_y = self.rect.top - 8 

                #Retanguulo vermelho
                outline_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                fill_rect = pygame.Rect(bar_x, bar_y, fill, bar_height)
            
                pygame.draw.rect(surface, (255, 0, 0), outline_rect)
                pygame.draw.rect(surface, (0, 255, 0), fill_rect)


    def hit(self):
        if not self.is_flashing:
            self.is_flashing = True
            self.flash_timer = 0

            self.flash_image = self.original_image.copy()
            self.flash_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = self.flash_image

    def update(self, enemy_group, enemy_bullet_group):
        self.rect.y += self.speed_y

        

        #Flash de imapcto
        if self.is_flashing: 
            self.flash_timer += 1
            if self.flash_timer > self.flash_duration:
                self.is_flashing = False
                self.image = self.original_image

        # Disparo do inimigo 
        if self.can_shoot: 
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval: 
                self.shoot_timer = 0
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, bullet_type=self.bullet_type)
                enemy_bullet_group.add(bullet)


        #evitar colisao entre inimigos 
        for other in enemy_group: 
            if other != self:
                if self.rect.colliderect(other.rect):
                    if self.rect.centerx < other.rect.centerx:
                        self.rect.x -= 3
                    else:
                        self.rect.x += 3

        if self.rect.top > settings.HEIGHT:
            self.reset_state()
