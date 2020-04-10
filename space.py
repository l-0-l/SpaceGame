from direction import Direction
from screen import Screen
from player import Player
import pygame

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (0, 128, 128)
NOMINAL_ACCELERATION = 0.5

move_right = [pygame.image.load("res/spaceship_N_00.png"),
              pygame.image.load("res/spaceship_R_01.png"),
              pygame.image.load("res/spaceship_R_02.png"),
              pygame.image.load("res/spaceship_R_03.png"),
              pygame.image.load("res/spaceship_R_04.png"),
              pygame.image.load("res/spaceship_R_05.png"),
              pygame.image.load("res/spaceship_R_06.png")]

move_left = [pygame.image.load("res/spaceship_N_00.png"),
             pygame.image.load("res/spaceship_L_01.png"),
             pygame.image.load("res/spaceship_L_02.png"),
             pygame.image.load("res/spaceship_L_03.png"),
             pygame.image.load("res/spaceship_L_04.png"),
             pygame.image.load("res/spaceship_L_05.png"),
             pygame.image.load("res/spaceship_L_06.png")]

class Space(object):
    def __init__(self):
        # Initialization
        pygame.init()
        self.screen = Screen(width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             bg_color=BG_COLOR)
        self.player = Player(x=self.screen.width/2,
                             y=self.screen.height-self.screen.height/10,
                             screen=self.screen,
                             nominal_acceleration=NOMINAL_ACCELERATION,
                             pic_move_right=move_right,
                             pic_move_left=move_left)

        # Caption and icon
        pygame.display.set_caption("Space")
        pic_logo = pygame.image.load("res/spaceship_N_00.png")
        pygame.display.set_icon(pic_logo)
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
                    if event.key == pygame.K_LEFT:
                        self.player.set_direction(Direction.left)
                    if event.key == pygame.K_RIGHT:
                        self.player.set_direction(Direction.right)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        if self.player.get_direction() == Direction.left:
                            self.player.set_direction(Direction.none)
                    elif event.key == pygame.K_RIGHT:
                        if self.player.get_direction() == Direction.right:
                            self.player.set_direction(Direction.none)

            # Calculate the next player location on the x axis
            self.player.move()

            # Update the display
            self.screen.window.fill(self.screen.bg_color)
            self.screen.window.blit(self.player.get_current_pic(), (self.player.x, self.player.y))
            pygame.display.update()


if __name__ == '__main__':
    space = Space()
    space.main()
