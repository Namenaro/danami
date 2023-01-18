import random


class StructColorator:
    def __init__(self):
        self.ids_to_colors = {}

    def get_color_for_id(self, global_id):
        return self.ids_to_colors[global_id]

    def add_new_id(self, new_id):
        r = random.random()
        b = random.random()
        g = random.random()

        color = (r, g, b)
        self.ids_to_colors[new_id] = color

    def add_several_ids(self, ids_list):
        for global_id in ids_list:
            self.add_new_id(global_id)