from common_utils import HtmlLogger
from recogniser import BasicGenerationSorted, RecogniserEngine
from cogmap import Cogmap
from drawers.realisation_graph_drawer import draw_several_realisations_same_cogmap

import matplotlib.pyplot as plt


def draw_process_precognition_on_cogmap(colorator, structure, cogmap, logger):
    # для каждого поколения
    # рисуем горизонтальный рядочек вошедших в него реализаций
    # каждый рядочек это fig, добавляем ее в логгер

    engine = RecogniserEngine(structure, cogmap)
    engine.recognise()
    logger.add_text("Длина распознаваемой здесь структуры: " + str(len(structure)))

    for sorted_generation in engine.generations_list:
        realisations_sorted = sorted_generation.get_all_realisations_sorted()
        energies_sorted = sorted_generation.get_all_energies_sorted()
        titles = [str(energy) for energy in energies_sorted]
        draw_several_realisations_same_cogmap(colorator, realisations_sorted, cogmap, logger, structure,titles)

    win_qualities = engine.get_all_win_qualities()
    fig, ax = plt.subplots()
    ax.plot(win_qualities)
    ax.set_xlabel("Кач-во победы лучшего ростка в поколении")
    ax.set_xlabel("Номер поколения ростков")
    ax.set_title("Процесс роста качества победы победителя в каждом поколении")
    logger.add_fig(fig)
