# importing libraries
import pygame
from coots import Coots
from camera import Camera
from chunks import ChunkLoader
from battery import Battery
from bgmcontroller import BGMController
from laser_pointer import LaserPointer
from batteryicon import BatteryIcon
from signpost import Signpost
from toast import Toaster
from platformclass import Platform
from parallax import Parallax
from scorekeeper import ScoreKeeper
from mutehelper import MuteHelper
import math


# define a function to restart the program
global coots
global battery_icon
global batteries
global platforms
global birds
global score_keeper
global laser_pointer
global has_laser_pointer
global bgmcontroller
global battery_sign
global unlimited_battery_unlocked

# Initialising pygame
pygame.init()


def initialize_room():
    global coots
    global battery_icon
    global batteries
    global platforms
    global birds
    global score_keeper
    global laser_pointer
    global has_laser_pointer
    global bgmcontroller
    global battery_sign
    global unlimited_battery_unlocked

    unlimited_battery_unlocked = False

    bgmcontroller.reset_soundfront()

    has_laser_pointer = False

    coots = Coots(200, 500)
    battery_icon = BatteryIcon(window_x, window_y)
    battery_sign = Signpost(-100, 100)

    laser_pointer = LaserPointer(600, 500)

    bat = Battery(1950, 100)
    batteries = [bat]
    batteries.append(Battery(2050, 100))
    batteries.append(Battery(2150, 100))
    batteries.append(Battery(2250, 100))
    batteries.append(Battery(2350, 100))
    batteries.append(Battery(70, -946))
    batteries.append(Battery(782, 28))
    batteries.append(Battery(1800, -2000))
    batteries.append(Battery(1084, -6552))
    batteries.append(Battery(86, -8389))
    batteries.append(Battery(1132, -9459))
    batteries.append(Battery(533, -11771))
    batteries.append(Battery(485, -5760))
    batteries.append(Battery(1506, -7291))
    batteries.append(Battery(2381, -8421))
    batteries.append(Battery(123, -9174))
    batteries.append(Battery(127, -10180))
    batteries.append(Battery(2295, -10074))
    batteries.append(Battery(1549, -12670))
    batteries.append(Battery(1088, -12843))
    batteries.append(Battery(1245, -13023))
    batteries.append(Battery(2435, -15393))
    batteries.append(Battery(498, -16481))
    batteries.append(Battery(1191, -1360))
    # batteries.append(Battery(2466, -6050))
    batteries.append(Battery(577, -1446))
    batteries.append(Battery(894, -1948))
    batteries.append(Battery(1134, -4850))
    batteries.append(Battery(1134, -4956))
    batteries.append(Battery(423, -365))
    batteries.append(Battery(2187, -5572))
    batteries.append(Battery(440, -7154))
    batteries.append(Battery(1333, -1565))

    platforms = []
    platforms.append(Platform(-200, 750, 2700, 850))
    platforms.append(Platform(600, 650, 1200, 660))
    platforms.append(Platform(500, 550, 700, 560))
    platforms.append(Platform(700, 450, 900, 460))
    platforms.append(Platform(1300, 450, 1600, 460))
    platforms.append(Platform(300, 250, 500, 260))
    platforms.append(Platform(500, 350, 700, 360))
    platforms.append(Platform(700, 150, 900, 160))
    platforms.append(Platform(-200, 150, 200, 160))
    platforms.append(Platform(world_x - 600, 150, world_x + 200, 160))
    platforms.append(Platform(1200, 150, 1500, 160))

    chunkLoader = ChunkLoader(0, world_x)
    chunkLoader.generate_doublestair_chunk()
    chunkLoader.generate_ladder_chunk()
    chunkLoader.generate_flock_chunk()
    chunkLoader.generate_stair_chunk()
    chunkLoader.backtrack(500)
    chunkLoader.generate_doublestair_chunk()
    chunkLoader.generate_ladder_chunk()
    chunkLoader.backtrack(500)
    chunkLoader.generate_stair_chunk()
    chunkLoader.generate_doublestair_chunk()
    chunkLoader.generate_doublestair_chunk()
    chunkLoader.generate_flock_chunk()
    chunkLoader.generate_doublestair_chunk()
    chunkLoader.generate_ladder_chunk()
    chunkLoader.generate_stair_chunk()
    chunkLoader.generate_flock_chunk()

    birds = chunkLoader.get_random_birds()
    platforms.extend(chunkLoader.get_platforms())
    score_keeper = ScoreKeeper()

    y_values = [plat.y1 for plat in platforms]
    highest_platform_index = y_values.index(min(y_values))
    platforms[highest_platform_index].highlight()



game_speed = 60

# Window size
world_x = 2500

# get the dimensions of the screen

# create a Pygame window and set it to full screen
#screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)


# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)

laser_image = pygame.image.load('laser.png')
laser_sound = pygame.mixer.Sound('sfx/laser.wav')
laser_sound.set_volume(0.5)

# Initialise game window
pygame.display.set_caption('Coots Can Climb')

parallax = Parallax(1440)

display_height = pygame.display.Info().current_h
if display_height>1200: full_screen = False

full_screen = True
if full_screen:
    window_x = pygame.display.Info().current_w
    window_y = pygame.display.Info().current_h
    game_window = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN)
else:
    window_x = 1440
    window_y = 810
    game_window = pygame.display.set_mode((window_x, window_y), 0)

bgmcontroller = BGMController(world_x)
mutehelper = MuteHelper()

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
camera = Camera(window_x, window_y)

toaster = Toaster(window_x, window_y)
toaster.send_toast("Casey and Matt present...", 240)
toaster.send_toast("", 60)
toaster.send_toast("Coots Can Climb", 240, 40)

initialize_room()


def detect_exit_or_volume_change():
    global full_screen
    global music_volume
    global game_window
    global window_x
    global window_y
    # Handle escaping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        quit()
    if keys[pygame.K_RETURN]:
        initialize_room()
    # Handle music volume control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pass
                bgmcontroller.cycle_volume()
            if event.key == pygame.K_BACKSPACE:
                full_screen = not full_screen
                if full_screen:
                    window_x = pygame.display.Info().current_w
                    window_y = pygame.display.Info().current_h
                    game_window = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN)
                else:
                    window_x = 1440
                    window_y = 810
                    game_window = pygame.display.set_mode((window_x, window_y), 0)


def lerp_color(color1, color2, t):
    t = t * t * t
    r = int(color1.r + (color2.r - color1.r) * t)
    g = int(color1.g + (color2.g - color1.g) * t)
    b = int(color1.b + (color2.b - color1.b) * t)
    return pygame.Color(r, g, b)


# Main Function
while True:

    # See if we should close or set volume
    detect_exit_or_volume_change()

    bottom_color = pygame.Color(0, 0, 0)
    top_color = pygame.Color(150, 220, 255)

    vertical_progress = float(coots.pos()[1]) / -17000

    if vertical_progress < 0:
        vertical_progress = 0

    if vertical_progress > 1:
        vertical_progress = 1

    lerped_color = lerp_color(bottom_color, top_color, vertical_progress)

    # Fill screen with black
    game_window.fill(lerped_color)

    parallax.draw(game_window, camera)

    border_rect_left_fill = pygame.Rect(-1000 - camera.x, -20000 - camera.y, 1000, 25000)
    border_rect_right_fill = pygame.Rect(world_x - camera.x, -20000 - camera.y, 1000, 25000)
    border_rect_left = pygame.Rect(-1 - camera.x, -20000 - camera.y, 1, 25000)
    border_rect_right = pygame.Rect(world_x - camera.x, -20000 - camera.y, 1, 25000)

    pygame.draw.rect(game_window, black, border_rect_left_fill)
    pygame.draw.rect(game_window, black, border_rect_right_fill)
    pygame.draw.rect(game_window, pygame.Color(255, 190, 90), border_rect_left)
    pygame.draw.rect(game_window, pygame.Color(90, 190, 255), border_rect_right)

    bgmcontroller.draw(game_window, camera)
    # Draw platforms
    for platform in platforms:
        platform.draw(game_window, camera)

    # Update camera position
    # camera.y -= 1

    # Set the laser position and draw it (if on)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0] + camera.x, mouse_pos[1] + camera.y)
    if not has_laser_pointer:
        has_laser_pointer = laser_pointer.check_caught(mouse_pos)
        if (has_laser_pointer):
            toaster.send_toast("Click to point the laser.", 240)
    lmb, _, _ = pygame.mouse.get_pressed(3)
    if has_laser_pointer and lmb and (battery_icon.has_charge() or coots.has_unlimited_battery()):
        laser_sound.play(0)
        laser_x = mouse_pos[0] - 4
        laser_y = mouse_pos[1] - 4
        game_window.blit(laser_image, (laser_x - camera.x, laser_y - camera.y))
        camera.fly_to(coots, 0.01)
        battery_icon.drain(0.1)
    else:
        laser_sound.stop()
        laser_x = -100000
        laser_y = 10000
        camera.fly_to(coots)
    laser_pos = (laser_x, laser_y)

    coots.update(platforms)
    score_keeper.update(coots.pos()[1], unlimited_battery_unlocked)
    laser_pointer.update(platforms)  # just to pick up at the start
    for bird in birds:
        bird.update(platforms)
        bird.check_caught(coots)
    for battery in batteries:
        battery.update(platforms)
        battery.check_caught(coots, battery_icon)
    bgmcontroller.update(coots.pos()[1])
    battery_sign.update(platforms)

    coots.override_input(laser_pos, birds)
    coots.act_on_input(world_x)

    #platforms[1].highlight()

    coots.draw(game_window, camera)
    laser_pointer.draw(game_window, camera)
    for bird in birds:
        bird.draw(game_window, camera)
    for battery in batteries:
        low_battery = battery_icon.is_low()
        battery.draw(game_window, camera, low_battery)
    battery_sign.draw(game_window, camera)

    if not coots.has_unlimited_battery():
        battery_icon.draw(game_window)
    else:
        if not unlimited_battery_unlocked:
            unlimited_battery_unlocked = True
            toaster.send_toast("Unlimited Battery Unlocked")
    toaster.draw(game_window)

    mutehelper.draw(game_window)

    camera.update()

    # displaying score continuously
    score_keeper.draw(game_window)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(game_speed)
