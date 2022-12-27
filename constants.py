from enum import Enum
import pygame
WINDOW_WIDTH = MENU_WIDTH = 770
WINDOW_HEIGHT = 870
MENU_HEIGHT = 100
GAME_NAME = "CROSSWORD"
STATES = Enum("STATES", "START PLAYING FINISHED")
BUTTONS = Enum("BUTTONS", "NEW_GAME CHECK HELP EXIT")
BOARD_SIZE = 11
BOARD_WIDTH = BOARD_HEIGHT = WINDOW_HEIGHT - MENU_HEIGHT
OFFSET = 2
LINE_WIDTH = 4
MENU_FONT_SIZE = 20
MENU_BUTTON_WIDTH = MENU_WIDTH // 6
MENU_BUTTON_HEIGHT = MENU_HEIGHT // 4