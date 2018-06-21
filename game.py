import sys
import random
import time
import keys


#Constants
BOARD_SIZE = 80 #in block
BLOCK_SIZE = 8 #1 block in pixels
GAME_SPEED = 10 #Game Speed


class Snake():
    def __init__(self):
        self.head = [int(BOARD_SIZE/4), int(BOARD_SIZE/4)]
        self.body =[[self.head[0], self.head[1]], [self.head[0]-1, self.head[1]], [self.head[0]-2, self.head[1]]]
        self.direction = "RIGHT"
        self.inter_frame_move_block = False

    def change_direction_to(self, dir):
        if not self.inter_frame_move_block:
            if dir == keys.RIGHT and not self.direction == keys.LEFT:
                self.direction = keys.RIGHT
                self.inter_frame_move_block = True
            if dir == keys.LEFT and not self.direction == keys.RIGHT:
                self.direction = keys.LEFT
                self.inter_frame_move_block = True
            if dir == keys.UP and not self.direction == keys.DOWN:
                self.direction = keys.UP
                self.inter_frame_move_block = True
            if dir == keys.DOWN and not self.direction == keys.UP:
                self.direction = keys.DOWN
                self.inter_frame_move_block = True

    def move(self,food_pos):
        if self.direction == keys.RIGHT:
            self.head[0]+=1
            self.inter_frame_move_block = False
        if self.direction == keys.LEFT:
            self.head[0]-=1
            self.inter_frame_move_block = False
        if self.direction == keys.UP:
            self.head[1]-=1
            self.inter_frame_move_block = False
        if self.direction == keys.DOWN:
            self.head[1]+=1
            self.inter_frame_move_block = False

        self.body.insert(0,list(self.head))
        if self.head == food_pos:
            return 1
        else:
            self.body.pop()
            return 0

    def check_collision(self):
        #BOARD
        if self.head[0]>=BOARD_SIZE or self.head[0] <0:
            return 1
        elif self.head[1]>BOARD_SIZE or self.head[1]<0:
            return 1
        #BODY
        for body in self.body[1:]:
            if self.head == body:
                return 1
        return 0

    def get_body(self):
        return self.body


class FoodSpawner():
    def __init__(self):
        self.head = [random.randrange(1,BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
        self.is_food_on_screen = True

    def spawn_food(self):
        if self.is_food_on_screen == False:
            self.head = [random.randrange(1, BOARD_SIZE), random.randrange(1,BOARD_SIZE)]
            self.is_food_on_screen = True
        return self.head

    def set_food_on_screen(self,bool_value):
        self.is_food_on_screen = bool_value


class Player():
    def __init__(self):
        self.snake = Snake()
        self.score = 0
        self.input = ""

    def game_over(self):
        print("GAME OVER")
        self.state = keys.GAME_OVER

    def set_input(self, input):
        self.input = input

class Game():
    def __init__(self):
        self.food_spawner = FoodSpawner()
        self.list_of_players = []
        self.number_of_players = 0
        self.game_started = False
        self.game_finished = False
        self.food_pos = [-1,-1]

    def add_player(self, player):
        if( self.number_of_players < 2 ):
            self.list_of_players.append(player)
            self.number_of_players +=1
            return True
        else:
            return False

    def return_your_player(self, player):
        for p in self.list_of_players:
            if p == player:
                return player

    def return_opposite_player(self, player):
        for p in self.list_of_players:
            if p != player:
                return player

    def game_loop(self):
            self.food_pos = self.food_spawner.spawn_food()

            for player in self.list_of_players:
                if player.input == keys.RIGHT:
                    player.input = ""
                    player.snake.change_direction_to(keys.RIGHT)
                if player.input == keys.LEFT:
                    player.input = ""
                    player.snake.change_direction_to(keys.LEFT)
                if player.input == keys.UP:
                    player.input = ""
                    player.snake.change_direction_to(keys.UP)
                if player.input == keys.DOWN:
                    player.input = ""
                    player.snake.change_direction_to(keys.DOWN)
                if player.snake.move(self.food_pos) ==1:
                    player.score +=1
                    self.food_spawner.set_food_on_screen(False)
                if player.snake.check_collision() == 1:
                    player.game_over()


