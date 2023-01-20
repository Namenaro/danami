from globals import GLOBALS
from cogmap import *
from common_utils import *
from drawers import draw_cogmap, draw_cogmap1


def test_cogmap(log_name="TEST_COGMAP"):
    GLOBALS.DATA.reset_class_num(201)


    logger = HtmlLogger(log_name)

    cogmap = GLOBALS.DATA.get_TRUE_test()[0]#Cogmap(etalon_pic)
    draw_cogmap(cogmap, logger)
    draw_cogmap1(cogmap, logger)


if __name__ == "__main__":
    test_cogmap()