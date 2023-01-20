from samplers.stat_object import StatObject

def select_best_stat_object(stat_objects):
    index, value = max(enumerate(stat_objects), key=lambda item: item[1].get_F1())
    return index
