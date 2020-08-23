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
    def __init__(self, space, screen):
        self.space = space
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
        self.blinking_period = 0
        self.blinking_time = 0
        self.blink = False
        self.first_blink = False
        self.level_notification = False
        self.death_notification = False
        self.spaceship_state = self.SpaceshipState.normal

    class Probability(enum.Enum):
        very_low = 100
        low = 80
        medium = 60
        high = 40
        very_high = 20

    class SpaceshipState(enum.Enum):
        normal = 0
        hit = 1
        blinking = 2

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
            self.space.quit()
        if not self.level_initialized:
            self.level_initialized = True
            self.invaders_in_place = False
        for invader_location in self.current_level().get_invader_locations():
            self.enemies.add_invader(x=invader_location[0],
                                     y=invader_location[1],
                                     speed=1)
        self.level_notification = True
        self.notification_time = clock() + Const.NOTIFICATION_TIME

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

    def spaceship_was_hit(self):
        self.spaceship.hit()
        self.death_notification = True
        self.notification_time = clock() + Const.NOTIFICATION_TIME
        self.player.hit()
        self.spaceship_state = self.SpaceshipState.hit
        if self.player.get_lives() == 0:
            # The game will end when there are 0 lives left
            # TODO: this is a very sad ending...
            self.space.quit()

    def check_hits(self):
        """
        Check if a rocket or a spaceship hit something
        """
        for enemy in self.enemies.get_enemies():
            # Spaceship
            if self.spaceship_state == self.SpaceshipState.normal and \
                    pygame.Rect(self.spaceship.hitbox).colliderect(enemy.hitbox):
                if not enemy.is_hit():
                    enemy.hit()
                # Spaceship death. It can be hit by an exploding enemy as well.
                self.spaceship_was_hit()
            # Rocket
            for rocket in [self.rocket_left, self.rocket_right]:
                if rocket.is_launched():
                    if pygame.Rect(rocket.hitbox).colliderect(enemy.hitbox):
                        rocket.gone()
                        enemy.hit()
                        self.add_score(enemy)

    def spaceship_state_machine(self):
        if self.spaceship_state == self.SpaceshipState.hit and not self.spaceship.is_hit():
            # The spaceship was indeed hit, but it isn't exploding yet
            self.spaceship_state = self.SpaceshipState.blinking
            self.spaceship.restore_xy()
            self.spaceship.reinitialize()
            self.blinking_period = clock() + Const.BLINKING_PERIOD
            self.blinking_time = clock() + Const.BLINKING_PERIOD / 3
            # The first blink will be longer, i.e. the spaceship will disappear for a while after explosion
            self.first_blink = True
            self.blink = True

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
        self.spaceship_state_machine()

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
                self.space.quit()
            # Respond to keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.space.quit()
                if self.spaceship_state == self.SpaceshipState.normal:
                    # In any of the abnormal spaceship states, do not allow firing the rockets
                    if event.key == pygame.K_z:
                        self.rocket_left.launch()
                    if event.key == pygame.K_x:
                        self.rocket_right.launch()
                if self.spaceship_state != self.SpaceshipState.hit and not self.first_blink:
                    # Allow movement of the spaceship if it is normal or blinking, but not if it is exploding
                    # Also, don't allow moving the ship during the first, long blink
                    if event.key == pygame.K_LEFT:
                        self.spaceship.set_direction(Direction.left)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.set_direction(Direction.right)
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
        Draw everything, including static player-related data and notifications
        """
        self.screen.draw()
        self.enemies.draw()
        self.player.draw()
        for rocket in [self.rocket_left, self.rocket_right]:
            if rocket.is_launched():
                rocket.draw()

        if clock() < self.blinking_period:
            if clock() > self.blinking_time:
                self.blink = not self.blink
                self.first_blink = False
                self.blinking_time = clock() + Const.BLINKING_TIME
            if not self.blink:
                self.spaceship.draw()
                self.rocket_left.draw()
                self.rocket_right.draw()
        else:
            if self.spaceship_state == self.SpaceshipState.blinking:
                self.spaceship_state = self.SpaceshipState.normal
            self.spaceship.draw()
            if self.spaceship_state != self.SpaceshipState.hit:
                self.rocket_left.draw()
                self.rocket_right.draw()

        if clock() < self.notification_time:
            label = ""
            if self.level_notification:
                label = self.player.font.render("Level " + str(self.level + 1), True, Const.COLOR_WHITE)
            elif self.death_notification:
                label = self.player.font.render("Lives:" + str(self.player.get_lives()), True, Const.COLOR_RED)
            width, height = label.get_rect().size
            label = pygame.transform.scale(label, (width * 4, height * 4))
            width, height = label.get_rect().size
            x = (Const.SCREEN_WIDTH - width) / 2
            y = (Const.SCREEN_HEIGHT - height) / 2
            self.screen.window.blit(label, (x, y))
        else:
            self.level_notification = False
            self.death_notification = False
