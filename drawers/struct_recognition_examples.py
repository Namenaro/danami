from drawers.realisation_graph_drawer import draw_several_realisations_different_cogmaps
from recogniser import RecogniserEngine


def draw_examples_recognition(colorator, structure, cogmaps, logger):
    # для получившейся структуры покажем примеры ее распознавания на ряде когмап
    realisations_list = []
    for cogmap in cogmaps:
        recog_engine = RecogniserEngine(structure, cogmap)
        best_realisation = recog_engine.recognise()
        realisations_list.append(best_realisation)

    draw_several_realisations_different_cogmaps(colorator, realisations_list, cogmaps, logger, structure)
