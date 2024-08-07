import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 700
screen_height = 388
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Colors
background_color = (35, 92, 118)
bird_color = (224, 214, 68)
pipe_color = (94, 201, 72)
text_color = (255, 255, 255)

# Bird properties
bird_x = 62
bird_width = 30
bird_height = 25

# Playing area properties
playing_area_width = 300
playing_area_height = 388

# Pipe properties
pipe_space_height = 100
pipe_width = 54

# Initialize variables
bird_y = 200
bird_y_speed = 0

pipe_1_x = playing_area_width
pipe_1_space_y = random.randint(54, playing_area_height - pipe_space_height - 54)

pipe_2_x = playing_area_width + ((playing_area_width + pipe_width) / 2)
pipe_2_space_y = random.randint(54, playing_area_height - pipe_space_height - 54)

score = 0
upcoming_pipe = 1

clock = pygame.time.Clock()

def new_pipe_space_y():
    pipe_space_y_min = 54
    pipe_space_y = random.randint(
        pipe_space_y_min,
        playing_area_height - pipe_space_height - pipe_space_y_min
    )
    return pipe_space_y

def reset():
    global bird_y, bird_y_speed, pipe_1_x, pipe_1_space_y, pipe_2_x, pipe_2_space_y, score, upcoming_pipe
    bird_y = 200
    bird_y_speed = 0
    pipe_1_x = playing_area_width
    pipe_1_space_y = new_pipe_space_y()
    pipe_2_x = playing_area_width + ((playing_area_width + pipe_width) / 2)
    pipe_2_space_y = new_pipe_space_y()
    score = 0
    upcoming_pipe = 1

def update(dt):
    global bird_y, bird_y_speed, pipe_1_x, pipe_2_x, pipe_1_space_y, pipe_2_space_y
    bird_y_speed += 516 * dt
    bird_y += bird_y_speed * dt

    def move_pipe(pipe_x, pipe_space_y):
        pipe_x -= 60 * dt
        if (pipe_x + pipe_width) < 0:
            pipe_x = playing_area_width
            pipe_space_y = new_pipe_space_y()
        return pipe_x, pipe_space_y

    pipe_1_x, pipe_1_space_y = move_pipe(pipe_1_x, pipe_1_space_y)
    pipe_2_x, pipe_2_space_y = move_pipe(pipe_2_x, pipe_2_space_y)

    def is_bird_colliding_with_pipe(pipe_x, pipe_space_y):
        return (
            bird_x < (pipe_x + pipe_width)
            and (bird_x + bird_width) > pipe_x
            and (
                bird_y < pipe_space_y
                or (bird_y + bird_height) > (pipe_space_y + pipe_space_height)
            )
        )

    if (
        is_bird_colliding_with_pipe(pipe_1_x, pipe_1_space_y)
        or is_bird_colliding_with_pipe(pipe_2_x, pipe_2_space_y)
        or bird_y > playing_area_height
    ):
        reset()

    def update_score_and_closest_pipe(this_pipe, pipe_x, other_pipe):
        global score, upcoming_pipe
        if (
            upcoming_pipe == this_pipe
            and bird_x > (pipe_x + pipe_width)
        ):
            score += 1
            upcoming_pipe = other_pipe

    update_score_and_closest_pipe(1, pipe_1_x, 2)
    update_score_and_closest_pipe(2, pipe_2_x, 1)

def on_key_down():
    global bird_y_speed
    if bird_y > 0:
        bird_y_speed = -165

def draw():
    screen.fill(background_color)

    pygame.draw.rect(
        screen,
        bird_color,
        pygame.Rect(
            (bird_x, bird_y),
            (bird_width, bird_height)
        )
    )

    def draw_pipe(pipe_x, pipe_space_y):
        pygame.draw.rect(
            screen,
            pipe_color,
            pygame.Rect(
                (pipe_x, 0),
                (pipe_width, pipe_space_y)
            )
        )
        pygame.draw.rect(
            screen,
            pipe_color,
            pygame.Rect(
                (pipe_x, pipe_space_y + pipe_space_height),
                (pipe_width, playing_area_height - pipe_space_y - pipe_space_height)
            )
        )

    draw_pipe(pipe_1_x, pipe_1_space_y)
    draw_pipe(pipe_2_x, pipe_2_space_y)

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(str(score), True, text_color)
    screen.blit(score_text, (15, 15))

# Main game loop
running = True
while running:
    dt = clock.tick(30) / 1000  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            on_key_down()

    update(dt)
    draw()
    pygame.display.flip()
