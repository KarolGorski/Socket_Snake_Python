import pygame
import keys
import sys


class GameRender():
    def __init__(self):
        self.BOARD_SIZE = 80 #in block
        self.BLOCK_SIZE = 8 #1 block in pixels
        self.HEAD_COLOR = (0,100,0) #Dark Green
        self.BODY_COLOR = (0,200,0) #Light Green
        self.FOOD_COLOR = (200,0,0) #Dark Red
        self.GAME_SPEED = 10
        self.window = pygame.display.set_mode((self.BOARD_SIZE*self.BLOCK_SIZE,
                                               self.BOARD_SIZE*self.BLOCK_SIZE))
        pygame.display.set_caption(keys.GAME_NAME)
        self.fps = pygame.time.Clock()

    def game_over(self, score):
        pygame.display.set_caption("SNAKE GAME | Score:" + str(score) + " | GAME OVER. Press any key to quit.")
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                break
        pygame.quit()
        sys.exit()


    def game_start(self):
        self.window.fill(pygame.Color(0, 0, 0))

    def game_update(self, snake_body, food_pos, score):
        # Draw Snake
        head = 1
        for pos in snake_body:
            if head == 1:
                pygame.draw.rect(self.window,
                                 self.HEAD_COLOR,
                                 pygame.Rect(pos[0] * self.BLOCK_SIZE,
                                             pos[1] * self.BLOCK_SIZE,
                                             self.BLOCK_SIZE,
                                             self.BLOCK_SIZE))
                head = 0
            else:
                pygame.draw.rect(self.window, self.BODY_COLOR, pygame.Rect(pos[0] * self.BLOCK_SIZE, pos[1] * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))

        # Draw Food
        pygame.draw.rect(self.window, self.FOOD_COLOR, pygame.Rect(food_pos[0] * self.BLOCK_SIZE, food_pos[1] * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))

        pygame.display.set_caption("SNAKE GAME | Score:" + str(score))
        pygame.display.flip()
        self.fps.tick(self.GAME_SPEED)