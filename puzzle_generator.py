from constants import BOARD_SIZE
import random
from z3 import *
import pygame
import requests
import json
SYNONYMS_URL = "https://synonymord.se/api/?q={word}"

ALPHA_TO_NUM = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
         'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
         'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
         'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, 'å': 26, 'ä': 27, 'ö': 28}

NUM_TO_ALPHA = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h',
                8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o',
                15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v',
                22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: 'å', 27: 'ä', 28: 'ö'}

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
        
        
        
        
        