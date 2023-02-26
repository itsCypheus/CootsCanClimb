import pygame

class BGMController:
    def __init__(self, window_x):
        self.music_volume = 0.66
        self.window_x = window_x
        # Load background music

        pygame.mixer.music.load("sr.ogg")
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.channel2 = pygame.mixer.Channel(1)
        self.channel2.play(pygame.mixer.Sound("loop.ogg"), loops=-1)

        pygame.mixer.music.set_volume(0.0)
        self.channel2.set_volume(1.0)

        self.reset_soundfront()

        self.crossfade_width = 1000


    def reset_soundfront(self):
        self.soundfront = 0
        pygame.mixer.music.rewind()

    def update(self, coots_vertical):
        if coots_vertical<0:
            self.soundfront -= 1.6
        else:
            pass #pygame.mixer.music.rewind()
        if coots_vertical < self.soundfront - self.crossfade_width:
            pygame.mixer.music.set_volume(self.music_volume)
            self.channel2.set_volume(0.0)
        elif coots_vertical > self.soundfront:
            pygame.mixer.music.set_volume(0.0)
            self.channel2.set_volume(self.music_volume)
        else:
            volume = abs((coots_vertical - self.soundfront) / self.crossfade_width)
            pygame.mixer.music.set_volume(self.music_volume * volume)
            self.channel2.set_volume(self.music_volume * (1 - volume))

    def cycle_volume(self):
        self.music_volume += 0.33
        if self.music_volume > 0.66:
            self.music_volume = 0
        pygame.mixer.music.set_volume(self.music_volume)

    def draw(self, surface, cam):
        start = -20000
        height = self.soundfront - start
        soundfront_rect = pygame.Rect(-10002 - cam.x, start - cam.y, 10000, height)
        soundfront_rect2 = pygame.Rect(self.window_x + 2 - cam.x, start - cam.y, 10000, height)
        pygame.draw.rect(surface, pygame.Color(40, 30, 30), soundfront_rect)
        pygame.draw.rect(surface, pygame.Color(40, 30, 30), soundfront_rect2)

