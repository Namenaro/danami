from globals import *
from cogmap import *
from common_utils import *

def test_cogmap(log_name="TEST_COGMAP"):
    DATA.reset_class_num(200)
    etalon_pic = DATA.get_etalon()
    logger = HtmlLogger(log_name)
    cogmap = Cogmap(etalon_pic)
    draw_cogmap(cogmap, logger)

test_cogmap()