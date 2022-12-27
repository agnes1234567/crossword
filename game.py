import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_NAME, STATES, OFFSET, \
    BOARD_SIZE, MENU_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, BUTTONS
from menu import Menu
from board import Board

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.menu = Menu(self.screen, 0, WINDOW_HEIGHT - MENU_HEIGHT + OFFSET)
        self.board = Board(self.screen,0,0)
        self.state = STATES.START
        self.running = True
    
    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.key_pressed(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click(event.pos)
            self.draw()  
            pygame.display.update()
        pygame.quit()
        
    def mouse_click(self, pos):
        if pos[1] > WINDOW_HEIGHT - MENU_HEIGHT:
            button = self.menu.mouse_click(pos)
            if button == BUTTONS.NEW_GAME:
                self.state = STATES.PLAYING
                self.board.set_up_new_game()
            elif button == BUTTONS.CHECK:
                if self.board.check():
                    print("Correct")
                else:
                    print("Incorrect")
            elif button == BUTTONS.HELP:
                self.board.help()
            elif button == BUTTONS.EXIT:
                self.running = False
        else:
            self.board.mouse_click(pos)

    
    def key_pressed(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        if self.board.selected:
            self.board.key_pressed(key)
    
    def draw(self):
        if self.state == STATES.START or self.state == STATES.PLAYING:
            self.menu.draw()
            self.board.draw()
        elif self.state == STATES.FINISHED:
            pass
    
