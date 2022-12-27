import pygame
from constants import MENU_WIDTH, MENU_HEIGHT, BUTTONS, MENU_FONT_SIZE, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT

class Menu:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        
        div = MENU_WIDTH // 9
        self.new_game_button = pygame.Rect(x + div//2, y + MENU_HEIGHT // 3, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        self.check_button = pygame.Rect(x + MENU_BUTTON_WIDTH + div,
                                        y + MENU_HEIGHT // 3, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        self.help_button = pygame.Rect(x + MENU_BUTTON_WIDTH * 2  + div * 2,
                                        y + MENU_HEIGHT // 3, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        self.exit_button = pygame.Rect(x + div*7, y + MENU_HEIGHT // 3, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        
        self.font = pygame.font.SysFont("menlo", MENU_FONT_SIZE)
        
    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.new_game_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.check_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.help_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.exit_button)
        
        new_game_button_text = self.font.render("New Game", True, (0, 0, 0))
        check_button_text = self.font.render("Check", True, (0, 0, 0))
        help_button_text = self.font.render("Help", True, (0, 0, 0))
        exit_button_text = self.font.render("Exit", True, (0, 0, 0))
        
        self.screen.blit(new_game_button_text, (self.new_game_button.x + self.new_game_button.width // 2 - new_game_button_text.get_width() // 2, self.new_game_button.y + self.new_game_button.height // 2 - new_game_button_text.get_height() // 2))
        self.screen.blit(check_button_text, (self.check_button.x + self.check_button.width // 2 - check_button_text.get_width() // 2, self.check_button.y + self.check_button.height // 2 - check_button_text.get_height() // 2))
        self.screen.blit(help_button_text, (self.help_button.x + self.help_button.width // 2 - help_button_text.get_width() // 2, self.help_button.y + self.help_button.height // 2 - help_button_text.get_height() // 2))
        self.screen.blit(exit_button_text, (self.exit_button.x + self.exit_button.width // 2 - exit_button_text.get_width() // 2, self.exit_button.y + self.exit_button.height // 2 - exit_button_text.get_height() // 2))
    
    def mouse_click(self, pos):
        if self.new_game_button.collidepoint(pos):
            return BUTTONS.NEW_GAME
        elif self.check_button.collidepoint(pos):
            return BUTTONS.CHECK
        elif self.help_button.collidepoint(pos):
            return BUTTONS.HELP
        elif self.exit_button.collidepoint(pos):
            return BUTTONS.EXIT
        else:
            return None
        
        