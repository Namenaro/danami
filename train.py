from globals import GLOBALS
from cogmap import Cogmap
from event import EventMemory

from grower import get_dammy_struct_and_realisation, GrowEngine
from common_utils import HtmlLogger
from globals import GLOBALS
from drawers import StructColorator, draw_examples_recognition, draw_process_precognition_on_cogmap, draw_realisation_on_ax, draw_stat_object


import matplotlib.pyplot as plt
import random

def LOG_every_step(structure, master_realisation, master_cogmap, colorator, stat_object, step_num):
    # ----------------------------------------------------------------------------------------:
    #-----ОБЩИЙ ЛОГ---------------------------------------------------------------------------:
    main_log = GLOBALS.LOG_GROUTH

    # 1. Как выглядит мастер-реализация на данном шаге
    main_log.add_line_big()
    main_log.add_text("Шаг роста " + str(step_num) + ", F1 = " + str(stat_object.get_F1()))
    fig, ax = plt.subplots(figsize=(GLOBALS.FIGSIZE, GLOBALS.FIGSIZE), dpi=GLOBALS.DPI)
    draw_realisation_on_ax(master_realisation, colorator, structure, master_cogmap, ax)
    main_log.add_fig(fig)

    # 2. как структура распозналась на разных изображениях
    target_test_cogmaps = GLOBALS.DATA.get_TRUE_test()
    main_log.add_text("Примеры распознавания  стр-ры на прямых изображениях из теста:")
    draw_examples_recognition(colorator, structure, target_test_cogmaps, main_log)

    # 3. Гистограмма распределения энергий на прямых и констрастных (тест)  на данном шаге
    main_log.add_text("Гистограммы энергий на тесте:")
    draw_stat_object(stat_object, main_log)

    # ----------------------------------------------------------------------------------------:
    # -----ВСПОМОГАТЕЛЬНЫЙ ЛОГ----------------------------------------------------------------:

    # 1. Пример процесса распознавания на конкретной картинке (как растут ростки распознавания)
    logger_recognition_process = GLOBALS.LOG_RECOG
    logger_recognition_process.add_text("ШАГ роста " + str(step_num))
    logger_recognition_process.add_text("Распознаваемая структура (точнее, ее текущая мастер_реализация) -")
    fig, ax = plt.subplots(figsize=(8, 8), dpi=60)
    draw_realisation_on_ax(master_realisation, colorator, structure, master_cogmap, ax)
    logger_recognition_process.add_fig(fig)

    logger_recognition_process.add_text("Процесс распознавания на некоторой картинке:")
    test_cogmap = GLOBALS.DATA.get_TRUE_test()[0]

    draw_process_precognition_on_cogmap(colorator, structure, test_cogmap, logger_recognition_process)
    logger_recognition_process.add_line_little()


def LOG_learning_curve(F1_history):
    fig, ax = plt.subplots()
    ax.plot(F1_history, color='blue')
    ax.set_ylim([-0.1, 1.1])
    ax.set_ylabel('F1')
    ax.set_xlabel('шаг обучения')
    GLOBALS.LOG_CURVE.add_fig(fig)


def train(class_num, num_events):
    GLOBALS.DATA.reset_class_num(class_num)
    print("Learning started...")
    cogmap = GLOBALS.DATA.get_etalon_cogmap()
    master_struct, master_realisation = get_dammy_struct_and_realisation(cogmap, num_events=num_events)
    print("Master-realisation/partial-struct were created...")

    colorator = StructColorator()
    colorator.update(master_struct.get_all_global_ids())

    F1_history = []

    grow_engine = GrowEngine(master_struct, master_realisation)
    for step_num in range(1, len(master_realisation)):
        print("Learning: step " + str(step_num) + " started...")
        success = grow_engine.grow_step()
        if not success:
            print("Learning ended abruptly")
            break
        # -----------блок визуального логирования--------------

        LOG_every_step(structure = grow_engine.growing_structure,
                       master_realisation=grow_engine.growing_realisation,
                       master_cogmap = cogmap,
                       colorator=colorator,
                       stat_object=grow_engine.stat_object,
                       step_num=step_num)

        F1_history.append(grow_engine.stat_object.get_F1())
        # -----------------------------------------------------

    print("Learning ended fully!")
    LOG_learning_curve(F1_history)
    if len(F1_history) == 0:
        return 0
    return F1_history[-1]


if __name__ == "__main__":
    num_events = 4
    class_numbers = random.sample(range(0, 300))
    F1_sum = 0
    for class_number in class_numbers:
        GLOBALS.LOG_GROUTH.add_text("Symbol is " + str(class_number))
        F1 = train(class_number, num_events)
        F1_sum += F1

    mean_F1 = F1_sum/len(class_numbers)
    print("mean F1 = " + str(mean_F1))





