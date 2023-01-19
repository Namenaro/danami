from structure import StructureRealisation, StructureMemory
from cogmap import Cogmap
from event import EventRealisation
from drawers.colorator import StructColorator

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def draw_realisation_on_ax(struct_realisation, struct_colorator, structure, cogmap, ax):
    cm = plt.get_cmap('seismic')
    ax.imshow(cogmap.pic, cmap=cm, vmin=0, vmax=1)

    # рисуем сами события
    for global_id, id_in_cogmap in struct_realisation.global_ids_to_locals.items():
        event_realisation = cogmap.get_event_by_id(id_in_cogmap)
        color = struct_colorator.get_color_for_id(global_id)

        for coord in event_realisation.zmeika_points:
            ax.scatter(coord.x, coord.y, c=color, marker='o', alpha=0.4, s=200)

        point = cogmap.get_point_by_event_id(id_in_cogmap)
        ax.scatter(point.x, point.y, color, alpha=0.7)

        ax.annotate(str(global_id), (point.x, point.y))

    # соединяем их стрелочками:
    if len(struct_realisation) > 1:
        for global_id in structure.recognition_order[1:]:
            parent_global_id = structure.get_parent_id(global_id)

            local_parent_id = struct_realisation.get_local_id_by_global(parent_global_id)
            local_child_id = struct_realisation.get_local_id_by_global(global_id)

            child_point = cogmap.get_point_by_event_id(local_child_id)
            parent_point = cogmap.get_point_by_event_id(local_parent_id)

            arrow = mpatches.FancyArrowPatch((parent_point.x, parent_point.y), (child_point.x, child_point.y),
                                             mutation_scale=10)
            ax.add_patch(arrow)



def draw_several_realisations_same_cogmap(colorator, realisations_list, cogmap, logger):
    # создаем рядок и в лог

def draw_several_realisations_different_cogmaps(colorator, realisations_list, cogmaps_list, logger):
    # создаем рядок и в лог