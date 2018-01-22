#!/usr/bin/env python
'''
    @author: Robert Herrera
    @modified: Brandon Radosevich
    @description: pac-man game using ncurses
'''
from GameAI import GhostAI
from GameAI import PacManAI

class PacMan(object):
    def __init__(self, _file):
        self.body = None
        self.body_id = 4
        self.AI = None
        self.map_file = _file

    def setBody(self,x,y):
        self.body = (x,y)

    def init_search_agent(self):
        self.AI = GhostAI(self.map_file)

    def move(self, coord):
        self.body = coord

class PacManAux(object):
    def __init__(self, _file):
        self.body = None
        self.body_id = 4
        self.AI = None
        self.map_file = _file
    
    def setBody(self,x,y):
        self.body = (x,y)
    
    def init_search_agent(self):
        self.AI = PacManAI(self.map_file)
    
    def move(self, coord):
        self.body = coord

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
