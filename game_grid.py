#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 20:45:52 2021

@author: stephaniedinh
"""
from random import seed
from random import randint
import numpy as np
import secrets
from users import User
from users import Game
from users import Suggestion


seed(1)

character_count = 0
width = 11
height = 11
weapons_list = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6']
character_list = ['Colonel Mustard','Miss Scarlet','PP','Mr. Green','MW','Mrs. Peacock']
gridline = []
for i in range(width):
    gridline.append('  ')
grid = []
for j in range(height):
    grid.append(list(gridline))

def populate_room(x_rng_start, x_rng_end, y_rng_start, y_rng_end, room_number):
    for i in range(x_rng_start, x_rng_end):
        for j in range(y_rng_start, y_rng_end):
            grid[i][j]=room_number

#populate rooms
populate_room(0,3,0,3,'r1')
populate_room(4,7,0,3,'r2')
populate_room(8,11,0,3,'r3')
populate_room(0,3,4,7,'r4')
populate_room(4,7,4,7,'r5')
populate_room(8,11,4,7,'r6')
populate_room(0,3,8,11,'r7')
populate_room(4,7,8,11,'r8')
populate_room(8,11,8,11,'r9')


#populate hallway
grid[3][1]='h '
grid[1][3]='h '
grid[1][7]='h '
grid[7][1]='h '
grid[3][5]='h '
grid[5][3]='h '
grid[7][5]='h '
grid[5][7]='h '
grid[9][7]='h '
grid[7][9]='h '
grid[9][3]='h '
grid[3][9]='h '

#populate secret passage
grid[10][10] = ' s'
grid[0][0] = 's '
grid[0][10] = ' s'
grid[10][0] = 's '

#function to print out formatted grid 
def format_grid(grid):
  for row in grid:
      for element in row:
          print(element, end=" ")
      print('')
  return grid

grid[2][4] = 'PP'
grid[10][3] = 'MW'
secretpassage_rooms = [[1,1],[1,9], [9,1],[9,9]]


format_grid(grid)

def start_game(game_id,pl1):
    new_game = Game(game_id,pl1)
    print("New game id is " + str(game_id) + " and current player is " + pl1.name + " " +pl1.character)
    return new_game


def createPlayer(id,name):
    character = secrets.choice(character_list)
    player = User(id,name,character)
    print("Player " + name +" is ready to join the game " +"as " + character)
    return player

def makeSuggestion(character,room,weapon):
    new_suggestion = Suggestion(character,room,weapon)
    return new_suggestion


#get position of character
def getCharacterPosition(character):
    #print(np.where(np.array(grid)==character))
    return np.asarray(np.where(np.array(grid)==character))


def moveCharacter(character, direction, steps):
    print(character, 'will be moving by', steps, 'steps in', direction, 'direction.')
    position = getCharacterPosition(character)
    x_pos = position[0][0]
    y_pos = position[1][0]

    if direction == 'left':
        y_pos = y_pos - steps
    elif direction == 'right':
        y_pos = y_pos + steps
    elif direction == 'top':
        x_pos = x_pos - steps
    elif direction == 'secretPassage': # secret passage moving condition
        for i in range(len(secretpassage_rooms)):
            secretpassage = secretpassage_rooms[i]
            if(secretpassage[0][0] != x_pos and secretpassage[1][0] != y_pos): # check if passage exists first in that room
                return
            else:
                print('secret passage exists.')
    else:
        x_pos = x_pos + steps

    print('New position of character is: (', x_pos, ',', y_pos, ')')
    print('Grid updation by', grid[x_pos][y_pos])
    if(x_pos > 0 and x_pos < 11 and y_pos > 0 and y_pos < 11):
     grid[x_pos][y_pos] = character
     print('After moving the character new grid is ::::::::')
     format_grid(grid)
    else:
     print('Character can not move outside the grid.')
    

characterPos = getCharacterPosition('PP')
characterPos_x = characterPos[0][0]
characterPos_y = characterPos[1][0]
print('PP is at position (', characterPos_x, ',', characterPos_y, ')')
# moveCharacter('c1', 'left', 6)






