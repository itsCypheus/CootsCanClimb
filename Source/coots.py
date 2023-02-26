import pygame
import math
import random
from gameobject import GameObject

def SquareDistance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

class Coots(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('cat.png')
        self.image_idle_body = pygame.image.load('coots/idle_body.png')
        self.image_idle_head = pygame.image.load('coots/idle_head.png')
        self.origin_x = self.image.get_width()/2
        self.origin_y = self.image.get_height()

        self.jump_sound = pygame.mixer.Sound('sfx/jump.wav')
        self.land_sound = pygame.mixer.Sound('sfx/land.wav')
        self.wrap_sound = pygame.mixer.Sound('sfx/teleport.wav')
        self.victory_sound = pygame.mixer.Sound('sfx/victory.wav')
        self.victory_sound.set_volume(0.4)
        self.trill_sound = pygame.mixer.Sound('sfx/trill.wav')
        self.trill_sound.set_volume(0.25)

        self.dropping = False
        self.input_x = 0
        self.input_y = 0

        self.eager = False
        self.facing_right = True
        self.unlimited_battery = False
        self.flying = False

    def has_unlimited_battery(self):
        return self.unlimited_battery

    def run(self, dx):
        if self.touchingPlatform:
            self.hspeed += dx * 6
        else:
            self.hspeed += dx * 1

    def lift(self, dy):
        self.vspeed += dy * 0.25

    def jump(self):
        if self.touchingPlatform:
            print(self.jump_sound.get_num_channels() > 0)
            self.jump_sound.play(0,250,250)
            self.jump_sound.set_volume(0.25)
            print(self.jump_sound.get_num_channels() > 0)
            self.flying = True
            self.vspeed -= 30

    def wrap_edges(self, window_width):
        if self.x < 0:
            self.move(window_width, 0)
            self.wrap_sound.play()
        if self.x > window_width:
            self.move(-window_width, 0)
            self.wrap_sound.play()

    def find_poi(self, birds, laser_pos):
        poi = laser_pos
        was_eager = self.eager

        self.eager = False
        self.agape = False

        birds = [bird for bird in birds if not bird.disabled]

        if len(birds)>0:
            bird_positions = [bird.pos() for bird in birds]
            bird_sqdistances = [SquareDistance(self.pos(), bird) for bird in bird_positions]
            if min(bird_sqdistances)<300*300:
                min_index = bird_sqdistances.index(min(bird_sqdistances))
                closest_bird = bird_positions[min_index]

                if SquareDistance(self.pos(), closest_bird)*2 < SquareDistance(self.pos(), laser_pos):
                    poi = closest_bird
                    self.eager = True
                    if not was_eager and random.random()>0.5:
                        self.trill_sound.play()

        return poi

    def hit_platform(self):
        self.land_sound.play()

    def override_input(self, laser_pos, birds):
        poi = self.find_poi(birds, laser_pos)

        if self.touchingHighlighted:
            if not self.unlimited_battery:
                self.trill_sound.stop()
                self.victory_sound.play()
                self.unlimited_battery = True

        if laser_pos[0]>0:
            print(laser_pos)

        # Bot logic - override input for laser controls
        self.input_x = 0
        self.input_y = 0
        dist = math.sqrt(SquareDistance(self.pos(), poi))
        if 30 < abs(poi[0] - self.x) < 800 or self.eager:
            self.input_x = min(1, max(-1, poi[0] - self.x))
        if dist < 300:
            if poi[1] - self.y < -100:
                self.input_y = -1

        self.dropping = ((dist < 80 or self.eager) and poi[1] > self.y + 20)

        if self.input_x > 0 and not self.facing_right:
            self.facing_right = True
        if self.input_x < 0 and self.facing_right:
            self.facing_right = False

    def act_on_input(self, window_x):
        if (self.input_y < 0):
            self.jump()
        self.run(self.input_x)
        self.lift(self.input_y)
        self.wrap_edges(window_x)

    def draw(self, surface, cam):
        #super().draw(surface, cam)

        # Draw idle stuff.
        body_x = self.x - self.image_idle_body.get_width()/2 - cam.x
        draw_y = self.y - cam.y
        body_position = (body_x, draw_y + 5 - self.image_idle_body.get_height())
        head_position = (body_x + self.input_x*6, draw_y-60 + self.input_y*12)

        if self.facing_right:
            surface.blit(self.image_idle_body, body_position)
        else:
            surface.blit(pygame.transform.flip(self.image_idle_body, True, False), body_position)

        if self.facing_right:
            surface.blit(self.image_idle_head, head_position)
        else:
            surface.blit(pygame.transform.flip(self.image_idle_head, True, False), head_position)


