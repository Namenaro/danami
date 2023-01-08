import numpy as np
from scipy.stats import entropy


def measure_win_quality(arr: list) -> float:
    sorted_arr = sorted(arr, reverse=True)
    normed_arr = sorted_arr / np.sum(sorted_arr)
    res = entropy(normed_arr, base=2)

    return 1 / res
