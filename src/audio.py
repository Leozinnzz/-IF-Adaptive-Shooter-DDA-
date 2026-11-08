import pygame 

class AudioManager: 
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

        pygame.mixer.set_num_channels(32)
        
        self.sounds = {}

        #Volume padrao
        self.music_volume = 0.8  
        self.sfx_volume = 0.6    
        self.current_track = None

        self.muted = False

    def play_sound(self, path, volume=0.4):
        if path not in self.sounds:
            try:
                self.sounds[path] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Aviso: Não foi possível carregar o som {path} - {e}")
                return

        sound_effect = self.sounds[path]

        final_vol = volume * self.sfx_volume 
        sound_effect.set_volume(max(0.0, min(1.0, final_vol)))
        sound_effect.play()

    def play_menu_move(self):
        self.play_sound("src/assets/sounds/option_sound.mp3", 0.3)


    def set_mute(self, is_muted):
        self.muted = is_muted
        if self.muted:
            pygame.mixer.music.set_volume(0)  
        else:
            pygame.mixer.music.set_volume(self.music_volume)

    def play_music(self, filepath, loop=-1):
        try:
            if self.current_track != filepath:
                self.current_track = filepath
                pygame.mixer.music.load(filepath)
                
                vol = 0 if self.muted else self.music_volume
                pygame.mixer.music.set_volume(vol)
                pygame.mixer.music.play(loop)
        except Exception as e:
            pass


    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_track = None


    def start_slowmo(self): 
        if not self.muted: 
            pygame.mixer.music.set_volume(0.1)
            self.play_sound("src/assets/sounds/slow_clock.mp3", 1.0)

    def stop_slowmo(self):
        if not self.muted: 
            pygame.mixer.music.set_volume(self.music_volume)
            self.set_sfx_volume(self.sfx_volume)

    def set_music_volume(self, volume): 
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
