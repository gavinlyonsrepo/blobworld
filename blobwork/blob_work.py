""" module imported into blobworld containing functions for various utilises"""

# ======== IMPORTS ===========
from tkinter import Tk
from tkinter import messagebox
import numpy as np


# ===================== FUNCTIONS =========================
def is_touching(bone, btwo):
    """check if blob touching passed a blue blob and another color blob
    usings numpy.linalg.norm """
    return np.linalg.norm(np.array([bone.x, bone.y]) - np.array([btwo.x, btwo.y])) < (bone.size + btwo.size)


def get_size(list_of_blobs):
    """function to sum size of blobs for main display passed a list of blobs"""
    total = 0
    for blob_id, blob_object, in list_of_blobs.copy().items():
        total += blob_object.size
    return total


def my_text_box(text):
    """function to handle text message passed displays using tkhinter"""
    Tk().wm_withdraw()
    messagebox.showinfo("BlobWorld", text)
    Tk().destroy()
    return


def handle_collisions(blob_list):
    """ function to handle collisions of blobs passed a list of 3 dictionaries"""
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


def test():
    """import code"""
    pass

# ===============MAIN =============


if __name__ == '__main__':
    test()

# =============== END ===============
