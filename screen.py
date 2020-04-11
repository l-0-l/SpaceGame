import pygame
from star import Star
from random import randint, uniform
from const import Const
from images import Images


class Screen:

    def __init__(self):
        self.window = pygame.display.set_mode((Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT))
        self.stars = []
        for i in range(Const.STAR_NUM_SMALL):
            self.stars.append(Star(pic=Images.pic_star_small,
                                   speed=uniform(Const.STAR_SPEED_SMALL[0], Const.STAR_SPEED_SMALL[1]),
                                   x=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_WIDTH),
                                   y=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_HEIGHT)))
        for i in range(Const.STAR_NUM_BRIGHT):
            self.stars.append(Star(pic=Images.pic_star_bright,
                                   speed=uniform(Const.STAR_SPEED_BRIGHT[0], Const.STAR_SPEED_BRIGHT[1]),
                                   x=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_WIDTH),
                                   y=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_HEIGHT)))

    def draw(self):
        self.window.fill(Const.BG_COLOR)
        for star in self.stars:
            star.move()
            self.window.blit(star.get_current_pic(), star.get_xy())
