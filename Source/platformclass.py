import pygame
import camera

class Platform:
    def __init__(self, x1, y1, x2, y2):
        self.image_left = pygame.image.load('platform_left.png')
        self.image_mid = pygame.image.load('platform_mid.png')
        self.image_right = pygame.image.load('platform_right.png')
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.highlighted = False

    def highlight(self):
        self.image_left = pygame.image.load('platform_left_r.png')
        self.image_mid = pygame.image.load('platform_mid_r.png')
        self.image_right = pygame.image.load('platform_right_r.png')
        self.highlighted = True

    def lowlight(self):
        self.image_left = pygame.image.load('platform_left.png')
        self.image_mid = pygame.image.load('platform_mid.png')
        self.image_right = pygame.image.load('platform_right.png')
        self.highlighted = False

    def draw(self, surface, cam):
        platform_rect = pygame.Rect(self.x1 - cam.x, self.y1 - cam.y, self.x2 - self.x1, self.y2 - self.y1)
        platform_width = platform_rect.width
        root_position = (self.x1 - cam.x, self.y1 - cam.y)
        right_position = (root_position[0] + platform_width - self.image_right.get_width(), root_position[1])
        middle_width = right_position[0] - root_position[0] - self.image_left.get_width() + 1
        surface.blit(self.image_left, root_position)
        surface.blit(pygame.transform.scale(self.image_mid, (middle_width, self.image_mid.get_height())),
                     (root_position[0] + self.image_left.get_width(), root_position[1]))
        surface.blit(self.image_right, right_position)
