class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.hspeed = 0
        self.vspeed = 0
        self.friction = 0.5

        self.max_y = 0

    def apply(self, obj):
        return obj[0] - self.x, obj[1] - self.y

    def update(self):
        self.x += self.hspeed
        self.y += self.vspeed
        self.hspeed *= (1 - self.friction)
        self.vspeed *= (1 - self.friction)

        if self.y>self.max_y: self.y = self.max_y

    def fly_to(self, target_object, rate=0.05):
        target = target_object.pos()
        x = target[0] - int(self.width / 2)
        y = target[1] - int(self.height / 2)
        self.hspeed -= (self.x - x) * rate
        self.vspeed -= (self.y - y) * rate