from structure import StructureRealisation, StructureMemory
from cogmap import Cogmap
from event import EventRealisation
from drawers.colorator import StructColorator
from globals import GLOBALS

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def draw_realisation_on_ax(struct_realisation, struct_colorator, structure, cogmap, ax, title=None):

    cm = plt.get_cmap(GLOBALS.CMAP_NAME)
    ax.imshow(cogmap.pic, cmap=cm, vmin=0, vmax=1)
    if title is not None:
        ax.set_title(str(title))
    # рисуем сами события
    for global_id, id_in_cogmap in struct_realisation.global_ids_to_locals.items():
        event_realisation = cogmap.get_event_by_id(id_in_cogmap)
        color = struct_colorator.get_color_for_id(global_id)

        for coord in event_realisation.zmeika_points:
            ax.scatter(coord.x, coord.y, c=[color], marker='o', alpha=0.4, s=200)

        point = cogmap.get_point_by_event_id(id_in_cogmap)
        ax.scatter(point.x, point.y, c=[color], alpha=0.7, s=170)

        ax.annotate(str(global_id), (point.x, point.y))

    # соединяем их стрелочками:
    if len(struct_realisation) > 1:
        for global_id in structure.recognition_order[1:]:
            parent_global_id = structure.get_parent_id(global_id)

            local_parent_id = struct_realisation.get_local_id_by_global(parent_global_id)
            local_child_id = struct_realisation.get_local_id_by_global(global_id)
            if local_child_id is None:
                continue

            child_point = cogmap.get_point_by_event_id(local_child_id)
            parent_point = cogmap.get_point_by_event_id(local_parent_id)

            arrow = mpatches.FancyArrowPatch((parent_point.x, parent_point.y), (child_point.x, child_point.y),
                                             mutation_scale=10)
            ax.add_patch(arrow)



def draw_several_realisations_same_cogmap(colorator, realisations_list, cogmap, logger, structure, titles = None):
    # создаем рядок и в лог
    num_axs = len(realisations_list)
    fig, axs = plt.subplots(1, num_axs, figsize=(GLOBALS.FIGSIZE * num_axs, GLOBALS.FIGSIZE), dpi=GLOBALS.DPI)
    for i in range(num_axs):
        realisation = realisations_list[i]
        if realisation is None:
            continue
        if titles is not None:
            title = str(titles[i])
        else:
            title = None

        draw_realisation_on_ax(realisation, colorator, structure, cogmap, axs[i], title)
    logger.add_fig(fig)


def draw_several_realisations_different_cogmaps(colorator, realisations_list, cogmaps_list, logger, structure, titles=None):
    # создаем рядок и в лог
    num_axs = len(realisations_list)
    fig, axs = plt.subplots(1, num_axs, figsize=(GLOBALS.FIGSIZE * num_axs, GLOBALS.FIGSIZE), dpi=GLOBALS.DPI)
    for i in range(num_axs):
        realisation = realisations_list[i]
        if titles is not None:
            title = str(titles[i])
        else:
            title = None
        draw_realisation_on_ax(realisation, colorator, structure, cogmaps_list[i], axs[i], title)
    logger.add_fig(fig)
