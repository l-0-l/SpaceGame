from direction import Direction
from screen import Screen
from spaceship import Spaceship
from missile import Missile
from enemy import Enemy
from const import Const
from random import randint
import pygame


class Space(object):
    def __init__(self):
        # Initialization
        pygame.init()

        self.screen = Screen()

        # There's one player in this game
        self.spaceship = Spaceship(x=Const.INITIAL_X_POS, y=Const.INITIAL_Y_POS, screen=self.screen)

        # There are only two missiles in this game, the left one and the right one
        self.missile_left = Missile(player=self.spaceship, side=Direction.left)
        self.missile_right = Missile(player=self.spaceship, side=Direction.right)

        # Caption and icon
        pygame.display.set_caption("Space")
        pic_logo = pygame.image.load("res/spaceship_N_00.png")
        pygame.display.set_icon(pic_logo)

        # For now, initialize a simple enemy here
        self.enemy = Enemy(self.screen)

        # Begin running :)
        self.running = True

    def main(self):
        """ Main game loop """

        while self.running:

            # Check for events
            for event in pygame.event.get():
                # Exit event
                if event.type == pygame.QUIT:
                    self.running = False
                # Respond to keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_LEFT:
                        self.spaceship.set_direction(Direction.left)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.set_direction(Direction.right)
                    if event.key == pygame.K_z:
                        self.missile_left.launch()
                    if event.key == pygame.K_x:
                        self.missile_right.launch()
                    if event.key == pygame.K_a:
                        self.enemy.add_asteroid()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        # Check the direction change is relevant
                        if self.spaceship.get_direction() == Direction.left:
                            self.spaceship.set_direction(Direction.none)
                    elif event.key == pygame.K_RIGHT:
                        # Check the direction change is relevant
                        if self.spaceship.get_direction() == Direction.right:
                            self.spaceship.set_direction(Direction.none)

            # Calculate the next player location on the x axis
            self.spaceship.move()
            self.missile_left.move()
            self.missile_right.move()
            self.enemy.move()

            # A bit of missile logic
            if self.missile_left.is_away():
                self.missile_left.reload()
            if self.missile_right.is_away():
                self.missile_right.reload()

            # Just randomly adding asteroids for fun
            if randint(0, 40) == 0:
                self.enemy.add_asteroid()

            # Update the display
            self.screen.draw()
            self.missile_left.draw()
            self.missile_right.draw()
            self.spaceship.draw()
            self.enemy.draw()

            pygame.display.update()


if __name__ == '__main__':
    space = Space()
    space.main()
