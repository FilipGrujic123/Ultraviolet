import pygame
from time import time

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Ultraviolet')
pygame.display.set_icon(pygame.image.load('img/icon.png'))

BACKGROUND_IMG = pygame.transform.scale(pygame.image.load('img/background.png').convert(), (640, 640))

# Portals
PORTAL_ENTER_IMG = pygame.transform.scale(pygame.image.load('img/portal_enter.png'), (80, 80))
PORTAL_EXIT_IMG = pygame.transform.scale(pygame.image.load('img/portal_exit.png'), (80, 80))

portal_exit = pygame.Rect(0, 480, 80, 80)
portal_enter = pygame.Rect(80, 160, 80, 80)

# Block stuff
GRASS_IMG = pygame.transform.scale(pygame.image.load('img/grass.png').convert(), (80, 80))
DIRT_IMG = pygame.transform.scale(pygame.image.load('img/dirt.png').convert(), (80, 80))

current_level = 0
levels = [
    [],
    [],
    [([0, 560], GRASS_IMG), ([80, 560], GRASS_IMG), ([160, 560], GRASS_IMG), ([240, 560], GRASS_IMG), ([320, 560], GRASS_IMG), ([400, 560], GRASS_IMG), ([480, 560], GRASS_IMG), ([560, 560], DIRT_IMG), ([560, 480], GRASS_IMG), ([400, 400], GRASS_IMG), ([320, 400], GRASS_IMG), ([240, 400], GRASS_IMG), ([80, 240], GRASS_IMG), ([160, 320], GRASS_IMG)],
    [],
]
levels_player_positions = [
    [100000, -100000],
    [10000, -100000],
    [0, 480]
]
levels_portal_positions = [
    [(10000, 10000), (20000, 20000)],
    [(10000, 10000), (20000, 20000)],
    [(0, 480), (80, 160)]
]
levels_text_positions = [
    [("ULTRAVIOLET", 48, [150, 200]), ("Press E to play", 32, [210, 400])],
    [("You died!", 48, [180, 200]), ("Press E to play again", 32, [160, 400])],
    [("Don't be on the sun for too long!", 16, [300, 30])]
]

current_texts = []

blocks = levels[0]

# Player stuff
PLAYER_STANDING = pygame.transform.scale(pygame.image.load('img/player_standing.png'), (80, 80))
PLAYER_RUNNING_1 = pygame.transform.scale(pygame.image.load('img/player_running_1.png'), (80, 80))
PLAYER_RUNNING_2 = pygame.transform.scale(pygame.image.load('img/player_running_2.png'), (80, 80))
player_coords = [0, 480]
current_sprite = PLAYER_STANDING
TIME_BETWEEN_MOVES = 1/20
SPRITE_UPDATE = 1/5
time_since_sprite_update = 0
time_since_move = 0
grounded = False
velocity_g = 0
sun_detector = pygame.Rect(player_coords[0], player_coords[1] - 1000, 40, 1000)
sun_meter = 0
sun_fillup_speed = 1/4
sun_drain_speed = 1/5

def check_if_on_sun():
    global blocks
    global sun_detector
    for block in blocks:
        if sun_detector.colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
            return False
    return True

def change_level(i):
    global blocks
    global levels
    global current_level
    global levels_player_positions
    global levels_portal_positions
    global levels_text_positions
    global velocity_g, grounded
    global player_coords
    global portal_enter, portal_exit
    global current_texts
    global sun_meter
    current_level = i
    blocks = levels[current_level]
    current_texts = levels_text_positions[current_level]
    velocity_g = 0
    grounded = True
    player_coords = levels_player_positions[current_level]
    portal_exit = levels_portal_positions[current_level][0]
    portal_enter = levels_portal_positions[current_level][1]
    sun_meter = 0

change_level(0)

def die():
    change_level(1)

old_time = time()
while True:
    dt = time() - old_time
    old_time = time()

    time_since_move += dt
    time_since_sprite_update += dt

    [[pygame.quit(), quit()] for event in pygame.event.get() if event.type == pygame.QUIT]

    keys = pygame.key.get_pressed()

    # Start and restart the game
    if keys[pygame.K_e] and current_level in [0, 1]:
        change_level(2)

    if keys[pygame.K_RIGHT]:
        change_level(current_level + 1)
    if keys[pygame.K_LEFT]:
        change_level(current_level - 1)

    # Updating moves
    if time_since_move >= TIME_BETWEEN_MOVES:
        time_since_move = 0

        if keys[pygame.K_d]:
            can_go_right = True
            for block in blocks:
                if pygame.Rect(player_coords[0] + 10, player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    can_go_right = False
            if player_coords[0] >= 560:
                can_go_right = False
            if can_go_right:
                player_coords[0] += 10
        elif keys[pygame.K_a]:
            can_go_left = True
            for block in blocks:
                if pygame.Rect(player_coords[0] - 10, player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    can_go_left = False
            if player_coords[0] <= 0:
                can_go_left = False
            if can_go_left:
                player_coords[0] -= 10
        if grounded:
            velocity_g = 0
            was_grounded = False
            for block in blocks:
                if pygame.Rect(player_coords[0], player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    player_coords[1] = block[0][1] - 80
                    was_grounded = True

            if not was_grounded:
                grounded = False
            else:
                grounded = True
        if not grounded:
            velocity_g += 10
            player_coords[1] += velocity_g
            for block in blocks:
                if pygame.Rect(player_coords[0], player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    if block[0][1] > player_coords[1]:
                        player_coords[1] = block[0][1] - 80
                        grounded = True
                    elif block[0][1] < player_coords[1]:
                        player_coords[1] = block[0][1] + 80
                        velocity_g = 0

    sun_detector.x = player_coords[0] + 20
    sun_detector.y = player_coords[1] - 1000
    # Updating sprites
    if time_since_sprite_update > SPRITE_UPDATE:
        time_since_sprite_update = 0
        if keys[pygame.K_d] and grounded:
            if current_sprite == PLAYER_RUNNING_1 or current_sprite == PLAYER_STANDING:
                current_sprite = PLAYER_RUNNING_2
            elif current_sprite == PLAYER_RUNNING_2:
                current_sprite = PLAYER_RUNNING_1
        elif keys[pygame.K_a] and grounded:
            if current_sprite == PLAYER_RUNNING_1 or current_sprite == PLAYER_STANDING:
                current_sprite = PLAYER_RUNNING_2
            elif current_sprite == PLAYER_RUNNING_2:
                current_sprite = PLAYER_RUNNING_1
        else:
            current_sprite = PLAYER_STANDING
    
    if keys[pygame.K_SPACE] and grounded:
        grounded = False
        velocity_g = -50
    
    if current_level not in [0, 1]:
        if check_if_on_sun():
            sun_meter += dt * sun_fillup_speed
        else:
            sun_meter -= dt * sun_drain_speed
    
    if pygame.Rect(player_coords[0], player_coords[1], 80, 80).colliderect(pygame.Rect(portal_enter[0], portal_enter[1], 80, 80)):
        change_level(current_level + 1)
    
    if current_level not in [0, 1]:
        sun_meter = max(sun_meter, 0)
        sun_meter = min(sun_meter, 1)

    if sun_meter >= 1:
        die()

    if player_coords[1] > 640:
        change_level(current_level)

    win.blit(BACKGROUND_IMG, (0, 0))
    
    win.blit(PORTAL_ENTER_IMG, portal_enter)
    win.blit(PORTAL_EXIT_IMG, portal_exit)

    win.blit(current_sprite, player_coords)

    for pos, img in blocks:
        win.blit(img, pos)

    for text_ in current_texts:
        font = pygame.font.Font('freesansbold.ttf', text_[1])
        text = font.render(text_[0], True, (255, 208, 0))
        win.blit(text, text_[2])

    if current_level not in [0, 1]:
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(10, 10, 250, 60))
        pygame.draw.rect(win, (100, 100, 100), pygame.Rect(20, 20, 230, 40))
        pygame.draw.rect(win, (255, 208, 0), pygame.Rect(20, 20, (230 * sun_meter) // 10 * 10, 40))

    pygame.display.update()