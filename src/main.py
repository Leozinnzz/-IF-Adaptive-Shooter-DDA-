import pygame
import random
import settings 
from player import Player
from enemy import Enemy
from powerup import PowerUp
from explosion import Explosion    
from menu import Menu 
from audio import AudioManager


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("IF Adaptive Shooter ")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
font_gameover = pygame.font.SysFont("arial", 50, bold=True)
font_instructions = pygame.font.SysFont("arial", 20)

audio = AudioManager()
main_menu = Menu()

#Reiniciar todas as variáveis do jogo
def reset_game(): 
    global all_sprites, enemy_group, powerup_group, bullet_group, explosion_group, player, score, current_sanity, powerup_spawn_timer

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
    current_sanity = 100
    powerup_spawn_timer = 0
running = True
game_state = "MENU" #Estados do game ["MENU" "PLAYING" "GAME_OVER"]
current_music_state = None

#colisao do inimigo
def collide_hitboxes(sprite1, sprite2):
    return sprite1.hitbox.colliderect(sprite2.hitbox)

reset_game()

while running:

    #musica de menu no jogo
    if game_state == "MENU" and current_music_state != "MENU":
        audio.play_music("src/assets/sounds/menu_music.mp3")
        current_music_state = "MENU"
        
    elif game_state == "PLAYING" and current_music_state != "PLAYING":
        audio.stop_music()
        current_music_state = "PLAYING"
        
    elif game_state == "GAME_OVER" and current_music_state != "GAME_OVER":
        audio.stop_music()
        current_music_state = "GAME_OVER"

    #eventos no teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE: 
            #atualiza a tela com o novo tamanho 
            settings.WIDTH = event.w
            settings.HEIGHT = event.h

            player.rect.centerx = settings.WIDTH // 2 
            player.rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05) 
            player.hitbox.center = player.rect.center

        elif event.type == pygame.KEYDOWN: 
            if game_state == "MENU":
                # passa o evento para tratar as setas
                main_menu.handle_input(event)
                
                # confirma a opção com enter
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    escolha = main_menu.get_selected_action()
                    if escolha == "Iniciar Jogo":
                        reset_game()
                        game_state = "PLAYING"
                    elif escolha == "Sair":
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "PLAYING":
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullet_group.add(bullet)
                    
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    game_state = "MENU"

    keys = pygame.key.get_pressed()

    # Spawn de power Up
    if game_state == "PLAYING":
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
        powerup_collisions = pygame.sprite.spritecollide(player, powerup_group, True, collided=collide_hitboxes)
        for p in powerup_collisions:
            if p.type == 'coffee':
                score += 100
                if current_sanity < 100:
                    current_sanity += 10
                    if current_sanity > 100:
                        current_sanity = 100
            elif p.type == 'auxilio':
                score += 700

        #Colisao do jogador com o inimigo
        player_colision = pygame.sprite.spritecollide(player, enemy_group, True, collided=collide_hitboxes)
        for p in player_colision: 
            current_sanity -= 32;

            if current_sanity <= 0:
                current_sanity = 0
                game_state = "GAME_OVER"

    if game_state == "MENU": 
        main_menu.draw(screen)

    elif game_state == "PLAYING" or game_state == "GAME_OVER":
        screen.fill(settings.BLACK)
        all_sprites.draw(screen)

        # HUD (Vidas e Score)
        Health_text = font.render(f"Sanidade: {current_sanity}", True, settings.WHITE)
        score_text = font.render(f"Score: {score}", True, settings.WHITE)

        Health_rect = Health_text.get_rect()
        Health_rect.left = int(settings.WIDTH * 0.08)
        Health_rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05)
        screen.blit(Health_text, Health_rect)

        score_rect = score_text.get_rect() 
        score_rect.right = int(settings.WIDTH * 0.92)
        score_rect.bottom = settings.HEIGHT - int(settings.HEIGHT * 0.05)
        screen.blit(score_text, score_rect)

    #GAMEOVER
    if game_state == "GAME_OVER":
        game_over_text = font_gameover.render("GAME OVER - SANIDADE ESGOTADA", True, (255, 0, 0))
        go_rect = game_over_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 30))
        screen.blit(game_over_text, go_rect)

        restart_text = font_instructions.render("Pressione Qualquer Tecla para continuar...", True, settings.WHITE)
        restart_rect = restart_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 30))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()