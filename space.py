from screen import Screen
from gameplay import Gameplay
import pygame


class Space(object):
    def __init__(self):
        # Initialization
        pygame.init()
        self.clock = pygame.time.Clock()

        # Screen class holds the actual window and whatever is in the background, like stars and planets
        self.screen = Screen()

        # The Gameplay class holds the main game business logic
        self.game = Gameplay(self, self.screen)

        # Caption and icon
        pygame.display.set_caption("Space")
        pic_logo = pygame.image.load("res/spaceship_N_00.png")
        pygame.display.set_icon(pic_logo)

        # Start running :)
        self.running = True

        # Even though the default initialization has been performed, this will pop up the first level number
        self.game.initialize_level()

    def quit(self):
        """
        Getting here will cause the game loop to end
        """
        self.running = False

    def main(self):
        """
        Main game loop lives here
        """

        while self.running:
            # Make sure the game pace is steady
            self.clock.tick(60)
            # Check for events
            self.game.handle_events()
            # Move all game objects
            self.game.run()
            # Redraw everything
            self.game.draw()
            # Update the display
            pygame.display.update()


if __name__ == '__main__':
    space = Space()
    space.main()
