from typing import NamedTuple

import numpy as np


class Trace(NamedTuple):
    """Contains data trace from ChipWhisperer
    """
    key: np.array
    wave: np.array
    text: np.array


class Mask(NamedTuple):
    """Masks data

    Boolean and Indices are useful so both are provided here
    """
    boolean: np.array
    indices: np.array
