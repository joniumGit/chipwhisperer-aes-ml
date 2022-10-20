from typing import List

import numpy as np

from .entity import Trace, Mask


def calculate_sads(traces: List[Trace]) -> List[np.array]:
    """Calculates the Sum of Absolute Differences for a labeled signal

    Calculates SAD for each feature using all classes.
    Classes are assumed to be labeled by integers from 0-(n-1) for n features.
    """
    from itertools import combinations

    category_averages_per_byte = [{
        j: [] for j in range(256)} for _ in range(len(traces[0].key))
    ]

    for t in traces:
        for idx, b in enumerate(t.key):
            category_averages_per_byte[idx][b].append(t.wave)

    return [
        np.sum(
            np.fromiter((np.abs(a1 - a2) for a1, a2 in combinations((
                np.mean(v, axis=0) for v in category_averages_per_byte[i].values()
            ), 2)), dtype=np.dtype(('float64', len(traces[0].wave))), count=len(traces)),
            axis=0
        )
        for i in range(len(traces[0].key))
    ]


def create_masks(sads: List[np.array], threshold: int = 96) -> List[Mask]:
    """Creates masks for taking only parts of data based on SAD

    :param sads:      SAD data for each feature
    :param threshold: Percentile of which under the data is masked
    :return:          Mask for each feature for filtering input data
    """
    return [
        Mask(
            boolean=sad > np.percentile(sad, threshold),
            indices=np.arange(len(sad))[sad > np.percentile(sad, threshold)]
        ) for sad in sads
    ]
