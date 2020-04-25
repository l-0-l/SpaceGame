from const import Const
from resources import Resources
import pygame


class Player:
    def __init__(self, game):
        self.lives = Const.PLAYER_LIVES
        self.score = 0
        self.game = game
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
        return self.score

    def draw(self):
        """
        Draw all player related data
        """
        for i in range(self.lives):
            shift = i * self.image_width * 1.2
            position = tuple(map(sum, zip((shift, 0), Const.PLAYER_LIVES_POSITION)))
            self.game.screen.window.blit(self.image, position)
        score = self.font.render(str(self.score).zfill(6), True, (255, 255, 255))
        self.game.screen.window.blit(score, Const.PLAYER_SCORE_POSITION)
