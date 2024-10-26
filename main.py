import pygame as pyg
from random import randrange

#Window and Screen
WINDOW = 1000
TILE_SIZE = 25
screen = pyg.display.set_mode([WINDOW] * 2)
clock = pyg.time.Clock()

#Snake & Position
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
random_coord = lambda: [randrange(*RANGE), randrange(*RANGE)]

snake = pyg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = random_coord()
snake_starting_length = 1
snake_length = [snake.copy()]
snake_movement = (0,0)
snake_direction = {pyg.K_w: 1, pyg.K_s: 1, pyg.K_a: 1, pyg.K_d: 1}

#Time Variables for Speed
time = 0
time_step = 60

#Snake Food
food = snake.copy()
food.center = random_coord()

while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            exit()
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_w and snake_direction[pyg.K_w]:
                snake_movement = (0, -TILE_SIZE)
                snake_direction = {pyg.K_w: 1, pyg.K_s: 0, pyg.K_a: 1, pyg.K_d: 1}
            if event.key == pyg.K_s and snake_direction[pyg.K_s]:
                snake_movement = (0, TILE_SIZE)
                snake_direction = {pyg.K_w: 0, pyg.K_s: 1, pyg.K_a: 1, pyg.K_d: 1}
            if event.key == pyg.K_a and snake_direction[pyg.K_a]:
                snake_movement = (-TILE_SIZE, 0)
                snake_direction = {pyg.K_w: 1, pyg.K_s: 1, pyg.K_a: 1, pyg.K_d: 0}
            if event.key == pyg.K_d and snake_direction[pyg.K_d]:
                snake_movement = (TILE_SIZE, 0)
                snake_direction = {pyg.K_w: 1, pyg.K_s: 1, pyg.K_a: 0, pyg.K_d: 1}
    screen.fill((255, 255, 255))
    #Append Snake
    if snake.center == food.center:
        food.center = random_coord()
        snake_starting_length += 1
    #Self Eating
    snake_self = pyg.Rect.collidelist(snake, snake_length[:-1]) != -1
    #Check Boarders
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or snake_self:
        snake.center = random_coord()
        food.center = random_coord()
        snake_starting_length = 1
        snake_movement = (0,0)
        snake_length = [snake.copy()]
    #Draw Snake
    [pyg.draw.rect(screen, 'green', length) for length in snake_length]
    #Draw Food
    pyg.draw.rect(screen, 'blue', food)
    #Controlling the Snake
    time_current = pyg.time.get_ticks()
    if time_current - time > time_step:
        time = time_current
        snake.move_ip(snake_movement)
        snake_length.append(snake.copy())
        snake_length = snake_length[-snake_starting_length:]
    pyg.display.flip()
    clock.tick(144)