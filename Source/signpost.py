import pygame
import math
from gameobject import GameObject

class Signpost(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('sign.png')
        self.origin_x = self.image.get_width()/2
        self.origin_y = self.image.get_height()
        self.disabled = False


    def update(self, platforms):
        if not self.touchingPlatform:
            super().update(platforms)
