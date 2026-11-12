import pygame
import settings
from PIL import Image, ImageSequence

class Menu:
    def __init__(self):
        # Aumentei um pouco a fonte para ficar proporcional aos botões da imagem
        self.font_options = pygame.font.SysFont("arial", 32, bold=True)
        
        # Opções atualizadas para bater exatamente com a tua imagem
        self.options = ["JOGAR", "OPÇÕES", "SAIR"]
        self.selected_index = 0

        # --- Background Animation Setup (Pillow) ---
        gif_path = 'src/assets/img/menu/menu.gif'
        self.background_frames = self.load_gif_direct(gif_path)
            
        self.current_frame = 0.0
        self.animation_speed = 0.3 

    def load_gif_direct(self, path):
        frames = []
        pil_image = Image.open(path)
        for frame in ImageSequence.Iterator(pil_image):
            frame_rgba = frame.convert("RGBA")
            pygame_surface = pygame.image.frombytes(
                frame_rgba.tobytes(), frame_rgba.size, "RGBA"
            ).convert()
            pygame_surface = pygame.transform.scale(pygame_surface, (settings.WIDTH, settings.HEIGHT))
            frames.append(pygame_surface)
        return frames

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected_action(self):
        return self.options[self.selected_index]

    def draw(self, screen):
        # --- Draw Animated Background ---
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.background_frames):
            self.current_frame = 0.0
            
        frame_index = int(self.current_frame)
        screen.blit(self.background_frames[frame_index], (0, 0))
        
        button_width = 500
        button_height = 60
        spacing = 80
        
        center_x = settings.WIDTH // 3.5  
        start_y = settings.HEIGHT // 2.2  
        
        for i, option in enumerate(self.options):
            center_y = start_y + (i * spacing)
            
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (center_x, center_y)
            
            if i == self.selected_index:
                bg_color = (168, 255, 0) 
                text_color = (0, 0, 0)
                
                pygame.draw.rect(screen, bg_color, button_rect, border_radius=15)
                pygame.draw.rect(screen, (100, 180, 0), button_rect, width=3, border_radius=15)
            else:
                border_color = (0, 255, 255) 
                text_color = (255, 255, 255)
                pygame.draw.rect(screen, border_color, button_rect, width=3, border_radius=15)

            option_text = self.font_options.render(option, True, text_color)
            text_rect = option_text.get_rect(center=button_rect.center)
            
            screen.blit(option_text, text_rect)