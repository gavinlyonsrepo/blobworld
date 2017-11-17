"""
module imported into blobworld
containing  class with methods to display blobs with move and check bounds
methods
"""

# ======== IMPORTS ===========
import random

# ========= CLASS ==========


class Blob:
    """class blob to display blobs with move and check bounds methods"""
    def __init__(self, color, x_boundary, y_boundary, size_range=(4, 8), movement_range=(-1, 2)):
        self.size = random.randrange(size_range[0], size_range[1])
        self.color = color
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x = random.randrange(0, self.x_boundary)
        self.y = random.randrange(0, self.y_boundary)
        self.movement_range = movement_range

    def move(self):
        """ method to move blob"""
        self.move_x = random.randrange(self.movement_range[0], self.movement_range[1])
        self.move_y = random.randrange(self.movement_range[0], self.movement_range[1])
        self.x += self.move_x
        self.y += self.move_y

    def check_bounds(self):
        """ method to check bounds of blob against set boundaries"""
        if self.x < 0:
            self.x = 0
        elif self.x > self.x_boundary:
            self.x = self.x_boundary

        if self.y < 0:
            self.y = 0
        elif self.y > self.y_boundary:
            self.y = self.y_boundary


def test():
    """import code"""
    pass

# =============== MAIN =============


if __name__ == '__main__':
    test()

# =============== END ===============
