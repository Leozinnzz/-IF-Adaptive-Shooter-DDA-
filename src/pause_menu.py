import pygame
import settings

class PauseMenu:
    def __init__(self):
        self.options = ["CONTINUAR", "REINICIAR", "MENU PRINCIPAL"]
        self.selected_index = 0
        self.font_title = pygame.font.SysFont("arial", 52, bold=True)
        self.font_option = pygame.font.SysFont("arial", 30, bold=True)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected_action(self):
        return self.options[self.selected_index]

    def draw(self, surface):
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        center_x = settings.WIDTH // 2
        title_y = int(settings.HEIGHT * 0.26)

        title_surf = self.font_title.render("JOGO PAUSADO", True, (168, 255, 0))
        shadow_surf = self.font_title.render("JOGO PAUSADO", True, (0, 0, 0))

        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (4, 4)]:
            outline_rect = shadow_surf.get_rect(center=(center_x + dx, title_y + dy))
            surface.blit(shadow_surf, outline_rect)

        title_rect = title_surf.get_rect(center=(center_x, title_y))
        surface.blit(title_surf, title_rect)

        button_width = 360
        button_height = 58
        spacing = 78
        start_y = int(settings.HEIGHT * 0.42)

        for i, option in enumerate(self.options):
            center_y = start_y + (i * spacing)
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (center_x, center_y)

            if i == self.selected_index:
                bg_color = (168, 255, 0)
                text_color = (0, 0, 0)
                pygame.draw.rect(surface, bg_color, button_rect, border_radius=15)
                pygame.draw.rect(surface, (100, 180, 0), button_rect, width=3, border_radius=15)
            else:
                border_color = (0, 255, 255)
                text_color = (255, 255, 255)
                pygame.draw.rect(surface, border_color, button_rect, width=3, border_radius=15)

            text_surf = self.font_option.render(option, True, text_color)
            text_rect = text_surf.get_rect(center=button_rect.center)
            surface.blit(text_surf, text_rect)