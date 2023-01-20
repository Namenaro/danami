from globals import GLOBALS
from structure import StructureMemory, StructureRealisation
from evaluator import evaluate_F1, eval_realisation_non_triviality
from recogniser import RecogniserEngine

class StatObject:
    def __init__(self, struct_memory):
        self.F1 = None
        self.struct_memory = struct_memory

        self.true_class_test_sample = []
        self.contrast_class_test_sample = []

        self.true_class_win_qualities = []
        self.contrast_class_win_qualities = []


    def fill(self):
        true_class_train_sample = sample_enegries_on_cogmaps(self.struct_memory, cogmaps=GLOBALS.DATA.get_TRUE_train())
        contrast_class_train_sample = sample_enegries_on_cogmaps(self.struct_memory, cogmaps=GLOBALS.DATA.get_CONTRAST_train())

        self.true_class_test_sample, self.true_class_win_qualities = \
            sample_enegries_on_cogmaps(self.struct_memory, cogmaps=GLOBALS.DATA.get_TRUE_test())
        self.contrast_class_test_sample, self.contrast_class_win_qualities \
            = sample_enegries_on_cogmaps(self.struct_memory, cogmaps=GLOBALS.DATA.get_CONTRAST_test())

        self.F1 = evaluate_F1(true_class_train=true_class_train_sample,
                              contrast_class_train=contrast_class_train_sample,
                              true_class_test=self.true_class_test_sample,
                              contrast_class_test=self.contrast_class_test_sample)
        print("Stat object filled")

    def get_F1(self):
        return self.F1

    def get_win_qualities_true_class(self):
        return self.true_class_win_qualities

    def get_win_qualities_contrast(self):
        return self.contrast_class_win_qualities


def sample_enegries_on_cogmaps(structure, cogmaps):
    energies = []
    win_qalities = []
    for cogmap in cogmaps:
        engine = RecogniserEngine(structure, cogmap)
        best_realisation = engine.recognise()
        energy = eval_realisation_non_triviality(best_realisation, structure, cogmap)
        energies.append(energy)
        win_qalities.append(engine.get_win_quality())
    return energies, win_qalities
