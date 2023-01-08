from globals import DATA
from cogmap import Cogmap
from event import EventRealisation, EventMemory
from structure import structure_realisation, structure_memory
from grower import init_struct, grow_step
from common_utils import HtmlLogger
from evaluator import eval_user_properties_of_struct

import matplotlib.pyplot as plt


def train(class_num, max_epochs=10):
    DATA.reset_class_num(class_num)
    struct = init_struct()

    f1_history = []
    while True:
        grow_step(struct)
        F1 = eval_user_properties_of_struct(struct)
        f1_history.append(F1)

        print("F1 = " + str(F1) + "-------------------------------------------------------------------------------")
        if F1 > 0.8:
            break
        if len(f1_history) == max_epochs:
            break

    # лог:
    train_logger = HtmlLogger("TRAIN_LOG")
    fig, axs = plt.subplots()
    train_logger.add_text("f1_history:")
    axs.plot(f1_history)
    train_logger.add_fig(fig)


train(201)





