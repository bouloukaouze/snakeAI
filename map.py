import random as rd

import pygame
from snake import *


class Map:

    def __init__(self, snake):
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.reward = [rd.randint(1, 18), rd.randint(1, 18)]
        i = self.reward[0]
        j = self.reward[1]
        self.map[i][j] = 2

        self.snake = snake

        for position in self.snake.positions:
            x = position[0]
            y = position[1]
            self.map[x][y] = 3

    def put_new_reward(self):

        available_cases = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0:
                    available_cases.append((i, j))

        new_reward = rd.randint(0, len(available_cases))
        i = available_cases[new_reward][0]
        j = available_cases[new_reward][0]
        while self.reward == [i, j]:
            new_reward = rd.randint(0, len(available_cases))
            i = available_cases[new_reward][0]
            j = available_cases[new_reward][0]

        self.reward = [i, j]
        print(self.reward)
        self.map[i][j] = 2

    def move_snake(self):

        self.snake.move()

        if self.snake.head == self.reward:
            self.put_new_reward()
            self.snake.eat()

        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        if self.map[head_x][head_y] == 1 \
                or self.map[head_x][head_y] == 3:
            self.snake.die()

        for position in self.snake.positions:
            x = position[0]
            y = position[1]
            self.map[x][y] = 3

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if not ([i, j] in self.snake.positions) \
                        and self.map[i][j] == 3:
                    self.map[i][j] = 0

    def display(self, window):

        SPRITE_SIZE = 30

        wall = pygame.image.load("./images/wall.png").convert()
        food = pygame.image.load("./images/apple.png").convert_alpha()
        snake = pygame.image.load("./images/snake.png").convert_alpha()

        window.fill([0, 0, 0])

        num_line = 0
        for line in self.map:
            num_case = 0
            for case in line:
                x = num_case * SPRITE_SIZE
                y = num_line * SPRITE_SIZE
                if case == 1:
                    window.blit(wall, (x, y))
                if case == 2:
                    window.blit(food, (x, y))
                if case == 3:
                    window.blit(snake, (x, y))
                num_case += 1
            num_line += 1
