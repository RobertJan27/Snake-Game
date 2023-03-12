import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:
    global head,snake,w,h,display,clock,snake,food

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
        # init game state


    def reset(self):

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        print(self.snake)
        self.score = 0
        self.food = None
        self._place_food()
        self._update_ui()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        print("food=",x,y)
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()
    
    def is_collision(self, pt=None):
        # hits boundary
        if pt is None:
            pt = self.head
        if pt in self.snake[1:]:
            return True
        return False

    def euclideanCost(self,current, goal):  # use a euclidean measurement to use as a cost
        return ((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2) ** 0.5

    def isGoalState(self,current):
        if current[0]== self.food[0] and current[1]==self.food[1]:
            #print(current[0], current[1])
            return True
        else:
            return False

    def getStartState(self):
        return self.head


    def getSuccesors(self,current_pos):
            cost=0
            successors=[]
            possible_moves=[+BLOCK_SIZE,-BLOCK_SIZE]

            for move in possible_moves:
                nextx=current_pos[0]+move
                nexty=current_pos[1]
                point=Point(nextx,nexty)
                if point not in self.snake[1:] and point[0]<640 and point[0]>0:
                    nextState=point
                    if nextState!=current_pos:
                        if nextState not in successors:
                            dirr="Right"
                            if move == +BLOCK_SIZE:
                                dirr="Right"
                                cost= (self.euclideanCost(current_pos, self.food) / 2)
                            elif move == -BLOCK_SIZE:
                                dirr="Left"
                                cost= (self.euclideanCost(current_pos, self.food) / 2)
                            successors.append((nextState,dirr,cost))

            for move in possible_moves:
                nextx=current_pos[0]
                nexty=current_pos[1]+move
                point=Point(nextx,nexty)
                if point not in self.snake[1:] and point[1]<480 and point[1]>0:
                    nextState=point
                    if nextState!=current_pos:
                        if nextState not in successors:
                            dirr = "Up"
                            if move == +BLOCK_SIZE:
                                dirr = "Up"
                                cost= (self.euclideanCost(current_pos, self.food) / 2)
                            elif move == -BLOCK_SIZE:
                                dirr = "Down"
                                cost= (self.euclideanCost(current_pos, self.food) / 2)
                            successors.append((nextState,dirr,cost))

            return successors


    def game_over(self):
        if self.head in self.snake[1:]:
            return True
        else:
            return False



    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt[0] + 4, pt[1] + 4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, dirr):
        # [Left , Right , Up,Down]

            x = self.head[0]
            y = self.head[1]
            if dirr == "Right":

                    x += BLOCK_SIZE
            if dirr == "Left":

                      x -= BLOCK_SIZE
            if dirr == "Down":

                    y  -= BLOCK_SIZE

            if dirr == "Up":

                    y += BLOCK_SIZE

            i=len(self.snake)
            i -=1
            while i>0:

                self.snake[i]=self.snake[i-1]
                i -= 1

            self.snake[0]=(x,y)
            self.head=(x,y)



            

