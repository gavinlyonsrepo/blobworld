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
from tkinter import *
from tkinter import messagebox

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
WHITE = (255, 255, 255)
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
        """blue blob eats red and blue"""
        logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
        if other_blob.color == RED:
            self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == GREEN:
            pass
        elif other_blob.color == BLUE:
            self.size += other_blob.size
            other_blob.size -= self.size
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')


class RedBlob(Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, RED, x_boundary, y_boundary)

    def __add__(self, other_blob):
        """red blob eats red and green"""
        logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
        if other_blob.color == RED:
            self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == GREEN:
            self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BLUE:
            pass
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')


class GreenBlob(Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, GREEN, x_boundary, y_boundary)

    def __add__(self, other_blob):
        """green blob eats blue and green"""
        logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
        if other_blob.color == RED:
            pass
        elif other_blob.color == GREEN:
            self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BLUE:
            self.size += other_blob.size
            other_blob.size -= self.size
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')

def is_touching(b1, b2):
    """check if blob touching passed a blue blob and another color blob
    usings numpy.linalg.norm """
    return np.linalg.norm(np.array([b1.x, b1.y]) - np.array([b2.x, b2.y])) < (b1.size + b2.size)


def handle_collisions(blob_list):
    """ function to handle collisions of blobs passed a list of 3 dictionaries"""
    blues, reds, greens = blob_list
    # check if blues colling with reds and blues
    # key , value , make a copy
    for blue_id, blue_blob, in blues.copy().items():
        for other_blobs in blues, reds:
            for other_blob_id, other_blob in other_blobs.copy().items():
                # logging.debug(
                # 'Checking if blobs are touching {} + {}'.format(str(blue_blob.color), str(other_blob.color)))
                if blue_blob == other_blob:
                    # it is touching itself , do nothing
                    pass
                else:
                    if is_touching(blue_blob, other_blob):
                        blue_blob + other_blob
                        if other_blob.size <= 0:
                           del other_blobs[other_blob_id]

    # check if reds colling with greens and reds
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
                        if other_blob.size <= 0:
                            del other_blobs[other_blob_id]

    return blues, reds, greens


def draw_environment(blob_list):
    """ function to draw the environment passed a list of 3 dictionaries """
    blues, reds, greens = handle_collisions(blob_list)
    GAME_DISPLAY.fill(BEIGE)
    # display labels section
    elapsed_time = time.time() - START_TIME
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    timelabel = myfont.render("Time: {0:.2f}".format(elapsed_time), 1, BLACK, WHITE)
    GAME_DISPLAY.blit(timelabel, (10, 60))
    label_list = [None] * 3
    label_list[0] = myfont.render("Reds left: {}".format(len(reds)), 1, RED, WHITE)
    label_list[1] = myfont.render("Green left:{}".format(len(greens)), 1, GREEN, WHITE)
    label_list[2] = myfont.render("Blues left:{}".format(len(blues)), 1, BLUE, WHITE)
    for x in range(0, 3):
        GAME_DISPLAY.blit(label_list[x], (10, 20*x))

    for blob_dict in blob_list:
        for blob_id in blob_dict:
            blob = blob_dict[blob_id]
            pygame.draw.circle(GAME_DISPLAY, blob.color, [blob.x, blob.y], blob.size)
            blob.move()
            blob.check_bounds()

    pygame.display.update()
    return blues, reds, greens

def my_text_box(text):
    """function to handle text message"""
    Tk().wm_withdraw()
    messagebox.showinfo("BLOB", text)
    return

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
                    my_text_box("Goodbye")
                    pygame.quit()
                    quit()

            blue_blobs, red_blobs, green_blobs = draw_environment([blue_blobs, red_blobs, green_blobs])
            if (len(blue_blobs) + len(red_blobs) + len(green_blobs)) == 1:
                my_text_box("Game over")
                pygame.quit()
                quit()
            # frames per second
            CLOCK.tick(60)
        except Exception as e:
            logging.critical(str(e))
            my_text_box("Error")
            pygame.quit()
            quit()
            break

# =====================MAIN===============================

if __name__ == '__main__':
    main()

# =====================END===============================