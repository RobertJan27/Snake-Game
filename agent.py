from turtle import goto

import pygame.time
import torch
import random
import numpy
from collections import deque
from  snake_game import SnakeGameAI,Direction,Point



class Agent:


    def df_search(self,game):
        from util import Queue
        global directions, tempFood, startState

        def manhattanHeuristic(position):
            # uses distance as a score for heuristic
            xy1 = position
            return abs(xy1[0] - game.food.x) + abs(xy1[1] - game.food.y)

        from util import PriorityQueue
        priorityqueue = PriorityQueue()  # fringe
        visited = set()

        def goto(linenum):
            global line
            line = linenum

        def performAction():
            #game._place_food()
            for action in directions:
                game._move(action)
                game._update_ui()
                pygame.time.delay(500)
            print("am reusit")
            game.snake.insert(0, game.head)

        priorityqueue.push((SnakeGameAI.getStartState(game), [], 0), 0)
        while 1:
            if priorityqueue.isEmpty():
                break
            current,directions,costs=priorityqueue.pop()
            if current not in visited:
                visited.add(current)
                if  game.isGoalState(current):
                    game.score+=1
                    performAction()
                    game._place_food()
                    visited=set()
                    priorityqueue=PriorityQueue()
                    priorityqueue.push((SnakeGameAI.getStartState(game), [], 0), 0)
                    directions=[]
                    goto(43)
                for childNode,direction,cost in game.getSuccesors(current):
                    if childNode not in priorityqueue.heap:
                        if childNode in visited:
                            continue
                        hCost = costs + cost + manhattanHeuristic(childNode)
                        priorityqueue.push((childNode,directions+[direction],costs+cost),hCost)




def train():

    agent=Agent()
    game=SnakeGameAI()
    agent.df_search(game)
    pygame.time.delay(1500)

if __name__ == '__main__':
    train()