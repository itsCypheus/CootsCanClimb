import pygame
import math

class MuteHelper:
    def __init__(self):
        self.font = 'impact'
        self.size = 20
        self.score = 0
        self.color = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)

    def draw(self, surface):

        message_text = "Press [M] to mute music."
        if pygame.time.get_ticks()>10000:
            message_text = "[Backspace] to toggle full-screen."
        if pygame.time.get_ticks()>20000:
            message_text = ""

        height = surface.get_height()
        width = surface.get_width()

        message_font = pygame.font.SysFont(self.font, self.size)
        message_surface = message_font.render(message_text, True, self.color)
        shadow_surface = message_font.render(message_text, True, self.black)
        message_rect = message_surface.get_rect()
        shadow_rect = shadow_surface.get_rect()
        message_rect[0] = width/2 - message_rect[2]*0.5
        message_rect[1] = height - message_rect[3] - 10
        shadow_rect[0] = message_rect[0] + 2
        shadow_rect[1] = message_rect[1] + 2
        surface.blit(shadow_surface, shadow_rect)
        surface.blit(message_surface, message_rect)
