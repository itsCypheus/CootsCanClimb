import pygame
import math
import camera

class Toaster:
    def __init__(self, window_x, window_y):
        self.window_x = window_x
        self.window_y = window_y
        self.toasts = []

        self.toast_sound = pygame.mixer.Sound('sfx/toast.wav')

    def send_toast(self, message, duration=120, size=24):
        self.toast_sound.play()
        self.toasts.append(Toast(self, message, duration, size))

    def draw(self, surface):
        self.toasts = [toast for toast in self.toasts if not toast.disabled]
        if len(self.toasts)==0:
            return None
        self.toasts[0].draw(surface)


class Toast:
    def __init__(self, toaster, message, duration=120, size=24):
        self.window_x = toaster.window_x
        self.window_y = toaster.window_y
        self.display_duration = duration
        self.font = pygame.font.SysFont("Impact", size)
        self.x = toaster.window_x/2
        self.y = toaster.window_y/2
        self.message = message
        self.color = (255, 255, 255)
        self.disabled = False

    def draw(self, surface):
        if not self.disabled:
            self.draw_message(surface)
            self.display_duration -= 1
            if self.display_duration<0:
                self.disabled = True

    def draw_message(self, surface):
        text = self.font.render(self.message, True, self.color)
        text_rect = text.get_rect(center=(self.window_x // 2, self.window_y // 2))
        surface.blit(text, text_rect)