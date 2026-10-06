import pygame
import settings

class Menu:
    def __init__(self):
        self.font_title = pygame.font.SysFont("arial", 60, bold=True)
        self.font_options = pygame.font.SysFont("arial", 28)
        
        self.options = ["Iniciar Jogo", "Sair"]
        self.selected_index = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected_action(self):
        return self.options[self.selected_index]

    def draw(self, screen):
        screen.fill(settings.BLACK)
        
        # Titulo do jogo
        title_text = self.font_title.render("IF ADAPTIVE SHOOTER", True, (0, 255, 128)) # Verde tecnológico
        title_rect = title_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Desenha as Opções do Menu
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                color = (255, 255, 0) 
                text_content = f"> {option} <"
            else:
                color = (200, 200, 200)
                text_content = option

            option_text = self.font_options.render(text_content, True, color)
            option_rect = option_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + (i * 50)))
            screen.blit(option_text, option_rect)