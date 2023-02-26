import pygame
import math

class ScoreKeeper:
    def __init__(self):
        self.font = 'impact'
        self.size = 20
        self.score = 0
        self.color = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)
        self.ticks = 0
        self.current_height = 0
        self.time = "0:00"

    def update(self, coots_vertical, unlimited_battery):
        score = math.floor((1000 - coots_vertical)/100)
        self.current_height = score
        if self.score < score:
            self.score = score

        if not unlimited_battery:
            self.ticks += 1

        seconds = self.ticks / 60
        minutes = int(seconds) // 60
        milliseconds = int((seconds % 1) * 100)
        seconds = int(seconds) % 60
        self.time = f"{minutes:02}:{seconds:02}.{milliseconds:02}"

    def draw(self, surface):
        score_font = pygame.font.SysFont(self.font, self.size)
        score_text = 'Record height: ' + str(self.score) + 'ft'
        score_text += "  "+'(Currently at '+str(self.current_height)+'ft)'
        score_text += '  '+'('+self.time+')'
        score_surface = score_font.render(score_text, True, self.color)
        score_surface2 = score_font.render(score_text, True, self.black)
        score_rect = score_surface.get_rect()
        score_rect2 = score_surface2.get_rect()
        score_rect[0] += 5
        score_rect[1] += 5
        score_rect2[0] += 6
        score_rect2[1] += 6
        surface.blit(score_surface2, score_rect2)
        surface.blit(score_surface, score_rect)
