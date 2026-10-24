import pygame
import settings

class SettingsMenu:
    def __init__(self):
        self.options = ["Áudio: Ativado", "Resolução: 1280x720", "Voltar"]
        self.selected_index = 0
        

        self.audio_on = True
        self.resolutions = [(1280, 720), (1366, 768), (1920, 1080)]
        self.res_index = 0

        self.font = pygame.font.SysFont("arial", 28)
        self.font_title = pygame.font.SysFont("arial", 45, bold=True)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
                if self.selected_index == 0:  # Áudio
                    self.audio_on = not self.audio_on
                    state = "Ativado" if self.audio_on else "Desativado"
                    self.options[0] = f"Áudio: {state}"
                    if self.audio_on:
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()

                elif self.selected_index == 1:  # Resolução
                    self.res_index = (self.res_index + 1) % len(self.resolutions)
                    w, h = self.resolutions[self.res_index]
                    self.options[1] = f"Resolução: {w}x{h}"

    def get_selected_action(self):
        return self.options[self.selected_index]

    def draw(self, surface):
        surface.fill((20, 20, 30)) 

        # Título
        title_surf = self.font_title.render("CONFIGURAÇÕES", True, settings.WHITE)
        title_rect = title_surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 4))
        surface.blit(title_surf, title_rect)

        # Opções
        for i, option in enumerate(self.options):
            color = (0, 255, 255) if i == self.selected_index else (200, 200, 200)
            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + i * 50))
            surface.blit(text_surf, text_rect)