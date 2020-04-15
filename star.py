from random import randint
from const import Const
from interstellar import Interstellar


class Star(Interstellar):
    def __init__(self, images, speed, x, y):
        super().__init__(images, speed, x, y)
        self.animate_in_progress = False
        self.animation_frame = 0

    def move(self):
        """
        Move the stars over the screen, they're in the background.
        """
        self.y += self.speed[1]
        # The star has gone beyond the screen
        if self.y > Const.SCREEN_HEIGHT:
            self.x = randint(Const.STAR_COORD_APPEAR, Const.SCREEN_WIDTH)
            self.y = Const.STAR_COORD_APPEAR

    def get_current_pic(self):
        """
        Return the current picture for the star.
        """
        if self.animate_in_progress:
            # If we're animating, go to the next step
            self.animation_frame += 1
            if self.animation_frame >= len(self.images):
                # If the animation ended, stop it
                self.animation_frame = 0
                self.animate_in_progress = False
        else:
            # We may want to start the animation
            if randint(0, Const.STAR_ANIMATION_CHANCE) == 0:
                self.animate_in_progress = True
        return self.images[self.animation_frame]
