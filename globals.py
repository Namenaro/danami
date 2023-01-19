import common_utils
from  common_utils import HtmlLogger as Logger
from dataset import Dataset

import os.path


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})): pass


class Globals(Singleton):
    def __init__(self):

        self.GLOBAL_IDS_GEN = common_utils.IdsGenerator()  # генетатор уникальных имен для событий, из которых строятся структуры
        self.DIR_PATH = os.path.dirname(os.path.abspath(__file__))  # адрес корня проекта

        #логгеры
        self.LOG_GROUTH = Logger("LOG_GROUTH", self.DIR_PATH)  # шаги роста структуры
        self.LOG_GROUTH.add_text("Лог как росла структура со 2 шага, пошагово ")

        self.LOG_CURVE = Logger("LOG_CURVE", self.DIR_PATH)  # кривая обучения
        self.LOG_CURVE.add_text("Лог кривая обучения ")

        self.LOG_RECOG = Logger("LOG_RECOG_PROCESS", self.DIR_PATH)
        self.LOG_RECOG.add_text("Процесс распознавания (рост ростков) ")

        # датасет
        self.TRAIN_CONTRAST_LEN = 200
        self.DATA = Dataset(self.TRAIN_CONTRAST_LEN)

        # --------константы, управляющие обучением----------
        self.PIC_SIDE = 105


        # для процесса распознавания:
        self.GROW_MAX = 8  # при росте реализации столько можно отрастить вариантов события для данного ростка
        self.SURVIVIVING_MAX = 12  # сколько оставлять реализаций в каждом поколении

GLOBALS = Globals()














