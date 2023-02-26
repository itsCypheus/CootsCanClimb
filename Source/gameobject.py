import pygame
import camera



class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface([16, 16])
        self.image.fill(pygame.Color(255, 255, 255))
        self.origin_x = self.image.get_width()/2
        self.origin_y = self.image.get_height()/2
        self.hspeed = 0;
        self.vspeed = 0;

        self.gravity = 2
        self.friction = 0.1

        self.touchingPlatform = False
        self.touchingHighlighted = False
        self.dropping = False

        self.disabled = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, platforms):
        if self.disabled:
            pass

        # Apply momentum
        self.move(self.hspeed, self.vspeed)

        self.check_grounded(platforms)

        # Apply Gravity
        if not self.touchingPlatform:
            self.vspeed += self.gravity

        # Apply Friction
        self.hspeed *= (1 - self.friction)
        self.vspeed *= (1 - self.friction)

    def hit_platform(self):
        pass

    def check_grounded(self, platforms):
        self.touchingPlatform = False
        self.touchingHighlighted = False
        for platform in platforms:
            x1 = platform.x1
            x2 = platform.x2
            y1 = platform.y1
            y2 = platform.y2
            platform_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1 + 15)
            if platform_rect.collidepoint(self.x - 5, self.y) or platform_rect.collidepoint(self.x + 5, self.y):
                if not self.dropping or platform_rect.collidepoint(self.x, self.y + 25):
                    lost_vspeed = self.vspeed
                    if (lost_vspeed>5):
                        self.hit_platform()
                    self.vspeed = 0
                    self.hspeed *= 0.25
                    self.touchingPlatform = True
                    if platform.highlighted:
                        self.touchingHighlighted = True
                    while platform_rect.collidepoint(self.x - 5, self.y) or platform_rect.collidepoint(self.x + 5, self.y):
                        self.move(0, -1)

    def pos(self):
        return self.x, self.y

    def draw(self, surface, cam):
        if not self.disabled:
            surface.blit(self.image, (self.x-self.origin_x-cam.x, self.y-self.origin_y-cam.y))
