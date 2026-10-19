import pygame
import random
from enemy_bullet import EnemyBullet
from settings import WIDTH, HEIGHT, RED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type

        # Dicionario dos caminhos das pixel arts
        image_paths = {
            "bug": "src/assets/img/bug.png",
            "drone_sintaxe": "src/assets/img/drone_sintaxe.png", 
            "AND_corrompido": "src/assets/img/AND_corrompido.png",
            "NOT_corrompido": "src/assets/img/NOT_corrompido.png"
        }

        try:
            path = image_paths[enemy_type]
            self.original_image = pygame.image.load(path).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (100, 100))
            self.image = self.original_image
        except pygame.error:
            self.original_image = pygame.Surface((30, 30))
            self.original_image.fill((255, 60, 60)) 
            self.image = self.original_image

        #definir a posição inicial do rect
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-100, -40)

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
        else:
            self.max_health = 200
            self.speed_y = random.randint(1,3)
            self.can_shoot = True
            self.shoot_interval = 90 
            self.shoot_timer = random.randint(0, 30)

        self.health = self.max_health

        # encontra a hitbox do jogo
        pixel_rect = self.image.get_bounding_rect()   # descobri como achar quantos bits ocupa
        self.hitbox = pixel_rect.copy() 
        self.hitbox.center = self.rect.center


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

        #disparo do inimigo 
        if self.can_shoot: 
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval: 
                self.shoot_timer = 0
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                enemy_bullet_group.add(bullet)


        #evitar colisao entre inimigos 
        for other in enemy_group: 
            if other != self:
                if self.hitbox.colliderect(other.hitbox):
                    if self.rect.centerx < other.rect.centerx:
                        self.rect.x -= 3
                    else:
                        self.rect.x += 3

        self.hitbox.center = self.rect.center
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(50, WIDTH - 50)
