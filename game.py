from map import *
from snake import *
from pygame.locals import *
from neuronal_network import *
from time import sleep
import matplotlib.pyplot as plt
import pygame
import cv2

def pg_to_cv2(cvarray:np.ndarray)->np.ndarray:
    cvarray = cvarray.swapaxes(0,1) #rotate
    cvarray = cv2.cvtColor(cvarray, cv2.COLOR_RGB2BGR) #RGB to BGR
    return cvarray


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
                if event.key == K_ESCAPE:       
                    alive = False
                if event.key == K_RIGHT:
                    snake.direction = 'right'
                elif event.key == K_LEFT:
                    snake.direction = 'left'
                elif event.key == K_UP:
                    snake.direction = 'up'
                elif event.key == K_DOWN:
                    snake.direction = 'down'

    def inputs_AI(self, choice, snake):
        """
        match choice:
            case 0:
                snake.direction = snake.direction
            case 1:
                match snake.direction:
                    case 'up':
                        snake.direction = 'right'
                    case 'right':
                        snake.direction = 'down'
                    case 'down':
                        snake.direction = 'left'
                    case 'left':
                        snake.direction = 'up'
            case 2:
                match snake.direction:
                    case 'up':
                        snake.direction = 'left'
                    case 'right':
                        snake.direction = 'up'
                    case 'down':
                        snake.direction = 'right'
                    case 'left':
                        snake.direction = 'down'
        """

        match choice:
            case 0:
                snake.direction = "up"
            case 1:
                snake.direction = "right"
            case 2:
                snake.direction = "down"
            case 3:
                snake.direction = "left"


    def run(self, speed=5):

        SPRITE_NUMBER = 20
        SPRITE_SIZE = 30
        WINDOW_SIZE = SPRITE_NUMBER * SPRITE_SIZE
        WINDOW_TITLE = "Snake"

        pygame.init()
        game_window = pygame.display.set_mode((int(WINDOW_SIZE), WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)

        snake = Snake()
        current_map = Map(snake)

        alive = True
        self.display(game_window, current_map)
        while alive:
            self.display(game_window, current_map)
            pygame.time.Clock().tick(speed)
            self.inputs_management(snake,alive)
            current_map.move_snake()
            alive = snake.alive

        self.score = snake.length
        return self.score

    def run_AI(self, NN): #, speed=10000000):

        """SPRITE_NUMBER = 20
        SPRITE_SIZE = 30
        WINDOW_SIZE = SPRITE_NUMBER * SPRITE_SIZE
        WINDOW_TITLE = "Snake"

        pygame.init()
        game_window = pygame.display.set_mode((int(WINDOW_SIZE), WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)"""

        snake = Snake()
        current_map = Map(snake)

        alive = True
        count = 0
        penalty = 0
        while alive:
            #pygame.time.Clock().tick(speed)
            self.inputs_AI(NN.choose(current_map), snake)
            #self.display(game_window, current_map)
            current_map.move_snake()
            alive = snake.alive
            count += 1
            if count >= snake.length*100:
                penalty = 1
                break
        self.score = 5*np.sqrt(count) + snake.length**2 + 2**(snake.length - count/10) - penalty*1000
        return self.score, snake.length

    def run_AI_dis(self, NN, speed=10):

        SPRITE_NUMBER = 20
        SPRITE_SIZE = 30
        WINDOW_SIZE = SPRITE_NUMBER * SPRITE_SIZE
        WINDOW_TITLE = "Snake"

        pygame.init()
        game_window = pygame.display.set_mode((int(WINDOW_SIZE), WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)

        snake = Snake()
        current_map = Map(snake)
        self.display(game_window, current_map)

        alive = True
        count = 0
        penalty = 0
        while alive:
            self.display(game_window, current_map)
            pygame.time.Clock().tick(speed)
            self.inputs_AI(NN.choose(current_map), snake)
            current_map.move_snake()
            alive = snake.alive
            count += 1
            if count >= snake.length*100:
                penalty = 1
                break
        self.score = 5*np.sqrt(count) + 10*snake.length + 2.5**(snake.length - count/10) - penalty*100
        sleep(0.5)
        pygame.display.quit()
        pygame.quit()
        return self.score, snake.length

    def run_demo(self, folder, speed=50):
        SPRITE_NUMBER = 20
        SPRITE_SIZE = 30
        WINDOW_SIZE = SPRITE_NUMBER * SPRITE_SIZE
        pygame.init()
        pygame.mixer.init()
        game_window = pygame.display.set_mode((int(WINDOW_SIZE), WINDOW_SIZE))
        frame = pygame.surfarray.pixels3d(game_window.copy())
        cv_frame = pg_to_cv2(frame)
        height, width, _ = cv_frame.shape
        video = cv2.VideoWriter(f"./{folder}/result.avi", cv2.VideoWriter_fourcc(*'DIVX'), 17, (width,height))
        video.write(cv_frame)
        scores = []
        for i in range(0,750,50):
            if i == -1:
                continue
            print(f"\nGENERATION {i}")
            moy = 0
            snakeNN = NeuronalNetwork()
            data = np.load(f"{folder}/gen_{i}/snake_0.npy",encoding = 'bytes', allow_pickle=True)
            snakeNN.weights = data[0]
            snakeNN.biases = data[1]
            for _ in range(2):
                
                WINDOW_TITLE = "Snake"

                pygame.display.set_caption(WINDOW_TITLE)

                snake = Snake()
                current_map = Map(snake)
                self.display(game_window, current_map)

                alive = True
                count = 0
                while alive:
                    self.display(game_window, current_map)
                    pygame.time.Clock().tick(speed)
                    frame = pygame.surfarray.pixels3d(game_window.copy())
                    cv_frame = pg_to_cv2(frame)
                    video.write(cv_frame)
                    self.inputs_AI(snakeNN.choose(current_map), snake)
                    current_map.move_snake()
                    alive = snake.alive
                    count += 1
                    if count >= snake.length*100:
                        break                    
                moy += snake.length/2
            scores.append(moy)
        cv2.destroyAllWindows()
        video.release()
        pygame.display.quit()
        pygame.quit()
        plt.plot(scores, 'b')
        plt.savefig(f"{folder}/demo_graph.png")





