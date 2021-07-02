
class Snake:

    def __init__(self):
        self.length = 4
        self.head = [10, 10]
        self.tail = [10, 13]
        self.positions = [self.head, [10, 11], [10, 12], self.tail]
        self.grow = False
        self.alive = True
        self.direction = "left"

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
