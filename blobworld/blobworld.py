#!/usr/bin/env python3
"""python script to display pygame automated animation of a blobworld"""

#=========================HEADER=======================================
# title             :blobwold.py
# description       :python script to display pygame automated animation of a blobworld
# author            :Gavin Lyons
# date              :01/11/2017
# version           :1.0-1
# web               :https://github.com/gavinlyonsrepo/blobworld
# mail              :glyons66@hotmail.com
# python_version    :3.6.0

# ==========================IMPORTS======================
# Import the system modules needed to run blobwold.py
import logging
import time
import pygame
import numpy as np
# my modules
from blobclass import Blob

logging.basicConfig(filename='/tmp/bloblogfile.log', level=logging.INFO)

""" logging level information
DEBUG   Detailed information, typically of interest only when diagnosing problems.
INFO    Confirmation that things are working as expected.
WARNING An indication that unexpected happened, or indicative of some problem in the near future
ERROR   Due to a more serious problem, the software has not been able to perform some function.
CRITICAL    A serious error, indicating that the program itself may be unable to continue running.
"""

# =======================GLOBALS=========================
STARTING_BLUE_BLOBS = 15
STARTING_RED_BLOBS = 15
STARTING_GREEN_BLOBS = 15

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
BEIGE = (238, 232, 170)
BLUE = (0, 0, 255)
GREEN = (0, 139, 69)
RED = (255, 0, 0)

GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOB WORLD!")
CLOCK = pygame.time.Clock()
START_TIME = time.time()

# ====================FUNCTION CLASS SECTION===============================


class BlueBlob(Blob):
    """ subclass of Blob contains an add method to eat other color blobs"""
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, BLUE, x_boundary, y_boundary)

    def __add__(self, other_blob):
        logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
        if other_blob.color == RED:
            self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == GREEN:
            self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BLUE:
            self.size += other_blob.size
            other_blob.size -= self.size
            # pass
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')


class RedBlob(Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, RED, x_boundary, y_boundary)


class GreenBlob(Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, GREEN, x_boundary, y_boundary)


def is_touching(b1, b2):
    """check if blob touching passed a blue blob and another color blob
    usings numpy.linalg.norm """
    return np.linalg.norm(np.array([b1.x, b1.y]) - np.array([b2.x, b2.y])) < (b1.size + b2.size)


def handle_collisions(blob_list):
    """ function to handle collusions of blobs passed a list of 3 dictionaries"""
    blues, reds, greens = blob_list
    # key , value , make a copy
    for blue_id, blue_blob, in blues.copy().items():
        for other_blobs in blues, reds, greens:
            for other_blob_id, other_blob in other_blobs.copy().items():
                logging.debug(
                    'Checking if blobs are touching {} + {}'.format(str(blue_blob.color), str(other_blob.color)))
                if blue_blob == other_blob:
                    # it is touching itself , do nothing
                    pass
                else:
                    if is_touching(blue_blob, other_blob):
                        blue_blob + other_blob
                        if other_blob.size <= 0:
                            del other_blobs[other_blob_id]
                        if blue_blob.size <= 0:
                            del blues[blue_id]

    return blues, reds, greens


def draw_environment(blob_list):
    """ function to draw the environment passed a list of 3 dictionaries """
    blues, reds, greens = handle_collisions(blob_list)
    GAME_DISPLAY.fill(BEIGE)
    # display labels section
    elapsed_time = time.time() - START_TIME
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    label1 = myfont.render("Reds left: {}".format(len(reds)), 1, RED)
    label2 = myfont.render("Green left:{}".format(len(greens)), 1, GREEN)
    label3 = myfont.render("Blues left:{}".format(len(blues)), 1, BLUE)
    label4 = myfont.render("Time: {0:.2f}".format(elapsed_time), 1, BLACK)
    GAME_DISPLAY.blit(label1, (20, 20))
    GAME_DISPLAY.blit(label2, (20, 40))
    GAME_DISPLAY.blit(label3, (20, 60))
    GAME_DISPLAY.blit(label4, (20, 80))

    for blob_dict in blob_list:
        for blob_id in blob_dict:
            blob = blob_dict[blob_id]
            pygame.draw.circle(GAME_DISPLAY, blob.color, [blob.x, blob.y], blob.size)
            blob.move()
            blob.check_bounds()

    pygame.display.update()
    return blues, reds, greens

# =====================MAIN===============================

def main():
    """main function loop"""
    pygame.init()
    blue_blobs = dict(enumerate([BlueBlob(WIDTH, HEIGHT) for i in range(STARTING_BLUE_BLOBS)]))
    red_blobs = dict(enumerate([RedBlob(WIDTH, HEIGHT) for i in range(STARTING_RED_BLOBS)]))
    green_blobs = dict(enumerate([GreenBlob(WIDTH, HEIGHT) for i in range(STARTING_GREEN_BLOBS)]))

    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            blue_blobs, red_blobs, green_blobs = draw_environment([blue_blobs, red_blobs, green_blobs])
            # frames per second
            CLOCK.tick(60)
        except Exception as e:
            logging.critical(str(e))
            pygame.quit()
            quit()
            break


if __name__ == '__main__':
    main()

# =====================END===============================