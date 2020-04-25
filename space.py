from direction import Direction
from screen import Screen
from spaceship import Spaceship
from missile import Missile
from const import Const
from gameplay import Gameplay
from resources import Resources
import pygame


class Space(object):
    def __init__(self):
        # Initialization
        pygame.init()
        self.screen = Screen()
        self.game = Gameplay(self.screen)

        # There's one spaceship in this game
        self.spaceship = Spaceship(x=Const.INITIAL_X_POS, y=Const.INITIAL_Y_POS, screen=self.screen)

        # There are only two missiles in this game, the left one and the right one
        self.missile_left = Missile(spaceship=self.spaceship,
                                    side=Direction.left,
                                    enemies=self.game.enemies,
                                    launch_sound=Resources.wav_launch,
                                    game=self.game)
        self.missile_right = Missile(spaceship=self.spaceship,
                                     side=Direction.right,
                                     enemies=self.game.enemies,
                                     launch_sound=Resources.wav_launch,
                                     game=self.game)

        # Caption and icon
        pygame.display.set_caption("Space")
        pic_logo = pygame.image.load("res/spaceship_N_00.png")
        pygame.display.set_icon(pic_logo)

        # Start running :)
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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        # Check the direction change is relevant
                        if self.spaceship.get_direction() == Direction.left:
                            self.spaceship.set_direction(Direction.none)
                    elif event.key == pygame.K_RIGHT:
                        # Check the direction change is relevant
                        if self.spaceship.get_direction() == Direction.right:
                            self.spaceship.set_direction(Direction.none)

            # Calculate the next locations of everything
            self.spaceship.move()
            self.missile_left.move()
            self.missile_right.move()
            self.game.run()
            if self.game.end_level():
                self.game.next_level()

            # A bit of missile logic - reloading when off the screen
            if self.missile_left.is_away():
                self.missile_left.reload()
            if self.missile_right.is_away():
                self.missile_right.reload()

            # Update the display
            self.screen.draw()
            self.missile_left.draw()
            self.missile_right.draw()
            self.spaceship.draw()
            self.game.draw()

            pygame.display.update()


if __name__ == '__main__':
    space = Space()
    space.main()
