from typing import List

import numpy as np

from .entity import Trace, Mask

TRACE_FILE = 'traces.npy'


def load_from_disk(file: str = TRACE_FILE) -> List[Trace]:
    """Un-Pickles numpy arrays from disk
    """
    all_traces = []

    with open(file, 'rb') as f:
        try:
            while True:
                e = np.load(f, allow_pickle=True)
                all_traces.append(Trace(
                    key=np.array(e[0], dtype='uint8'),
                    wave=np.array(e[1], dtype='float64'),
                    text=np.array(e[2], dtype='uint8'),
                ))
        except:
            pass

    return all_traces


def train_and_score(
        *bytes_and_models,
        training_data: List[Trace],
        predict_data: List[Trace],
        feature_masks: List[Mask] = None,
        show_print=True,
        **kwargs
) -> List[float]:
    """Trains a model/pipeline and scores it by its default metric

    :param bytes_and_models: tuples of (feature, model) to use
    :param training_data:    data
    :param predict_data:     data (should not be training data)
    :param feature_masks:    masks for data obtained from SAD
    :param show_print:       If True prints score to output
    :return:                 List, Scores for each byte_and_model tuple
    """
    if feature_masks is None:
        from .processing import create_masks, calculate_sads
        feature_masks = create_masks(calculate_sads(training_data))
    scores = []
    for (byte, model), mask in zip(bytes_and_models, feature_masks):
        model.fit([t.wave[mask.indices] for t in training_data], [t.key[byte] for t in training_data], **kwargs)
        score = model.score([t.wave[mask.indices] for t in predict_data], [t.key[byte] for t in predict_data])
        if show_print:
            print(byte, score)
        scores.append(score)
    return scores
