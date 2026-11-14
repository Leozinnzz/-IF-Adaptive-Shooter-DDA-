import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size=(100, 100)):
        super().__init__()
        
        spritesheet = pygame.image.load('src/assets/img/effects/morte_inimigo.png').convert_alpha()
        
        self.frames = []
        num_frames = 6
        
        frame_width = spritesheet.get_width() // num_frames
        frame_height = spritesheet.get_height()
        
        for i in range(num_frames):
            rect = (i * frame_width, 0, frame_width, frame_height)
            frame = spritesheet.subsurface(rect)
            
            frame = pygame.transform.scale(frame, size)
            self.frames.append(frame)
            
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 

    def update(self):
        now = pygame.time.get_ticks()
        
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            
            
            if self.current_frame == len(self.frames):
                self.kill()
            else:
                
                center = self.rect.center
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center