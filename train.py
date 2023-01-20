from globals import GLOBALS
from cogmap import Cogmap
from event import EventRealisation, EventMemory

from grower import init_struct, grow_step
from common_utils import HtmlLogger
from grower import GrowStep
from globals import GLOBALS
from drawers import StructColorator, draw_examples_recognition, draw_process_precognition_on_cogmap, draw_realisation_on_ax, draw_stat_object

import matplotlib.pyplot as plt


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


def train(class_num, max_epochs=10):
    GLOBALS.DATA.reset_class_num(class_num)
    print("learning started...")
    cogmap = GLOBALS.DATA.get_etalon_cogmap()
    struct, master_realisation = init_struct(cogmap)

    colorator = StructColorator()
    F1_history = []

    grow_engine = GrowStep(struct, master_realisation, cogmap)
    for step_num in range(1, max_epochs):
        print("Learning: step " + str(step_num) + " started...")
        success = grow_engine.grow_step()
        if not success:
            print("Learninng ended because master-realisation can not grow further")
            break
        # -----------блок визуального логирования--------------
        colorator.update(grow_engine.structure.get_all_global_ids())

        LOG_every_step(grow_engine.structure, grow_engine.master_realisation,
                       grow_engine.master_cogmap, colorator,
                        grow_engine.stat_object, step_num)

        F1_history.append(grow_engine.stat_object.get_F1())
        # -----------------------------------------------------
    print("Learning ended fully!")
    LOG_learning_curve(F1_history)


if __name__ == "__main__":
    class_number = 201
    GLOBALS.LOG_GROUTH.add_text("symbol is " + str(class_number))
    train(class_number)





