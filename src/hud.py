import pygame
import math

class HUD:
    def __init__(self):
        
        base_path = "src/assets/img/"
        
        
        self.frame = pygame.image.load(f"{base_path}sanidade_frame.png").convert_alpha()
        self.fill = pygame.image.load(f"{base_path}sanidade_fill.png").convert_alpha()
        self.empty = pygame.image.load(f"{base_path}sanidade_empty.png").convert_alpha()
        self.eye_mid = pygame.image.load(f"{base_path}sanidade_eye_instavel.png").convert_alpha()
        self.eye_low = pygame.image.load(f"{base_path}sanidade_eye_critico.png").convert_alpha()

        self.size = (512, 170)
        self.fill_rect = pygame.Rect(90, 81, 360, 27)

    def draw_sanity(self, surface, amount, pos=(0, 0), scale=1):
        amount = max(0, min(100, amount))
        hud_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        hud_surface.blit(self.empty, (0, 0))

        width = round(self.fill_rect.w * amount / 100)
        if width > 0:
            area = pygame.Rect(self.fill_rect.x, self.fill_rect.y, width, self.fill_rect.h)
            hud_surface.blit(self.fill, (self.fill_rect.x, self.fill_rect.y), area=area)

        # 3. Moldura
        hud_surface.blit(self.frame, (0, 0))
        
        # 4. Efeitos Visuais 
        now = pygame.time.get_ticks() / 1000
        if amount <= 30:
            self.eye_low.set_alpha(round(130 + 125 * (0.5 + 0.5 * math.sin(now * 8))))
            hud_surface.blit(self.eye_low, (0, 0))
        elif amount <= 60:
            hud_surface.blit(self.eye_mid, (0, 0))

        if scale != 1:
            scaled_size = (int(self.size[0] * scale), int(self.size[1] * scale))
            hud_surface = pygame.transform.scale(hud_surface, scaled_size)
            
        # Desenha na tela principal
        surface.blit(hud_surface, pos)