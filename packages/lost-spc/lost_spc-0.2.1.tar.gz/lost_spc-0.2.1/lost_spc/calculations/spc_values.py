import numpy as np
import scipy.stats as st

from lost_spc.constants import get_d


def calculate_means(data: np.ndarray) -> np.ndarray:
    """Calculates the mean (average) of each row (sample) in a dataset.

    Args:
        data (np.ndarray): Array of numerical values.

    Returns:
        np.ndarray: Array of means for each row.

    Examples:
        >>> calculate_means(np.array([[10, 12, 14], [15, 16, 17]]))
        array([12., 16.])
    """
    return np.mean(data, axis=1)


def calculate_ranges(data: np.ndarray) -> np.ndarray:
    """Calculates the range (max - min) of each row (sample) in a dataset.

    Args:
        data (np.ndarray): Array of numerical values.

    Returns:
        np.ndarray: Array of ranges for each row.

    Examples:
        >>> calculate_ranges(np.array([[10, 12, 14], [15, 16, 17]]))
        array([4., 2.])
    """
    return np.ptp(data, axis=1).astype(float)


def calculate_standard_deviations(data: np.ndarray) -> np.ndarray:
    """Calculates the sample standard deviation for each row (sample) in the dataset.

    Args:
        data (np.ndarray): Array of numerical values, where each row is a sample.

    Returns:
        np.ndarray: Array of sample standard deviations for each row.

    Examples:
        >>> calculate_standard_deviations(np.array([[10, 12, 14], [15, 16, 17]]))
        array([2., 1.])
    """
    return np.std(data, axis=1, ddof=1)


# X̄ control chart
def oc(k: np.ndarray, m: int) -> np.ndarray:
    """Calculates the operational characteristic (OC) for the X̄ control chart.

    Args:
        k (float): Deviation from the mean in units of k * sigma0.
        m (int): Number of measurements per sample.

    Returns:
        float: Probability value for the operational characteristic.

    Examples:
        >>> oc(1, 5)
        np.float64(0.7775460413896245)
        >>> oc(0.5, 15)
        np.float64(0.85622385678665)
    """
    return st.norm.cdf(3 - k * np.sqrt(m)) - st.norm.cdf(-3 - k * np.sqrt(m))


def power(k: np.ndarray, m: int) -> np.ndarray:
    """Calculates the power of the test for the X̄ control chart.

    Args:
        k (float): Deviation from the mean in units of k * sigma0.
        m (int): Number of measurements per sample.

    Returns:
        float: Test power, which is 1 - OC.

    Examples:
        >>> power(1, 5)
        np.float64(0.22245395861037554)
        >>> power(0.5, 3)
        np.float64(0.016477741898883624)
    """
    return 1 - oc(k, m)


def ARL(**kwargs) -> np.float64:
    """Calculates the ARL based on k and m or oc.

    Args:
        k: Deviation from the mean in k*sigma0
        m: Measurements per sample
        oc: Operational characteristic

    Returns:
        float: Average Run Length (ARL) for the X̄ chart.

    Examples:
        >>> ARL(k=0, m=5)
        np.float64(370.3983473449564)
        >>> ARL(oc=0.0027)
        np.float64(1.002707309736288)
    """
    if "k" in kwargs and "m" in kwargs:
        operational_characteristic = oc(k=kwargs["k"], m=kwargs["m"])
    elif "oc" in kwargs:
        operational_characteristic = kwargs["oc"]
    else:
        raise ValueError("Either k and m or oc have to be supplied!")

    return np.float64(1 / (1 - operational_characteristic))


# R card
def oc_r(lam: float | np.ndarray, m) -> float | np.ndarray:
    """Calculates the operational characteristic (OC) for the R and S charts.

    Args:
        lam (float): lambda -> Deviation from sigma0
        m (int): Measurements per sample

    Returns:
        float: Operational characteristic for the R chart.

    Examples:
        >>> oc_r(1, 5)
        np.float64(0.9973002039367398)
        >>> oc_r(0.5, 3)
        np.float64(0.99997875160547)
    """
    d = get_d(m)
    d2 = d.d2
    d3 = d.d3

    T1 = st.norm.cdf(((1 - lam) * d2 - 3 * d3) / lam / d3)
    T2 = st.norm.cdf(((1 - lam) * d2 + 3 * d3) / lam / d3)
    return T2 - T1


def power_R(lam: float | np.ndarray, m: int) -> float | np.ndarray:
    """Calculates the power of the test for the R chart.

    Args:
        lam (float): lambda -> Deviation from sigma1 to sigma0.
        m (int): Number of measurements per sample.

    Returns:
        float: Test power, which is 1 - OC.

    Examples:
        >>> power_R(1, 5)
        np.float64(0.002699796063260207)
        >>> power_R(0.5, 3)
        np.float64(2.1248394529993497e-05)
    """
    return 1 - oc_r(lam, m)


def ARL_R(
    lam: float | np.ndarray | None = None, m: int | None = None, oc: float | None = None
) -> float | np.ndarray:
    """Calculates the ARL based on lam and m or oc_r.

    Args:
        lam (float): lambda -> Deviation from sigma1 to sigma0
        m: Measurements per sample
        oc (float): Operational characteristic for the R chart

    Returns:
        float: Average Run Length (ARL) for the R chart.

    Examples:
        >>> ARL_R(lam=1, m=5)
        370.3983473449564
        >>> ARL_R(oc=0.0027)
        1.002707309736288
    """
    if lam is not None and m is not None:
        operational_characteristic = oc_r(lam, m)
    elif oc is not None:
        operational_characteristic = oc
    else:
        raise ValueError("Either lambda and m or oc have to be supplied!")

    if not isinstance(operational_characteristic, np.ndarray):
        operational_characteristic = float(operational_characteristic)

    return 1 / (1 - operational_characteristic)


def calculate_process_capability(lsl: float, usl: float, mu: float, sigma: float) -> float:
    """
    Calculates the probability that the process is within the specification limits (LSL and USL).

    Args:
        lsl (float): Lower Specification Limit.
        usl (float): Upper Specification Limit.
        mu (float): Process mean.
        sigma (float): Process standard deviation.

    Returns:
        float: Probability that the process lies within the limits.

    Examples:
        >>> calculate_process_capability(2.0, 8.0, 5.0, 1.0)
        0.9973002039367398
        >>> calculate_process_capability(0.0, 10.0, 5.0, 2.0)
        0.9875806693484477
    """
    lower_prob = st.norm.cdf((lsl - mu) / sigma)
    upper_prob = st.norm.cdf((usl - mu) / sigma)
    return float(upper_prob - lower_prob)


def calculate_cp(usl: float, lsl: float, sigma: float, z: float = 6) -> float:
    """
    Calculates the Process Capability Index (Cp) with a customizable factor.

    Args:
        usl (float): Upper Specification Limit.
        lsl (float): Lower Specification Limit.
        std_dev (float): Standard deviation of the process.
        factor (float): Multiplication factor for the standard deviation (default is 6).

    Returns:
        float: Cp value.

    Raises:
        ValueError: If the standard deviation is less than or equal to 0.

    Examples:
        >>> calculate_cp(10, 2, 1, z=6)
        1.3333333333333333
        >>> calculate_cp(10, 2, 1, z=4)
        2.0
    """

    return (usl - lsl) / (z * sigma)


def calculate_cpk(usl: float, lsl: float, mu: float, sigma: float) -> float:
    """
    Calculates the Critical Process Capability Index (Cpk).

    Args:
        usl (float): Upper Specification Limit.
        lsl (float): Lower Specification Limit.
        mean (float): Process mean.
        std_dev (float): Standard deviation of the process.

    Returns:
        float: Cpk value.

    Raises:
        ValueError: If the standard deviation is less than or equal to 0.

    Examples:
        >>> calculate_cpk(10, 3, 6, 1)
        1.0
    """
    cp_upper = (usl - mu) / (3 * sigma)
    cp_lower = (mu - lsl) / (3 * sigma)
    return min(cp_upper, cp_lower)


def calculate_ewma(X: np.ndarray, lambda_: float) -> np.ndarray:
    """
    Calculate the EWMA values recursively.

    Args:
    - X (numpy.ndarray): Input data to compute EWMA.
    - lambda_ (float): Smoothing factor (0 < lambda_ ≤ 1).

    Returns:
    - numpy.ndarray: EWMA values.
    """
    if not 0 < lambda_ <= 1:
        raise ValueError("lambda_ must be between 0 and 1.")

    ewma = [np.mean(X[0])]
    for i in range(1, len(X)):
        ewma.append(lambda_ * np.mean(X[i]) + (1 - lambda_) * ewma[-1])
    return np.array(ewma)
