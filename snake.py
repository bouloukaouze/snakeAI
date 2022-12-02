from numpy.random import randint


class Snake:

    def __init__(self):
        self.length = 1
        self.head = [randint(2,18), randint(2,18)]
        self.positions = [self.head]
        self.alive = True
        match randint(0,4):
            case 0:
                self.direction = 'left'
            case 1:
                self.direction = 'right'
            case 2:
                self.direction = 'up'
            case 3:
                self.direction = 'down'

        self.grow = True

    def move_up(self):
        if self.grow:
            self.head = [self.head[0] - 1, self.head[1]]
            self.positions = [self.head] + self.positions
            self.grow = False
        else:
            self.head = [self.head[0] - 1, self.head[1]]
            self.positions = [self.head] + self.positions[:-1]
        self.direction = "up"

    def move_left(self):
        if self.grow:
            self.head = [self.head[0], self.head[1] - 1]
            self.positions = [self.head] + self.positions
            self.grow = False
        else:
            self.head = [self.head[0], self.head[1] - 1]
            self.positions = [self.head] + self.positions[:-1]
        self.direction = "left"

    def move_down(self):
        if self.grow:
            self.head = [self.head[0] + 1, self.head[1]]
            self.positions = [self.head] + self.positions
            self.grow = False
        else:
            self.head = [self.head[0] + 1, self.head[1]]
            self.positions = [self.head] + self.positions[:-1]
        self.direction = "down"

    def move_right(self):
        if self.grow:
            self.head = [self.head[0], self.head[1] + 1]
            self.positions = [self.head] + self.positions
            self.grow = False
        else:
            self.head = [self.head[0], self.head[1] + 1]
            self.positions = [self.head] + self.positions[:-1]
        self.direction = "right"

    def move(self):
        if self.direction == 'left':
            self.move_left()
        elif self.direction == 'right':
            self.move_right()
        elif self.direction == 'up':
            self.move_up()
        elif self.direction == 'down':
            self.move_down()

    def eat(self):

        self.grow = True
        self.length += 1

    def die(self):

        self.alive = False
