class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.num_of_invaders = 0
        self.asteroids_probability = 0

    def set_num_of_invaders(self, num):
        self.num_of_invaders = num

    def get_num_of_invaders(self):
        return self.num_of_invaders

    def set_asteroids_probability(self, probability):
        self.asteroids_probability = probability

    def get_asteroids_probability(self):
        return self.asteroids_probability
