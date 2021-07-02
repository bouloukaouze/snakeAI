from map import *

class Snake:

    def __init__(self):
        self.length = 4
        self.head = [10, 10]
        self.tail = [10, 13]
        self.positions = [self.head, [10, 11], [10, 12], self.tail]
        self.grow = False

    def move_up(self):
        if self.grow:
            self.positions = [self.head[0]-1, self.head[1]] + self.positions
            self.grow = False
        else:
            self.positions = [self.head[0]-1, self.head[1]] + self.positions[:-1]

    def move_left(self):
        if self.grow:
            self.positions = [self.head[0], self.head[1]-1] + self.positions
            self.grow = False
        else:
            self.positions = [self.head[0], self.head[1]-1] + self.positions[:-1]

    def move_down(self):
        if self.grow:
            self.positions = [self.head[0]+1, self.head[1]] + self.positions
            self.grow = False
        else:
            self.positions = [self.head[0]+1, self.head[1]] + self.positions[:-1]

    def move_right(self):
        if self.grow:
            self.positions = [self.head[0], self.head[1]+1] + self.positions
            self.grow = False
        else:
            self.positions = [self.head[0], self.head[1]+1] + self.positions[:-1]

    def eat(self, current_map):

        current_map.put_new_reward()
        self.grow = True
        self.length += 1


