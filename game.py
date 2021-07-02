from map import *
from snake import *
from pygame.locals import *


class Game:

    def __init__(self):
        self.score = 0

    def display(self, window, map):

        map.display(window)
        pygame.display.flip()

    def inputs_management(self, snake, alive):

        for event in pygame.event.get():
            if event.type == QUIT:
                alive = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:       #
                    alive = False
                if event.key == K_RIGHT:
                    snake.direction = 'right'
                elif event.key == K_LEFT:
                    snake.direction = 'left'
                elif event.key == K_UP:
                    snake.direction = 'up'
                elif event.key == K_DOWN:
                    snake.direction = 'down'


    def run(self, speed=5):

        SPRITE_NUMBER = 20
        SPRITE_SIZE = 30
        WINDOW_SIZE = SPRITE_NUMBER * SPRITE_SIZE
        WINDOW_TITLE = "Snake"

        pygame.init()
        game_window = pygame.display.set_mode((int(WINDOW_SIZE * 2), WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)

        snake = Snake()
        current_map = Map(snake)

        alive = True
        while alive:
            pygame.time.Clock().tick(speed)
            self.inputs_management(snake,alive)
            self.display(game_window, current_map)
            current_map.move_snake()
            alive = snake.alive

        self.score = snake.length
        return "Fin de partie :", self.score





