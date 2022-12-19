import common_utils
from dataset import Dataset

import os.path

###########################################
# Глобальные объекты будем называть каплоком,
# а локальные маленькими буквами, чтоб
# не возникало конфликтов
##########################################

# основной лог (хотим, чтоб сохранялся в папке проекта)
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
LOGGER = common_utils.HtmlLogger("MAIN_LOG", DIR_PATH)

# датасет
DATA = Dataset()








