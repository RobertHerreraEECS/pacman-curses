#!/usr/bin/env python
'''
    @author: Robert Herrera
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
    #        if direction == 259 and prev_move != 258: # up
    #            return False
    #        elif direction == 258 and prev_move != 259: # down
    #            return False
    #        elif direction == 261 and prev_move != 260: # right
    #            return False
    #        elif direction == 260 and prev_move != 261: # left
    #            return False
    #        else:
    #            return True
    #
    #        return False
    
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
                    # pac man
                elif game_screen.screen[i,j] == 4:
                    stdscr.addstr('P' + ' ',curses.color_pair(4))
                elif game_screen.screen[i,j] == 5:
                    stdscr.addstr('G' + ' ',curses.color_pair(5))
                elif game_screen.screen[i,j] == 6:
                    stdscr.addstr('=' + ' ',curses.color_pair(6))
            stdscr.addstr('\n')

        stdscr.refresh()
        stdscr.move(0, 0)
        time.sleep(0.1)



def main(stdscr):
    
    # initialize integer mask
    game_screen = GameScreen()
    game_screen.read_text_map('map.txt')
    game_screen.setScreenSize()
    
    main_game = Game()
    
    # pacman character
    pacman = PacMan()
    pacman.setBody((game_screen.x/2) + 2,(game_screen.y/2))
    
    # other dude
    ghost = Ghost()
    ghost.setBody((game_screen.x/2),(game_screen.y/2) - 1)
    ghost.set_map_file('map.txt')
    ghost.init_search_agent()
    
    
    file = open('newfile.txt','rb')
    
    data = file.read()
    
    file.close()
    ghost_trail = []
    for match in re.findall(r'(?<=\().*?(?=\))',data):
        a,b = map(int,match.split(','))
        # do something with a and b, for example
        ghost_trail.append((a,b))
    
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    # set past move as zero
    prev_move = 0
    prev_state = 1
    
    '''
        *** GAME LOOP ***
        '''
    while True: # game loop
        
        '''
            *** CHECK USER INPUT ***
            '''
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        valid_moves = [258, 259, 260, 261]
        if c in valid_moves : # if user enters direction info
            # check for illegal moves
            illegal_move_status = main_game.check_move(c,prev_move)
            
            if illegal_move_status == False:
                # check direction value
                move_status = main_game.check_bounds(game_screen,c,pacman)
                if move_status == True:
                    game_screen.screen[pacman.body[0],pacman.body[1]] = 1
                    pacman.move(c,True)
                    main_game.check_wrapping(game_screen,c,pacman)
                    prev_move = c
            else:
                move_status = main_game.check_bounds(game_screen,prev_move,pacman)
                if move_status == True:
                    game_screen.screen[pacman.body[0],pacman.body[1]] = 1
                    pacman.move(prev_move,True)
                    main_game.check_wrapping(game_screen,prev_move,pacman)
        else: # else screen is updated
            # update logic
            # continue momentum on previous movement
            move_status = main_game.check_bounds(game_screen,prev_move,pacman)
            if move_status == True:
                game_screen.screen[pacman.body[0],pacman.body[1]] = 1
                pacman.move(prev_move,True)
                main_game.check_wrapping(game_screen,prev_move,pacman)
    
    
        '''
            *** GAME LOGIC ***
        '''
        # if gen new flag or curr list is empty
        # check for pacman location
        
        # generate new path
        start = (ghost.body[1],ghost.body[0])
        goal = (pacman.body[1],pacman.body[0])
        ghost.AI.search(start,goal)
        #trail = None
        trail = [(t[1], t[0]) for t in ghost.AI.path]
        # remove current position
        trail.pop(0)
        
        if prev_state == 1:
            #prev_state = game_screen.screen[trail[0][0],trail[0][1]]
            game_screen.screen[ghost.body[0],ghost.body[1]] = prev_state
            ghost.move(trail[0])
            prev_state = game_screen.screen[trail[0][0],trail[0][1]]
            trail.pop(0)
        else:
            prev_state = game_screen.screen[trail[0][0],trail[0][1]]
            game_screen.screen[ghost.body[0],ghost.body[1]] = prev_state
            ghost.move(trail[0])
            trail.pop(0)
        
        # move
        # else
        # move to next coord in current list
        
        
        '''
            *** REFRESH GAME SCREEN WITH LATEST POSITION ***
            '''
        game_screen.refresh()
        game_screen.impose([pacman.body],pacman.body_id)
        game_screen.impose([ghost.body],ghost.body_id)
        main_game.printScreen(stdscr,game_screen)
        time.sleep(0.08)
        # end loop


if __name__ == '__main__':
    #    main('a')
    curses.wrapper(main)
