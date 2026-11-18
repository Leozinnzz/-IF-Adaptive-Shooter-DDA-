import pygame
import settings

class GameOverMenu:
    def __init__(self):
        self.options = ["TENTAR NOVAMENTE", "VOLTAR AO MENU", "SAIR DO JOGO"]
        self.selected_index = 0
        self.font_options = pygame.font.SysFont("arial", 26, bold=True)
        self.font_score = pygame.font.SysFont("arial", 22, bold=True)
        
        self.image_path = "src/assets/img/menu/game_over.png"
        self.bg_image = None
        self.last_size = (0, 0)
        self.load_background()

    def load_background(self):
        self.last_size = (settings.WIDTH, settings.HEIGHT)
        try:
            raw = pygame.image.load(self.image_path).convert()
            self.bg_image = pygame.transform.scale(raw, self.last_size)
        except (pygame.error, FileNotFoundError):
            self.bg_image = pygame.Surface(self.last_size)
            self.bg_image.fill((6, 18, 12))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected_action(self):
        return self.options[self.selected_index]

    def draw(self, screen, score=0, wave=1):
        if (settings.WIDTH, settings.HEIGHT) != self.last_size:
            self.load_background()

        screen.blit(self.bg_image, (0, 0))

        stats_text = self.font_score.render(f"SCORE: {score}  |  WAVE: {wave}", True, (75, 245, 150))
        stats_rect = stats_text.get_rect(center=(settings.WIDTH // 2, int(settings.HEIGHT * 0.33)))
        screen.blit(stats_text, stats_rect)

        button_width = int(settings.WIDTH * 0.34)
        button_height = int(settings.HEIGHT * 0.068)
        spacing = int(settings.HEIGHT * 0.085)
        center_x = settings.WIDTH // 2
        start_y = int(settings.HEIGHT * 0.64)

        for i, option in enumerate(self.options):
            center_y = start_y + (i * spacing)
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (center_x, center_y)

            if i == self.selected_index:
                bg_color = (14, 58, 34)
                border_color = (52, 235, 134)
                text_color = (255, 255, 255)
                border_width = 3

                pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
                pygame.draw.rect(screen, border_color, button_rect, width=border_width, border_radius=12)

                arrow_offset = 16
                arrow_size = 10
                left_arrow = [
                    (button_rect.left - arrow_offset - arrow_size, center_y),
                    (button_rect.left - arrow_offset, center_y - arrow_size),
                    (button_rect.left - arrow_offset, center_y + arrow_size)
                ]
                right_arrow = [
                    (button_rect.right + arrow_offset + arrow_size, center_y),
                    (button_rect.right + arrow_offset, center_y - arrow_size),
                    (button_rect.right + arrow_offset, center_y + arrow_size)
                ]
                pygame.draw.polygon(screen, (75, 245, 150), left_arrow)
                pygame.draw.polygon(screen, (75, 245, 150), right_arrow)
            else:
                bg_color = (6, 18, 12)
                border_color = (32, 74, 52)
                text_color = (175, 195, 185)
                border_width = 2

                pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
                pygame.draw.rect(screen, border_color, button_rect, width=border_width, border_radius=12)

            text_surf = self.font_options.render(option, True, text_color)
            text_rect = text_surf.get_rect(center=button_rect.center)
            screen.blit(text_surf, text_rect)