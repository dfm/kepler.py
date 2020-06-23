# -*- coding: utf-8 -*-

import numpy as np

from kepler import kepler


def get_M_and_f(e, E):
    M = E - e * np.sin(E)
    f = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(0.5 * E))
    return M, f


def test_edge():
    E = np.array([0.0, 2 * np.pi, -226.2, -170.4])
    e = (1 - 1e-6) * np.ones_like(E)
    e[-1] = 0.9939879759519037

    M, f = get_M_and_f(e, E)
    E0, cosf0, sinf0 = kepler(M, e)

    assert np.all(np.isfinite(sinf0))
    assert np.all(np.isfinite(cosf0))
    assert np.allclose(np.sin(f), sinf0)
    assert np.allclose(np.cos(f), cosf0)
    assert np.allclose(E % (2 * np.pi), E0)


def test_pi():
    e = np.linspace(0, 1.0, 100)[:-1]
    E = np.pi + np.zeros_like(e)

    M, f = get_M_and_f(e, E)
    E0, cosf0, sinf0 = kepler(M, e)

    assert np.all(np.isfinite(sinf0))
    assert np.all(np.isfinite(cosf0))
    assert np.allclose(np.sin(f), sinf0)
    assert np.allclose(np.cos(f), cosf0)
    assert np.allclose(E % (2 * np.pi), E0)


def test_solver():
    e = np.linspace(0, 1, 500)[:-1]
    E = np.linspace(-300, 300, 1001)
    e = e[None, :] + np.zeros((len(E), len(e)))
    E = E[:, None] + np.zeros_like(e)

    M, f = get_M_and_f(e, E)
    E0, cosf0, sinf0 = kepler(M, e)

    assert np.all(np.isfinite(sinf0))
    assert np.all(np.isfinite(cosf0))
    assert np.allclose(np.sin(f), sinf0)
    assert np.allclose(np.cos(f), cosf0)
    assert np.allclose(E % (2 * np.pi), E0)
