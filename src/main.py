import pygame
import random
import settings 
from player import Player
from enemy import Enemy
from powerup import PowerUp
from explosion import Explosion    

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("IF Adaptive Shooter ")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

# Grupos de Sprites
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()  # Grupo exclusivo para os tiros
explosion_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


quantity = settings.WIDTH // 200

for _ in range(quantity):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_group.add(enemy)

score = 0
max_sanity = 100
current_sanity = 10
lives = 1
powerup_spawn_timer = 0
running = True

#colisao do inimigo
def collide_hitboxes(sprite1, sprite2):
    return sprite1.hitbox.colliderect(sprite2.hitbox)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE: 
            #atualiza a tela com o novo tamanho 
            settings.WIDTH = event.w
            settings.HEIGHT = event.h

            #screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            player.rect.centerx = settings.WIDTH // 2 
            player.rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05) 
            player.hitbox.center = player.rect.center

        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullet_group.add(bullet)

    keys = pygame.key.get_pressed()

    # Spawn de power Up
    powerup_spawn_timer += 1
    if powerup_spawn_timer > 300:
        chosen_type = random.choice(['coffee', 'auxilio'])
        powerup = PowerUp(chosen_type)
        all_sprites.add(powerup)
        powerup_group.add(powerup)
        powerup_spawn_timer = 0

    # Atualizações
    player.update(keys)
    enemy_group.update()
    powerup_group.update()
    bullet_group.update()
    explosion_group.update()

    # colisao
    hits = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True, collided=collide_hitboxes)
    for hit in hits:
        score += 100

        #Cria a explosao do inimigo atingido
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        explosion_group.add(explosion)
        # Cria um novo inimigo para substituir o destruído 
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemy_group.add(new_enemy)

    # Colisão Power up
    powerup_collisions = pygame.sprite.spritecollide(player, powerup_group, True)
    for p in powerup_collisions:
        if p.type == 'coffee':
            score += 500
        elif p.type == 'auxilio':
            lives += 1

    
    screen.fill(settings.BLACK)
    all_sprites.draw(screen)

    
    lives_text = font.render(f"Lives: {lives}", True, settings.WHITE)
    score_text = font.render(f"Score: {score}", True, settings.WHITE)

    lives_rect = lives_text.get_rect()
    lives_rect.left = int(settings.WIDTH * 0.08)
    lives_rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05)
    screen.blit(lives_text, lives_rect)

    score_rect = score_text.get_rect() 
    score_rect.right = int(settings.WIDTH * 0.92)
    score_rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05)
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()