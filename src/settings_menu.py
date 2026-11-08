import pygame
import settings

class SettingsMenu:
    def __init__(self):
        self.options = ["Volume Música: 100%", "Volume Efeitos: 100%", "Áudio: Ativado", "Tela Cheia: Desativado", "Voltar"]
        self.selected_index = 0

        self.audio_on = True
        self.fullscreen = False

        self.font = pygame.font.SysFont("arial", 28)
        self.font_title = pygame.font.SysFont("arial", 45, bold=True)

    def handle_input(self, event, audio):
        if event.type == pygame.KEYDOWN:
            
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE, pygame.K_a, pygame.K_d):
                
                if self.selected_index == 0:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        audio.set_music_volume(round(audio.music_volume - 0.1, 1))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        audio.set_music_volume(round(audio.music_volume + 0.1, 1))

                elif self.selected_index == 1:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        audio.set_sfx_volume(round(audio.sfx_volume - 0.1, 1))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        audio.set_sfx_volume(round(audio.sfx_volume + 0.1, 1))

                elif self.selected_index == 2 and event.key in (pygame.K_RETURN, pygame.K_SPACE):  
                    self.audio_on = not self.audio_on
                    audio.set_mute(not self.audio_on) 
                
                # 3: Tela Cheia
                elif self.selected_index == 3 and event.key in (pygame.K_RETURN, pygame.K_SPACE): 
                    self.fullscreen = not self.fullscreen


    def draw(self, audio, surface):
        surface.fill((20, 20, 30)) 

        title_surf = self.font_title.render("CONFIGURAÇÕES", True, settings.WHITE)
        title_rect = title_surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 5))
        surface.blit(title_surf, title_rect)

        music_pct = int(audio.music_volume * 100)
        sfx_pct = int(audio.sfx_volume * 100) 
        
        self.options[0] = f"Volume Música: < {music_pct}% >"
        self.options[1] = f"Volume Efeitos: < {sfx_pct}% >"
        self.options[2] = f"Áudio: {'Ativado' if self.audio_on else 'Desativado'}"
        
        self.options[3] = f"Tela Cheia: {'Ativado' if self.fullscreen else 'Desativado'}"

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 3 + i * 55))
            surface.blit(text_surf, text_rect)