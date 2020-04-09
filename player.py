from math import copysign
from direction import Direction


class Player(object):

    def __init__(self, x, y, screen, nominal_acceleration, pic):
        self.current_acceleration = 0
        self.current_speed = 0
        self.screen = screen
        self.nominal_acceleration = nominal_acceleration
        self.pic = pic
        self.width, self.height = pic.get_rect().size
        self.x = x - self.width/2   # Center of the pic
        self.y = y - self.height/2  # Center of the pic

    def direction(self, direction):
        """ Set acceleration according to the direction """
        self.current_acceleration = direction.value * self.nominal_acceleration

    def move(self):
        """ Move the player for each cycle, making sure we don't go past the walls """
        # Accelerate/decelerate
        if self.current_acceleration != 0:
            # Accelerate
            self.current_speed += self.current_acceleration
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
            self.current_speed /= 2
