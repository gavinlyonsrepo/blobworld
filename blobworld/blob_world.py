#!/usr/bin/env python3
"""python script to display pygame automated animation of a blobworld"""

# =========================HEADER=======================================
# title             :blobworld.py
# description       :python script to display pygame automated animation of a blobworld
# author            :Gavin Lyons
# date              :01/11/2017
# version           :1.1-2
# web               :https://github.com/gavinlyonsrepo/blobworld
# mail              :glyons66@hotmail.com
# python_version    :3.6.0

# ==========================IMPORTS======================
# Import the system modules needed to run blobworld.py
import logging
import time
import os
import configparser
import pygame


# my modules
from blobclass import blob_class 
from blobwork import blob_work as Work

# set up the logfile
logging.basicConfig(filename='/tmp/bloblogfile.log', level=logging.INFO)

# =======================GLOBALS=========================

# set the path for config file holds starting blobs
DESTCONFIG = os.environ['HOME'] + "/.config/blobworld"
if not os.path.exists(DESTCONFIG):
    os.makedirs(DESTCONFIG)
DESTCONFIG = DESTCONFIG + "/" + "blobworld.cfg"
if os.path.isfile(DESTCONFIG):
    # if config file exists read it catch exception and out of limit values
    try:
        config_file = configparser.ConfigParser()
        config_file.read(DESTCONFIG)
        STARTING_BLUE_BLOBS = int(config_file.get("MAIN", "STARTING_BLUE_BLOBS"))
        STARTING_RED_BLOBS = int(config_file.get("MAIN", "STARTING_RED_BLOBS"))
        STARTING_GREEN_BLOBS = int(config_file.get("MAIN", "STARTING_GREEN_BLOBS"))
        sum_blobs = STARTING_BLUE_BLOBS + STARTING_GREEN_BLOBS + STARTING_RED_BLOBS
        if sum_blobs <= 1 or sum_blobs >= 150:
            print("config file sum {}".format(sum_blobs))
            print("Cfg file: sum values blobs must between 1 & 150")
            logging.critical("Cfg file: sum values blobs must between 1 & 150 {}".format(sum_blobs))
            quit()
    except Exception as error:
        logging.critical("Config file error at {} ".format(DESTCONFIG) + " " + str(error))
        print("Config file error at {} ".format(DESTCONFIG))
        quit()
else:
    # set default value if no config file
    logging.warning("Config file is missing at {}".format(DESTCONFIG))
    print("Config file is missing at {}".format(DESTCONFIG))
    STARTING_BLUE_BLOBS = 15
    STARTING_RED_BLOBS = 15
    STARTING_GREEN_BLOBS = 15

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
SLIVER = (192, 192, 192)
WHITE = (255, 255, 255)
BEIGE = (238, 232, 170)
BLUE = (0, 0, 255)
GREEN = (0, 139, 69)
RED = (255, 0, 0)

CLOCK = pygame.time.Clock()
START_TIME = time.time()
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOB WORLD!")
# set the icon catch an error if issue with the file
try:
    gameicon = pygame.image.load('/usr/share/pixmaps/blobicon.png')
    pygame.display.set_icon(gameicon)
except Exception as error4:
    print("Problem with icon file blobicon.png")
    logging.error(str(error4))


# ==================== CLASS SECTION===============================

class BlueBlob(blob_class.Blob):
    """ subclass of Blob contains an add method to eat other color blobs"""
    def __init__(self, x_boundary, y_boundary):
        blob_class.Blob.__init__(self, BLUE, x_boundary, y_boundary)

    def __add__(self, other_blob):
        """blue blob method blue  eats red and blue"""
        # logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
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


class RedBlob(blob_class.Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        blob_class.Blob.__init__(self, RED, x_boundary, y_boundary)

    def __add__(self, other_blob):
        """red blob eats red and green"""
        # logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
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


class GreenBlob(blob_class.Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        blob_class.Blob.__init__(self, GREEN, x_boundary, y_boundary)

    def __add__(self, other_blob):
        """green blob eats blue and green"""
        # logging.info('Blob add op {} + {}'.format(str(self.color), str(other_blob.color)))
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

# ==================== FUNCTION SECTION===============================


def play_sound(sound_file):
    """function to play sound file"""
    try:
        start_sound = pygame.mixer.Sound('/usr/share/sounds/blobworld/' + sound_file)
        pygame.mixer.Sound.play(start_sound)
        pygame.mixer.music.stop()
    except Exception as error1:
        print("Problem with sound file {}".format(sound_file))
        logging.error(str(error1))


def draw_environment(blob_list):
    """ function to draw the environment passed a list of 3 dictionaries """
    # check for collisions
    blues, reds, greens, kill = Work.handle_collisions(blob_list)

    if kill:
        play_sound("kill.wav")

    # set background
    GAME_DISPLAY.fill(BEIGE)

    # display labels section
    elapsed_time = time.time() - START_TIME
    elapsed_time = int(elapsed_time)
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    timelabel = myfont.render("Time: {0}:{1} {2:120}".format(*divmod(elapsed_time, 60), " "), 1, BLACK, SLIVER)
    GAME_DISPLAY.blit(timelabel, (5, 510))
    label_list = [None] * 3
    size_reds = Work.get_size(reds)
    size_greens = Work.get_size(greens)
    size_blues = Work.get_size(blues)
    label_list[0] = myfont.render("Reds     =  left : size = {0:5} : {1:2} {2:90}".format(len(reds), size_reds, " "), 1, RED, SLIVER)
    label_list[1] = myfont.render("Greens =  left : size = {0:5} : {1:2} {2:90}".format(len(greens), size_greens, " "), 1, GREEN, SLIVER)
    label_list[2] = myfont.render("Blues    =  left : size = {0:5} : {1:2} {2:90}".format(len(blues), size_blues, " "), 1, BLUE, SLIVER)
    for labelx in range(0, 3):
        GAME_DISPLAY.blit(label_list[labelx], (5, 530+(labelx*20)))

    for blob_dict in blob_list:
        for blob_id in blob_dict:
            blob = blob_dict[blob_id]
            pygame.draw.circle(GAME_DISPLAY, blob.color, [blob.x, blob.y], blob.size)
            blob.move()
            blob.check_bounds()

    pygame.display.update()
    return blues, reds, greens


def my_quit_func(text):
    """Function to handle exit"""
    play_sound("end.wav")
    Work.my_text_box(text)
    logging.info("blobworld exiting {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    pygame.quit
    quit()
    return


def main():
    """main function loop"""
    pygame.init()
    Work.my_text_box("Hello and Welcome to Blobworld. https://github.com/gavinlyonsrepo/blobworld")
    play_sound("start.wav")
    # create the blob dictionaries
    blue_blobs = dict(enumerate([BlueBlob(WIDTH, HEIGHT-110) for i in range(STARTING_BLUE_BLOBS)]))
    red_blobs = dict(enumerate([RedBlob(WIDTH, HEIGHT-110) for i in range(STARTING_RED_BLOBS)]))
    green_blobs = dict(enumerate([GreenBlob(WIDTH, HEIGHT-110) for i in range(STARTING_GREEN_BLOBS)]))

    # Pause Variable
    pause = False

    while True:
        try:
            for event in pygame.event.get():
                # user press X on window
                if event.type == pygame.QUIT:
                    my_quit_func("You closed the window, Goodbye")
                # keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        my_quit_func("You pressed q to quit, Goodbye")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = True
                        play_sound("pause.wav")
                while pause == 1:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                pause = False
                                play_sound("pause.wav")

            # draw env return blobs dictionaries
            blue_blobs, red_blobs, green_blobs = draw_environment([blue_blobs, red_blobs, green_blobs])
            # if only one blob left quit
            if (len(blue_blobs) + len(red_blobs) + len(green_blobs)) == 1:
                my_quit_func("Game Over, we have a winner")

            # frames per second
            CLOCK.tick(60)
        except Exception as error2:
            print(error2)
            logging.critical(str(error2))
            Work.my_text_box("Error Exception in main loop, see /tmp/bloblogfile.log ")
            print(error2)
            my_quit_func(error2)
            break

# =====================MAIN===============================


if __name__ == '__main__':
    main()

# =====================END===============================
