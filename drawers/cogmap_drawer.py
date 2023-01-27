from cogmap import Cogmap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def draw_cogmap(cogmap, logger):
    num_axs = len(cogmap.events_ids_to_points)
    fig, axs = plt.subplots(1, num_axs, figsize=(8 * num_axs, 8), dpi=60)
    i = 0
    for id_in_cogmap, point in cogmap.events_ids_to_points.items():
        zmeyka = cogmap.get_zmeika_by_event_id(id_in_cogmap)
        draw_event_realisation(cogmap.pic, axs[i], zmeyka, id_in_cogmap, point)
        i += 1
    logger.add_fig(fig)


def draw_cogmap1(cogmap, logger):
    fig, axs = plt.subplots(figsize=(8, 8), dpi=60)

    cm = plt.get_cmap('seismic')
    axs.imshow(cogmap.pic, cmap=cm, vmin=0, vmax=1)

    for id_in_cogmap, point in cogmap.events_ids_to_points.items():
        axs.scatter(point.x, point.y, s=200)

    logger.add_fig(fig)



def draw_event_realisation(back_pic_binary, ax, zmeyka, id_in_cogmap, point):
    #ax.title.set_text("event " + str(id_in_cogmap))
    cm = plt.get_cmap('seismic')
    ax.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)

    color = 'green'
    marker = 'o'
    for coord in zmeyka:
        ax.scatter(coord.x, coord.y, c=color, marker=marker, alpha=0.4, s=200)

    ax.scatter(point.x, point.y)
    annotation_str = "id=" + str(id_in_cogmap) + ", mass=" + str(len(zmeyka))
    ax.annotate(annotation_str, (point.x, point.y), fontsize=20, color='yellow', xytext=(20, 15), textcoords='offset points',
                ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc=color, alpha=0.6),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95', color='b'))
