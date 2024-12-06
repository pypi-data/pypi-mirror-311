from dataclasses import dataclass

import numpy as np


@dataclass
class SampleSize:
    m: int  # Stichprobengrösse
    n: int  # Anzahl Stichproben


def get_sample_size(data: np.ndarray) -> SampleSize:
    """Returns the sample size (number of columns) and the number of rows (probes)
    for a NumPy array dataset.

    Args:
        data (np.ndarray): 2D NumPy array of numerical values.

    Returns:
        SampleSize: A dataclass containing the sample size (m) and the number of probes (n).

    Examples:
        >>> data = np.array([[10, 12, 14], [15, 16, 17]])
        >>> get_sample_size(data)
        SampleSize(m=3, n=2)
    """
    m = data.shape[1]  # Stichprobengrösse
    n = data.shape[0]  # Anzahl Stichproben
    return SampleSize(m=m, n=n)
