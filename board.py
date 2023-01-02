from constants import BOARD_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, MENU_HEIGHT, OFFSET, BOARD_WIDTH, BOARD_HEIGHT, LINE_WIDTH
import pygame
from puzzle_generator import Puzzle_generator
import math
import random

class Board:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.grid = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.x = x
        self.y = y
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.selected = None
        self.font = pygame.font.SysFont("menlo", 40)
        self.puzzle_generator = Puzzle_generator()
        self.solution = None

        
    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.width, self.height)) 
        increment = self.width // BOARD_SIZE
        
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (self.x + increment * i, self.y),
                             (self.x + increment * i, self.y + self.height))
            pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y + increment * i),
                             (self.x + self.width, self.y + increment * i))
        if self.solution:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.grid[i][j] == '_':
                        pygame.draw.rect(self.screen, (0, 0, 0), (self.x + increment * i + OFFSET,
                                                                 self.y + increment * j + OFFSET,
                                                                 increment - OFFSET, increment - OFFSET))
                    elif self.grid[i][j] != '':
                        text = self.grid[i][j]
                        if len(self.grid[i][j]) == 1:
                            font = pygame.font.SysFont("menlo", 40)
                            rendered_text = font.render(text, True, (0, 0, 0))
                            self.screen.blit(rendered_text, (self.x + increment * i + increment // 2 - rendered_text.get_width() // 2,
                                                    self.y + increment * j + increment // 2 - rendered_text.get_height() // 2))     
                        else:
                            font = pygame.font.SysFont("menlo", 10)
                            direction = text[-3:]
                            text = text[:-3]
                            text_rows = [(text[i:i+7] + '-') for i in range(0, len(text), 7)]
                            if text_rows[-1][-1] == '-':
                                text_rows[-1] = text_rows[-1][:-1]
                            text_rows.append(direction)
                            middle_of_square = self.y + increment * j + increment // 2
                            y_placement = middle_of_square - ((len(text_rows) * 10 + 1// 2) * 1// 2)
                            for t in text_rows:
                                rendered_text = font.render(t, True, (0, 0, 0))
                                self.screen.blit(rendered_text, (self.x + increment * i + increment // 2 - rendered_text.get_width() // 2,
                                                        y_placement))  
                                y_placement += rendered_text.get_height()  
                                
                        
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x + increment * self.selected[0], self.y + increment * self.selected[1],
                                                       increment, increment), LINE_WIDTH)
            
    def mouse_click(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            pos = (pos[0] - self.x) // (self.width // BOARD_SIZE), (pos[1] - self.y) // (self.height // BOARD_SIZE)
            self.selected = pos
        else:
            return None
        
    def set_up_new_game(self):
        self.grid = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.selected = None
        self.solution = self.puzzle_generator.generate_puzzle()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.solution[i][j] == '_' or len(self.solution[i][j]) > 1:
                    self.grid[i][j] = self.solution[i][j]
        
    def check(self):
        if self.solution:
            done = True
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.grid[i][j] != self.solution[i][j]:
                        self.grid[i][j] = ''
                        done = False
                        
            return done
        return False

    def help(self):
        if self.solution:
            left = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.grid[i][j] == '' and self.solution[i][j] != '_']
            if len(left) == 0:
                return False
            rand_index = random.randint(0, len(left) - 1)
            self.grid[left[rand_index][0]][left[rand_index][1]] = self.solution[left[rand_index][0]][left[rand_index][1]]
            return True
        return False
    
    def key_pressed(self, key):
        if self.selected:
            if key == pygame.K_BACKSPACE:
                self.grid[self.selected[0]][self.selected[1]] = ''
            elif key == pygame.K_RETURN:
                self.selected = None
            elif key == pygame.K_LEFT:
                self.selected = (self.selected[0] - 1, self.selected[1]) if self.selected[0] > 0 else (BOARD_SIZE - 1, self.selected[1] - 1)
            elif key == pygame.K_RIGHT:
                self.selected = (self.selected[0] + 1, self.selected[1]) if self.selected[0] < BOARD_SIZE - 1 else (0, self.selected[1] + 1)
            elif key == pygame.K_UP:
                self.selected = (self.selected[0], self.selected[1] - 1) if self.selected[1] > 0 else (self.selected[0] - 1, BOARD_SIZE - 1)
            elif key == pygame.K_DOWN:
                self.selected = (self.selected[0], self.selected[1] + 1) if self.selected[1] < BOARD_SIZE - 1 else (self.selected[0] + 1, 0)
            else:
                if self.grid[self.selected[0]][self.selected[1]] != '_' and len(self.grid[self.selected[0]][self.selected[1]]) < 2:
                    self.grid[self.selected[0]][self.selected[1]] = chr(key)
                    self.selected = (self.selected[0] + 1, self.selected[1]) if self.selected[0] < BOARD_SIZE - 1 else (0, self.selected[1] + 1)
            if self.selected[1] > BOARD_SIZE - 1:
                self.selected = None
        
    