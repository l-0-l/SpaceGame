from level import Level
from enemies import Enemies
from const import Const
from direction import Direction
from random import randint
import enum


class Gameplay:
    def __init__(self, screen):
        self.level = 0
        self.levels = []
        self.screen = screen
        self.level_initialized = False
        self.enemies = Enemies(self.screen)
        self.invaders_in_place = False
        self.num_of_levels = 5
        self.__setup_levels()

    class Probability(enum.Enum):
        very_low = 100
        low = 80
        medium = 60
        high = 40
        very_high = 20

    def __setup_levels(self):
        for i in range(self.num_of_levels):
            self.levels.append(Level(level_number=i))
        self.levels[0].set_num_of_invaders(15)
        self.levels[0].set_asteroids_probability(self.Probability.very_low)
        self.levels[1].set_num_of_invaders(15)
        self.levels[1].set_asteroids_probability(self.Probability.low)
        self.levels[2].set_num_of_invaders(15)
        self.levels[2].set_asteroids_probability(self.Probability.medium)
        self.levels[3].set_num_of_invaders(15)
        self.levels[3].set_asteroids_probability(self.Probability.high)
        self.levels[4].set_num_of_invaders(15)
        self.levels[4].set_asteroids_probability(self.Probability.very_high)

    def get_enemies(self):
        return self.enemies

    def current_level(self):
        return self.levels[self.level]

    def initialize_level(self):
        if not self.level_initialized:
            self.invaders_in_place = False

    def end_level(self):
        if self.enemies.current_number_of_invaders() > 0:
            return False
        return True

    def next_level(self):
        if self.level < self.num_of_levels:
            self.level += 1
            self.initialize_level()

    def run(self):
        if not self.invaders_in_place:
            if self.enemies.all_invaders_appeared():
                if self.enemies.current_number_of_invaders() < self.current_level().get_num_of_invaders():
                    self.enemies.add_invader(Const.INVADER_STARTING_X,
                                             Const.INVADER_STARTING_Y,
                                             (10, 0),
                                             Direction.right)
                else:
                    self.invaders_in_place = True
                    self.enemies.set_invaders_speed((0.5, 0))

        if randint(0, self.current_level().get_asteroids_probability().value) == 0:
            self.enemies.add_asteroid()

        self.enemies.move()

    def draw(self):
        self.enemies.draw()
