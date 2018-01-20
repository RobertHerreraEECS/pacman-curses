#!/usr/bin/env python
'''
    @author: Robert Herrera
    @modified: Brandon Radosevich
    @description: pac-man game using ncurses
    '''
import numpy as np
import random
import time
import sys
import re
import curses
from search_agent import searchAgent
from PacCharacters import PacMan,Ghost


class ScreenSizeException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class ScreenException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class GameScreen(object):
    def __init__(self,x=10):
        self.x = x
        self.y = x
        self.screen_data = None
        self.screen = None

    def read_text_map(self,file_path):
        with open(file_path,'rb') as fid:
            data = fid.read()
            self.screen_data = data

    def updateBitAtLocation(self,cx,cy,char):
        self.screen_data[cx + cy*self.y] = char

    @staticmethod
    def get_map_size(data):
        row = 0
        col = 0
        for index,line in enumerate(data.split('\n')):
            if index == 0:
                col = len(line.split(' '))
            if line != '':
                row += 1
        return row, col

    @staticmethod
    def get_bit_map(data):
        bit_map = []
        for line in data.split('\n'):
            if line != '':
                bit_map.append(line.split(' '))
        return bit_map

    def setScreenSize(self):
        if(self.screen_data is None):
            raise ScreenSizeException("No bitmask file provided.")
        else:
            # cast text data as 2d plane
            row,col = self.get_map_size(self.screen_data)
            self.x = row
            self.y = col
            map = self.get_bit_map(self.screen_data)
            # form integer mask
            self.screen = np.zeros(shape=(row,col+1))
            for i in range(0,row):
                for j in range(0,col):
                    if map[i][j] == '0':
                        self.screen[i,j] = 0
                    elif map[i][j] == '-' or map[i][j] == '|':
                        self.screen[i,j] = 1
                    elif map[i][j] == '+':
                        self.screen[i,j] = 2
                    elif map[i][j] == '*':
                        self.screen[i,j] = 3
                    elif map[i][j] == '#':
                        self.screen[i,j] = 6
                    else:
                        self.screen[i,j] = 0

    def refresh(self):
        pass

    def impose(self,coord_list,id_):
        for coord in coord_list:
            self.screen[coord[0],coord[1]] = id_

class Game(object):
    def __init__(self):
        pass
    def check_bounds(self,game_screen,direction,sprite):
        if sprite.body_id == 4:
            #check next cell relative to direction of movement
            if direction == 259 and (game_screen.screen[sprite.body[0] - 1,sprite.body[1]] == 0 or game_screen.screen[sprite.body[0] - 1,sprite.body[1]] == 6): #down
                return False
            elif direction == 258  and (game_screen.screen[sprite.body[0] + 1,sprite.body[1]] == 0 or game_screen.screen[sprite.body[0] + 1,sprite.body[1]] == 6): # up
                return False
            elif direction == 261 and (game_screen.screen[sprite.body[0],sprite.body[1] + 1] == 0 or game_screen.screen[sprite.body[0],sprite.body[1] + 1] == 6): #right
                return False
            elif direction == 260 and (game_screen.screen[sprite.body[0],sprite.body[1] - 1] == 0 or game_screen.screen[sprite.body[0],sprite.body[1] - 1] == 6) : # left
                return False
            else:
                return True
        else:
            #check next cell relative to direction of movement
            if direction == 259 and game_screen.screen[sprite.body[0] - 1,sprite.body[1]] == 0: #down
                return False
            elif direction == 258  and game_screen.screen[sprite.body[0] + 1,sprite.body[1]] == 0: # up
                return False
            elif direction == 261 and game_screen.screen[sprite.body[0],sprite.body[1] + 1] == 0: #right
                return False
            elif direction == 260 and game_screen.screen[sprite.body[0],sprite.body[1] - 1] == 0: # left
                return False
            else:
                return True

    def check_wrapping(self,game_screen,direction,sprite):
        #check next cell relative to direction of movement
            if direction == 261 and sprite.body[1] == game_screen.y - 1: #right
                temp = list(sprite.body)
                temp[1] = 0
                sprite.body = tuple(temp)
            elif direction == 260 and sprite.body[1] == 0: #right
                temp = list(sprite.body)
                temp[1] = game_screen.y - 1
                sprite.body = tuple(temp)

    def check_move(self, direction, prev_move):
        # utilize prev move later, and next move too
        return False

    def printScreen(self,stdscr,game_screen):
    # stdscr.addstr(str(game_screen.screen) + ' ',curses.color_pair(1))
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_GREEN)
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
        #pac man color
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        #ghost 1 color
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
        for i in range(game_screen.x):
            for j in range(game_screen.y):
                if game_screen.screen[i,j] == 0:
                    stdscr.addstr('#' + ' ',curses.color_pair(1))
                elif game_screen.screen[i,j] == 1:
                    stdscr.addstr(' ' + ' ',curses.color_pair(1))
                elif game_screen.screen[i,j] == 2:
                    stdscr.addstr('*' + ' ',curses.color_pair(3))
                elif game_screen.screen[i,j] == 3:
                    stdscr.addstr(' ' + ' ',curses.color_pair(2))
                elif game_screen.screen[i,j] == 4:
                    stdscr.addstr('P' + ' ',curses.color_pair(4))
                elif game_screen.screen[i,j] == 5:
                    stdscr.addstr('G' + ' ',curses.color_pair(5))
                elif game_screen.screen[i,j] == 6:
                    stdscr.addstr('=' + ' ',curses.color_pair(6))
            stdscr.addstr('\n')
        stdscr.refresh()
        stdscr.move(0, 0)
        time.sleep(0.2)


    def findNextFood(self, pacman, nextFood):
        pass


def main(stdscr):
    # initialize integer mask
    game_screen = GameScreen()
    game_screen.read_text_map('map.txt')
    game_screen.setScreenSize()
    #print game_screen
    main_game = Game()
    # pacman character
    pacman = PacMan('map.txt')
    pacman.setBody((game_screen.x/2) + 2,(game_screen.y/2))
    food = pacman.init_search_agent()
    # other dude
    ghost = Ghost()
    ghost.setBody((game_screen.x/2),(game_screen.y/2) - 1)
    ghost.set_map_file('map.txt')
    ghost.init_search_agent()
    ghost_trail = []
    # set past move as zero
    prev_move = 0
    g_prev_state = 1
    p_prev_state = 1
    #*** GAME LOOP ***
    f = False
    p_loc = (pacman.body[1],pacman.body[0])
    while True: # game loop
        # No need for keyboard input need in AI VS AI
        # generate new path
        g_start = (ghost.body[1],ghost.body[0])
        g_goal = p_loc
        p_start = (pacman.body[1],pacman.body[0])
        pacman.AI.search(p_start)
        ghost.AI.search(g_start,g_goal)
        g_trail = [(t[1], t[0]) for t in ghost.AI.path]
        p_trail = [(t[1], t[0]) for t in pacman.AI.path]
        # remove current position
        p_trail.pop(0)
        g_trail.pop(0)
        if g_prev_state == 1:
            #prev_state = game_screen.screen[trail[0][0],trail[0][1]]
            pacman.move(p_trail[0])
            p_loc = p_trail.pop(0)
            game_screen.screen[pacman.body[0],pacman.body[1]] = p_prev_state
            game_screen.screen[ghost.body[0],ghost.body[1]] = g_prev_state
            ghost.move(g_trail[0])
            g_prev_state = game_screen.screen[g_trail[0][0],g_trail[0][1]]
            p_prev_state = game_screen.screen[p_trail[0][0],p_trail[0][1]]
            g_trail.pop(0)
        else:
            g_prev_state = game_screen.screen[g_trail[0][0],g_trail[0][1]]
            p_prev_state = game_screen.screen[p_trail[0][0],p_trail[0][1]]
            game_screen.screen[ghost.body[0],ghost.body[1]] = g_prev_state
            game_screen.screen[pacman.body[0],pacman.body[1]] = p_prev_state
            pacman.move(p_trail[0])
            p_loc = p_trail.pop(0)
            ghost.move(g_trail[0])
            g_trail.pop(0)
        #*** REFRESH GAME SCREEN WITH LATEST POSITION ***
        game_screen.refresh()
        game_screen.impose([pacman.body],pacman.body_id)
        game_screen.impose([ghost.body],ghost.body_id)
        main_game.printScreen(stdscr,game_screen)
        time.sleep(1.10)
        #end loop


if __name__ == '__main__':
    #import sys
    #main(sys.stdout)
    curses.wrapper(main)
