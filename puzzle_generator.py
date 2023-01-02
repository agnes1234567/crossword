from constants import BOARD_SIZE
import random
from z3 import *
import pygame
import requests
import json
SYNONYMS_URL = "https://synonymord.se/api/?q={word}"
SYN_SYM = '0'
END_W_SYM = '/'
EMPTY_SYM = '_'

class Puzzle_generator():
    
    def __init__(self):
        self.solution = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.grid = [['_' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.start_pos_v = {}
        self.start_pos_h = {}
        self.words = []
        with open('words.txt', 'r') as f:
            for line in f:
                self.words.append(line.strip())
        
    def generate_puzzle(self):
        
        print('Generating puzzle...')
        self.grid = [['_' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.start_pos_v = {}
        self.start_pos_h = {}
        
        for i in range(1, BOARD_SIZE, 2):
            self.fill_vertical_cols([i])
            self.fill_horizontal_rows([i])
        self.print_grid()
        print(self.start_pos_v)
        print(self.start_pos_h)
        synonyms = get_synonyms_for_grid(self.start_pos_v, self.start_pos_h)
        for pos in self.start_pos_v:
            word = self.start_pos_v[pos]
            col = pos[0]
            row = pos[1]
            self.grid[col][row] = synonyms[word] + '(v)'
            
        for pos in self.start_pos_h:
            word = self.start_pos_h[pos]
            col = pos[0]
            row = pos[1]
            self.grid[col][row] = synonyms[word] + '(h)'
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.grid[i][j] == END_W_SYM:
                    self.grid[i][j] = EMPTY_SYM
        
        print('Puzzle generated')
        return self.grid
        
    def print_grid(self):
        for i in range(BOARD_SIZE):
            out = ''
            for j in range(BOARD_SIZE):
                out += self.grid[j][i] + ' '
            print(out)
            
    def fill_vertical_cols(self, cols):
        for col in cols:
            column_pattern = ''.join([self.grid[col][i] for i in range(BOARD_SIZE)])
            possible_patterns_by_start = {}
            for syn_row in range(len(column_pattern)):
                for stop_row in range(syn_row + 2, len(column_pattern) + 1):
                    if column_pattern[syn_row] == SYN_SYM or \
                        column_pattern[syn_row] == END_W_SYM or \
                            column_pattern[syn_row] == EMPTY_SYM:
                        if stop_row == BOARD_SIZE or \
                            (stop_row < BOARD_SIZE and \
                                (self.grid[col][stop_row] == END_W_SYM or self.grid[col][stop_row] == EMPTY_SYM)):
                            pattern = column_pattern[syn_row+1:stop_row]
                            if syn_row not in possible_patterns_by_start:
                                possible_patterns_by_start[syn_row] = []
                            possible_patterns_by_start[syn_row].append(pattern)
            possible_words_by_start = {}
            for start_row in possible_patterns_by_start:
                possible_words_by_start[start_row] = []
                for pattern in possible_patterns_by_start[start_row]:
                    possible_words_by_start[start_row].extend(get_all_words_matching_pattern(pattern, self.words))
            longest_word_length, lowest_index = get_longest_word_with_lowest_index(possible_words_by_start)
            if longest_word_length > 0:
                longest_word = random.choice([word for word in possible_words_by_start[lowest_index] if len(word) == longest_word_length])
                self.grid[col][lowest_index] = SYN_SYM
                for i in range(len(longest_word)):
                    self.grid[col][lowest_index + i + 1] = longest_word[i]
                if lowest_index + len(longest_word) + 1 < BOARD_SIZE \
                    and self.grid[col][lowest_index + len(longest_word) + 1] == EMPTY_SYM:
                    self.grid[col][lowest_index + len(longest_word) + 1] = END_W_SYM
                self.start_pos_v[(col, lowest_index)] = longest_word
                
    def fill_horizontal_rows(self, rows):
        for row in rows:
            row_pattern = ''.join([self.grid[i][row] for i in range(BOARD_SIZE)])
            possible_patterns_by_start = {}
            for syn_col in range(len(row_pattern)):
                for stop_col in range(syn_col + 2, len(row_pattern) + 1):
                    if row_pattern[syn_col] == SYN_SYM or \
                        row_pattern[syn_col] == END_W_SYM or \
                            row_pattern[syn_col] == EMPTY_SYM:
                        if stop_col == BOARD_SIZE or \
                            (stop_col < BOARD_SIZE and \
                                (self.grid[stop_col][row] == END_W_SYM or self.grid[stop_col][row] == EMPTY_SYM)):
                            pattern = row_pattern[syn_col+1:stop_col]
                            if syn_col not in possible_patterns_by_start:
                                possible_patterns_by_start[syn_col] = []
                            possible_patterns_by_start[syn_col].append(pattern)
            possible_words_by_start = {}
            for start_col in possible_patterns_by_start:
                possible_words_by_start[start_col] = []
                for pattern in possible_patterns_by_start[start_col]:
                    possible_words_by_start[start_col].extend(get_all_words_matching_pattern(pattern, self.words))
            longest_word_length, lowest_index = get_longest_word_with_lowest_index(possible_words_by_start)
            if longest_word_length > 0:
                longest_word = random.choice([word for word in possible_words_by_start[lowest_index] if len(word) == longest_word_length])
                self.grid[lowest_index][row] = SYN_SYM
                for i in range(len(longest_word)):
                    self.grid[lowest_index + i + 1][row] = longest_word[i]
                if lowest_index + len(longest_word) + 1 < BOARD_SIZE and \
                    self.grid[lowest_index + len(longest_word) + 1][row] == EMPTY_SYM:
                    self.grid[lowest_index + len(longest_word) + 1][row] = END_W_SYM
                self.start_pos_h[(lowest_index, row)] = longest_word
        
            
def get_longest_word_with_lowest_index(possible_words_by_start):
    longest_word = ''
    lowest_index = BOARD_SIZE
    for start_row in possible_words_by_start:
        for word in possible_words_by_start[start_row]:
            if len(word) > len(longest_word):
                longest_word = word
                lowest_index = start_row
            elif len(word) == len(longest_word) and start_row < lowest_index:
                longest_word = word
                lowest_index = start_row
    longest_word_length = len(longest_word)
    return longest_word_length, lowest_index
    
def fill_vertical_cols(grid, words, cols, start_pos_v):
    for col in cols:
        start_row = 1
        options = {}
        full_pattern = ''.join([grid[col][i] for i in range(start_row, BOARD_SIZE)])
        letter_count = get_letter_count(full_pattern)
        patterns = []
            
        while start_row < BOARD_SIZE - 1:
            top_pattern, bottom_pattern = get_split_pattern(full_pattern, start_row)
            if string_contains_all_letters(top_pattern + bottom_pattern, letter_count):
                if len(top_pattern) > 1 and len(bottom_pattern) > 1:
                    patterns.append((top_pattern, bottom_pattern))
                    top_words = get_all_words_matching_pattern(top_pattern, words)
                    bottom_words = get_all_words_matching_pattern(bottom_pattern, words)
                    if top_words and bottom_words:
                        options[(1, start_row + 2)] = (top_words, bottom_words)
                    elif top_words:
                        options[(1, -1)] = (top_words, [])
            start_row += 1
        row_pair = get_best_option(options)
        if row_pair:
            upper_word = random.choice(options[row_pair][0])
            grid[col][row_pair[0] - 1] = SYN_SYM
            for i in range(len(upper_word)):
                grid[col][row_pair[0] + i] = upper_word[i]
            if row_pair[0] + len(upper_word) < BOARD_SIZE - 1:
                grid[col][row_pair[0] + len(upper_word)] = END_W_SYM
            
            if row_pair[1] != -1:
                start_pos_v[(col, row_pair[0])] = upper_word
                lower_word = random.choice(options[row_pair][1])
                start_pos_v[(col, row_pair[1])] = lower_word
                grid[col][row_pair[1] - 1] = SYN_SYM
                
                for i in range(len(lower_word)):
                    grid[col][row_pair[1] + i] = lower_word[i]
                
                if row_pair[1] + len(lower_word) < BOARD_SIZE - 1:
                    grid[col][row_pair[1] + len(lower_word)] = END_W_SYM
            
                
    return grid, start_pos_v
 
def fill_horizontal(grid, words, rows, start_pos_h):
    for row in rows:
        curr_col = 1
        options = {}
        full_pattern = ''.join([grid[i][row] for i in range(1, BOARD_SIZE)])
        letter_count = get_letter_count(full_pattern)
        patterns = []
        
        while curr_col < BOARD_SIZE - 1:
            left_pattern, right_pattern = get_split_pattern(full_pattern, curr_col)
            if string_contains_all_letters(left_pattern + right_pattern, letter_count):
                if len(left_pattern) > 1 and len(right_pattern) > 1:
                    patterns.append((left_pattern, right_pattern))
                    left_words = get_all_words_matching_pattern(left_pattern, words)
                    right_words = get_all_words_matching_pattern(right_pattern, words)
                    if left_words and right_words:
                        options[(1, curr_col + 2)] = (left_words, right_words)
                    elif left_words:
                        options[(1, -1)] = (left_words, [])
                    
            curr_col += 1
        col_pair = get_best_option(options)
        if col_pair:
            left_col = col_pair[0]
            right_col = col_pair[1]
            
            left_word = random.choice(options[col_pair][0])
            grid, start_pos_h = insert_word_horizontal(grid, row, left_col, left_word, start_pos_h)
            
            if right_col != -1:
                right_word = random.choice(options[col_pair][1])
                grid, start_pos_h = insert_word_horizontal(grid, row, right_col, right_word, start_pos_h)
            
    return grid, start_pos_h

def insert_word_horizontal(grid, row, start_col, word, start_pos_h):
    start_pos_h[start_col, row] = word
    for i in range(len(word)):
        grid[start_col + i][row] = word[i]
    grid[start_col - 1][row] = SYN_SYM
    if start_col + len(word) < BOARD_SIZE and grid[start_col + len(word)][row] == '_':
        grid[start_col + len(word)][row] = END_W_SYM
    return grid, start_pos_h

def get_best_option(options):
    max_options = 0
    max_pair = None
    for pair in options:
        opt1 = len(options[pair][0])
        opt2 = len(options[pair][1])
        if opt1 * opt2 > max_options:
            max_options = opt1 * opt2
            max_pair = pair
    return max_pair

def string_contains_all_letters(string, letter_count):
    for key in letter_count:
        if string.count(key) < letter_count[key]:
            return False
    return True

def get_letter_count(pattern):
    letters = {}
    for letter in pattern:
        if letter in letters:
            letters[letter] += 1
        elif letter != '_':
            letters[letter] = 1
    return letters

def get_split_pattern(full_pattern, index):
    pattern_1 = ''
    pattern_2 = ''
    for i in range(len(full_pattern)):
        if i < index:
            pattern_1 += full_pattern[i]
        if i > index:
            pattern_2 += full_pattern[i]
    
    return pattern_1, pattern_2

def get_synonyms_for_grid(start_pos_h, start_pos_v):
    synonyms = {}
    for word in start_pos_v.values():
        synonyms[word] = get_synonym(word)
            
    for word in start_pos_h.values():
        synonyms[word] = get_synonym(word)
    
    return synonyms
    
def get_synonym(word):
    r = requests.get(SYNONYMS_URL.format(word=word))
    res_json = json.loads((r.text.strip())[1:])
    return random.choice(res_json['synonyms'])


def get_all_words_matching_pattern(pattern, words):
    res = []
    for word in words:
        if word_matches_pattern(word, pattern):
            res.append(word)
    return res

def word_matches_pattern(word, pattern):
    if len(word) != len(pattern):
        return False
    for i in range(len(word)):
        if pattern[i] != '_' and pattern[i] != word[i]:
            return False
    return True