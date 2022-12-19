from cogmap import Cogmap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def draw_cogmap(cogmap, logger):
    num_axs = len(cogmap.events_ids_to_points)
    fig, axs = plt.subplots(1, num_axs, figsize=(8 * num_axs, 8), dpi=60)
    i = 0
    for id_in_cogmap, point in cogmap.events_ids_to_points.items():
        realisation = cogmap.get_event_by_id(id_in_cogmap)
        draw_event_realisation(cogmap.pic, axs[i], realisation, id_in_cogmap, point)
        i += 1
    logger.add_fig(fig)
    logger.save()


def draw_event_realisation(back_pic_binary, ax, realisation, id_in_cogmap, point):
    ax.title.set_text("event " + str(id_in_cogmap))
    cm = plt.get_cmap('gray')
    ax.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)

    color = 'green'
    marker = 'o'
    for coord in realisation.zmeika_points:
        ax.scatter(coord.x, coord.y, c=color, marker=marker, alpha=0.8, s=200)

    ax.scatter(point.x, point.y)
    annotation_str = "LUE_id=" + str(id_in_cogmap) + ", mass=" + str(realisation.mass)
    ax.annotate(annotation_str, (point.x, point.y), color='blue', xytext=(20, 15), textcoords='offset points',
                ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc=color, alpha=0.6),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95', color='b'))
