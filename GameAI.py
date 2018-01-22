#!/usr/bin/env python
'''
    @author: Brandon Radosevich
    @modified: Robert Herrera
'''
from search_agent import searchAgent

class PacManAI(object):
    def __init__(self, filename,costs = {'+': 1, '|' : 1, '-' : 1, '*':1,'#' : 2, '0' : 1000}):
        self.filename =  filename
        self.costs = costs
        self.board = []
        self.width = []
        self.height = []
        self.nodes = {}
        self.graph = {}
        self.path = []
        self.screen = None
        maze = self.readFile()
        self.convertToGraph(maze)
        self.food = None

    # row col -> insert as col row
    def search(self,start):
        heursitics = {}
        for f in self.food:
            h = searchAgent(self.graph,self.nodes,self.costs,start,f,'manhattan').heuristic(start,f,'manhattan')
            heursitics[f] = h
        goal = sorted(heursitics.iterkeys(),key=lambda k: heursitics[k])[0]
        self.food.remove(goal)
        came_from, cost_so_far = searchAgent(self.graph,self.nodes,self.costs,start,goal,'manhattan').a_star()
        self.path = self.reconstruct_path(came_from,start,goal)

    def findFood(self):
        food = []
        for node,bitmap in self.nodes.items():
            if bitmap == '+':
                food.append(node)
        self.food = food

    def readFile(self):
        f = open(self.filename,'r')
        maze = []
        for line in f:
            maze.append(line.replace(" ",'').rstrip('\n'))
        self.height = len(maze)
        self.width = len(maze[0])
        return maze

    def convertToGraph(self,maze):
        for i in range(0,self.height):
            for j in range(0,self.width):
                vertices = self.findNeighbors((j,i))
                self.graph[(j,i)] = vertices
                self.nodes[(j,i)] = maze[i][j]

    def cost(self, a, b):
        return self.costs[self.nodes[a]] + self.costs[self.nodes[b]]

    def reconstruct_path(self,came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path

    def findNeighbors(self,tile):
        x,y = (tile)
        UP = (x, y - 1)
        DOWN = (x, y + 1)
        LEFT = (x - 1,y)
        RIGHT = (x + 1, y)
        ulu = (x-1, y-1)
        uld = (x-1, y+1)
        uru = (x+1, y-1)
        urd = (x+1, y+1)
        directions = [UP,DOWN,LEFT,RIGHT]#, ulu,uld,uru,urd]
        neighbors = []
        for direc in directions:
            if direc[0] >= 0  and direc[0] < self.width and direc[1] >= 0 and direc[1] < self.height:
                neighbors.append(direc)
        return neighbors


class GhostAI(object):
    def __init__(self, filename,costs = {'+': 1, '|' : 1, '-' : 1, '*':1,'#' : 2, '0' : 1000}):
        self.filename =  filename
        self.costs = costs
        self.board = []
        self.width = []
        self.height = []
        self.nodes = {}
        self.graph = {}
        self.path = []
        self.screen = None
        maze = self.readFile()
        self.convertToGraph(maze)

    # row col -> insert as col row
    def search(self,Start, Goal):
        start,goal = Start,Goal
        came_from, cost_so_far = searchAgent(self.graph,self.nodes,self.costs,start,goal,'simple').a_star()
        self.path = self.reconstruct_path(came_from,start,goal)

    def readFile(self):
        f = open(self.filename,'r')
        maze = []
        for line in f:
            maze.append(line.replace(" ",'').rstrip('\n'))
        self.height = len(maze)
        self.width = len(maze[0])
        return maze

    def convertToGraph(self,maze):
        for i in range(0,self.height):
            for j in range(0,self.width):
                vertices = self.findNeighbors((j,i))
                self.graph[(j,i)] = vertices
                self.nodes[(j,i)] = maze[i][j]

    def cost(self, a, b):
        return self.costs[self.nodes[a]] + self.costs[self.nodes[b]]

    def reconstruct_path(self,came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path

    def findNeighbors(self,tile):
        x,y = (tile)
        UP = (x, y - 1)
        DOWN = (x, y + 1)
        LEFT = (x - 1,y)
        RIGHT = (x + 1, y)
        ulu = (x-1, y-1)
        uld = (x-1, y+1)
        uru = (x+1, y-1)
        urd = (x+1, y+1)
        directions = [UP,DOWN,LEFT,RIGHT]#, ulu,uld,uru,urd]
        neighbors = []
        for direc in directions:
            if direc[0] >= 0  and direc[0] < self.width and direc[1] >= 0 and direc[1] < self.height:
                neighbors.append(direc)
        return neighbors
