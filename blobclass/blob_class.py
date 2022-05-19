"""
module imported into blobworld
containing  class with methods to display blobs with move and check bounds
methods
"""

# === IMPORTS ===
import random
import numpy as np
from blobwork import blob_work as Work

logger = Work.my_logging(__name__)

# === CLASS ===


class Blob:
    """super class blob to display blobs with move and check bounds methods"""
    def __init__(self, color, x_boundary, y_boundary,
                 size_range=(4, 8), movement_range=(-1, 2)):
        self.size = random.randrange(size_range[0], size_range[1])
        self.color = color
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x_pos = random.randrange(0, self.x_boundary)
        self.y_pos = random.randrange(0, self.y_boundary)
        self.movement_range = movement_range
        self.move_x = 0
        self.move_y = 0

    def move(self):
        """ method to move blob"""
        self.move_x = random.randrange(self.movement_range[0],
                                       self.movement_range[1])
        self.move_y = random.randrange(self.movement_range[0],
                                       self.movement_range[1])
        self.x_pos += self.move_x
        self.y_pos += self.move_y

    def check_bounds(self):
        """ method to check bounds of blob against set boundaries"""
        if self.x_pos < 0:
            self.x_pos = 0
        elif self.x_pos > self.x_boundary:
            self.x_pos = self.x_boundary

        if self.y_pos < 0:
            self.y_pos = 0
        elif self.y_pos > self.y_boundary:
            self.y_pos = self.y_boundary


# === Functions ===

def is_touching(bone, btwo):
    """check if blob touching passed a blob and another color blob
    usings numpy.linalg.norm """
    return np.linalg.norm(np.array([bone.x_pos, bone.y_pos])
                          - np.array([btwo.x_pos, btwo.y_pos])) < \
                         (bone.size + btwo.size)


def get_size(list_of_blobs):
    """function to sum size of blobs for main display passed a list of blobs"""
    total = 0
    for blob_id, blob_object, in list_of_blobs.copy().items():
        total += blob_object.size
    return total


def handle_collisions(blob_list):
    """ function to handle collisions of blobs
    passed a list of 3 dictionaries
    returns dictionaries and kill flag"""
    blues, reds, greens = blob_list
    kill = False
    # check if blues colliding with reds and blues
    # key , value , make a copy
    for blue_id, blue_blob, in blues.copy().items():
        for other_blobs in blues, reds:
            for other_blob_id, other_blob in other_blobs.copy().items():
                # Checking if blobs are touching
                if blue_blob == other_blob:
                    # it is touching itself , do nothing
                    pass
                else:
                    if is_touching(blue_blob, other_blob):
                        blue_blob + other_blob
                        kill = True
                        if other_blob.size <= 0:
                            del other_blobs[other_blob_id]

    # check if reds colliding with greens and reds
    # key , value , make a copy
    for red_id, red_blob, in reds.copy().items():
        for other_blobs in greens, reds:
            for other_blob_id, other_blob in other_blobs.copy().items():
                if red_blob == other_blob:
                    # it is touching itself , do nothing
                    pass
                else:
                    if is_touching(red_blob, other_blob):
                        red_blob + other_blob
                        kill = True
                        if other_blob.size <= 0:
                            del other_blobs[other_blob_id]

    # Check if greens colliding with blue and greens
    for green_id, green_blob, in greens.copy().items():
        for other_blobs in blues, greens:
            for other_blob_id, other_blob in other_blobs.copy().items():
                if green_blob == other_blob:
                    # it is touching itself , do nothing
                    pass
                else:
                    if is_touching(green_blob, other_blob):
                        green_blob + other_blob
                        kill = True
                        if other_blob.size <= 0:
                            del other_blobs[other_blob_id]
    return blues, reds, greens, kill


def start(text):
    """import code test"""
    logger.info(text)

# === MAIN ===


if __name__ == '__main__':
    start("main")
else:
    start(" Imported " + __name__)

# === END ===
