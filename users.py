import pygame

from enum import Enum

def imageloading(path, w, h):
    img = pygame.image.load(path)
    scaledimg = pygame.transform.scale(img, (w, h))
    return scaledimg

class User:
    def __init__(self, id, name, character,current_position,cards, is_accusation: bool = False):
        self.id = id
        self.name = name
        self.character = character
        self.current_position = current_position
        self.cards = cards
        self.is_accusation = is_accusation


    def move_character(self, current_position, future_position):
        return current_position

    def draw(self,surface):
        """ Draw on surface """
        image = imageloading(self.character.value[1], 50, 100)
        # blit yourself at your current position
        surface.blit(image, (self.current_position[0], self.current_position[1]))

class Characters(Enum):
    Colonel_Mustard = 'Colonel Mustard','img/character-mustard.png','img/card-suspect-green.png'
    Miss_Scarlet = 'Miss Scarlet','img/character-scarlet.png','img/card-suspect-scarlet.png'
    PP = 'Mr. Plum','img/character-plum.png','img/card-suspect-plum.png'
    Green = 'Mr. Green','img/character-green.png','img/card-suspect-green.png'
    MW = 'Mr. White','img/character-white.png','img/card-suspect-white.png'
    Peacock = 'Mr. Peacock','img/character-peacock.png','img/card-suspect-peacock.png'

class Weapons(Enum):
    Candlestick = "candlestick", 'img/weapon-candlestick.png'
    Knife = "knife", 'img/weapon-knife.png'
    Pipe = "pipe",'img/weapon-pipe.png'
    Revolver = "revolver", 'img/weapon-revolver.png'
    Wrench = "wrench", 'img/weapon-wrench.png'
    Rope = "rope", 'img/weapon-rope.png'


class Rooms(Enum):
    Ballroom = 'ballroom', 'img/board-ballroom.png'
    Billiard = 'billiard','img/board-billiard_room.png'
    Conservatory = 'conservatory','img/board-conservatory.png'
    Dining = 'dining', 'img/board-dining_room.png'
    Hall = 'hall','img/board-hall.png'
    Kitchen = 'kitchen', 'img/board-kitchen.png'

class Game:
    def __init__(self, id, players,game_log,suggestions,accusations,confidential_case):
        self.id = id
        self.players = players
        self.game_log = game_log
        self.suggestions = suggestions
        self.accusations = accusations
        self.confidential_case = confidential_case
        print(self.id)

    def start_game(self, id, players):
        return id



class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1
