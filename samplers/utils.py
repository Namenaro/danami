from globals import GLOBALS
from common_utils import Point

import random

def get_random_point():
    x = random.randint(GLOBALS.PIC_SIDE)
    y = random.randint(GLOBALS.PIC_SIDE)
    return Point(x,y)

def get_random_contrast_cogmap():
    random_contrast_cogmap = random.choice(GLOBALS.GLOBAL_IDS_GEN.get_contrast_cogmaps())
    return random_contrast_cogmap