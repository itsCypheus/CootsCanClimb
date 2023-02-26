import pygame
import math
import camera


class BatteryIcon:
    def __init__(self, window_x, window_y):
        self.images = []
        self.images.append(pygame.image.load("bat_0.png"))
        self.images.append(pygame.image.load("bat_1.png"))
        self.images.append(pygame.image.load("bat_2.png"))
        self.images.append(pygame.image.load("bat_3.png"))
        self.images.append(pygame.image.load("bat_4.png"))
        self.images.append(pygame.image.load("bat_5.png"))
        self.images.append(pygame.image.load("bat_6.png"))
        self.images.append(pygame.image.load("bat_7.png"))
        self.image_empty = pygame.image.load("bat_8.png")

        self.x = window_x - 11
        self.y = 7

        self.max_charge = 1100
        self.charge = self.max_charge
        self.font = pygame.font.SysFont("Courier", 24)
        self.window_x = window_x
        self.window_y = window_y

    def draw(self, surface):
        if self.charge <= 0:
            self.draw_dead_battery(surface)
            root_position = (self.x - 20, self.y)
            surface.blit(self.image_empty, root_position)
            return None

        number_of_frames = len(self.images)
        frame = (self.max_charge - self.charge) // (self.max_charge // (number_of_frames+3))
        frame = math.floor(frame)
        frame = max(0, frame)
        frame = min(frame, number_of_frames - 1)
        blit_image = self.images[frame]
        if frame+1 >= number_of_frames:
            if (pygame.time.get_ticks()/1000) % 1 < 0.5:
                blit_image = self.image_empty
            else:
                self.draw_low_battery(surface)
        # return without drawing if second mod 2 == 0
        root_position = (self.x-20, self.y)
        surface.blit(blit_image, root_position)

    def draw_low_battery(self, surface):
        text = self.font.render("Low Battery", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.window_x // 2, self.window_y // 2))
        surface.blit(text, text_rect)

    def draw_dead_battery(self, surface):
        text = self.font.render("[Enter] to Restart.", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.window_x // 2, self.window_y // 2))
        surface.blit(text, text_rect)

    def drain(self, amount):
        self.charge -= amount*10
        if self.charge < 0:
            self.charge = 0

    def recharge(self):
        self.charge = self.max_charge

    def has_charge(self):
        return self.charge > 0

    def is_low(self):
        return self.charge/self.max_charge < 0.20