import pygame
import math
from gameobject import GameObject

def SquareDistance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

class Bird(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('bird.png')
        self.image_idle = pygame.image.load('bird/idle.png')
        self.image_flap1 = pygame.image.load('bird/flap_up.png')
        self.image_flap2 = pygame.image.load('bird/flap_down.png')
        self.origin_x = self.image_idle.get_width()/2
        self.origin_y = self.image_idle.get_height()
        self.disabled = False
        self.fly_away = False
        self.fly_direction = 1
        if (self.x+self.y % 2)<=1:
            self.fly_direction = -1

        self.flutter_sound = pygame.mixer.Sound('sfx/flutter.wav')


    def update(self, platforms):
        super().update(platforms)
        if self.fly_away:
            self.hspeed += self.fly_direction * (self.vspeed + 1)
            self.vspeed -= 2

    def check_caught(self, coots):
        if SquareDistance(self.pos(), coots.pos())<300:
            if not self.fly_away:
                self.fly_away = True
                self.flutter_sound.play()

            self.fly_direction = math.copysign(1, coots.pos()[0]-self.pos()[0])

    def draw(self, surface, cam):
        #if self.fly_direction > 0:
        #    surface.blit(self.image, (self.x - self.origin_x - cam.x, self.y - self.origin_y - cam.y))
        #else:
        #    surface.blit(pygame.transform.flip(self.image, True, False),
        #                 (self.x - self.origin_x - cam.x, self.y - self.origin_y - cam.y))
        if not self.fly_away:
            if self.fly_direction>0:
                surface.blit(self.image_idle, (self.x - self.origin_x - cam.x, self.y - self.origin_y - cam.y))
            else:
                surface.blit(pygame.transform.flip(self.image_idle, True, False), (self.x - self.origin_x - cam.x, self.y - self.origin_y - cam.y))
        else:
            frame_image = self.image_flap1
            loop_period = 200
            if (pygame.time.get_ticks()%loop_period)<loop_period/2:
                frame_image = self.image_flap2
            if self.fly_direction < 0:
                surface.blit(frame_image, (self.x - self.origin_x - cam.x, self.y - self.origin_y - cam.y))
            else:
                surface.blit(pygame.transform.flip(frame_image, True, False),
                             (self.x - self.origin_x - cam.x, self.y - self.origin_y - cam.y))
