from globals import GLOBALS
from cogmap import Cogmap
from event import EventRealisation, EventMemory
from structure import structure_realisation, structure_memory
from grower import init_struct, grow_step
from common_utils import HtmlLogger
from evaluator import eval_user_properties_of_struct
from grower import GrowStep
from globals import GLOBALS

import matplotlib.pyplot as plt


def train(class_num, max_epochs=10):
    #TODO завести тут логгер, который в реальном времени будет логировать историю обучения: f1, win_quality_difference
    GLOBALS.DATA.reset_class_num(class_num)

    etalon_pic = GLOBALS.DATA.get_etalon()
    cogmap = Cogmap(etalon_pic)

    struct, master_realisation = init_struct(cogmap)

    grow_engine = GrowStep(struct, master_realisation, cogmap)
    for i in range(max_epochs):
        grow_engine.grow_step()
        # логировать в глобальный лог результаты grow_step:
        # 1) grow_engine.stat_object 2)grow_engine.structure


train(201)





