from const import Const
from resources import Resources
import pygame


class Player:
    def __init__(self, screen):
        self.lives = Const.PLAYER_LIVES
        self.score = 0
        self.screen = screen
        # Resize the spaceship image to small scale
        self.image = pygame.transform.scale(Resources.ship_move_right[0],
                                            (Const.PLAYER_LIVE_SIZE, Const.PLAYER_LIVE_SIZE))
        self.image_width, _ = self.image.get_rect().size
        self.font = pygame.font.Font("res/PixelEmulator-xq08.ttf", 24)

    def get_score(self):
        """
        Return current points
        """
        return self.score

    def add_score(self, score):
        """
        Add a value to current score
        """
        self.score += score

    def get_lives(self):
        """
        Return current number of lives
        """
        return self.lives

    def hit(self):
        """
        In case the player was hit, reduce a life
        """
        if self.lives > 0:
            # In debug mode, don't reduce lives
            if not Const.DEBUG:
                self.lives -= 1

    def draw(self):
        """
        Draw all player related data
        """
        # Draw all lives as small spaceships
        for i in range(self.lives):
            shift = i * self.image_width * 1.2  # This coefficient is just for having some distance between images
            position = tuple(map(sum, zip((shift, 0), Const.PLAYER_LIVES_POSITION)))
            self.screen.window.blit(self.image, position)
        # Draw the score as a zero-padded six digit number
        score = self.font.render(str(self.score).zfill(6), True, Const.COLOR_WHITE)
        self.screen.window.blit(score, Const.PLAYER_SCORE_POSITION)
