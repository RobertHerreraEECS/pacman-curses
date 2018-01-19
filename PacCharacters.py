#!/usr/bin/env python
'''
    @author: Robert Herrera
    @description: pac-man game using ncurses
'''
from GameAI import GhostAI

class PacMan(object):
    def __init__(self):
        self.body = None
        self.body_id = 4

    def setBody(self,x,y):
        self.body = (x,y)

    def move(self, direction,status):
        if status == True:
            head_temp = self.body
            if direction == 259: # up
                temp = list(head_temp)
                temp[0] -= 1
                self.body = tuple(temp)
            elif direction == 258: # down
                temp = list(head_temp)
                temp[0] += 1
                self.body = tuple(temp)
            elif direction == 261: # right
                temp = list(head_temp)
                temp[1] += 1
                self.body = tuple(temp)
            elif direction == 260: # left
                temp = list(head_temp)
                temp[1] -= 1
                self.body = tuple(temp)

class Ghost(object):
    def __init__(self):
        self.body = None
        self.body_id = 5
        self.map_file = ''
        self.AI = None
    
    def set_map_file(self,input_file):
        self.map_file = input_file
    
    def init_search_agent(self):
        self.AI = GhostAI(self.map_file)

    def setBody(self,x,y):
        self.body = (x,y)

    def move(self, coord):
        self.body = coord

class Food(object):
    def __init__(self):
        self.body = None
        self.body_id = 8
    def setBody(self,x,y):
        self.body = (x,y)


