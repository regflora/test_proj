import random
import pygame
import sys
import time
import socket
import logging
import os
import re

import pygame_gui

from users import User
from users import Game
from respond import Respond
from _thread import *
from threading import Thread
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.core import IncrementalThreadedResourceLoader
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED
from pygame.rect import Rect
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame_gui.elements.ui_label import UILabel

from InputBox import InputBox
from users import Rooms
from users import Characters
from users import Weapons
from users import DropDown
from Guess import Accusation, Suggestion
from respond import Respond

from network import Network

from pygame.locals import *
from enum import Enum

from random import seed
from random import randint


# Received Data blob
received_data = None

# random initialization
seed(1)
sys_random = random.SystemRandom()

# screen set up
pygame.init()
screensizex = 1600
screensizey = 1000
screen_size = (screensizex, screensizey)
roomscalex = int(screensizex / 8)
roomscaley = int(screensizey / 5)
display_surface = pygame.display.set_mode(screen_size)
steps = 150
character_assigned = False
background_surface = pygame.Surface(screen_size)


# colors
white = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = BLACK
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
YELLOW = (255, 255,	0)
PURPLE = (128, 0, 128)
BLUE = (0,	0, 255)
DARKGRAY = (40, 40, 40)

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)
magenta = ((255, 0, 230))
brown = ((100, 40, 0))
forest_green = ((0, 50, 0))
navy_blue = ((0, 0, 100))
rust = ((210, 150, 75))
dandilion_yellow = ((255, 200, 0))
highlighter = ((255, 255, 100))
sky_blue = ((0, 255, 255))
light_gray = ((200, 200, 200))
dark_gray = ((50, 50, 50))
tan = ((230, 220, 170))
coffee_brown = ((200, 190, 140))
moon_glow = ((235, 245, 255))
pygame.display.set_caption('Clue Board Game')

game_logs = []
class SCREENS(Enum):
    START = 1
    ROOMS = 2


def create_large_text_box(game_log):
    return UITextBox(
            '<font face=Montserrat color=regular_text><font color=#E784A2 size=4.5>'
            '<br><b><u>Game Logs</u><br><br>'
            '</b> </font>'
             + str(game_log),
            pygame.Rect(1200, 30, 350, 580),
            manager=ui_manager,
            object_id='#text_box_1')


loader = IncrementalThreadedResourceLoader()
clock = pygame.time.Clock()
ui_manager = UIManager(
    screen_size, 'data/themes/theme_1.json', resource_loader=loader)
ui_manager.add_font_paths("Montserrat",
                          "data/fonts/Montserrat-Regular.ttf",
                          "data/fonts/Montserrat-Bold.ttf",
                          "data/fonts/Montserrat-Italic.ttf",
                          "data/fonts/Montserrat-BoldItalic.ttf")

load_time_1 = clock.tick()
ui_manager.preload_fonts([{'name': 'Montserrat', 'html_size': 4.5, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 2, 'style': 'italic'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 6,
                              'style': 'bold_italic'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'italic'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'regular'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'bold'},
                          {'name': 'fira_code', 'html_size': 2,
                              'style': 'bold_italic'}
                          ])
loader.start()
finished_loading = False
while not finished_loading:
    finished_loading, progress = loader.update()
load_time_2 = clock.tick()
print('Font load time taken:', load_time_2/1000.0, 'seconds.')

time_1 = clock.tick()
time_2 = clock.tick()


time_3 = clock.tick()

print('Time taken 1st window:', time_2/1000.0, 'seconds.')
print('Time taken 2nd window:', time_3/1000.0, 'seconds.')


ui_manager.print_unused_fonts()

# helper function to upload images


def imageloading(path, w, h):
    img = pygame.image.load(path)
    scaledimg = pygame.transform.scale(img, (w, h))
    return scaledimg


clueImg = imageloading('clue.jpeg', screensizex, screensizey)
display_surface.fill(white)
display_surface.blit(clueImg, (0, 0))
print('Welcome to Clue-Less!')


# Load and scale the image of rooms and halls
ballroomimg = imageloading('ballroom.png', roomscalex, roomscaley)
kitchenimg = imageloading('img/board-kitchen.png', roomscalex, roomscaley)
studyimg = imageloading('study.png', roomscalex, roomscaley)
loungeimg = imageloading('img/board-lounge.png', roomscalex, roomscaley)
libraryimg = imageloading('img/board-library.png', roomscalex, roomscaley)
hallimg = imageloading('hall.png', roomscalex, roomscaley)
billardsimg = imageloading('billiards_room.png', roomscalex, roomscaley)
conservatoryimg = imageloading('conservatory.png', roomscalex, roomscaley)
diningimg = imageloading('img/board-dining_room.png', roomscalex, roomscaley)
horiz = imageloading('hallway_horizontal.png', 100, 100)
verti = imageloading('hallway_vertical.png', 100, 100)
blackbg = imageloading('black-bkg.jpg', screensizex, screensizey)

# Character Tokens
Blueimg = imageloading('blue.png', 40, 40)
Redimg = imageloading('red.png', 40, 40)
Greenimg = imageloading('green.png', 40, 40)
Purpleimg = imageloading('purple.png', 40, 40)
Whiteimg = imageloading('white.png', 40, 40)
Yellowimg = imageloading('yellow.png', 40, 40)

white_block = imageloading("block.png", 2000, 50)

current_screen = SCREENS.START
html_text_line = None

display_start_characters = 1
end_player_turn_flag = 0
#turn_counter = -1
character_turn_start = 1
suggestion_flag = 0
move_character_flag = 0



def resetscreen():
    blackbg = imageloading('black-bkg.jpg', screensizex, screensizey)
    display_surface.blit(blackbg, (0, 0))


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def display_rooms(network):
    player = network.user
    display_surface.fill(white)
    display_surface.blit(ballroomimg, (0, 0))
    display_surface.blit(diningimg, (0, 300))
    display_surface.blit(kitchenimg, (0, 600))
    display_surface.blit(studyimg, (300, 0))
    display_surface.blit(loungeimg, (600, 0))
    display_surface.blit(libraryimg, (600, 300))
    display_surface.blit(billardsimg, (600, 600))
    display_surface.blit(billardsimg, (300, 300))
    display_surface.blit(hallimg, (300, 600))
    display_surface.blit(verti, (50, 200))
    display_surface.blit(verti, (50, 500))
    display_surface.blit(horiz, (500, 50))
    display_surface.blit(horiz, (200, 50))
    display_surface.blit(horiz, (200, 650))
    display_surface.blit(verti, (650, 200))
    display_surface.blit(horiz, (500, 650))

    display_surface.blit(verti, (350, 200))
    display_surface.blit(verti, (350, 500))
    display_surface.blit(horiz, (200, 350))
    display_surface.blit(horiz, (500, 350))

    display_surface.blit(verti, (650, 500))

    font_small = pygame.font.Font('freesansbold.ttf', 24)
    text = font_small.render(player.name, True, RED, white)
    textRect = text.get_rect()
    textRect.center = (1000, 20)
    display_surface.blit(text, textRect)

    text = font_small.render(player.character.value[0], True, RED, white)
    textRect = text.get_rect()
    textRect.center = (1000, 60)
    display_surface.blit(text, textRect)

    player_card_character = imageloading((player.cards[0].value[2]), 100, 150)
    display_surface.blit(player_card_character, (850, 90))

    player_card_weapon = imageloading((player.cards[2].value[1]), 100, 150)
    display_surface.blit(player_card_weapon, (950, 90))

    player_card_room = imageloading((player.cards[1].value[1]), 100, 150)
    display_surface.blit(player_card_room, (1050, 90))

    # text = font_small.render("GAME LOG", True, BLACK, white)
    # textRect = text.get_rect()
    # textRect.center = (1000, 400)
    # display_surface.blit(text, textRect)

def display_sug_text():
    font_small = pygame.font.Font('./data/fonts/Montserrat-Bold.ttf', 15)
    font_xsmall = pygame.font.Font('./data/fonts/Montserrat-Regular.ttf', 12)

    text = font_small.render("Suggestions/Accusations", True, PURPLE, white)
    textRect = text.get_rect()
    textRect.topleft = (815, 300-30)
    display_surface.blit(text, textRect)

    text = font_small.render("Disprove Suggestion", True, PURPLE, white)
    textRect = text.get_rect()
    textRect.topleft = (815, 565-30)
    display_surface.blit(text, textRect)

    #displaying labels for input boxes suggestions
    text1 = font_small.render("Enter suspect:", True, BLACK, white)
    textRect = text1.get_rect()
    textRect.topleft = (815, 320-30)
    display_surface.blit(text1, textRect)
    text1 = font_xsmall.render("(colonel_mustard, miss_scarlet, pp, green, mw, peacock)", True, BLACK, white)
    textRect = text1.get_rect()
    textRect.topleft = (815, 340-30)
    display_surface.blit(text1, textRect)

    text2 = font_small.render("Enter room:", True, BLACK, white)
    textRect = text2.get_rect()
    textRect.topleft = (815, 390-30)
    display_surface.blit(text2, textRect)
    text2 = font_xsmall.render("(ballroom, billiard, conservatory, dining, hall, kitchen)", True, BLACK, white)
    textRect = text2.get_rect()
    textRect.topleft = (815, 410-30)
    display_surface.blit(text2, textRect)

    text3 = font_small.render("Enter weapon:", True, BLACK, white)
    textRect = text3.get_rect()
    textRect.topleft = (815, 460-30)
    display_surface.blit(text3, textRect)
    text3 = font_xsmall.render("(candlestick, knife, pipe, revolver, wrench, rope)", True, BLACK, white)
    textRect = text3.get_rect()
    textRect.topleft = (815, 480-30)
    display_surface.blit(text3, textRect)

    text4 = font_small.render("Enter card to disprove:", True, BLACK, white)
    textRect = text4.get_rect()
    textRect.topleft = (815, 585-30)
    display_surface.blit(text4, textRect)

def display_sug_labels():
    # adding section for suggestion inputs display
    font_small = pygame.font.Font('./data/fonts/Montserrat-Bold.ttf', 15)
    font_xsmall = pygame.font.Font('./data/fonts/Montserrat-Regular.ttf', 12)

    text = font_small.render("Suggestions/Accusations", True, PURPLE, white)
    textRect = text.get_rect()
    textRect.topleft = (815, 300-30)
    display_surface.blit(text, textRect)

    text = font_small.render("Disprove Suggestion", True, PURPLE, white)
    textRect = text.get_rect()
    textRect.topleft = (815, 565-30)
    display_surface.blit(text, textRect)

    #displaying labels for input boxes suggestions
    text1 = font_small.render("Enter suspect:", True, BLACK, white)
    textRect = text1.get_rect()
    textRect.topleft = (815, 320-30)
    display_surface.blit(text1, textRect)
    text1 = font_xsmall.render("(colonel_mustard, miss_scarlet, pp, green, mw, peacock)", True, BLACK, white)
    textRect = text1.get_rect()
    textRect.topleft = (815, 340-30)
    display_surface.blit(text1, textRect)

    text2 = font_small.render("Enter room:", True, BLACK, white)
    textRect = text2.get_rect()
    textRect.topleft = (815, 390-30)
    display_surface.blit(text2, textRect)
    text2 = font_xsmall.render("(ballroom, billiard, conservatory, dining, hall, kitchen)", True, BLACK, white)
    textRect = text2.get_rect()
    textRect.topleft = (815, 410-30)
    display_surface.blit(text2, textRect)

    text3 = font_small.render("Enter weapon:", True, BLACK, white)
    textRect = text3.get_rect()
    textRect.topleft = (815, 460-30)
    display_surface.blit(text3, textRect)
    text3 = font_xsmall.render("(candlestick, knife, pipe, revolver, wrench, rope)", True, BLACK, white)
    textRect = text3.get_rect()
    textRect.topleft = (815, 480-30)
    display_surface.blit(text3, textRect)

    text4 = font_small.render("Enter card to disprove:", True, BLACK, white)
    textRect = text4.get_rect()
    textRect.topleft = (815, 585-30)
    display_surface.blit(text4, textRect)

def display_sug_boxes():
    #displaying input boxes for suggestions
    global suspect_input, room_input, weapon_input, disprove_input
    suspect_input = UITextEntryLine(relative_rect=Rect(840, 360-30, 325, 25), manager=ui_manager)
    room_input = UITextEntryLine(relative_rect=Rect(840, 430-30, 325, 25), manager=ui_manager)
    weapon_input = UITextEntryLine(relative_rect=Rect(840, 500-30, 325, 25), manager=ui_manager)
    disprove_input = UITextEntryLine(relative_rect=Rect(840, 625-30, 325, 25), manager=ui_manager)
    #return suspect_input, room_input, weapon_input

def display_userinput_options(network,character_room):
    ucards = []
    for c in network.user.cards:
        ucards.append((c.name).lower())
    font_xsmall = pygame.font.Font('./data/fonts/Montserrat-Regular.ttf', 12)
    text4 = font_xsmall.render(str(ucards).strip('[]'), True, BLACK, white)
    textRect = text4.get_rect()
    textRect.topleft = (815, 605-30)
    display_surface.blit(text4, textRect)

    text2 = font_xsmall.render("currently in: "+character_room, True, BLACK, white)
    textRect = text2.get_rect()
    textRect.topleft = (920, 390-30)
    display_surface.blit(text2, textRect)

def reset_input_suggestions():
    suspect_input.set_text('')
    room_input.set_text('')
    weapon_input.set_text('')


def reset_input_disprove():
    disprove_input.set_text('')

def display_suggest_button():
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    suggest_button = pygame.draw.rect(display_surface, YELLOW, (810, 535-30, 175, 25))
    text = font_small.render('Make a Suggestion', True, BLACK, YELLOW)
    textRect = text.get_rect()
    textRect.center = (845+50,535-30+15)
    display_surface.blit(text, textRect)
    return suggest_button

def display_disprove_button():
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    disprove_button = pygame.draw.rect(display_surface, YELLOW, (810, 660-30, 175, 25))
    text = font_small.render('Disprove', True, BLACK, YELLOW)
    textRect = text.get_rect()
    textRect.center = (845+50,660-30+15)
    display_surface.blit(text, textRect)
    return disprove_button

def display_pass_button():
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    disprove_button = pygame.draw.rect(display_surface, YELLOW, (990, 660-30, 175, 25))
    text = font_small.render('Pass', True, BLACK, YELLOW)
    textRect = text.get_rect()
    textRect.center = (1025+50,660-30+15)
    display_surface.blit(text, textRect)
    return disprove_button

def display_accusation_button():
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    accusation_button = pygame.draw.rect(display_surface, YELLOW, (990, 535-30, 175, 25))
    text = font_small.render('Make an Accusation', True, BLACK, YELLOW)
    textRect = text.get_rect()
    textRect.center = (1025+50,535-30+15)
    display_surface.blit(text, textRect)
    return accusation_button

def display_endturn_button():
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    endturn_button = pygame.draw.rect(display_surface, YELLOW, (990, 565-30, 175, 25))
    text = font_small.render('End Turn', True, BLACK, YELLOW)
    textRect = text.get_rect()
    textRect.center = (990+35+50,565-30+15)
    display_surface.blit(text, textRect)
    return endturn_button



class Player():  # remove this class and have to use User class
    """
    Spawn a player
    """

    def __init__(self, character, image):
            self.image = image
            self.x = 0
            self.y = 0
            self.frame = 0
            self.color = character
            self.rect = self.image.get_rect()

    def control(self, x, y):
        """
        control player movement
        """
        self.x += x
        self.y += y
        print("in control", self.x, self.y)

    def update(self):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.x
        self.rect.y = self.rect.y + self.y
        print("in update", self.rect.x, self.rect.y)

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


first_players = [User(1, "Alex", Characters.Colonel_Mustard, (0, 0), [Characters.PP, Rooms.Kitchen, Weapons.Rope]), User(
    2, "Kate", Characters.Miss_Scarlet, (600, 600), [Characters.MW, Rooms.Billiard, Weapons.Knife])]


def insert_list_of_users(user):
    if user.character.value[0] == 'Colonel Mustard':
        list_of_users[0] = user
    elif user.character.value[0] == 'Miss Scarlet':
        list_of_users[1] = user
    elif user.character.value[0] == 'Mr. Plum':
        list_of_users[2] = user
    elif user.character.value[0] == 'Mr. Green':
        list_of_users[3] = user
    elif user.character.value[0] == 'Mr. White':
        list_of_users[4] = user
    elif user.character.value[0] == 'Mr. Peacock':
        list_of_users[5] = user
    else:
        None


def update_list_of_users_pos(user, x_pos, y_pos):
    print("IN UPDATE USER POST METHOD")
#    print(user)
    user_idx = 0
    if user.character.value[0] == 'Colonel Mustard':
        user_idx = 0
    elif user.character.value[0] == 'Miss Scarlet':
        user_idx = 1
    elif user.character.value[0] == 'Mr. Plum':
        user_idx = 2
    elif user.character.value[0] == 'Mr. Green':
        user_idx = 3
    elif user.character.value[0] == 'Mr. White':
        user_idx = 4
    elif user.character.value[0] == 'Mr. Peacock':
        user_idx = 5
    else:
        -1
#    print(len(list_of_users))
#    for i in range(len(list_of_users)):
#        if list_of_users[i] != 0:
#            print("i= ",i, " , value= ", list_of_users[i].character.value[0])
#    print("user index=" , user_idx)
#    print("updating list of users obj=" , list_of_users[user_idx])
#    print("x_pos=", x_pos)
#    print("y_pos=", y_pos)
#    print("list of users x-coord at i = ", user_idx , ", val = " , list_of_users[user_idx].current_position[0])
#    print("list of users y-coord at i = ", user_idx , ", val = " , list_of_users[user_idx].current_position[1])
#    print(type(list_of_users))
#    print(type(list_of_users[user_idx].current_position))
#    print(type(list_of_users[user_idx].current_position[0]))
    list_of_users_current_pos_tmp = list(list_of_users[user_idx].current_position)
    list_of_users_current_pos_tmp[0] = x_pos
    list_of_users_current_pos_tmp[1] = y_pos
    list_of_users[user_idx].current_position = list_of_users_current_pos_tmp
#    print("after update pos...")
#    print("list of users x-coord at i = ", user_idx , ", val = " , list_of_users[user_idx].current_position[0])
#    print("list of users y-coord at i = ", user_idx , ", val = " , list_of_users[user_idx].current_position[1])
#    list_of_users[user_idx].current_position[0] = x_pos
#    list_of_users[user_idx].current_position[1] = y_pos

#    list_of_users_tmp[user_idx].current_position[0] = x_pos
#    list_of_users_tmp[user_idx].current_position[1] = y_pos
#    list_of_users = list_of_users_tmp



def display_characters(list_of_users, network):
    global purple, red, yellow, green, white
    global display_start_characters
    add_player_1 = User(1,"Alex1" , Characters.Colonel_Mustard, (75,50), [Characters.Colonel_Mustard, Rooms.Ballroom, Weapons.Pipe])
    add_player_2 = User(2,"Alex1" , Characters.Miss_Scarlet, (675,350), [Characters.Colonel_Mustard, Rooms.Ballroom, Weapons.Pipe])
    add_player_3 = User(3,"Alex1" , Characters.PP, (375,50), [Characters.Colonel_Mustard, Rooms.Ballroom, Weapons.Pipe])
    add_player_4 = User(4,"Alex1" , Characters.Green, (675,50), [Characters.Peacock, Rooms.Conservatory, Weapons.Candlestick])
    add_player_5 = User(5,"Alex1" , Characters.MW, (75,350), [Characters.Green, Rooms.Dining, Weapons.Revolver])
    add_player_6 = User(6,"Alex1" , Characters.Peacock, (375,350), [Characters.Miss_Scarlet, Rooms.Hall, Weapons.Wrench])

    if display_start_characters == 1:
        if network.user.character.value[0] == "Mr. Plum":
            network.user.current_position[0] = 375
            network.user.current_position[1] = 50
            list_of_users[0] = add_player_1
            list_of_users[1] = add_player_2
            list_of_users[3] = add_player_4
            list_of_users[4] = add_player_5
            list_of_users[5] = add_player_6
        elif network.user.character.value[0] == "Mr. Green":
            network.user.current_position[0] = 675
            network.user.current_position[1] = 50
            list_of_users[0] = add_player_1
            list_of_users[1] = add_player_2
            list_of_users[2] = add_player_3
            list_of_users[4] = add_player_5
            list_of_users[5] = add_player_6
        elif network.user.character.value[0] == "Mr. White":
            network.user.current_position[0] = 75
            network.user.current_position[1] = 350
            list_of_users[0] = add_player_1
            list_of_users[1] = add_player_2
            list_of_users[2] = add_player_3
            list_of_users[3] = add_player_4
            list_of_users[5] = add_player_6
        elif network.user.character.value[0] == "Mr. Peacock":
            network.user.current_position[0] = 375
            network.user.current_position[1] = 350
            list_of_users[0] = add_player_1
            list_of_users[1] = add_player_2
            list_of_users[2] = add_player_3
            list_of_users[3] = add_player_4
            list_of_users[4] = add_player_5
        elif network.user.character.value[0] == "Miss Scarlet":
            network.user.current_position[0] = 675
            network.user.current_position[1] = 350
            list_of_users[0] = add_player_1
            list_of_users[2] = add_player_3
            list_of_users[3] = add_player_4
            list_of_users[4] = add_player_5
            list_of_users[5] = add_player_6
        elif network.user.character.value[0] == "Colonel Mustard":
            network.user.current_position[0] = 75
            network.user.current_position[1] = 50
            list_of_users[1] = add_player_2
            list_of_users[2] = add_player_3
            list_of_users[3] = add_player_4
            list_of_users[4] = add_player_5
            list_of_users[5] = add_player_6

        display_start_characters-= 1
    print(network.user)
    for i in range(len(list_of_users)):
#        print("list of users LIST:")
#        print(list_of_users[i])
        if list_of_users[i] != 0:
#            print("i = ", i, ", value = ", list_of_users[i].character.value[0], ",x=", list_of_users[i].current_position[0],", y=", list_of_users[i].current_position[1])
            list_of_users[i].draw(display_surface)
            pygame.display.update()


move_dir_list = ["Left", "Right", "Up", "Down", "Secret Passage"]


def check_valid_move_dir(x_pos, y_pos, room):

    print("in check move validation...")
    print("x pos = ", x_pos)
    print("y pos = ", y_pos)
    print("room = ", room)
    move_dir_list = ["Left", "Right", "Up", "Down"]
    secret_passage = check_room_with_secret_passage(room)
    print("in check_valid_move_dir")
    print("secret passage = ", secret_passage)
    if room == 'ballroom':
        move_dir_list.remove("Left")
        move_dir_list.remove("Up")
        if _is_exit_blocked(x_pos + 150, y_pos):
            move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos, y_pos + 150):
            move_dir_list.remove("Down")
    elif room == 'study':
        move_dir_list.remove("Up")
        if _is_exit_blocked(x_pos + 150, y_pos):
            move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos - 150, y_pos):
            move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos, y_pos + 150):
            move_dir_list.remove("Down")
    elif room == 'lounge':
        move_dir_list.remove("Right")
        move_dir_list.remove("Up")
        if _is_exit_blocked(x_pos - 150, y_pos):
            move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos, y_pos + 150):
            move_dir_list.remove("Down")
    elif room == 'dining':
        move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos + 150, y_pos):
            move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos, y_pos + 150):
            move_dir_list.remove("Down")
        if _is_exit_blocked(x_pos, y_pos - 150):
            move_dir_list.remove("Up")
    elif room == 'library':
        move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos, y_pos - 150):
            move_dir_list.remove("Up")
        if _is_exit_blocked(x_pos - 150, y_pos):
            move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos, y_pos + 150):
            move_dir_list.remove("Down")
    elif room == 'kitchen':
        move_dir_list.remove("Left")
        move_dir_list.remove("Down")
        if _is_exit_blocked(x_pos + 150, y_pos):
            move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos, y_pos - 150):
            move_dir_list.remove("Up")
    elif room == 'hall':
        move_dir_list.remove("Down")
        if _is_exit_blocked(x_pos - 150, y_pos):
            move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos + 150, y_pos):
            move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos, y_pos - 150):
            move_dir_list.remove("Up")
    elif room == 'billiards':
        move_dir_list.remove("Right")
        move_dir_list.remove("Down")
        if _is_exit_blocked(x_pos - 150, y_pos):
            move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos, y_pos - 150):
            move_dir_list.remove("Up")
    elif room == 'conservatory':
        if _is_exit_blocked(x_pos - 150, y_pos):
            move_dir_list.remove("Left")
        if _is_exit_blocked(x_pos + 150, y_pos):
            move_dir_list.remove("Right")
        if _is_exit_blocked(x_pos, y_pos - 150):
            move_dir_list.remove("Up")
        if _is_exit_blocked(x_pos, y_pos + 150):
            move_dir_list.remove("Down")
    elif room == 'Hallway':
        if x_pos == 75:
            move_dir_list.remove("Left")
        if x_pos == 675:
            move_dir_list.remove("Right")
        if y_pos == 50 or y_pos == 650:
            move_dir_list.remove("Up")
            move_dir_list.remove("Down")
        elif y_pos == 200 or y_pos == 500:
            if "Left" in move_dir_list:
                move_dir_list.remove("Left")
            if "Right" in move_dir_list:
                move_dir_list.remove("Right")
        elif y_pos == 350:
            move_dir_list.remove("Up")
            move_dir_list.remove("Down")
    else:
        move_dir_list = ["Left", "Right", "Up", "Down"]
    if secret_passage == True:
        move_dir_list.append("Secret Passage")
    return move_dir_list


def update_move_dir_list(move_dir_list):
    list1.options = move_dir_list


def check_room_with_secret_passage(room):
    if room == 'ballroom' or room == 'lounge' or room == 'kitchen' or room == 'billiards':
        print("this room has a secret passage")
        return True
    else:
        print("this room does NOT have a secret passage")


def get_character_room(x_pos, y_pos):
    if(x_pos == 75.0 and y_pos == 50.0):
        return 'ballroom'
    elif(x_pos == 375.0 and y_pos == 50.0):
        return 'study'
    elif(x_pos == 675.0 and y_pos == 50.0):
        return 'lounge'
    elif(x_pos == 75.0 and y_pos == 350.0):
        return 'dining'
    elif(x_pos == 375.0 and y_pos == 350.0):
        return 'conservatory'
    elif(x_pos == 675.0 and y_pos == 350.0):
        return 'library'
    elif(x_pos == 75.0 and y_pos == 650.0):
        return 'kitchen'
    elif(x_pos == 375.0 and y_pos == 650.0):
        return 'hall'
    elif(x_pos == 675.0 and y_pos == 650.0):
        return 'billiards'
    else:
        return 'Hallway'


def get_room_coords(room):
    if 'ballroom' in room:
        x_pos = 75.0
        y_pos = 50.0
    elif 'study' in room:
        x_pos = 375.0
        y_pos = 50.0
    elif 'lounge' in room:
        x_pos = 675.0
        y_pos = 50.0
    elif 'dining' in room:
        x_pos = 75.0
        y_pos = 350.0
    elif 'conservatory' in room:
        x_pos = 375.0
        y_pos = 350.0
    elif 'library' in room:
        x_pos = 675.0
        y_pos = 350.0
    elif 'kitchen' in room:
        x_pos = 75.0
        y_pos = 650.0
    elif 'hall' in room:
        x_pos = 375.0
        y_pos = 650.0
    elif 'billiard' in room:
        x_pos = 675.0
        y_pos = 650.0

    return x_pos, y_pos


# def display_characters():
#    global purple, red, yellow, green,white
#    purple = Player('purple', Purpleimg)  # spawn player
#    purple.x = roomscalex / 2  # go to x
#    purple.y = roomscaley / 2  #
#    purple.draw(display_surface)
#
#    pygame.display.update()
#    # display_characters()


# def display_characters():
#     Purple = User(-1, 0, 'purple')
#     Purple.color = "Purple"
#     Purple.hexcolor = Purple

#     Blue = User(-1, 0, 'blue')
#     Blue.color = "Blue"
#     Blue.hexcolor = Blue

#     Green = User(-1, 0, 'green')
#     Green.color = "Green"
#     Green.hexcolor = Green

#     Red = User(-1, 0, 'red')
#     Red.color = "Red"
#     Red.hexcolor = Red

#     White = User(-1, 0, 'white')
#     White.color = "White"
#     White.hexcolor = White

#     Yellow = User(-1, 0, 'yellow')
#     Yellow.color = "Yellow"
#     Yellow.hexcolor = Yellow
#     listofplayers = [Purple, Blue, Green, Red, White, Yellow]

#     display_surface.blit(Redimg, (roomscalex*1.75, roomscaley*1.75))
#     display_surface.blit(Blueimg, (roomscalex*1.75, roomscaley/2))

#     display_surface.blit(Yellowimg, (roomscalex/2, roomscaley*1.75))

#     display_surface.blit(Purpleimg, (roomscalex / 2, roomscaley/2))

#     display_surface.blit(Whiteimg, (roomscalex/2, roomscaley * 3.25))

#     display_surface.blit(Greenimg, (roomscalex * 3.25, roomscaley/2))
#     pygame.display.update()
list1 = DropDown(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    900, 675, 200, 50,
    pygame.font.SysFont(None, 30),
    "Make a Move", ["Left", "Right", "Up", "Down"])


def check_player_turn(turn):
    global turn_counter
    print("in check player turn")
    print("turn=", turn)
    character = ""
    turn_counter = turn
    print("turn_counter=", turn_counter)
    if turn_counter == 0:
        character = "Colonel Mustard"
    elif turn_counter == 1:
        character = "Miss Scarlet"
    elif turn_counter == 2:
        character = "Mr. Plum"
    elif turn_counter == 3:
        character = "Mr. Green"
#        result = True
    elif turn_counter == 4:
        character = "Mr. White"
    elif turn_counter == 5:
        character = "Mr. Peacock"
    print("PLAYER TURN IS : ", character)
    return character

def check_end_player_turn():
    print("IN CHECK PLAYER TURN METHOD")
    #suggestion, accusation, move to hallway
    if end_player_turn_flag == 1:
#        send_next_player_turn(network)
        return True
   #exits blocked
    else:
        return False

def send_next_player_turn(network):
    print("**********IN SEND NEXT PLAYER***********")
    global character_turn_start
    global turn_counter
    if character_turn_start == 1:
        print("IN CHARACTER TURN START IF")
        turn_counter = 0
        character_turn_start = 0
    elif turn_counter == 2:
        print("IN MIDDLE IF")
        turn_counter = 0
    else:
        print("IN ELSE")
        turn_counter+= 1
    print("SENDING TURN COUNTER=" , turn_counter)
    network.send(Respond.PLAYER_COUNTER_S, turn_counter)
    print("*********END SEND NEXT PLAYER***********")

def send_next_player_turn_d(network):
    print("**********IN SEND NEXT PLAYER DISPROVE***********")
    global character_turn_start_d
    global turn_counter_d
    if character_turn_start_d == 1:
        print("IN CHARACTER TURN START IF")
        turn_counter_d = 0
        character_turn_start_d = 0
    elif turn_counter_d == 2:
        print("IN MIDDLE IF")
        turn_counter_d = 0
    else:
        print("IN ELSE")
        turn_counter_d+= 1
    print("SENDING TURN DISPROVE COUNTER=" , turn_counter_d)
    network.send(Respond.PLAYER_COUNTER_D, turn_counter_d)
    print("*********END SEND NEXT PLAYER DISPROVE***********")

def check_player_turn_d(turn_d):
    global turn_counter_d
    print("in check player turn disprove")
    print("turn=", turn_d)
    character = ""
    turn_counter_d = turn_d
    print("turn_counter=", turn_counter)
    if turn_counter_d == 0:
        character = "Colonel Mustard"
    elif turn_counter_d == 1:
        character = "Miss Scarlet"
    elif turn_counter_d == 2:
        character = "Mr. Plum"
    elif turn_counter_d == 3:
        character = "Mr. Green"
#        result = True
    elif turn_counter_d == 4:
        character = "Mr. White"
    elif turn_counter_d == 5:
        character = "Mr. Peacock"
    print("PLAYER TURN IS : ", character)
    return character


def next_disprove_turn(current_user, suggestor, disprove_tracker):
    #turn_list = ['Colonel Mustard','Miss Scarlet','Mr. Plum']#,'Mr. Green', 'Mr. White', 'Mr. Peacock']
    print("IN DISPROVE TRACKER 1:", disprove_tracker)

    print("LIST OF USERS SSS:", list_of_users)
    orig_list = []
    for i in list_of_users:
        orig_list.append((i.character.name).lower())
    print("ORIG LISTTT:", orig_list)

    suggestor_index = orig_list.index(suggestor)
    #current_index = turn_list.index(current_user)

    disprove_list = []
    start_index = suggestor_index
    for x in range(len(list_of_users)):
        disprove_list.append((list_of_users[(x + start_index) % len(list_of_users)].character.name).lower())
    print("DISPROVE LISTTT:", disprove_list)

    disprove_tracker = disprove_tracker + 1
    next_player_to_disprove = disprove_list[disprove_tracker]

    print("--NEXT PLAYER: "+ next_player_to_disprove + " DISPROVE OR PASS--")
    return next_player_to_disprove, disprove_tracker


def makeSuggestion(network, character_room, sug_room, suspect, sug_weap):

    global suggestion_flag
    global end_player_turn_flag
    print(" end_player_turn_flag = " , end_player_turn_flag)

    global suggestion

    print("---LIST OF USERS---")
    for user in list_of_users:
        print("ch name: ",user.character.name.lower())
        if user.character.name.lower() == suspect:
            suspect_user_obj = user



    #current_user = network.user.character.value[0]
    current_user = (network.user.character.name).lower()
    print("CURRENT USERRR:", current_user)
    if check_player_turn(turn_counter) == network.user.character.value[0]:
            #current user's turn
            if sug_room in character_room:
                suggestion = Suggestion(network.user, sug_room, sug_weap, suspect)
                message = suggestion.make_guess()

                suggestor = (network.user.character.name).lower()
                print("SUGGESTOR:", suggestor)
                disprove_tracker = 0 #first user (person who made the suggestion's index)
                closed = 0
                suggestion_list = [suspect, sug_room, sug_weap, suggestor, disprove_tracker, closed]
                network.send(Respond.SUGGESTION, suggestion_list)
                #next_player_name,disprove_tracker = next_disprove_turn(current_user, suggestor, disprove_tracker)

                # move suspect
                x_pos, y_pos = get_room_coords(sug_room)
                update_list_of_users_pos(suspect_user_obj, x_pos, y_pos)
                print(suspect + "user moved")

                suggestion_flag = 1
                #end_player_turn_flag = 1
                #print("--NEXT PLAYER: "+ next_player_name + " DISPROVE OR PASS--")
                #send_next_player_turn_d(network)
                smsg = []
                smsg.append("<br>"+message)
                network.send(Respond.GAME_LOG,smsg)
                return suggestion
            else:
                message = "Suggestion must include current room. Suggest again or end turn."
                print(message)
                game_logs.append(message)
                # network.send(Respond.SUGGESTION,[None,message])
                network.send(Respond.SUGGESTION, [None])  # ,message])
                #end_player_turn_flag = 1
                #send_next_player_turn(network)
                return

    else:
        print("not your turn")





def disproveSuggestion(network, suggestion_list, card):
    print("TOP DISPROVE SUG LIST", suggestion_list)
    suspect = suggestion_list[0]
    sug_room = suggestion_list[1]
    sug_weap = suggestion_list[2]
    suggestor = suggestion_list[3]
    disprove_tracker = suggestion_list[4]
    closed = suggestion_list[5]
    #current_username = (network.user.name).lower()

    suggestion = Suggestion(network.user, sug_room, sug_weap, suspect)
    if suggestion_list is None:
        reset_input_disprove()
    #player's turn to disprove
    msg_pass = []
    current_user_name = (network.user.character.name).lower()
    next_player_name, disprove_tracker = next_disprove_turn(current_user_name, suggestor, disprove_tracker)
    print("NEXT PLAYER NAME: ", next_player_name)
    print("CURRENT USER NAME ", current_user_name)
    print("DISPROVE COUNTER ", disprove_tracker)
    if next_player_name == current_user_name:
        if "pass" in card:
            print("IN PASSSSSS")
            #tracker[turn_counter_d] = 1
            #disprove_tracker = disprove_tracker + 1
            suggestion_list[-2] = disprove_tracker
            suggestion_list[-1] = 0 #closed = 0
            #msg_pass.append("<br>" +network.user.name + " was unable to disprove suggestion.")
            if closed == 0 and disprove_tracker == len(list_of_users) : #if suggestion not closed and all users have attempted
                msg = "<br> All other users have attempted disprove/pass"
                msg = "<br>" + suggestor + " - please accuse or end turn" #suggestions[-1][-3] = suggestor
                print(msg_pass)
                print("---ALL USERS DISPROVED: ",suggestion_list)
                network.send(Respond.SUGGESTION, suggestion_list)
                #writing to log
                msg_pass.append("<br>THE LAST USER (" + current_user_name + ") was unable to disprove suggestion.")
                network.send(Respond.GAME_LOG, msg_pass)
            else:
                #msg_pass.append("<br> next_player_username please disprove or pass.")
                print("---USER PASSED: ",suggestion_list)
                #send_next_player_turn_d(network)
                #disprove_tracker = disprove_tracker + 1
                suggestion_list[-2] = disprove_tracker
                print("PASS SUG LIST:", suggestion_list)
                network.send(Respond.SUGGESTION, suggestion_list)
                print("disprove tracker:", disprove_tracker)
                #writing to log
                msg_pass.append("<br>" +network.user.character.name + " was unable to disprove suggestion.")
                network.send(Respond.GAME_LOG, msg_pass)
                #network.send(Respond.DISPROVE_COUNTER, disprove_counter)
                return
        else:  # if there's an open suggestion
            message = suggestion.disprove_suggestion(network.user.cards, card)
            if "unable" in message:
                #tracker[turn_counter_d] = 1
                #disprove_tracker = disprove_tracker + 1
                suggestion_list[-2] = disprove_tracker
                suggestion_list[-1] = 0 #closed = 0
                network.send(Respond.SUGGESTION, suggestion_list)
                print(message)
                if closed == 0 and disprove_tracker == len(list_of_users):
                    msg = suggestor + " please accuse or end turn" #suggestions[-1][-3] = suggestor
                    print("---ALL USERS UNABLE TO DISPROVE: ", suggestion_list)
                    print(msg)
                    print("disprove counter:", disprove_tracker)
                    #writing to log
                    msg_pass.append("<br>LAST USER ("+network.user.name+") was unable to disprove suggestion.")
                    network.send(Respond.GAME_LOG, msg_pass)
                else:
                    #msg_list2.append("<br> next_player_username please disprove or pass.")
                    print("---USER DISPROVE ATTEMPT FAIL: ",suggestion_list)
                    network.send(Respond.SUGGESTION, suggestion_list)
                    #wrting to log
                    msg_pass.append("<br>" +network.user.name + " was unable to disprove suggestion.")
                    network.send(Respond.GAME_LOG, msg_pass)
                    #disprove_tracker = disprove_tracker + 1
                    suggestion_list[-2] = disprove_tracker
                    suggestion_list[-1] = 0
                    network.send(Respond.SUGGESTION, suggestion_list)
                    #network.send(Respond.DISPROVE_COUNTER, disprove_counter)
                    print("disprove counter:", disprove_tracker)
                    #send_next_player_turn_d(network)

                reset_input_disprove()
            else: #if suggestion was disproved
                #tracker[turn_counter_d] = 1
                #disprove_tracker = disprove_tracker + 1
                suggestion_list[-2] = disprove_tracker
                suggestion_list[-1] = 1 #closing suggestion
                print("SUGGESTION DISPROVED - NEXT USER TURN")
                msg_pass.append("<br> SUGGESTION WAS DISPROVED")
                network.send(Respond.GAME_LOG, msg_pass)
                network.send(Respond.SUGGESTION, suggestion_list)
                end_player_turn_flag = 1
                send_next_player_turn(network)
                reset_input_disprove()
            return
        return
    else:
        print("ERROR --- IT IS "+ next_player_name +"'S TURN'")
    return


def make_accusation(network, room, weapon, suspect):
    global end_player_turn_flag
    end_player_turn_flag = 1
    print(" end_player_turn_flag = " , end_player_turn_flag)
    if room in character_room:
        accusation = Accusation(player=network.user,
                                room=room, weapon=weapon, suspect=suspect)
        result = accusation.make_guess(game=new_game)
        accusation_list = [suspect, room, weapon]
        network.send(Respond.ACCUSATION, [accusation_list])
        game_logs.append(result)

        return accusation

    else:
        message = "Accusation is incorrect. Your turn has been lost."
        print(message)
        game_logs.append(message)
        network.send(Respond.ACCUSATION, [None])
        return


def display_start(pygame, network, clock):
    character_assigned_num = 0
    font_small = pygame.font.Font('freesansbold.ttf', 24)
    text = font_small.render('Input your name', True, RED, white)
    textRect = text.get_rect()
    textRect.center = (screensizex // 2, screensizey // 2 - 160)
    display_surface.blit(text, textRect)

    clock = pygame.time.Clock()
    input_box1 = InputBox(screensizex // 2 - 100,
                          screensizey // 2 - 130, 140, 32)
    done = False

    global name
    global character_assigned
    network.get_number_of_players()
    global received_data
    global list_of_users
    global number_of_players
    global character_turn_start
    p = 0
    while not received_data:
        p = p+1
    data = received_data.get('TOTAL_PLAYERS')
    print('data', data)
    if data is not None:
            global total_player_count
            print('data is', data)
            total_player_count = data
            print('players num', total_player_count)

    players_num = total_player_count
    print('players num', players_num)

    while not done:

            data = received_data.get('TOTAL_PLAYERS')
            players_num = data
         #   print('data', players_num)
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Connected players: ' +
                               str(players_num), True, RED, white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                input_box1.handle_event(event)
                input_box1.update()
                input_box1.draw(display_surface)
                pygame.display.update()


            textRect = text.get_rect()
            textRect.center = (170, 20)
            display_surface.blit(text, textRect)

            # name = input_box1.text
            if (input_box1.name_ready == True and character_assigned == False and players_num < 3):
                player_id = randint(0, 1000)
                name = input_box1.text
#                character = sys_random.choice(list(Characters))
                number_of_players = players_num
                print('players', number_of_players)
                character = list(Characters)[number_of_players]
                print(character)

#                card_weapon = sys_random.choice(list(Weapons))
                card_weapon = list(Weapons)[number_of_players]

                card_room = sys_random.choice(list(Rooms))
                card_character = sys_random.choice(list(Characters))
                cards = [card_character, card_room, card_weapon]
                print(cards)
                # create new player
                global new_player
                new_player = User(player_id, name, character, [75, 50], cards)
#                new_player = User(player_id,name,character,[0,0],cards)
                print(new_player.cards)
                network.user = new_player
                # character_assigned
                character_assigned = True
                network.connect_user_to_game(new_player)

                # network.get_number_of_players()
                # data = received_data.get('TOTAL_PLAYERS')
                # players_num = data
                # print('updated num',data)
                text = font_small.render("Hi, " + new_player.name + " you are playing for " + str(
                    new_player.character.value[0]), True, RED, white)
                textRect = text.get_rect()
                textRect.center = (screensizex // 2, screensizey // 2)
                display_surface.blit(text, textRect)

                character_image = imageloading((character.value[1]), 150, 200)
                display_surface.blit(
                    character_image, (screensizex // 2 - 50, screensizey // 2 + 25))
#                if turn_counter == -1:
#                    send_next_player_turn()
#                if character_turn_start == 0 and new_player.character.value[0] == "Colonel Mustard":

#                character_turn_start = 1
                send_next_player_turn(network)
                list_of_users = [0, 0, 0, 0, 0, 0]

                insert_list_of_users(first_players[0])
                insert_list_of_users(first_players[1])
                insert_list_of_users(new_player)
                input_box1.name_ready = False

                m1 = new_player.name + "has joined game"
                m2 = new_player.name + " playing as " + new_player.character.name
                print(m1, m2)

            if (input_box1.name_ready == True and character_assigned == False and players_num > 4):
                text = font_small.render(
                    "Hi,you cannot join the game at this point ", True, RED, white)
                textRect = text.get_rect()
                textRect.center = (screensizex // 2, screensizey // 2)
                display_surface.blit(text, textRect)

            # start the game
            if(players_num == 3):
                game_id = randint(0, 1000)
                players = network.get_connected_users()
                global eachInASeparateLine
                global game_logs
                game_logs = []
                game_logs.append(
                    '<br>' + new_player.name + " has joind game as a " + new_player.character.name)

                suggestions = [{"suggestion": None, "closed": 1}]
                accusations = [{"accusation": None, "closed": 1}]
                character = sys_random.choice(list(Characters))
                weapon = sys_random.choice(list(Weapons))
                room = sys_random.choice(list(Rooms))
                confidential_case = [character, room, weapon]
                global new_game
                new_game = Game(game_id, players, game_logs,
                                suggestions, accusations, confidential_case)
                print('logs', game_logs)
                display_rooms(network)
                        # network.get_number_of_players()
                print("PRINT NUMBER OF PLAYERS")
                        # print(network.receive())

                print("END")
                display_characters(list_of_users, network)
                display_sug_labels()
                display_chat_labels()
                display_sug_boxes()
                display_chatBox()
                suggest_button = display_suggest_button()
                disprove_button = display_disprove_button()
                pass_button = display_pass_button()
                #accusation_button = display_accusation_button()
                chat_button = display_chat_button()
                global current_screen
                current_screen = SCREENS.ROOMS
                done = True


        # global player_1
        # player_1 = createPlayer(player_id, player_name)
        # game_id = randint(0, 1000)
        # start_game(game_id, player_1)
        # print(getCharacterPosition(player_1.character))


def display_chat_labels():
    # adding section for suggestion inputs display
    font = pygame.font.Font('./data/fonts/Montserrat-Bold.ttf', 20)
    font1 = pygame.font.Font('./data/fonts/Montserrat-Bold.ttf', 14)

    text = font.render("Chat with Players", True, PURPLE, white)
    text1 = font1.render("Send Messages Here:", True, BLACK, white)
    textRect1 = text1.get_rect()
    textRect1.topleft = (1250, 700 - 30)
    textRect = text.get_rect()
    textRect.topleft = (1300, 650 - 30)
    display_surface.blit(text1, textRect1)
    display_surface.blit(text, textRect)

def display_chatBox():

    global chat_box
    chat_box = UITextEntryLine(relative_rect=Rect(
        1250, 730 - 40, 300, 40), manager=ui_manager)



def display_chat_button():
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    chat_button = pygame.draw.rect(
        display_surface, COLOR_ACTIVE, (1330, 760 - 30, 150, 30))
    text = font_small.render('Send Message', True, BLACK, COLOR_ACTIVE)
    textRect = text.get_rect()
    textRect.center = (1330 + 70, 760 - 30 + 15)
    display_surface.blit(text, textRect)
    return chat_button


def reset_chat():
    chat_box.set_text('')


"""
Create main function here when all code is done
"""


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


def _is_exit_blocked(x_pos, y_pos):
    for i in range(len(list_of_users)):
        x_pos_blocked = 0
        y_pos_blocked = 0
        if list_of_users[i].current_position[0] == x_pos:
            x_pos_blocked = 1
        if list_of_users[i].current_position[1] == y_pos:
            y_pos_blocked = 1
        if x_pos_blocked == 1 and y_pos_blocked == 1:
            return True
    else:
        return False

def _is_all_exit_blocked(room):
    result = False
    if room == "ballroom":
        if(_is_exit_blocked(75,200) and _is_exit_blocked(225,50)):
            result = True
    elif room == "study":
        if(_is_exit_blocked(225,50) and _is_exit_blocked(375,200) and _is_exit_blocked(525,50)):
            result = True
    elif room == "lounge":
        if(_is_exit_blocked(675,200) and _is_exit_blocked(525,50)):
            result = True
    elif room == "dining":
        if(_is_exit_blocked(75,200) and _is_exit_blocked(75,500) and _is_exit_blocked(225,350)):
            result = True
    elif room == "conservatory":
        if(_is_exit_blocked(225,350) and _is_exit_blocked(525,350) and _is_exit_blocked(375,200) and _is_exit_blocked(375,500)):
            result = True
    elif room == "library":
        if(_is_exit_blocked(675,200) and _is_exit_blocked(675,500) and _is_exit_blocked(525,350)):
            result = True
    elif room == "kitchen":
        if(_is_exit_blocked(75,500) and _is_exit_blocked(225,650)):
            result = True
    elif room == "hall":
        if(_is_exit_blocked(225,650) and _is_exit_blocked(375,500) and _is_exit_blocked(525,650)):
            result = True
    elif room == "billiards":
        if(_is_exit_blocked(525,650) and _is_exit_blocked(675,500)):
            result = True
    print("_is_all_exit_blocked...", result)
    return result

def _is_corner_room(room):
    if room == "ballroom" or room == "lounge" or room == "kitchen" or room == "billiards":
        return True
    else:
        return False

# move character accordin to given direction
def move_characters(network, player, room, direction):
    global move_character_flag
    global end_player_turn_flag
    print("************IN MOVE CHARACTERS*************")
    print("turn_counter=" , turn_counter)
    print("first param = " , check_player_turn(turn_counter))
    print("second param = ", player.character.value[0])
    print("**********END MOVE CHARACTERS**************")
    if check_player_turn(turn_counter) != player.character.value[0]:
       # print("END_PLAYER_TURN_FLAG = ", end_player_turn_flag)
        print("\nNOT YOUR TURN\n")
        return
    else:
        print("IN ELSE")
        print("END_PALYER_TURN_FLAG = ", end_player_turn_flag)
        #update flag if character is moved to hallway
#        check_move_character_to_hallway(player, room, direction)
        move_character_flag = 1
        #end_player_turn_flag = 1
        if(direction == 'Left'):
            player.current_position[0] -= steps
        elif (direction == 'Right'):
            player.current_position[0] += steps
        elif (direction == 'Up'):
            player.current_position[1] -= steps
        elif (direction == 'Secret Passage'):
            if room == 'ballroom':
                # move right and down (700,700)
    #            purple.control(600, 600)
                player.current_position[0] += 600
                player.current_position[1] += 600
            if room == 'billiards':
                # move to 100,100
    #            purple.control(-600,-600)
                player.current_position[0] -= 600
                player.current_position[1] -= 600
            if room == 'lounge':
                # 100,700
                player.current_position[0] -= 600
                player.current_position[1] += 600
    #            purple.control(-600,600)
            if room == 'kitchen':
                # move to 700,100
    #            player.control(600,-600)
                player.current_position[0] += 600
                player.current_position[1] -= 600
        else:
            player.current_position[1] += steps
        # move_msgs = []
        # move_msgs.append("<br>" +  network.user.character.value[0] + " moved to room " + room + "<br>")
        # network.send(Respond.GAME_LOG, move_msgs)
        if check_move_character_to_hallway(network, player, room, direction) == True:
            return
        else:
            check_move_character_and_make_suggestion(room,network)
            return
#            return 1
def check_move_character_and_make_suggestion(room,network):
    global end_player_turn_flag
    print("*******IN CHECK MOVE CHAR AND MAKE SUG*******")
    if room == "Hallway" and move_character_flag == 1 and suggestion_flag == 1:
        print("IN IF STATEMENT")
        end_player_turn_flag = 1
        print(" end_player_turn_flag =", end_player_turn_flag)
        send_next_player_turn(network)
    print("******END CHECK MOVE CHAR AND MAKE SUG******")

# move character accordin to given direction
def check_move_character_to_hallway(network, player, room, direction):
    global end_player_turn_flag
    print("*******IN CHECK MOVE CHAR TO HALLWAY *******")
    print("room =", room)
    print("dir = ", direction)
    if room != "Hallway" and direction != "Secret Passage":
        print("\n IN IF STATEMENT\n")
        end_player_turn_flag = 1
        send_next_player_turn(network)
        print(" end_player_turn_flag =", end_player_turn_flag)
        print("*******IN CHECK MOVE CHAR TO HALLWAY *******")
        return True



def listen_incoming_msgs(network):
    global received_data
    received_data = {}
    global logs
    while True:
        value = network.receive()
        print('valueeee', value)
        if(value['type'] is Respond.TOTAL_PLAYERS):
            received_data = {'TOTAL_PLAYERS': value['data']}
        if (value['type'] is Respond.GAME_LOG):
            print('here', value)
            global html_text_line
            if value['data'] is not None:
                for i in value['data']:
                    received_data.setdefault('GAME_LOG', []).append(i)
            logs = received_data.get('GAME_LOG')
            if html_text_line is not None: #fixed issue of gamelog scrolling
                html_text_line.kill()
            html_text_line = create_large_text_box(listToString(logs))
        if (value['type'] is Respond.SUGGESTION):
            print("suggestion added to received data")
            print(value['data'])
            # for i in value['data']:
            #     received_data.setdefault('SUGGESTION', []).append(i)
            received_data.setdefault('SUGGESTION', []).append(value['data'])
        if (value['type'] is Respond.ACCUSATION):
            print("Accusation added to received data")
            print(value['data'])
            #received_data.setdefault('ACCUSATION', []).append(value['data'])
            for i in value['data']:
                received_data.setdefault('ACCUSATION', []).append(i)
        if(value['type'] is Respond.CHARACTER_MOVE):
            received_data.setdefault('CHARACTER_MOVE', []).append(value['data'])
#            print("printing receiving CHARACTER MOVE data" , value['data'])
            test = received_data.get('CHARACTER_MOVE')
            print("printing receiving CHARACTER MOVE data" , value['data'])
            print(value['data'][0])
            print(value['data'][1])
            print(value['data'][2])
            update_list_of_users_pos(value['data'][0], value['data'][1], value['data'][2])
            display_rooms(network)
            display_characters(list_of_users, network)
            display_sug_labels()
            display_chat_labels()
            chat_button = display_chat_button()
            suggest_button = display_suggest_button()
            print("character move msg..." , test)
        if(value['type'] is Respond.PLAYER_COUNTER_S):
            received_data.setdefault('PLAYER_COUNTER_S', []).append(value['data'])
#            test = received_data.get('PLAYER_COUNTER_S')
            check_player_turn(value['data'])
            print("PLAYER_COUNTER_S = " , value['data'])
        # if(value['type'] is Respond.DISPROVE_COUNTER):
        #     print("DISPROVE COUNTER: ", value['data'])
        #     received_data = {'DISPROVE_COUNTER': value['data']}
        if(value['type'] is Respond.CHARACTER_MOVE_MSG):
            received_data = {'CHARACTER_MOVE_MSG': value['data']}
        print("Msg received", received_data)


def main() -> None:
    count = 0
    running = True
    network = Network()
    global clock
    global game_logs

    clock = pygame.time.Clock()
    t = Thread(target=listen_incoming_msgs, args=(network,))
    t.daemon = True
    t.start()
    while running:
        time_delta = clock.tick(60) / 1000.0
        count = count + 1
        clock.tick(60)
        event_list = pygame.event.get()
        for event in event_list:

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()

            # if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_f:
            #        print('hi')
            #    if event.key == pygame.K_k:
            #        html_text_line.kill()
            #    if event.key == pygame.K_b:
            #        html_text_line = create_large_text_box()

            if event.type == pygame.MOUSEBUTTONUP:
                # resetscreen()
                pos = pygame.mouse.get_pos()
                if clueImg.get_rect().collidepoint(pos):
                    if current_screen == SCREENS.START:
                        display_surface.fill(white)
                        display_start(pygame, network, clock, )
                        network.send(Respond.GAME_LOG, game_logs)


                    elif current_screen == SCREENS.ROOMS:
                        # if received_data:
                        #     data = received_data.get('GAME_LOG')
                        #     print('game log', data)
                        #     html_text_line = create_large_text_box(
                        #             listToString(data))
                        #
                        character_room = get_character_room(
                            network.user.current_position[0], network.user.current_position[1])
                        new_move_list = check_valid_move_dir(network.user.current_position[0],
                                                             network.user.current_position[1], character_room)
                        #display_rooms(network)
                        #display_characters(list_of_users, network)

                        #display_sug_boxes()
                        #display_chatBox()


#                        network.user.draw(display_surface)
#                        pygame.display.update()
                        update_move_dir_list(new_move_list)


                        suggest_button = display_suggest_button()
                        accusation_button = display_accusation_button()
                        chat_button = display_chat_button()
                        endturn_button = display_endturn_button()

                        # display_sug_boxes()
                        # display_chatBox()

                        if chat_button.collidepoint(pos):
                            msgs = []
                            msg = chat_box.get_text()
                            msgs.append('<br>' + new_player.name + ": " + msg)
                            network.send(Respond.GAME_LOG, msgs)
                            reset_chat()

                        display_sug_text()
                        display_userinput_options(network, character_room)


                        if suggest_button.collidepoint(pos):
                            sug_sus = (suspect_input.get_text()
                                       ).lower().strip()
                            sug_room = (room_input.get_text()).lower().strip()
                            sug_weap = (weapon_input.get_text()
                                        ).lower().strip()
                            # print(sug_room,sug_sus,sug_weap)
                            makeSuggestion(network, character_room,
                                           sug_room, sug_sus, sug_weap)
                            # resetting input boxes
                            reset_input_suggestions()

                        disprove_button = display_disprove_button()
                        pass_button = display_pass_button()

                        if disprove_button.collidepoint(pos):
                            #network.send(Respond.SINGLE_USER,[2,"clear"])
                            card = (disprove_input.get_text()).lower().strip()
                            #disproveSuggestion(network, None, card)
                            suggestions = received_data.get('SUGGESTION')
                            if suggestions is not None:
                                last_suggestion = suggestions[-1]
                                print("disprove button ",last_suggestion)
                                if last_suggestion is not None:  # if there's suggestion in there
                                    disproveSuggestion(network, last_suggestion, card)#, log_players)

                        if pass_button.collidepoint(pos):
                            #network.send(Respond.SINGLE_USER,[1,"hello"])
                            suggestions = received_data.get('SUGGESTION')
                            print("pass button 1 ", suggestions)
                            if suggestions is not None:
                                last_suggestion = suggestions[-1] #suggestion list
                                print("pass button 2", last_suggestion)
                                if last_suggestion is not None: #if there's suggestion in there
                                    disproveSuggestion(network,last_suggestion, "pass")

                        if accusation_button.collidepoint(pos):
                            accu_sus = (suspect_input.get_text()).lower().strip()
                            accu_room = (room_input.get_text()).lower().strip()
                            accu_weapon = (weapon_input.get_text()).lower().strip()
                            make_accusation(network, accu_room, accu_weapon, accu_sus)
                            reset_input_suggestions()

                        if endturn_button.collidepoint(pos):
                            end_player_turn_flag = 1
                            print("ENDING PLAYER TURN")
                            send_next_player_turn(network)
                            #next player turn



                        list1.draw(display_surface)
                        if selected_option >= 0:
                            list1.main = list1.options[selected_option]
                            print('list', list1.main)

                            character_room = get_character_room(network.user.current_position[0], network.user.current_position[1])
                            move_characters(network,network.user,character_room,list1.main)
#                            character_room = get_character_room(network.user.current_position[0], network.user.current_position[1])


                            message = [network.user, network.user.current_position[0], network.user.current_position[1]]
                            network.send(Respond.CHARACTER_MOVE, message)

                            if network.user is not None:
                                #display_rooms(network)
                                list1.draw(display_surface)

                                print("AT BOTTOM")

                                # display_characters(list_of_users, network)
                                # display_sug_boxes()
                                # display_chatBox()
                                #
                                # network.user.draw(display_surface)

            ui_manager.process_events(event)
            # Draws the surface object to the screen.
            ui_manager.update(time_delta)
            ui_manager.draw_ui(display_surface)
            selected_option = list1.update(event_list)
            pygame.display.update()

# start_new_thread(listen_incoming_msgs, ())
# start_new_thread(main_thread, ())
# Thread(target=main_thread, args=()).start()

if __name__ == "__main__":
    main()
