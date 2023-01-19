from samplers import StatObject
from common_utils import HtmlLogger

import matplotlib.pyplot as plt

def draw_stat_object(stat_object, logger):
    fig, axs = plt.subplots(nrows=1, ncols=2)

    # Рисуем гистограммы энергий на целевых изображениях и на контрастых (на одной картинке наложенно)
    axs[0].set_title("Энергии")
    axs[0].hist(stat_object.true_class_test_sample, color='green', label='Целевые', alpha=0.5)
    axs[0].hist(stat_object.contrast_class_test_sample, color='red', label='Контрастные', alpha=0.5)
    axs[0].set_xlabel("Значения энергии")
    axs[0].set_ylabel("Кол-во картинок")

    # Таким же образом рисуем в одних осях гистограмму качетсва победы лучшего финального ростка на целевых и контрастных
    axs[1].set_title("Качество победы лучшего ростка для ихображения")
    axs[1].hist(stat_object.get_win_qualities_true_class(), color='green', label='Целевые', alpha=0.5)
    axs[1].hist(stat_object.get_win_qualities_contrast(), color='red', label='Контрастные', alpha=0.5)
    axs[1].set_xlabel("Значения качества победы")
    axs[1].set_ylabel("Кол-во картинок ")

    logger.add_fig(fig)

