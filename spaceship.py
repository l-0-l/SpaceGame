from math import copysign
from direction import Direction
from time import clock
from random import randint
from images import Images
from const import Const


class Spaceship:
    """
    This class is a singleton, as in this game only one player can exist.
    """

    __instance = None

    def __init__(self, x, y, screen):
        if Spaceship.__instance:
            raise Exception("Only one player!")
        else:
            Spaceship.__instance = self
        self.current_acceleration = 0
        self.current_speed = 0
        self.screen = screen
        self.width, self.height = Images.ship_move_right[0].get_rect().size
        self.x = x - self.width/2   # Center of the pic
        self.y = y - self.height/2  # Center of the pic
        self.next_frame = 0
        self.current_flame_pic_num = 0

    def set_direction(self, direction):
        """
        Set acceleration according to the direction.
        """
        self.current_acceleration = direction.value * Const.SPACESHIP_ACCELERATION

    def move(self):
        """
        Move the player for each cycle, making sure we don't go past the walls.
        """
        # Accelerate/decelerate
        if self.current_acceleration != 0:
            # Accelerate
            self.current_speed += self.current_acceleration
            if abs(self.current_speed) > Const.SPACESHIP_MAX_SPEED:
                self.current_speed = copysign(1, self.current_speed) * Const.SPACESHIP_MAX_SPEED
        elif self.current_speed != 0:
            # Decelerate
            sign = copysign(1, self.current_speed)
            self.current_speed = sign * (abs(self.current_speed) - Const.SPACESHIP_ACCELERATION)
            # Set speed to zero if it is very low
            if abs(self.current_speed) < Const.SPACESHIP_ACCELERATION:
                self.current_speed = 0

        # Calculate the next x axis location
        if 0 < self.x + self.current_speed < Const.SCREEN_WIDTH - self.width:
            self.x += self.current_speed
        else:
            # We hit a wall, so change the direction
            self.current_speed = - self.current_speed
            # And slow down (lose energy on impact)
            self.current_speed /= Const.SPACESHIP_SPEED_DROP_ON_SIDE_IMPACT

    def get_direction(self):
        """
        Returns player's direction.
        Actually, the direction concept is a bit tricky. This method returns the
        direction the user wants to move to, even if currently he moves in the opposite
        direction, but if he doesn't press any button - the actual moving direction
        is returned.
        """
        if self.current_acceleration > 0:
            direction = Direction.right
        elif self.current_acceleration < 0:
            direction = Direction.left
        elif self.current_speed > 0:
            direction = Direction.right
        elif self.current_speed < 0:
            direction = Direction.left
        else:
            direction = Direction.none
        return direction

    def get_current_pic(self):
        """
        Returns the current player image.
        """
        # The current picture is determined by the spaceship speed
        num_pic = abs(round(self.current_speed / Const.SPACESHIP_ANIMATION_TO_SPEED_RATIO))
        total_pics = len(Images.ship_move_right) - 1

        # The number of the picture can't be more than the pictures we have
        if num_pic >= total_pics:
            num_pic = total_pics

        # Here the direction is the actual moving direction, rather than the direction
        # the user wants the spaceship to move as returned by self.get_direction method.
        direction = copysign(1, self.current_speed)

        # Now we select the actual picture from the lists
        if direction == Direction.right.value:
            # Going right
            pic = Images.ship_move_right[num_pic]
        elif direction == Direction.left.value:
            # Going left
            pic = Images.ship_move_left[num_pic]
        else:
            # Not moving
            pic = Images.ship_move_right[0]
        return pic

    def get_current_flame_pic(self):
        """
        Returns the current flame pic and changes it for the next time
        """
        if clock() > self.next_frame:
            # Make sure we're not randomly getting the same picture
            previous_number = self.current_flame_pic_num
            while previous_number == self.current_flame_pic_num:
                self.current_flame_pic_num = randint(1, len(Images.flame) - 1)
            self.next_frame += Const.FRAME_TIME_SEC
        return Images.flame[self.current_flame_pic_num]

    def get_xy(self):
        """
        Returns the position
        """
        return self.x, self.y

    def draw(self):
        """
        Draws itself with the flames
        """
        self.screen.window.blit(self.get_current_pic(), self.get_xy())
        self.screen.window.blit(self.get_current_flame_pic(),
                                (self.x + Const.SPACESHIP_FLAME_OFFSET_X_LEFT,
                                 self.y + Const.SPACESHIP_FLAME_OFFSET_Y))
        self.screen.window.blit(self.get_current_flame_pic(),
                                (self.x + Const.SPACESHIP_FLAME_OFFSET_X_RIGHT,
                                 self.y + Const.SPACESHIP_FLAME_OFFSET_Y))
