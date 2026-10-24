import settings as set
import pygame as py 

MAP_CONFIGS = {
    1: {
        "name": "Mapa 1: O impacto inicial",
        "enemies": ["bug", "drone_sintaxe", "AND_corrompido", "NOT_corrompido", "OR_corrompido"],
        "background_color": (30, 30, 40), 
        
        "image_paths": [
            "src/assets/maps/map_1.png",
            "src/assets/maps/map_1(2).png",
            "src/assets/maps/map_1(3).png"
        ],

        "music_path": "src/assets/sounds/map1.mp3"
    }, 
    2: {
        "name": "Mapa 2: A abstração de hardware", 
        "enemies": [], 
        "background_color": (10, 10, 30), 
        "image_paths": [], 
        #"music_path": "src/assets/sounds/mapa_2.mp3" Mapa 2 musica
    }
}

class mapManager:
    def __init__(self, current_map_id = 1):
        self.current_map_id = current_map_id
        self.config = MAP_CONFIGS[current_map_id]

        self.bg_images = []
        self.scroll_speed = 0.5
        
        self.load_map_images()
        self.reset_scroll()
        self.play_map_music() 

    def load_map_images(self):
        self.bg_images = []
        paths = self.config.get("image_paths", [])

        for path in paths:
            try:
                img = py.image.load(path).convert()
                img = py.transform.scale(img, (set.WIDTH, set.HEIGHT))
                self.bg_images.append(img)
            except (py.error, FileNotFoundError) as e:
                print(f"Erro ao carregar {path}: {e}") 

        if not self.bg_images:
            fallback = py.Surface((set.WIDTH, set.HEIGHT))
            color = self.config.get("background_color", (30, 30, 40))
            if not isinstance(color, tuple):
                color = (30, 30, 40)
            fallback.fill(color)
            self.bg_images = [fallback, fallback, fallback]

    def play_map_music(self): 
        music_path = self.config.get("music_path")
        if music_path:
            try:
                py.mixer.music.load(music_path)
                py.mixer.music.set_volume(0.8)
                py.mixer.music.play(-1)
            except (py.error, FileNotFoundError) as e: 
                print(f"Error ao carreg8ar musica {music_path}: {e}")


    def reset_scroll(self):
        h = self.bg_images[0].get_height() if self.bg_images else set.HEIGHT
        
        self.y1 = 0
        self.y2 = -h
        self.y3 = -h * 2

        self.scroll_speed = 0
        self.boss_triggered = False
        self.wave_2_stopped = False

    def set_map(self, map_id):
        if map_id in MAP_CONFIGS:
            self.current_map_id = map_id
            self.config = MAP_CONFIGS[map_id]
            self.load_map_images()
            self.reset_scroll()
            self.play_music()

    def resize(self):
        self.load_map_images()
        self.reset_scroll()

    def trigger_scroll_transition(self):
        self.scroll_speed = 0.5

    def check_stop_wave_2(self):
        if self.scroll_speed > 0 and not self.wave_2_stopped:
            h = self.bg_images[0].get_height()
            if self.y2 >= 0 and self.y2 < self.scroll_speed + 2:
                if not self.boss_triggered and self.y3 < 0:
                    self.y2 = 0
                    self.y1 = h
                    self.scroll_speed = 0 
                    self.wave_2_stopped = True

    def get_allowed_enemies(self):
        return self.config["enemies"]

    def update(self):
        if len(self.bg_images) >= 3 and self.scroll_speed > 0:
            self.y1 += self.scroll_speed
            self.y2 += self.scroll_speed
            self.y3 += self.scroll_speed

            self.check_stop_wave_2()
        
            if self.y3 >= 0:
                self.y3 = 0
                h = self.bg_images[0].get_height()
                self.y2 = h       
                self.y1 = h * 2   
                self.scroll_speed = 0
                self.boss_triggered = True  #Ativar a flag do boss

    
    def draw(self, surface):
        bg_color = self.config.get("background_color", (0, 0, 0))
        if isinstance(bg_color, tuple):
            surface.fill(bg_color)
        else:
            surface.fill((0, 0, 0))

        if len(self.bg_images) >= 3:
            # Desenha os 3 mapas em sequência exata (Mapa 1 -> Mapa 2 -> Mapa 3)
            surface.blit(self.bg_images[0], (0, int(self.y1)))
            surface.blit(self.bg_images[1], (0, int(self.y2)))
            surface.blit(self.bg_images[2], (0, int(self.y3)))