import pygame
from random import randint, uniform
from star import Star
from planet import Planet
from const import Const
from resources import Resources


class Screen:

    def __init__(self):
        self.window = pygame.display.set_mode((Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT))
        self.stars = []
        self.planet = None
        for i in range(Const.STAR_NUM_SMALL):
            self.stars.append(Star(image=Resources.star_small,
                                   speed=(0, uniform(Const.STAR_SPEED_SMALL[0], Const.STAR_SPEED_SMALL[1])),
                                   x=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_WIDTH),
                                   y=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_HEIGHT)))
        for i in range(Const.STAR_NUM_BRIGHT):
            self.stars.append(Star(image=Resources.star_bright,
                                   speed=(0, uniform(Const.STAR_SPEED_BRIGHT[0], Const.STAR_SPEED_BRIGHT[1])),
                                   x=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_WIDTH),
                                   y=randint(Const.STAR_COORD_APPEAR, Const.SCREEN_HEIGHT)))
        self.planet = Planet(image=Resources.planets[randint(0, len(Resources.planets) - 1)],
                             speed=(uniform(Const.PLANET_SPEED_X[0], Const.PLANET_SPEED_X[1]),
                                    uniform(Const.PLANET_SPEED_Y[0], Const.PLANET_SPEED_Y[1])))
        self.planet.set_xy(x=randint(-self.planet.width//2, Const.SCREEN_WIDTH-self.planet.width//2),
                           y=randint(-self.planet.height//2, Const.SCREEN_WIDTH-self.planet.height//2))

    def draw(self):
        self.window.fill(Const.BG_COLOR)
        for star in self.stars:
            star.move()
            self.window.blit(star.get_current_pic(), star.get_xy())
        if self.planet and not self.planet.is_away():
            self.planet.move()
            self.window.blit(self.planet.get_current_pic(), self.planet.get_xy())
