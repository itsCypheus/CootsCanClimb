import random
import math
from bird import Bird
from platformclass import Platform

class ChunkLoader:
    def __init__(self, start_y, window_x):
        self.start_x = 0
        self.start_y = start_y
        self.window_x = window_x
        self.platforms = []

        random.seed(1337)
        self.chunk_count = 0

        bird = Bird(500, 700)
        self.birds = [bird]


    def generate_random_chunk(self):
        choice = random.choice([0, 1, 2])

        if choice == 0:
            self.generate_ladder_chunk()
        elif choice == 1:
            self.generate_stair_chunk()
        elif choice == 2:
            pass
            # self.generate_other_chunk()

    def backtrack(self, distance):
        self.start_y += distance

    def generate_doublestair_chunk(self):
        cached_y = self.start_y
        cached_x = self.start_x
        stair_height = 1000
        self.generate_stair_chunk(stair_height, False, False)
        self.start_y = cached_y
        self.start_x = cached_x
        self.start_x = random.randint(200, self.window_x-200)
        self.generate_stair_chunk(stair_height, True, False)

    # Generate a ladder chunk
    def generate_ladder_chunk(self):
        chunk_platforms = []
        chunk_height = random.randint(10, 20)*200
        platform_gap = 100
        n_layers = math.floor(chunk_height/platform_gap)
        for i in range(n_layers):
            dy = self.start_y - i * platform_gap
            dx = 0

            min_gap = min(self.window_x-400, 300+i*100)
            max_gap = min(self.window_x-400, 500+300+i*100)
            gap_width = random.randint(min_gap, max_gap)

            gap_start_min = 100
            gap_start_max = self.window_x - 100 - gap_width
            gap_x = random.randint(gap_start_min, gap_start_max)

            chunk_platforms.append(Platform(dx, dy, gap_x, dy + 10))
            chunk_platforms.append(Platform(gap_x + gap_width, dy, self.window_x, dy + 10))

        last_platform = chunk_platforms[-1]
        if random.randint(0,1)>0:
            last_platform = chunk_platforms[-2]
        self.start_x = (last_platform.x1+last_platform.x2) * 0.5 # center enter of last platform
        self.start_y = chunk_platforms[-1].y1 # top of last platform

        self.platforms.extend(chunk_platforms)

    def get_random_birds(self, count=20):
        for i in range(count):
            dx = random.randint(100, self.window_x - 100)
            dy = random.randint(-10000, -1000)
            self.birds.append(Bird(dx, dy))
        return self.birds

    # Generate a ladder chunk
    def generate_stair_chunk(self, chunk_height=-1, going_left = False, narrow = False):
        chunk_platforms = []
        if chunk_height<0:
            chunk_height = random.randint(10, 20)*100
        platform_gap = 100
        n_layers = math.floor(chunk_height/platform_gap)
        for i in range(n_layers):
            dy = self.start_y - i * platform_gap
            dx = self.start_x
            if not narrow:
                plat_width = (2 + random.randint(0, 1)+random.randint(0, 1)+random.randint(-1, 1)) * 100
            else:
                plat_width = 150

            if not going_left and dx+plat_width > self.window_x:
                going_left = True

            self.start_x += plat_width

            if going_left:
                if len(chunk_platforms)>0:
                    last_platform = chunk_platforms[-1]
                    last_platform_start = last_platform.x1
                    dx = last_platform_start - plat_width

            if going_left and dx < 0:
                going_left = False
                last_platform = chunk_platforms[-1]
                last_platform_end = last_platform.x2
                dx = last_platform_end

            chunk_platforms.append(Platform(dx, dy, dx+plat_width, dy + 10))

        last_platform = chunk_platforms[-1]
        self.start_x = (last_platform.x1+last_platform.x2) * 0.5 # center enter of last platform
        self.start_y = last_platform.y1  # top of last platform
        self.platforms.extend(chunk_platforms)

    def generate_flock_chunk(self, n_layers=2):
        chunk_platforms = []
        for i in range(n_layers):
            dy = self.start_y
            dx = 0
            for k in range(random.randint(0,10)):
                self.birds.append(Bird(random.randint(100, self.window_x-100), dy-10))
            plat_width = self.window_x
            chunk_platforms.append(Platform(dx, dy, dx + plat_width, dy + 10))
            if i+1<n_layers:
                for j in range(5):
                    if random.randint(0, 2) > 1:
                        dx = self.window_x/6 * (j+1)
                        dy = self.start_y - 150
                        plat_width = self.window_x/12
                        if random.randint(0, 2) > 1:
                            self.birds.append(Bird(dx+plat_width*0.5+random.randint(-20, 20), dy-10))
                        chunk_platforms.append(Platform(dx, dy, dx + plat_width, dy + 10))

            self.start_y -= 300

        last_platform = chunk_platforms[-1]
        self.start_x = (last_platform.x1+last_platform.x2) * 0.5 # center enter of last platform
        self.start_y = last_platform.y1  # top of last platform
        self.platforms.extend(chunk_platforms)

    def get_platforms(self):
        return self.platforms
