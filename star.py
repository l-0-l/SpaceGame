from random import randint
from const import Const


class Star:
    def __init__(self, pic, speed, x, y):
        self.pic = pic
        self.speed = speed
        self.x = x
        self.y = y
        self.away = False
        self.animate_in_progress = False
        self.animation_frame = 0

    def get_xy(self):
        """
        Returns the position.
        """
        return self.x, self.y

    def move(self):
        """
        Move the stars over the screen, they're in the background.
        """
        self.y += self.speed
        # The star has gone beyond the screen
        if self.y > Const.SCREEN_HEIGHT:
            self.y = Const.STAR_COORD_APPEAR

    def get_current_pic(self):
        """
        Return the current picture for the star.
        """
        if self.animate_in_progress:
            # If we're animating, go to the next step
            self.animation_frame += 1
            if self.animation_frame >= len(self.pic):
                # If the animation ended, stop it
                self.animation_frame = 0
                self.animate_in_progress = False
        else:
            # We may want to start the animation
            if randint(0, Const.STAR_ANIMATION_CHANCE) == 0:
                self.animate_in_progress = True
        return self.pic[self.animation_frame]
