import pygame


class Screen(object):

    def __init__(self, width, height, bg_color):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.window = pygame.display.set_mode((self.width, self.height))
