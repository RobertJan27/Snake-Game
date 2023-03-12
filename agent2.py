from turtle import goto

import pygame.time
import torch
import random
import numpy
from collections import deque
from collections import namedtuple
from  snake_game import SnakeGameAI,Direction,Point

Node=namedtuple("coords","dirr")


class Agent:

    def aStar_search2(self,game):
        from util import Queue
        global directions,  startState

        def euclideanCost( current, goal1):  # use a euclidean measurement to use as a cost
            return ((current[0] - goal1[0]) ** 2 + (current[1] - goal1[1]) ** 2) ** 0.5
        def manhattanHeuristic(position):
            # uses distance as a score for heuristic
            xy1 = position
            return abs(xy1[0] - game.food.x) + abs(xy1[1] - game.food.y)

        """" namedtuple("coords", "dirr", "cost")"""

        from util import PriorityQueue
        lista_cancer = []
        startnode=(game.head,"")



        print("capul=",game.head)
        lista_cancer.append(game.head)
        openlist=set([])
        openlist.add(startnode)
        closed_list=set([])
        parents={}
        parents1={}
        closed_list1=set([])
        openlist1=set([])
        g={}
        for i in range(0, 31):
            for j in range(0, 23):
                for de in {"Down", "Up", "Left", "Right"}:
                    g[(i * 20, j * 20), de] = 1000
        g[startnode]=0


        parents[startnode]=startnode

        def goto(linenum):
            global line
            line = linenum

        def performAction(direction):
            #game._place_food()
            for action in direction:
                game._move(action)
                game._update_ui()
                pygame.time.delay(500)
            print("am reusit")
            game.snake.insert(0, game.head)

        while 1:
            if len(openlist)==0:
                break
            current= None

            for v in openlist:
                if current==None or g[v]+manhattanHeuristic(v[0])<g[current]+manhattanHeuristic(current[0]):
                    current=v

            if game.isGoalState(current[0]):
                win_path=[]
                print("sunt aproape")
                while parents[current]!=current:
                        print(current)
                        win_path.append(current[1])
                        aux=current[0]
                        current=parents[current]

                win_path.reverse()
                performAction(win_path)
                game._place_food()

                startnode = (game.head, "")
                print("capul=", game.head)
                openlist = openlist1
                openlist.add(startnode)
                closed_list = closed_list1
                parents.clear()
                parents=parents1
                g = {}
                for i in range(0, 31):
                    for j in range(0, 23):
                        for de in {"Down", "Up", "Left", "Right"}:
                            g[(i * 20, j * 20), de] = 1000


                g[startnode] = 0
                parents[startnode] = startnode
                print("sunt aici")
                goto(61)
            #print(current)

            for (node,dirr,costt) in game.getSuccesors(current[0]):
                if (node,dirr) not in openlist and (node,dirr) not in closed_list:



                    parents[(node, dirr)] = current
                    if current[1]=="":
                        g[(node,dirr)] = costt + 0
                    else:
                        g[(node, dirr)] = costt + g[current]
                    openlist.add((node,dirr))
                else:
                    if g[(node,dirr)]> g[current]+costt:
                        g[(node,dirr)]=g[current]+costt
                        parents[(node,dirr)]=current

                        if (node,dirr) in closed_list:
                            closed_list.remove((node,dirr))
                            openlist.add((node,dirr))

            openlist.discard(current)
            closed_list.add(current)





def train():

    agent=Agent()
    game=SnakeGameAI()
    agent.aStar_search2(game)
    pygame.time.delay(1500)

if __name__ == '__main__':
    train()