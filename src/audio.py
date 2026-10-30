import pygame 

class AudioManager: 
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

        pygame.mixer.set_num_channels(32)
        
        self.sounds = {}

    def play_sound(self, path, volume=0.5):
        """Função genérica: Carrega o som (se não existir) e toca-o."""
        if path not in self.sounds:
            try:
                self.sounds[path] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Aviso: Não foi possível carregar o som {path} - {e}")
                return

        sound_effect = self.sounds[path]
        sound_effect.set_volume(volume)
        sound_effect.play()

    def play_menu_move(self):
        self.play_sound("src/assets/sounds/option_sound.mp3", 0.3)

    def play_music(self, filepath, loop=-1):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(loop)
        except:
            print(f"Erro ao carregar a musica {filepath}")

    def stop_music(self):
        pygame.mixer.music.stop()