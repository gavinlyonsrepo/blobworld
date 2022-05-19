#!/usr/bin/env python3
"""python script to display pygame automated animation of a blobworld"""

# === HEADER ====
# title             :blobworld.py
# description       :script to display pygame automated animation
# author            :Gavin Lyons
# version           :1.2-3
# web               :https://github.com/gavinlyonsrepo/blobworld
# python_version    :3.10

# === IMPORTS ====
# Import the system modules needed to run blobworld.py
import tkinter as tk
from tkinter import messagebox
from importlib import resources
import time
import sys
import pygame



# my modules
from blobclass import blob_class
from blobwork import blob_work as Work

# === CLASS SECTION ===


class BlobWorldPyGame():
    """ class docstring"""
    def __init__(self):
        self.game_display = pygame.display.set_mode((Work.my_cfg_file.screen_width,
                                                     Work.my_cfg_file.screen_height))
        self.start_time = time.time()
        self.game_clock = pygame.time.Clock()
        self.color = {'BLACK': (0, 0, 0), 'SLIVER': (192, 192, 192), 'WHITE': (255, 255, 255),
                      'BEIGE': (238, 232, 170), 'BLUE': (0, 0, 255), 'GREEN': (0, 139, 69),
                      'RED': (255, 0, 0)}

    def main(self):
        """main game loop"""
        # 1 . Setup
        logger.info(" Blobworld Starting %s",
                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        self.start_time = time.time()
        pygame.init()
        pygame.display.set_caption("BLOB WORLD!")
        self.icon_work_func()
        self.play_sound("start.wav")
        # 2. create the blob dictionaries
        blue_blobs = dict(enumerate(
            [BlueBlob(Work.my_cfg_file.screen_width,
                      Work.my_cfg_file.screen_height - 130)
             for i in range(Work.my_cfg_file.starting_blue_blobs)]))
        red_blobs = dict(enumerate(
            [RedBlob(Work.my_cfg_file.screen_width,
                     Work.my_cfg_file.screen_height - 130)
             for i in range(Work.my_cfg_file.starting_red_blobs)]))
        green_blobs = dict(enumerate(
            [GreenBlob(Work.my_cfg_file.screen_width,
                       Work.my_cfg_file.screen_height - 130)
             for i in range(Work.my_cfg_file.starting_green_blobs)]))

        # 3. Main loop
        while True:
            try:
                for event in pygame.event.get():
                    # user press X on window
                    if event.type == pygame.QUIT:
                        self.my_quit_func("You closed\nthe window.\nGoodbye!", False)
                    # keyboard input
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.my_quit_func("You Pressed\nQ to quit", True)
                        elif event.key == pygame.K_p:
                            self.paused_func()
                        else:
                            pass

                # draw env return blobs dictionaries
                blue_blobs, red_blobs, green_blobs = \
                    self.draw_environment([blue_blobs, red_blobs, green_blobs])
                # if only one blob left quit
                if (len(blue_blobs) + len(red_blobs) + len(green_blobs)) == 1:
                    self.my_quit_func("Game Over!\nWe have a winner!")

                self.game_clock.tick(Work.my_cfg_file.clock_tick)
            except Exception as error:
                logger.exception(" Error in main loop :: %s ", error)
                self.my_quit_func(error, False)

    def draw_environment(self, blob_list):
        """ function to draw the environment
        passed a list of 3 dictionaries """
        try:
            # check for collisions
            blues, reds, greens, kill = blob_class.handle_collisions(blob_list)

            if kill:
                self.play_sound("kill.wav")

            # set background
            BlobGame.game_display
            BlobGame.game_display.fill(BlobGame.color[Work.my_cfg_file.back_ground_color])

            # display labels section
            elapsed_time = time.time() - BlobGame.start_time
            elapsed_time = int(elapsed_time)
            fps = self.game_clock.get_fps()
            myfont = pygame.font.SysFont("Comic Sans MS", 30)
            timelabel = myfont.render("Time: {0}:{1:0>2} FPS: {2:.2f} {3:110}".format(*divmod(elapsed_time, 60), fps, " "),
                                      1, BlobGame.color['BLACK'], BlobGame.color['SLIVER'])
            label_list = [None] * 3
            size_reds = blob_class.get_size(reds)
            size_greens = blob_class.get_size(greens)
            size_blues = blob_class.get_size(blues)
            label_list[0] = myfont.render("Reds     ::  left = {0:5} size =   {1:2} {2:90}"
                                          .format(len(reds), size_reds, " "), 1,
                                          BlobGame.color['RED'],
                                          BlobGame.color['SLIVER'])
            label_list[1] = myfont.render("Greens ::  left =  {0:5} size =   {1:2} {2:90}".
                                          format(len(greens), size_greens, " "), 1,
                                          BlobGame.color['GREEN'],
                                          BlobGame.color['SLIVER'])
            label_list[2] = myfont.render("Blues    ::  left = {0:5} size =   {1:2} {2:90}".
                                          format(len(blues), size_blues, " "), 1,
                                          BlobGame.color['BLUE'],
                                          BlobGame.color['SLIVER'])

            for blob_dict in blob_list:
                for blob_id in blob_dict:
                    blob = blob_dict[blob_id]
                    pygame.draw.circle(BlobGame.game_display,
                                       blob.color, [blob.x_pos, blob.y_pos], blob.size)
                    blob.move()
                    blob.check_bounds()
            text_offset = Work.my_cfg_file.screen_height-60
            BlobGame.game_display.blit(timelabel, (1, text_offset-20))
            for labelx in range(0, 3):
                BlobGame.game_display.blit(label_list[labelx], (1, text_offset+(labelx*20)))

            pygame.display.update()
            return blues, reds, greens
        except Exception as error:
            logger.exception(" Error in :: draw_environment function :: %s", error)
            self.my_quit_func(error, False)

    def my_quit_func(self, text, back_to_main):
        """Function to handle exit"""
        self.play_sound("end.wav")
        my_text_box(text)
        logger.info(" Blobworld exiting %s", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        pygame.quit
        if back_to_main is True:
            main_screen()
        else:
            sys.exit()

    def paused_func(self):
        """ method to handle pause in game"""
        try:
            self.play_sound("pause.wav")
            my_text_box("Game is paused. \nPress OK to continue.")
            self.play_sound("pause.wav")
        except Exception as error:
            logger.warning(" Error in  Pause function :: %s", error)

    def play_sound(self, sound_file):
        """function to play sound file"""
        try:
            with resources.open_binary('blobworld', sound_file) as file_pointer:
                sound_file_object = pygame.mixer.Sound(file_pointer)
                pygame.mixer.Sound.play(sound_file_object)
                pygame.mixer.music.stop()
        except Exception as error:
            logger.warning(" Error in play sound function :: %s", error)

    def icon_work_func(self):
        """ set the icon catch an error if issue with the file """
        try:
            game_icon_file = 'blobicon.png'
            with resources.open_binary('blobworld', game_icon_file) as file_pointer:
                game_icon_object = pygame.image.load(file_pointer)
                pygame.display.set_icon(game_icon_object)
        except Exception as error:
            logger.warning(" Error in draw icon function :: %s",  error)


class BlueBlob(blob_class.Blob):
    """ subclass of Blob contains an add method to eat other color blobs"""
    def __init__(self, x_boundary, y_boundary):
        self.size_limit = Work.my_cfg_file.max_size_blob
        blob_class.Blob.__init__(self, BlobGame.color['BLUE'], x_boundary, y_boundary)

    def __add__(self, other_blob):
        """blue blob method blue  eats red and blue"""
        logger.info(' Blob add op %s + %s', self.color, other_blob.color)
        if other_blob.color == BlobGame.color['RED']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BlobGame.color['GREEN']:
            pass
        elif other_blob.color == BlobGame.color['BLUE']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')


class RedBlob(blob_class.Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        blob_class.Blob.__init__(self, BlobGame.color['RED'], x_boundary, y_boundary)
        self.size_limit = Work.my_cfg_file.max_size_blob

    def __add__(self, other_blob):
        """red blob eats red and green"""
        logger.info(' Blob add op %s + %s', self.color, other_blob.color)
        if other_blob.color == BlobGame.color['RED']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BlobGame.color['GREEN']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BlobGame.color['BLUE']:
            pass
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')


class GreenBlob(blob_class.Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        blob_class.Blob.__init__(self, BlobGame.color['GREEN'], x_boundary, y_boundary)
        self.size_limit = Work.my_cfg_file.max_size_blob

    def __add__(self, other_blob):
        """green blob eats blue and green"""
        logger.info(' Blob add op %s + %s', self.color, other_blob.color)
        if other_blob.color == BlobGame.color['RED']:
            pass
        elif other_blob.color == BlobGame.color['GREEN']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BlobGame.color['BLUE']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        else:
            raise Exception(
                            'Tried to combine one or multiple blobs of unsupported colors.')


class BlackBlob(blob_class.Blob):
    """ subclass of Blob """
    def __init__(self, x_boundary, y_boundary):
        blob_class.Blob.__init__(self, BlobGame.color['BLACK'], x_boundary, y_boundary)
        self.size_limit = Work.my_cfg_file.max_size_blob

    def __add__(self, other_blob):
        """green blob eats blue and green"""
        logger.info(' Blob add op %s + %s', self.color, other_blob.color)
        if other_blob.color == BlobGame.color['RED']:
            pass
        elif other_blob.color == BlobGame.color['GREEN']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == BlobGame.color['BLUE']:
            if self.size < self.size_limit:
                self.size += other_blob.size
            other_blob.size -= self.size
        else:
            raise Exception(
                            'Tried to combine one or multiple blobs of unsupported colors.')

# === FUNCTION SECTION ===


def my_text_box(text):
    """function to handle text message passed displays using tkhinter"""
    tk.Tk().wm_withdraw()
    messagebox.showinfo(" BlobWorld :: ", text)
    tk.Tk().destroy()


def main_screen():
    """ function to display main screen before
    and after game start uses tkinter"""
    root = tk.Tk()
    root.geometry('600x400')
    root.title("Welcome to Blob World")

    def start_pressed():
        root.destroy()
        BlobGame.main()

    def high_score():
        pass  # TODO

    def quit_pressed():
        sys.exit()

    start_button = tk.Button(root, text="  START  ", relief='raised', borderwidth=5, command=start_pressed)
    high_scores_button = tk.Button(root, text="HIGH SCORES", relief='raised', borderwidth=5, state='disabled', command=high_score)
    quit_button = tk.Button(root, text="  QUIT   ", relief='raised', borderwidth=5, command=quit_pressed)

    start_button.place(x=20, y=20)
    high_scores_button.place(x=250, y=20)
    quit_button.place(x=500, y=20)

    label = tk.Label(root, text="  : Information :  ", relief='raised', border=True, )
    label.place(x=255, y=75)

    listbox = tk.Listbox(root, width=70, relief='sunken')
    listbox.insert(1, "Blob World")
    listbox.insert(2, "Version :: 1.2")
    listbox.insert(3, "Written :: Gavin Lyons")
    listbox.insert(4, "URL :: https://github.com/gavinlyonsrepo/blobworld")
    listbox.insert(5, " P :: Pause")
    listbox.insert(6, " Q :: Quit")
    listbox.place(x=20, y=100)

    root.mainloop()
    root.quit()


# === MAIN ===
logger = Work.my_logging(__name__)
BlobGame = BlobWorldPyGame()

if __name__ == '__main__':
    logger.info(" BlobWorld %s ",  __name__)
    main_screen()
else:
    logger.info(" Imported %s",  __name__)
# === EOF ===
