from math import copysign
from direction import Direction
from time import clock


class Player(object):

    def __init__(self, x, y, screen, nominal_acceleration, pic_move_right, pic_move_left):
        self.current_acceleration = 0
        self.current_speed = 0
        self.screen = screen
        self.nominal_acceleration = nominal_acceleration
        self.pic_move_right = pic_move_right
        self.pic_move_left = pic_move_left
        self.width, self.height = pic_move_right[0].get_rect().size
        self.x = x - self.width/2   # Center of the pic
        self.y = y - self.height/2  # Center of the pic
        self.current_pic = 0
        self.frame_time = clock()

    def set_direction(self, direction):
        """
        Set acceleration according to the direction
        """
        self.current_acceleration = direction.value * self.nominal_acceleration

    def move(self):
        """
        Move the player for each cycle, making sure we don't go past the walls
        """
        # Accelerate/decelerate
        if self.current_acceleration != 0:
            # Accelerate
            self.current_speed += self.current_acceleration
            # Change the image to the next one, assumed that number of images for right and left is identical
            if abs(self.current_pic + self.get_direction().value) < len(self.pic_move_right):
                if clock() > self.frame_time:
                    self.current_pic += self.get_direction().value
                    self.frame_time = clock() + 0.1  # TODO: magic number here
        elif self.current_speed != 0:
            # Decelerate
            sign = copysign(1, self.current_speed)
            self.current_speed = sign * (abs(self.current_speed) - self.nominal_acceleration)
            # Set speed to zero if it is very low
            if abs(self.current_speed) < self.nominal_acceleration:
                self.current_speed = 0
            # Change the image to the previous one
            if abs(self.current_pic - self.get_direction().value) >= 0:
                if clock() > self.frame_time:
                    self.current_pic -= int(copysign(1, self.current_pic))
                    self.frame_time = clock() + 0.1  # TODO: magic number here
        else:
            self.current_pic = 0

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
        Returns player's direction
        """
        if self.current_acceleration > 0:
            direction = Direction.right
        elif self.current_acceleration < 0:
            direction = Direction.left
        elif self.current_speed > 0:
            direction = Direction.left
        elif self.current_speed < 0:
            direction = Direction.right
        else:
            direction = Direction.none
        return direction

    def get_current_pic(self):
        """
        Returns the current player image
        """
        direction = self.get_direction()
        if direction == Direction.right:
            pic = self.pic_move_right[abs(self.current_pic)]
        elif direction == Direction.left:
            pic = self.pic_move_left[abs(self.current_pic)]
        else:
            pic = self.pic_move_right[0]
        return pic
