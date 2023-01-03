import random
from z3 import *
import pygame
import requests
import json
from constants import BOARD_SIZE
SYNONYMS_URL = "https://synonymord.se/api/?q={word}"
SYN_SYM = '0'
END_W_SYM = '/'
EMPTY_SYM = '_'
illegal_words = ['kåk', 'osa', 'jeppe', 'geni', 'gen', 'animerad', 'era',\
    'mer', 'rad', 'kon', 'vågrät', 'rät', 'våg', 'affär', 'färd', 'ifall', \
        'fall', 'all', 'fal', 'koj', 'åse', 'kapning', 'kap', 'rop', 'gren', \
            'där', 'ned', 'ren', 'ärbar', 'bar', 'instabil', 'stabil', 'stab',\
                'bil', 'opp', 'damm', 'dam']

ALPHA_TO_NUM = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,  'f': 5, 'g': 6,
         'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
         'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
         'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, 'å': 26, 'ä': 27,
         'ö': 28, '_': 29}

NUM_TO_ALPHA = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h',
                8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o',
                15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v',
                22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: 'å', 27: 'ä', 28: 'ö',
                29: '_'}

LETTER_FREQ = {'a': 0.104, 'b': 0.0131, 'c': 0.0171, 'd': 0.049, 'e': 0.0985, 'f': 0.0181, 'g': 0.0344,
                'h': 0.0285, 'i': 0.0501, 'j': 0.009, 'k': 0.0324, 'l': 0.0481, 'm': 0.0355, 'n': 0.0845,
                'o': 0.0406, 'p': 0.0157, 'q': 0.0001, 'r': 0.0788, 's': 0.0532, 't': 0.0889, 'u': 0.0186,
                'v': 0.0255, 'w': 0, 'x': 0.0011, 'y': 0.0049, 'z': 0.0004, 'å': 0.0166, 'ä': 0.021,
                'ö': 0.015}

NUM_FREQ = {0: 0.104, 1: 0.0131, 2: 0.0171, 3: 0.049, 4: 0.0985, 5: 0.0181, 6: 0.0344,
            7: 0.0285, 8: 0.0501, 9: 0.009, 10: 0.0324, 11: 0.0481, 12: 0.0355, 13: 0.0845,
            14: 0.0406, 15: 0.0157, 16: 0.0001, 17: 0.0788, 18: 0.0532, 19: 0.0889, 20: 0.0186,
            21: 0.0255, 22: 0, 23: 0.0011, 24: 0.0049, 25: 0.0004, 26: 0.0166, 27: 0.021,
            28: 0.015}

class Word():
    def __init__(self, word, row, col, direction):
        self.word = word
        self.start_row = row
        self.start_col = col
        self.direction = direction
        
    def __str__(self):
        return self.word + ', ' + str(self.start_row) + ', ' + str(self.start_col) + ', ' + self.direction + \
            ', ' + str(len(self.word)) 
    def get_word(self):
        return self.word
    
    def get_start_row(self):
        return self.start_row

    def get_start_col(self):
        return self.start_col
    
    def get_direction(self):
        return self.direction

class Puzzle_generator():
    
    def __init__(self):
        self.solution = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.words = []
        with open('words_no_spec.txt', 'r') as f:
            for line in f:
                word = line.strip()
                if len(word) < BOARD_SIZE and len(word) > 2 and word not in illegal_words:
                    numbers = [ALPHA_TO_NUM[letter] for letter in word]
                    if len(numbers) < BOARD_SIZE - 1:
                        numbers += [ALPHA_TO_NUM[EMPTY_SYM]]
                    self.words.append(numbers)
        self.numbers_to_choose_from = []
        for key in NUM_FREQ:
            self.numbers_to_choose_from += [key] * int(NUM_FREQ[key] * 100)
        self.words_in_grid = []
                
    
    def generate_puzzle(self):
        grid = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.solver = Solver()
        possible_numbers = [key for key in NUM_FREQ]
        
        print('Adding constraints...')
        for row in range(1,BOARD_SIZE):
            for col in range(1,BOARD_SIZE):
                if row % 2 == 0 and col % 2 == 0:
                    grid[row][col] = ALPHA_TO_NUM[EMPTY_SYM]
                else:
                    var = Int('%s_%s' % (row, col))
                    self.solver.add(var >= min(possible_numbers), var <= max(possible_numbers))
        
        print('Basic number constraints added')
        
        for row in range(1,BOARD_SIZE):
            if row % 2 != 0:
                variables = [Int('%s_%s' % (row, col)) for col in range(1,BOARD_SIZE)]
                word_constraints = []
                for word in self.words:
                    shifts = [i for i in range(len(variables) - len(word) + 1)]
                    for shift in shifts:
                        word_constraints.append(And([variables[i + shift] == word[i] for i in range(len(word))]))
                self.solver.add(Or(word_constraints))
        
        print('Horizontal word constraints added')
            
        for col in range(1,BOARD_SIZE):
            if col % 2 != 0:
                variables = [Int('%s_%s' % (row, col)) for row in range(1,BOARD_SIZE)]
                word_constraints = []
                for word in self.words:
                    shifts = [i for i in range(len(variables) - len(word) + 1)]
                    for shift in shifts:
                        word_constraints.append(And([variables[i + shift] == word[i] for i in range(len(word))]))
                self.solver.add(Or(word_constraints))
        
        print('Vertical word constraints added')
        
        variable_rows = []
        for row in range(1,BOARD_SIZE):
            if row % 2 != 0:
                variables = [Int('%s_%s' % (row, col)) for col in range(1,BOARD_SIZE)]
                variable_rows.append(variables)
        
        variable_cols = []
        for col in range(1,BOARD_SIZE):
            if col % 2 != 0:
                variables = [Int('%s_%s' % (row, col)) for row in range(1,BOARD_SIZE)]
                variable_cols.append(variables)
        
                    
                        
        
                
        print('Constraints added, checking for solution...')
                 
                    
                
                    
        
        
        
        
        res = self.solver.check()
        if res == sat:
            grid = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
            for row in range(0,BOARD_SIZE):
                for col in range(0,BOARD_SIZE):
                    if row == 0 or col == 0 or (row % 2 == 0 and col % 2 == 0):
                        grid[col][row] = '_'
                    else:
                        var = Int('%s_%s' % (row, col))
                        grid[col][row] = self.solver.model()[var].as_long()
                        
            self.grid = grid
            self.save_words_in_grid()
            for word_obj in self.words_in_grid:
                print(word_obj)
            self.remove_redudant_letters()
            self.print_grid()
                            
                    
        elif res == unsat:
            print('Unsat')



    def remove_redudant_letters(self):
        positions_to_keep = []
        
        for word_obj in self.words_in_grid:
            if word_obj.get_direction() == 'across':
                row = word_obj.get_start_row()
                start_col = word_obj.get_start_col()
                word = word_obj.get_word()
                cols_with_letters = [start_col + i for i in range(len(word))]
                for col in cols_with_letters:
                    positions_to_keep.append((col, row))
            else:
                col = word_obj.get_start_col()
                start_row = word_obj.get_start_row()
                word = word_obj.get_word()
                rows_with_letters = [start_row + i for i in range(len(word))]
                for row in rows_with_letters:
                    positions_to_keep.append((col, row))
        
        for row in range(1,BOARD_SIZE):
            for col in range(1,BOARD_SIZE):
                if (col, row) not in positions_to_keep:
                    self.grid[row][col] = '_'
                    
            
    def save_words_in_grid(self):
        for row in range(1,BOARD_SIZE):
            if row % 2 != 0:
                row_content = ''.join([NUM_TO_ALPHA[self.grid[row][col]] for col in range(1,BOARD_SIZE)])
                word = self.choose_word_from_content(row_content)
                start_col = row_content.index(word) + 1
                word_to_save = Word(word, row, start_col, 'across')
                self.words_in_grid.append(word_to_save)
            
        
        for col in range(1,BOARD_SIZE):
            if col % 2 != 0:
                col_content = ''.join([NUM_TO_ALPHA[self.grid[row][col]] for row in range(1,BOARD_SIZE)])
                word = self.choose_word_from_content(col_content)
                start_row = col_content.index(word) + 1
                word_to_save = Word(word,start_row, col, 'down')
                self.words_in_grid.append(word_to_save)
            
         
                
    def print_grid(self):
        for i in range(BOARD_SIZE):
            out = ''
            for j in range(BOARD_SIZE):
                if self.grid[i][j] == '_':
                    out += '_'
                else:
                    self.solution[i][j] = NUM_TO_ALPHA[self.grid[i][j]]
                    out += NUM_TO_ALPHA[self.grid[i][j]]
            print(out)
            
    def choose_word_from_content(self, content):
        found_words = []
        for word_num_repr in self.words:
            word = ''.join([NUM_TO_ALPHA[num] for num in word_num_repr])
            if word in content:
                found_words.append(word)
        if len(found_words) > 1:
            found_words.sort(key=len)
            word = found_words[-1]
        elif len(found_words) == 1:
            word = found_words[0]
        else:
            word = ''
        return word

                


puzzle_generator = Puzzle_generator()
puzzle_generator.generate_puzzle()
        