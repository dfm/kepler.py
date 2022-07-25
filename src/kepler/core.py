import numpy as np

from kepler._core import solve


def kepler(M, ecc, tol=1e-10):
    """Solve Kepler's equation

    Args:
        M ([type]): The mean anomaly
        ecc ([type]): The eccentricity
        tol ([type], optional): A tolerance parameter for numerical stability.
            Note: this is not an iterative solver so this is not a convergence
            parameter. You shouldn't need to change the default.
            Defaults to 1e-10.

    Raises:
        ValueError: If the eccentricity is out of bounds

    Returns:
        Three Numpy arrays with the eccentric anomaly ``E``, and the cosine and
        sine of the true anomaly ``cos(f), sin(f)``.

    """
    # Check the bounds of the eccentricity
    M, ecc = np.broadcast_arrays(M, ecc)
    if np.any(ecc < 0) or np.any(ecc >= 1.0):
        raise ValueError("ecc must be in the range 0 <= ecc < 1")

    # Solve Kepler's equation
    E = solve(M, ecc)
    cE = np.cos(E)
    sE = np.sin(E)

    # Compute cos(f), sin(f) where valid
    denom = 1 + cE
    m = denom > tol
    m_inv = ~m
    denom += 1.0 * m_inv

    # First, compute tan(0.5*E) = sin(E) / (1 + cos(E))
    tanf2 = np.sqrt((1 + ecc) / (1 - ecc)) * sE / denom  # tan(0.5*f)
    tanf2_2 = tanf2 * tanf2

    # Then we compute sin(f) and cos(f) using:
    #  sin(f) = 2*tan(0.5*f)/(1 + tan(0.5*f)^2), and
    #  cos(f) = (1 - tan(0.5*f)^2)/(1 + tan(0.5*f)^2)
    denom = 1 / (1 + tanf2_2)
    cosf = (1 - tanf2_2) * denom
    sinf = 2 * tanf2 * denom

    return E, cosf * m - 1.0 * m_inv, sinf * m
