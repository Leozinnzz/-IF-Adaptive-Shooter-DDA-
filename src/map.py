import pygame as py 
import settings as set 

MAP_CONFIGS = {
    1: {
        "name": "Mapa 1: O impacto inicial",
        "enemies": ["bug", "drone_sintaxe", "AND_corrompido", "NOT_corrompido", "OR_corrompido"],
        "background_color": (30, 30, 40), 
        "image_path": "src/assets/maps/mapa1.png",
        "music_path": "src/assets/sounds/map1.mp3"
    }, 
    2: {
        "name": "Mapa 2: A abstração de hardware", 
        "enemies": [], 
        "background_color": (10, 10, 30), 
        #"image_path": "src/assets/maps/map_2_completo.png", 
    }
}

class mapManager:
    def __init__(self, current_map_id = 1):
        self.current_map_id = current_map_id
        self.config = MAP_CONFIGS[current_map_id]

        self.scroll_speed = 0
        self.target_scroll_y = 0  # Ponto onde o mapa deve parar (checkpoint da wave)
        self.boss_triggered = False
        
        self.load_map_image()
        self.reset_scroll()
        self.play_map_music() 

    def load_map_image(self):
        path = self.config.get("image_path")
        try:
            raw_img = py.image.load(path).convert()
            orig_w, orig_h = raw_img.get_size()
            
            scale_factor = set.WIDTH / orig_w
            new_width = set.WIDTH
            new_height = int(orig_h * scale_factor)
            
            if new_height < set.HEIGHT * 3:
                scale_factor = (set.HEIGHT * 3) / orig_h
                new_width = int(orig_w * scale_factor)
                new_height = int(orig_h * scale_factor)

            self.bg_image = py.transform.scale(raw_img, (new_width, new_height))
        except (py.error, FileNotFoundError):
            self.bg_image = py.Surface((set.WIDTH, set.HEIGHT * 3))
            self.bg_image.fill(self.config.get("background_color", (30, 30, 40)))

    def play_map_music(self): 
        music_path = self.config.get("music_path")
        if music_path:
            try:
                py.mixer.music.load(music_path)
                py.mixer.music.set_volume(0.8)
                py.mixer.music.play(-1)
            except (py.error, FileNotFoundError) as e: 
                print(f"Erro ao carregar música {music_path}: {e}")

    def reset_scroll(self):
        # Começa no fundo do mapa
        self.scroll_y = -self.bg_image.get_height() + set.HEIGHT
        self.target_scroll_y = self.scroll_y
        self.scroll_speed = 0
        self.boss_triggered = False

    def resize(self):
        self.load_map_image()
        self.reset_scroll()

    def trigger_scroll_transition(self, current_wave):
        total_height = self.bg_image.get_height() - set.HEIGHT
        
        if current_wave == 2:
            self.target_scroll_y = -total_height * 0.66
        elif current_wave == 3:
            self.target_scroll_y = 0
            
        self.scroll_speed = 1.0  # Velocidade de transição suave

    def get_allowed_enemies(self):
        return self.config["enemies"]

    def update(self):
        if self.scroll_speed > 0:
            if self.scroll_y < self.target_scroll_y:
                self.scroll_y += self.scroll_speed
                # Garante que não passa do alvo
                if self.scroll_y >= self.target_scroll_y:
                    self.scroll_y = self.target_scroll_y
                    self.scroll_speed = 0
                
                    if self.scroll_y == 0:
                        self.boss_triggered = True

    def draw(self, surface):
        bg_color = self.config.get("background_color", (0, 0, 0))
        surface.fill(bg_color if isinstance(bg_color, tuple) else (0, 0, 0))

        # Desenha o mapa na posição atual de scroll
        surface.blit(self.bg_image, (0, int(self.scroll_y)))