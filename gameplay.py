from level import Level
from enemies import Enemies
from const import Const
from random import randint
import enum


class Gameplay:
    def __init__(self, screen, levels=5):
        self.level = 0
        self.levels = []
        self.screen = screen
        self.level_initialized = False
        self.enemies = Enemies(self.screen)
        self.invaders_in_place = False
        self.num_of_levels = levels
        self.__setup_levels()
        self.initialize_level()

    class Probability(enum.Enum):
        very_low = 100
        low = 80
        medium = 60
        high = 40
        very_high = 20

    def __setup_levels(self):
        for i in range(self.num_of_levels):
            self.levels.append(Level())
        self.levels[0].set_invader_locations(Gameplay.__layout_invaders(1, 5))
        self.levels[0].set_asteroids_probability(self.Probability.very_low)
        self.levels[1].set_invader_locations(Gameplay.__layout_invaders(2, 5))
        self.levels[1].set_asteroids_probability(self.Probability.low)
        self.levels[2].set_invader_locations(Gameplay.__layout_invaders(3, 5))
        self.levels[2].set_asteroids_probability(self.Probability.medium)
        self.levels[3].set_invader_locations(Gameplay.__layout_invaders(4, 6))
        self.levels[3].set_asteroids_probability(self.Probability.high)
        self.levels[4].set_invader_locations(Gameplay.__layout_invaders(5, 6))
        self.levels[4].set_asteroids_probability(self.Probability.very_high)

    @staticmethod
    def __layout_invaders(lines, columns):
        invaders_locations = []
        initial_shift = 40
        for line in range(lines):
            if line % 2 == 0:
                shift = 0
            else:
                shift = 70
            for column in range(columns):
                invaders_locations.append((initial_shift + Const.INVADER_SIZE * 1.7 * column + shift,
                                          -Const.INVADER_SIZE - Const.INVADER_SIZE * 1.2 * line))
        return invaders_locations

    def get_enemies(self):
        return self.enemies

    def current_level(self):
        return self.levels[self.level]

    def initialize_level(self):
        if self.level == self.num_of_levels:
            # Game end - this is a very sad ending...
            exit(0)
        if not self.level_initialized:
            self.level_initialized = True
            self.invaders_in_place = False
        for invader_location in self.current_level().get_invader_locations():
            self.enemies.add_invader(x=invader_location[0],
                                     y=invader_location[1],
                                     speed=1)

    def end_level(self):
        if self.enemies.current_number_of_invaders() > 0:
            return False
        return True

    def next_level(self):
        if self.level < self.num_of_levels:
            self.level += 1
            self.invaders_in_place = False
            self.initialize_level()

    def run(self):
        # Invaders may be still entering the screen
        if not self.invaders_in_place:
            if self.enemies.all_invaders_appeared():
                self.invaders_in_place = True
                self.enemies.invaders_arrived()
        # Add a random asteroid
        if randint(0, self.current_level().get_asteroids_probability().value) == 0:
            self.enemies.add_asteroid()
        # Move all enemies
        self.enemies.move()

    def draw(self):
        self.enemies.draw()
