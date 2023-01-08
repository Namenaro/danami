from globals import GLOBALS
from cogmap import *
from common_utils import *


def test_cogmap(log_name="TEST_COGMAP"):
    GLOBALS.DATA.reset_class_num(0)
    etalon_pic = GLOBALS.DATA.get_etalon()

    logger = HtmlLogger(log_name)

    cogmap = Cogmap(etalon_pic)
    draw_cogmap(cogmap, logger)
    draw_cogmap1(cogmap, logger)

test_cogmap()