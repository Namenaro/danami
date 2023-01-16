import common_utils
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
        self.LOGGER = common_utils.HtmlLogger("MAIN_LOG", self.DIR_PATH)  # основной лог (хотим, чтоб сохранялся в папке проекта)

        self.CONTRAST_SAMPLE_LEN_FOR_STAT = 200  # размер контрасной выборки для заполения статистики
        # датасет
        self.DATA = Dataset(self.CONTRAST_SAMPLE_LEN_FOR_STAT)

        # --------константы, управляющие обучением----------
        self.PIC_SIDE = 105


        # для процесса распознавания:
        self.GROW_MAX = 8  # при росте реализации столько можно отрастить вариантов события для данного ростка
        self.SURVIVIVING_MAX = 12  # сколько оставлять реализаций в каждом поколении

GLOBALS = Globals()














