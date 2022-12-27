from constants import BOARD_SIZE
import random
from z3 import *
import pygame
import requests
import json
SYNONYMS_URL = "https://synonymord.se/api/?q={word}"

class Puzzle_generator():
    
    def __init__(self):
        self.solution = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        
    def generate_puzzle(self):
        
        words = []
        with open('words.txt', 'r') as f:
            for line in f:
                words.append(line.strip())
            
        
        grid = [['_' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        
                    
        words_of_board_size = [ word for word in words if len(word) == (BOARD_SIZE - 1) ]
        word_for_middle_vertical = random.choice(words_of_board_size)
        
        words_of_board_size.remove(word_for_middle_vertical)
        
        pattern_for_middle_horizontal = '_' * (BOARD_SIZE // 2 - 1) + \
            word_for_middle_vertical[BOARD_SIZE // 2 - 1] + '_' * (BOARD_SIZE // 2) 
            
        word_for_middle_horizontal = random.choice(get_all_words_matching_pattern(pattern_for_middle_horizontal, words_of_board_size))
        
        for i in range(1,BOARD_SIZE):
            grid[BOARD_SIZE // 2][i] = word_for_middle_vertical[i - 1]
            
        for i in range(1,BOARD_SIZE):
            grid[i][BOARD_SIZE // 2] = word_for_middle_horizontal[i - 1]
            
        start_pos_v = {}
        start_pos_h = {}
        
        start_pos_v[(BOARD_SIZE // 2, 1)] = word_for_middle_vertical
        start_pos_h[(1, BOARD_SIZE // 2)] = word_for_middle_horizontal
        
        for i in range(1,BOARD_SIZE):
            if i != BOARD_SIZE // 2 and i % 2 != 0:
                pattern = ''.join([ grid[i][j] for j in range(1,BOARD_SIZE) ])
                word = random.choice(get_all_words_matching_pattern(pattern, words_of_board_size))
                start_pos_v[(i, 1)] = word
                for j in range(1,BOARD_SIZE):
                    grid[i][j] = word[j - 1]
        
            
        for i in range(1,BOARD_SIZE):
            if i != BOARD_SIZE // 2:
                full_pattern = ''.join([ grid[j][i] for j in range(1,BOARD_SIZE) ])
                subpatterns = get_subpatterns(full_pattern)
                possible_words = []
                for pattern in subpatterns:
                    possible_words += get_all_words_matching_pattern(pattern, words)
                if len(possible_words) != 0:
                    index_of_longest = 0
                    for w in possible_words:
                        if len(w) > len(possible_words[index_of_longest]):
                            index_of_longest = possible_words.index(w)
                    word = possible_words[index_of_longest]
                    start_col = full_pattern.index(word[0]) + 1
                    start_pos_h[(start_col, i)] = word
                    for j in range(len(word)):
                        grid[start_col + j][i] = word[j]
        
        synonyms = {}
        for word in start_pos_v.values():
            synonyms[word] = get_synonym(word)
            
        for word in start_pos_h.values():
            synonyms[word] = get_synonym(word)
        
        for key in start_pos_v:
            word = start_pos_v[key]
            grid[key[0]][key[1] - 1] = synonyms[word] + '(v)'
        
        for key in start_pos_h:
            word = start_pos_h[key]
            grid[key[0] - 1][key[1]] = synonyms[word] + '(h)'

            
        return grid
    
def get_synonym(word):
    r = requests.get(SYNONYMS_URL.format(word=word))
    res_json = json.loads((r.text.strip())[1:])
    return random.choice(res_json['synonyms'])
    
    
def get_all_substrings(word):
    return [word[i:j] for i in range(len(word)) for j in range(i+1, len(word)+1)]

def get_subpatterns(pattern):
    all_sub_patterns = get_all_substrings(pattern)
    valid = []
    for candidate in all_sub_patterns:
        if candidate not in valid:
            if candidate[0] != '_' and candidate[-1] != '_':
                valid.append(candidate)
    return valid
        

def get_all_words_matching_pattern(pattern, words):
    res = []
    for word in words:
        if word_matches_pattern(word, pattern):
            res.append(word)
    return res

def word_matches_pattern(word, pattern):
    for i in range(len(word)):
        if len(word) != len(pattern):
            return False
        if pattern[i] != '_' and pattern[i] != word[i]:
            return False
    return True

def get_relaxed_pattern(pattern):
    index_of_letters = []
    for i in range(len(pattern)):
        if pattern[i] != '_':
            index_of_letters.append(i)
    if len(index_of_letters) == 0:
        return '.' * len(pattern)
    else:
        test = '.' * index_of_letters[0]
        for i in range(index_of_letters[0], index_of_letters[-1] + 1):
            test += pattern[i]
        test += '.' * (len(pattern) - index_of_letters[-1] - 1)
        return test
        
        
        
        
        