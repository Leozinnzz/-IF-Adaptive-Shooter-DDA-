import pygame
import settings
from PIL import Image, ImageSequence

class SettingsMenu:
    def __init__(self, back_frames = None):
        self.options = ["Música: 100%", "Efeitos: 100%", "Áudio: Ativado", "Tela Cheia: Desativado", "VOLTAR"]
        self.selected_index = 0

        self.audio_on = True
        self.fullscreen = False

        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.font_title = pygame.font.SysFont("arial", 50, bold=True)

        self.current_frame = 0.0
        self.animation_speed = 0.3 

        if back_frames:
            self.background_frames = back_frames
        else:
            gif_path = 'src/assets/img/menu/menu_if_fundo_animado.gif'
            self.background_frames = self.load_gif_direct(gif_path)

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

    def handle_input(self, event, audio):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE, pygame.K_a, pygame.K_d):
                
                if self.selected_index == 0:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        novo_vol = max(0.0, audio.music_volume - 0.1)
                        audio.set_music_volume(round(novo_vol, 1))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        novo_vol = min(1.0, audio.music_volume + 0.1)
                        audio.set_music_volume(round(novo_vol, 1))

                elif self.selected_index == 1:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        novo_vol = max(0.0, audio.sfx_volume - 0.1)
                        audio.set_sfx_volume(round(novo_vol, 1))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        novo_vol = min(1.0, audio.sfx_volume + 0.1)
                        audio.set_sfx_volume(round(novo_vol, 1))

                elif self.selected_index == 2 and event.key in (pygame.K_RETURN, pygame.K_SPACE):  
                    self.audio_on = not self.audio_on
                    audio.set_mute(not self.audio_on) 
                
                elif self.selected_index == 3 and event.key in (pygame.K_RETURN, pygame.K_SPACE): 
                    self.fullscreen = not self.fullscreen

    def draw(self, audio, surface):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.background_frames):
            self.current_frame = 0.0
            
        frame_index = int(self.current_frame)
        surface.blit(self.background_frames[frame_index], (0, 0))

        music_pct = int(audio.music_volume * 100)
        sfx_pct = int(audio.sfx_volume * 100) 
        
        self.options[0] = f"Música: {music_pct}%"
        self.options[1] = f"Efeitos: {sfx_pct}%"
        self.options[2] = f"Áudio: {'Ativado' if self.audio_on else 'Desativado'}"
        self.options[3] = f"Tela Cheia: {'Ativada' if self.fullscreen else 'Desativada'}"
        self.options[4] = "VOLTAR"

        button_width = 460  
        button_height = 55  
        spacing = 70        
        
        center_x = settings.WIDTH // 3.5  
        start_y = settings.HEIGHT // 2.2 
        
        for i, option in enumerate(self.options):
            center_y = start_y + (i * spacing)
            
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (center_x, center_y)
            
            if i in [0, 1]:
                volume_atual = audio.music_volume if i == 0 else audio.sfx_volume
                
                if i == self.selected_index:
                    color = (168, 255, 0) 
                else:
                    color = (0, 255, 255) 
                    
                pygame.draw.rect(surface, color, button_rect, width=3, border_radius=15)
                
                text_surf = self.font.render(option, True, color if i == self.selected_index else (255, 255, 255))
                text_rect = text_surf.get_rect(midleft=(button_rect.x + 20, button_rect.centery))
                surface.blit(text_surf, text_rect)
                
                num_blocks = 10
                blocks_start_x = button_rect.x + 230 
                blocks_width = button_rect.width - 230 - 15
                block_w = blocks_width / num_blocks
                active_blocks = round(volume_atual * 10)
                
                for b in range(num_blocks):
                    bx = blocks_start_x + (b * block_w)
                    by = button_rect.y + 15
                    bw = block_w - 4
                    bh = button_rect.height - 30
                    
                    b_rect = pygame.Rect(bx, by, bw, bh)
                    if b < active_blocks:
                        pygame.draw.rect(surface, color, b_rect, border_radius=2)
                    else:
                        pygame.draw.rect(surface, (50, 50, 60), b_rect, border_radius=2)
                        
            else:
                if i == self.selected_index:
                    bg_color = (168, 255, 0)
                    text_color = (0, 0, 0)
                    pygame.draw.rect(surface, bg_color, button_rect, border_radius=15)
                    pygame.draw.rect(surface, (100, 180, 0), button_rect, width=3, border_radius=15)
                else:
                    border_color = (0, 255, 255)
                    text_color = (255, 255, 255)
                    pygame.draw.rect(surface, border_color, button_rect, width=3, border_radius=15)

                text_surf = self.font.render(option, True, text_color)
                text_rect = text_surf.get_rect(center=button_rect.center)
                surface.blit(text_surf, text_rect)