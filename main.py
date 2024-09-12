from typing import Mapping
import pygame
import random
import time

from pygame.constants import KEYDOWN, K_ESCAPE, SWSURFACE

# Initialising pygame
pygame.init()

# Initialising pygame music
pygame.mixer.init()

# Global variables for game
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 800
GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
EXIT_GAME = False
FPS_CLOCK = pygame.time.Clock()
GAME_SPRITES = {}
GAME_SOUNDS = {}

PIPE = 'sprites/pipe.png'
BACKGROUND = 'sprites/bgimg.png'
WELCOME = 'sprites/message.png'
LOGO = 'sprites/logo.jpg'

# Bird Images
downflap = 'sprites/downflap.png'
midflap = 'sprites/midflap.png'
upflap = 'sprites/upflap.png'
FLOOR = 'sprites/base1.png'

# Game sprites
GAME_SPRITES['background'] = (pygame.image.load(BACKGROUND).convert_alpha())
GAME_SPRITES['logo'] = (pygame.image.load(LOGO).convert_alpha())
GAME_SPRITES['welcome_screen'] = pygame.image.load(WELCOME).convert_alpha()

bird_downflap = pygame.image.load(downflap).convert_alpha()
bird_midflap = pygame.image.load(midflap).convert_alpha()
bird_upflap = pygame.image.load(upflap).convert_alpha()

GAME_SPRITES['floor'] = pygame.image.load(FLOOR).convert_alpha()
GAME_SPRITES['floor'] = pygame.transform.scale(
    GAME_SPRITES['floor'], (667, 112)).convert_alpha()

pipes = pygame.image.load(PIPE).convert_alpha()
pipes = pygame.transform.scale2x(pipes)

# Game sounds
Hit_sound = pygame.mixer.Sound('audio/hit.wav')
Flap_sound = pygame.mixer.Sound('audio/wing.wav')
Point_sound = pygame.mixer.Sound('audio/point.wav')

# Game specific variable

# Bird variables
bird_downflap = pygame.transform.scale(bird_downflap, (48, 35)).convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (48, 35)).convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (48, 35)).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 365))
bird_movement = 0
gravity = 0.24

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Floor variables
floorx_pos = 0
floory = 700

# Pipe variables
pipe_list = []
pipe_height = [300, 400, 600, 650]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Score variables
score = 0
pipe_passed = []  # To track pipes that the bird has passed

# Game condition
game_active = True

if __name__ == '__main__':
    pygame.init()

    # Game functions

    # background image, caption, logo
    def background():
        GAME_WINDOW.blit(GAME_SPRITES['background'], (0, 0))
        pygame.display.set_caption('Flappy Bird')
        pygame.display.set_icon(GAME_SPRITES['logo'])

    def floor_condition():
        global floorx_pos
        GAME_WINDOW.blit(GAME_SPRITES['floor'], (floorx_pos, floory))
        # Floor velocity
        floorx_pos -= 2
        # Floor condition
        if floorx_pos <= -50:
            floorx_pos = 0

    # displaying bird in our game
    def bird():
        global bird_movement, rotated_bird
        rotated_bird = rotate_bird(bird_surface)
        GAME_WINDOW.blit(rotated_bird, bird_rect)

    def create_pipe():
        random_pipe_height = random.choice(pipe_height)
        bottom_pipe = pipes.get_rect(midtop=(700, random_pipe_height))
        top_pipe = pipes.get_rect(midbottom=(700, random_pipe_height - 225))
        return bottom_pipe, top_pipe

    def move_pipes(pipe_list):
        for pipe in pipe_list:
            pipe.centerx -= 5
        return pipe_list

    def draw_pipes(pipe_list):
        for pipe in pipe_list:
            if pipe.bottom >= 800:
                GAME_WINDOW.blit(pipes, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipes, False, True)
                GAME_WINDOW.blit(flip_pipe, pipe)

    def check_collision(pipe_list):
        global EXIT_GAME, bird_movement, bird_rect
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                Hit_sound.play()
                return False

        if bird_rect.top <= -10 or bird_rect.bottom >= SCREEN_HEIGHT - 35 - 50:
            Hit_sound.play()
            return False

        return True

    def rotate_bird(bird):
        new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
        return new_bird

    def bird_animation():
        new_bird = bird_frames[bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
        return new_bird, new_bird_rect
    
    
   

    def display_score():
        global score
        score_font = pygame.font.Font('fonts/score_font_bold.ttf', 30)
        score_surface = score_font.render(f'Score: {score}', True, (255, 255, 255))
        GAME_WINDOW.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 50))

    def display_game_over(GAME_WINDOW):
        background()
        floor_condition()
        game_over_font = pygame.font.Font('fonts/game_over_font.otf', 96)
        screen_text = game_over_font.render("Game Over", True, (255, 0, 0))
        GAME_WINDOW.blit(screen_text, [170, 200])
        display_score()

    def welcome_screen():
        background()
        floor_condition()
        GAME_SPRITES['welcome_screen'] = pygame.transform.scale(
            GAME_SPRITES['welcome_screen'], (367, 450))
        GAME_WINDOW.blit(GAME_SPRITES['welcome_screen'], (100, 100))

    def game_loop():
        global EXIT_GAME, pipe_list, bird_movement, game_active, bird_index, bird_rect, bird_surface, score, pipe_passed
        while not EXIT_GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    EXIT_GAME = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_active == True:
                        Flap_sound.play()
                        bird_movement = 0
                        bird_movement += -7

                    if event.key == pygame.K_SPACE and game_active == False:
                        game_active = True
                        pipe_list.clear()
                        bird_rect.center = (100, 365)
                        bird_movement = 0
                        score = 0
                        pipe_passed = []

                if event.type == SPAWNPIPE:
                    pipe_list.extend(create_pipe())

                if event.type == BIRDFLAP:
                    if bird_index < 2:
                        bird_index += 1
                    else:
                        bird_index = 0
                    bird_surface, bird_rect = bird_animation()

            if game_active:
                background()
                bird_movement += gravity
                bird_rect.centery += bird_movement
                bird()
                draw_pipes(pipe_list)
                floor_condition()
                game_active = check_collision(pipe_list)

                # Pipes
                pipe_list = move_pipes(pipe_list)

                # Check if the bird has passed the pipe
                for pipe in pipe_list:
                    if pipe.centerx < bird_rect.left and pipe not in pipe_passed:
                        pipe_passed.append(pipe)
                        score += 1
                        Point_sound.play()

                display_score()

            else:
                background()
                floor_condition()
                welcome_screen()
                display_score()

            pygame.display.flip()
            FPS_CLOCK.tick(60)
    game_loop()
    pygame.quit()
