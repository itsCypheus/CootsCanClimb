import pygame
import math
from gameobject import GameObject


def SquareDistance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


class Battery(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('battery.png')
        self.image_arrow = pygame.image.load('arrow.png')
        self.pickup_sound = pygame.mixer.Sound("sfx/bloop.wav")
        self.pickup_sound.set_volume(0.25)

        self.origin_x = self.image.get_width() / 2
        self.origin_y = self.image.get_height()
        self.disabled = False
        self.show_hint = False

    def draw(self, surface, cam, low_battery=True):
        super().draw(surface, cam)
        self.show_hint = low_battery

        if not self.disabled and self.show_hint:
            arrow_offset_y = 110 - math.sin(pygame.time.get_ticks()/300)*5
            arrow_offset_x = self.image_arrow.get_width()/2
            surface.blit(self.image_arrow, (self.x - arrow_offset_x - cam.x, self.y - arrow_offset_y - cam.y))

    def update(self, platforms):
        if not self.touchingPlatform:
            super().update(platforms)

    def check_caught(self, coots, battery_icon):
        if SquareDistance(self.pos(), coots.pos()) < 300:
            if not self.disabled:
                self.pickup_sound.play()
                battery_icon.recharge()
                self.disabled = True
