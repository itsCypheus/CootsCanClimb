import pygame
import math
from gameobject import GameObject

def SquareDistance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

class LaserPointer(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('laser_pointer.png')
        self.image_arrow = pygame.image.load('arrow.png')
        self.origin_x = self.image.get_width()/2
        self.origin_y = self.image.get_height()

        self.show_hint = False

    def draw(self, surface, cam):
        super().draw(surface, cam)
        if pygame.time.get_ticks()>9000:
            self.show_hint = True

        if not self.disabled and self.show_hint:
            arrow_offset_y = 110 - math.sin(pygame.time.get_ticks()/300)*5
            arrow_offset_x = self.image_arrow.get_width()/2
            surface.blit(self.image_arrow, (self.x - arrow_offset_x - cam.x, self.y - arrow_offset_y - cam.y))
            # blit on the arrow image

    def update(self, platforms):
        super().update(platforms)

    def check_caught(self, mouse_position):
        if SquareDistance(self.pos(), mouse_position) < 30*30:
            self.disabled = True
            return True
        return False
            # unlock laser pointer
            # display laser pointer unlock toast