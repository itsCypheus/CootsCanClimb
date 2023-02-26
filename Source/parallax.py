import pygame
import random
import math

class Parallax:
    def __init__(self, window_x):
        random.seed(8)
        self.window_x = window_x
        self.shards = []
        for i in range(50):
            dx = random.randint(0, window_x)
            dy = random.randint(-17000, 2000)
            depth = random.random()*0.5 + 0.45
            width = (2-math.sqrt(depth))*500
            height = (2-math.sqrt(depth))*500
            self.shards.append(PShard(dx,dy,width,height,depth))
        # Sort the list of shards by depth
        self.shards.sort(key=lambda shard: shard.depth)

    def draw(self, surface, cam):
        for shard in self.shards:
            shard.draw(surface, cam)

class PShard:
    def __init__(self, x, y, width, height, depth):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        scalar = math.floor(200 * depth**1.3)
        scalar2 = math.floor(200 * depth*depth)
        self.color = pygame.Color(210 - scalar, 210 - scalar2, 235 - scalar2)
        self.depth = depth

    def draw(self, surface, cam):
        shard_rect = pygame.Rect(self.x - cam.x * self.depth * self.depth, self.y - cam.y*self.depth* self.depth, self.width, self.height)
        pygame.draw.rect(surface, self.color, shard_rect)
