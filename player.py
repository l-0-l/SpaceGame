from math import copysign
from direction import Direction
from time import clock
from random import randint


class Player:
    """
    This class is a singleton, as in this game only one player can exist.
    """

    __instance = None

    def __init__(self, x, y, screen, acceleration, max_speed, pic_move_right, pic_move_left, pic_flame, frame_time):
        if Player.__instance:
            raise Exception("Only one player!")
        else:
            Player.__instance = self
        self.current_acceleration = 0
        self.current_speed = 0
        self.screen = screen
        self.nominal_acceleration = acceleration
        self.pic_move_right = pic_move_right
        self.pic_move_left = pic_move_left
        self.pic_flame = pic_flame
        self.width, self.height = pic_move_right[0].get_rect().size
        self.x = x - self.width/2   # Center of the pic
        self.y = y - self.height/2  # Center of the pic
        self.max_speed = max_speed
        self.frame_time = frame_time
        self.next_frame = clock() + self.frame_time
        self.current_flame_pic_num = 0
        self.left_flame_xy_offset = (22, 73)
        self.right_flame_xy_offset = (44, 73)

    def set_direction(self, direction):
        """
        Set acceleration according to the direction.
        """
        self.current_acceleration = direction.value * self.nominal_acceleration

    def move(self):
        """
        Move the player for each cycle, making sure we don't go past the walls.
        """
        # Accelerate/decelerate
        if self.current_acceleration != 0:
            # Accelerate
            self.current_speed += self.current_acceleration
            if abs(self.current_speed) > self.max_speed:
                self.current_speed = copysign(1, self.current_speed) * self.max_speed
        elif self.current_speed != 0:
            # Decelerate
            sign = copysign(1, self.current_speed)
            self.current_speed = sign * (abs(self.current_speed) - self.nominal_acceleration)
            # Set speed to zero if it is very low
            if abs(self.current_speed) < self.nominal_acceleration:
                self.current_speed = 0

        # Calculate the next x axis location
        if 0 < self.x + self.current_speed < self.screen.width - self.width:
            self.x += self.current_speed
        else:
            # We hit a wall, so change the direction
            self.current_speed = - self.current_speed
            # And slow down (lose energy on impact)
            self.current_speed /= 1.5  # TODO: Magic number here

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
        num_pic = abs(round(self.current_speed / 2))  # TODO: Magic number here
        total_pics = len(self.pic_move_right) - 1
        # The number of the picture can't be more than the pictures we have
        if num_pic >= total_pics:
            num_pic = total_pics

        # Here the direction is the actual moving direction, rather than the direction
        # the user wants the spaceship to move as returned by self.get_direction method.
        direction = copysign(1, self.current_speed)

        # Now we select the actual picture from the lists
        if direction == Direction.right.value:
            # Going right
            pic = self.pic_move_right[num_pic]
        elif direction == Direction.left.value:
            # Going left
            pic = self.pic_move_left[num_pic]
        else:
            # Not moving
            pic = self.pic_move_right[0]
        return pic

        # Change the picture

    def get_current_flame_pic(self):
        if clock() > self.next_frame:
            previous_number = self.current_flame_pic_num
            while previous_number == self.current_flame_pic_num:
                self.current_flame_pic_num = randint(1, len(self.pic_flame) - 1)
            self.next_frame += self.frame_time
        return self.pic_flame[self.current_flame_pic_num]

    def get_xy(self):
        return self.x, self.y

    def draw(self):
        self.screen.window.blit(self.get_current_pic(), self.get_xy())
        self.screen.window.blit(self.get_current_flame_pic(),
                                tuple(map(sum, zip(self.get_xy(), self.left_flame_xy_offset))))
        self.screen.window.blit(self.get_current_flame_pic(),
                                tuple(map(sum, zip(self.get_xy(), self.right_flame_xy_offset))))
