import pygame
import random
from settings import WIDTH, HEIGHT, BLACK, WHITE
from player import Player
from enemy import Enemy
from powerup import PowerUp

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IF Adaptive Shooter ")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

# Grupos de Sprites
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()  # Grupo exclusivo para os tiros

player = Player()
all_sprites.add(player)

for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_group.add(enemy)

score = 0
max_sanity = 100
current_sanity = 10
lives = 1
powerup_spawn_timer = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Disparar ao pressionar a tecla ESPAÇO
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullet_group.add(bullet)

    keys = pygame.key.get_pressed()

    # Spawner de Power-Ups
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

    # Colisão: Tiro acerta no Inimigo (destrói ambos e soma pontos)
    hits = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
    for hit in hits:
        score += 100
        # Cria um novo inimigo para substituir o destruído mantendo o fluxo
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemy_group.add(new_enemy)

    # Colisão: Jogador apanha Power-Up
    powerup_collisions = pygame.sprite.spritecollide(player, powerup_group, True)
    for p in powerup_collisions:
        if p.type == 'coffee':
            score += 500
        elif p.type == 'auxilio':
            lives += 1

    # Renderização
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # HUD do jogo
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    
    screen.blit(lives_text, (20, HEIGHT - 40))
    screen.blit(score_text, (WIDTH - 150, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()