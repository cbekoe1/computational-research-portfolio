import numpy as np

def generate_wind_speeds(k: float, c: float, size: int = 10000) -> np.ndarray:
    """
    Generate wind speeds using a Weibull distribution.

    Parameters
    ----------
    k : float
        Shape parameter of the Weibull distribution.
    c : float
        Scale parameter of the Weibull distribution.
    size : int
        Number of samples to generate.

    Returns
    -------
    np.ndarray
        Array of simulated wind speeds.
    """
    return np.random.weibull(k, size) * c