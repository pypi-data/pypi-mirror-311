import numpy as np
import scipy.stats as st

from lost_spc.constants import get_c4, get_d
from lost_spc.utils import get_sample_size

from .spc_values import calculate_means, calculate_ranges, calculate_standard_deviations


def calculate_control_limits(
    data: np.ndarray, chart_type: str = "X_R", z: int = 3, **kwargs
) -> dict:
    """Calculates the control limits for different SPC charts (X_R, R, X_S, S or EWMA).

    Args:
        data (np.ndarray): The data for which the control limits are to be calculated.
        chart_type (str): Type of chart ('X_R', 'R', 'S' or 'X_S'). Determines
                          the control limits' calculations.
        z (int): The number of standard deviations for control limits. Default is 3.

    Returns:
        dict: A dictionary containing the center line (CL), upper control limit (UCL),
              and lower control limit (LCL).

    Examples:
        >>> data = np.array([[10, 12, 14], [15, 16, 17]])
        >>> calculate_control_limits(data, chart_type='X_R')
        {'CL': 14.0, 'UCL': 17.069198123276216, 'LCL': 10.930801876723784}
    """
    if chart_type != "EWMA":
        # Bestimme m und n automatisch für NumPy-Arrays
        sample_size = get_sample_size(data)
        m = sample_size.m  # Stichprobengrösse

    # Berechne die Kontrollgrenzen basierend auf dem Kartentyp
    if chart_type == "X_R":
        # X̄-R Karte: Mittelwert und Spannweite
        means = calculate_means(data)
        ranges = calculate_ranges(data)
        d = get_d(m)
        d2 = d.d2
        cl = np.mean(means)
        R_mean = np.mean(ranges)
        factor = z * (R_mean / d2) / np.sqrt(m)
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "R":
        # R-Karte: Spannweite
        ranges = calculate_ranges(data)
        d = get_d(m)
        d2 = d.d2
        d3 = d.d3
        range_mean = np.mean(ranges)
        cl = range_mean
        factor = cl * z * d3 / d2
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "S":
        # S-Karte: Standardabweichung
        std_devs = calculate_standard_deviations(data)
        c4 = get_c4(m)
        cl = np.mean(std_devs)
        factor = cl * z * np.sqrt(1 - c4**2) / c4
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "X_S":
        # X̄-S Karte: Mittelwert und Standardabweichung
        means = calculate_means(data)
        std_devs = calculate_standard_deviations(data)
        X_mean = np.mean(means)
        s_mean = np.mean(std_devs)
        c4 = get_c4(m)
        cl = X_mean
        factor = z * (s_mean / c4) / np.sqrt(m)
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "EWMA":
        X_mean = np.mean(data)
        s_mean = np.std(data)
        lambda_ = kwargs.get("lambda_", 0.2)
        cl = X_mean
        asymptotic_sigma = s_mean * np.sqrt(lambda_ / (2 - lambda_))
        ucl = cl + z * asymptotic_sigma
        lcl = cl - z * asymptotic_sigma
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    return {"CL": float(cl), "UCL": float(ucl), "LCL": float(lcl)}


def get_confidence_interval_cp(Cp, data, confidence_level=0.95):
    """
    Calculate the confidence interval for Cp based on variability.

    Args:
        Cp (float): Process capability index.
        sigma (float): Standard deviation of the process.
        confidence_level (float): Confidence level (default is 95%).

    Returns:
        tuple: (Cp_low, Cp_up), the lower and upper bounds of the confidence interval.
    """
    sample_size = get_sample_size(data)
    m = sample_size.m
    n = sample_size.n

    total_sample_size = n * m

    sigma = np.mean(calculate_standard_deviations(data))

    # Dynamically calculate z-value based on confidence level
    z = st.norm.ppf(1 - (1 - confidence_level) / 2)

    # Variability adjustment factor
    c4 = get_c4(m)
    fac = z * np.sqrt(1 - c4**2) / np.sqrt(total_sample_size)

    # Adjusted standard deviation bounds
    sigma_low = sigma * (1 - fac)
    sigma_high = sigma * (1 + fac)

    # Confidence interval for Cp
    Cp_low = Cp / (1 + fac)
    Cp_high = Cp / (1 - fac)

    return sigma_low, sigma_high, Cp_low, Cp_high
