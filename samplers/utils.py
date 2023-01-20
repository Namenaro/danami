from globals import GLOBALS
from common_utils import Point

import random

def get_random_point():
    x = random.randint(0, GLOBALS.PIC_SIDE-1)
    y = random.randint(0, GLOBALS.PIC_SIDE-1)
    return Point(x, y)

def get_random_contrast_cogmap():
    random_contrast_cogmap = random.choice(GLOBALS.DATA.get_CONTRAST_train())
    return random_contrast_cogmap
