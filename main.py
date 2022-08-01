import pygame
from time import time

win = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Ultraviolet')
pygame.display.set_icon(pygame.image.load('img/icon.png'))

# Block stuff
GRASS_IMG = pygame.transform.scale(pygame.image.load('img/grass.png').convert(), (80, 80))
DIRT_IMG = pygame.transform.scale(pygame.image.load('img/dirt.png').convert(), (80, 80))
blocks = [([280, 560], GRASS_IMG)]

# Player stuff
PLAYER_STANDING = pygame.transform.scale(pygame.image.load('img/player_standing.png'), (80, 80))
PLAYER_RUNNING_1 = pygame.transform.scale(pygame.image.load('img/player_running_1.png'), (80, 80))
PLAYER_RUNNING_2 = pygame.transform.scale(pygame.image.load('img/player_running_2.png'), (80, 80))
player_coords = [270, 100]
current_sprite = PLAYER_STANDING
TIME_BETWEEN_MOVES = 1/20
SPRITE_UPDATE = 1/5
time_since_sprite_update = 0
time_since_move = 0
grounded = False
velocity_g = 0

old_time = time()
while True:
    dt = time() - old_time
    old_time = time()

    time_since_move += dt
    time_since_sprite_update += dt

    [[pygame.quit(), quit()] for event in pygame.event.get() if event.type == pygame.QUIT]

    keys = pygame.key.get_pressed()

    # Updating moves
    if time_since_move >= TIME_BETWEEN_MOVES:
        time_since_move = 0
        # was_ever_grounded = False
        # for block in blocks:
        #     if pygame.Rect(player_coords[0], player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
        #         was_ever_grounded = True
        # grounded = was_ever_grounded

        if keys[pygame.K_d]:
            can_go_right = True
            for block in blocks:
                if pygame.Rect(player_coords[0] + 10, player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    can_go_right = False
            if can_go_right:
                player_coords[0] += 10
        elif keys[pygame.K_a]:
            can_go_left = True
            for block in blocks:
                if pygame.Rect(player_coords[0] - 10, player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    can_go_left = False
            if can_go_left:
                player_coords[0] -= 10
        if grounded:
            velocity_g = 0
        else:
            velocity_g += 10
            player_coords[1] += velocity_g
            for block in blocks:
                if pygame.Rect(player_coords[0], player_coords[1], 80, 80).colliderect(pygame.Rect(block[0][0], block[0][1], 80, 80)):
                    player_coords[1] = block[0][1] - 80
                    was_grounded = False
                    grounded = True

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

    win.fill((255, 255, 255))
    win.blit(current_sprite, player_coords)
    for pos, img in blocks:
        win.blit(img, pos)

    pygame.display.update()