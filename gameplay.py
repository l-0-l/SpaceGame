from level import Level
from enemies import Enemies
from spaceship import Spaceship
from rocket import Rocket
from direction import Direction
from const import Const
from random import randint
from player import Player
from time import clock
import pygame
import enum


class Gameplay:
    def __init__(self, game, screen):
        self.game = game
        self.level = 0
        self.levels = []
        self.screen = screen
        self.level_initialized = False
        self.spaceship = self.spaceship = Spaceship(x=Const.INITIAL_X_POS, y=Const.INITIAL_Y_POS, screen=self.screen)
        self.enemies = Enemies(self)
        self.rocket_left = Rocket(spaceship=self.spaceship, side=Direction.left)
        self.rocket_right = Rocket(spaceship=self.spaceship, side=Direction.right)
        self.player = Player(self.screen)
        self.invaders_in_place = False
        self.num_of_levels = 10
        self.__setup_levels()
        self.initialize_level()
        self.level_font = pygame.font.Font("res/PixelEmulator-xq08.ttf", 24)
        self.notification_time = 0

    class Probability(enum.Enum):
        very_low = 100
        low = 80
        medium = 60
        high = 40
        very_high = 20

    def __setup_levels(self):
        """
        Prepare all levels with their data
        """
        for i in range(self.num_of_levels):
            self.levels.append(Level())
        # Level one
        self.levels[0].set_invader_locations(Gameplay.__layout_invaders(1, 5))
        self.levels[0].set_asteroids_probability(self.Probability.very_low)
        # Level two
        self.levels[1].set_invader_locations(Gameplay.__layout_invaders(1, 6))
        self.levels[1].set_asteroids_probability(self.Probability.very_low)
        # Level three
        self.levels[2].set_invader_locations(Gameplay.__layout_invaders(2, 5))
        self.levels[2].set_asteroids_probability(self.Probability.low)
        # Level four
        self.levels[3].set_invader_locations(Gameplay.__layout_invaders(2, 6))
        self.levels[3].set_asteroids_probability(self.Probability.low)
        # Level five
        self.levels[4].set_invader_locations(Gameplay.__layout_invaders(3, 5))
        self.levels[4].set_asteroids_probability(self.Probability.medium)
        # Level six
        self.levels[5].set_invader_locations(Gameplay.__layout_invaders(3, 6))
        self.levels[5].set_asteroids_probability(self.Probability.medium)
        # Level seven
        self.levels[6].set_invader_locations(Gameplay.__layout_invaders(4, 5))
        self.levels[6].set_asteroids_probability(self.Probability.high)
        # Level eight
        self.levels[7].set_invader_locations(Gameplay.__layout_invaders(4, 6))
        self.levels[7].set_asteroids_probability(self.Probability.high)
        # Level nine
        self.levels[8].set_invader_locations(Gameplay.__layout_invaders(5, 5))
        self.levels[8].set_asteroids_probability(self.Probability.very_high)
        # Level ten
        self.levels[9].set_invader_locations(Gameplay.__layout_invaders(5, 6))
        self.levels[9].set_asteroids_probability(self.Probability.very_high)

    @staticmethod
    def __layout_invaders(lines, columns):
        """
        Arrange the invaders on the screen
        """
        invaders_locations = []
        nominal_shift = Const.INVADER_SIZE
        if lines == 1:
            additional_shift = 0
        else:
            additional_shift = Const.INVADER_SIZE
        initial_shift = ((Const.INVADER_RIGHT_BORDER + Const.INVADER_SIZE - Const.INVADER_LEFT_BORDER) -
                         (Const.INVADER_SIZE * 1.7 * (columns - 1) + nominal_shift + additional_shift)) / 2
        for line in range(lines):
            shift = (line % 2) * nominal_shift
            for column in range(columns):
                invaders_locations.append((initial_shift + Const.INVADER_SIZE * 1.7 * column + shift,
                                          -Const.INVADER_SIZE - Const.INVADER_SIZE * 1.2 * line))
        return invaders_locations

    def current_level(self):
        """
        Return the current level object
        """
        return self.levels[self.level]

    def add_score(self, enemy):
        """
        Add a score for hitting an enemy
        """
        # The farther the enemy was from the player, the more score he gets for shooting it
        self.player.add_score(enemy.score + int((Const.SCREEN_HEIGHT - enemy.get_xy()[1]) / 10))

    def initialize_level(self):
        """
        Initialize a new level
        """
        if self.level == self.num_of_levels:
            # TODO: this is a very sad ending...
            exit(0)
        if not self.level_initialized:
            self.level_initialized = True
            self.invaders_in_place = False
        for invader_location in self.current_level().get_invader_locations():
            self.enemies.add_invader(x=invader_location[0],
                                     y=invader_location[1],
                                     speed=1)
        self.notification_time = clock() + 3

    def end_level(self):
        """
        Returns true if the current level ended (no invaders left alive)
        """
        if self.enemies.current_number_of_invaders() > 0:
            return False
        return True

    def next_level(self):
        """
        Switch to the next level
        """
        if self.level < self.num_of_levels:
            self.level += 1
            self.invaders_in_place = False
            self.initialize_level()

    def check_hits(self):
        """
        Check if a rocket or a spaceship hit something
        """
        for enemy in self.enemies.get_enemies():
            # Spaceship
            if pygame.Rect(self.spaceship.hitbox).colliderect(enemy.hitbox):
                if not enemy.is_hit():
                    enemy.hit()
                # TODO: Spaceship death
                # self.spaceship.hit()
            # Rocket
            for rocket in [self.rocket_left, self.rocket_right]:
                if rocket.is_launched():
                    if pygame.Rect(rocket.hitbox).colliderect(enemy.hitbox):
                        rocket.gone()
                        enemy.hit()
                        self.add_score(enemy)

    def run(self):
        """
        Game running logic
        """
        # Enemies
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

        # Spaceship and rockets
        # Calculate the next locations of everything
        self.spaceship.move()
        self.rocket_left.move()
        self.rocket_right.move()

        # Check if something was hit
        self.check_hits()

        # Game
        if self.end_level():
            self.next_level()

    def handle_events(self):
        """
        Handle all game events, mostly keypress
        """
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                self.game.quit()
            # Respond to keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.quit()
                if event.key == pygame.K_LEFT:
                    self.spaceship.set_direction(Direction.left)
                if event.key == pygame.K_RIGHT:
                    self.spaceship.set_direction(Direction.right)
                if event.key == pygame.K_z:
                    self.rocket_left.launch()
                if event.key == pygame.K_x:
                    self.rocket_right.launch()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    # Check if a direction change is relevant
                    if self.spaceship.get_direction() == Direction.left:
                        self.spaceship.set_direction(Direction.none)
                elif event.key == pygame.K_RIGHT:
                    # Check if a direction change is relevant
                    if self.spaceship.get_direction() == Direction.right:
                        self.spaceship.set_direction(Direction.none)

    def draw(self):
        """
        Draw everything, including static player-related data
        """
        self.screen.draw()
        self.enemies.draw()
        self.player.draw()
        self.rocket_left.draw()
        self.rocket_right.draw()
        self.spaceship.draw()

        if clock() < self.notification_time:
            level = self.player.font.render("Level " + str(self.level + 1), True, (255, 255, 255))
            width, height = level.get_rect().size
            level = pygame.transform.scale(level, (width * 4, height * 4))
            width, height = level.get_rect().size
            x = (Const.SCREEN_WIDTH - width) / 2
            y = (Const.SCREEN_HEIGHT - height) / 2
            self.screen.window.blit(level, (x, y))
