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
        self.PIC_SIDE = 105
        self.GLOBAL_IDS_GEN = common_utils.IdsGenerator()  # генетатор уникальных имен для событий, из которых строятся структуры
        # основной лог (хотим, чтоб сохранялся в папке проекта)
        self.DIR_PATH = os.path.dirname(os.path.abspath(__file__))
        self.LOGGER = common_utils.HtmlLogger("MAIN_LOG", self.DIR_PATH)

        # датасет
        self.DATA = Dataset()


GLOBALS = Globals()














