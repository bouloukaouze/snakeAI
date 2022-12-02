import random as rd

import pygame
from snake import *
import numpy as np


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

        self.reward = []

        self.snake = snake

        for position in self.snake.positions:
            x = position[0]
            y = position[1]
            self.map[x][y] = 3
        self.map[self.snake.head[0]][self.snake.head[1]] = 4
        
        self.put_new_reward()

    def put_new_reward(self):

        available_cases = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0:
                    available_cases.append((i, j))

        i = available_cases[rd.randint(0, len(available_cases)-1)][0]
        j = available_cases[rd.randint(0, len(available_cases)-1)][1]
        while self.reward == [i, j]:
            i = available_cases[rd.randint(0, len(available_cases)-1)][0]
            j = available_cases[rd.randint(0, len(available_cases)-1)][1]


        self.reward = [i, j]
        self.map[i][j] = -1

    def move_snake(self):

        self.snake.move()

        if self.snake.head == self.reward:
            self.put_new_reward()
            self.snake.eat()

        if self.snake.length > 1:
            head_x = self.snake.head[0]
            head_y = self.snake.head[1]
            if self.map[head_x][head_y] == 1 \
                    or self.snake.head in self.snake.positions[1:]:
                self.snake.die()
        else:
            head_x = self.snake.head[0]
            head_y = self.snake.head[1]
            if self.map[head_x][head_y] == 1 \
                    or self.map[head_x][head_y] == 3:
                self.snake.die()


        for position in self.snake.positions:
            if position != self.snake.head:
                x = position[0]
                y = position[1]
                self.map[x][y] = 3

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if not ([i, j] in self.snake.positions) \
                        and self.map[i][j] == 3 or self.map[i][j] == 4:
                    self.map[i][j] = 0
        
        self.map[self.snake.head[0]][self.snake.head[1]] = 4

        

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
                if case == -1:
                    window.blit(food, (x, y))
                if case == 3 or case == 4:
                    window.blit(snake, (x, y))
                num_case += 1
            num_line += 1
