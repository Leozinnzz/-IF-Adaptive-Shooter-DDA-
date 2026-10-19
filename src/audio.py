import pygame 

class AudioManager: 
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

        #Efeitos sonoros
        try:
            # Efeitos sonoros
            self.menu_move_sound = pygame.mixer.Sound("src/assets/sounds/option_sound.mp3")
            #self.laser_sound = pygame.mixer.Sound("assets/laser.wav")
            #self.explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
            
            # Volumes
            self.menu_move_sound.set_volume(0.3)
            #self.laser_sound.set_volume(0.3)
            #self.explosion_sound.set_volume(0.5)
        except:
            print("Aviso: Alguns ficheiros de som não foram encontrados.")


    def play_menu_move(self):
        self.menu_move_sound.play()

    def play_music(self, filepath, loop=-1):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(loop)
        except:
            print(f"Erro ao carregar a musica {filepath}")

    def stop_music(self):
        pygame.mixer.music.stop()
