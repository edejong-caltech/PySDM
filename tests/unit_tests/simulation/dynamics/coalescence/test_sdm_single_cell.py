"""
Created at 06.06.2019

@author: Piotr Bartman
@author: Sylwester Arabas
"""

from PySDM.simulation.dynamics.coalescence import SDM
from PySDM.simulation.state import State
from PySDM.backends.default import Default
import numpy as np
import pytest
from tests.unit_tests.simulation.dynamics.coalescence.__parametrisation__ import StubKernel, backend_fill

# noinspection PyUnresolvedReferences
from tests.unit_tests.simulation.dynamics.coalescence.__parametrisation__ import x_2, n_2


backend = Default()


class TestSDMSingleCell:
    def test_single_collision(self, x_2, n_2):
        # Arrange
        sut = SDM(StubKernel(), dt=0, dv=1, n_sd=len(n_2), n_cell=1, backend=backend)
        sut.compute_gamma = lambda backend, prob, rand: backend_fill(backend, prob, 1)
        state = State.state_0d(n=n_2, extensive={'x': x_2}, intensive={}, backend=backend)
        # Act
        sut(state)
        # Assert
        assert np.sum(state['n'] * state['x']) == np.sum(n_2 * x_2)
        assert np.sum(state['n']) == np.sum(n_2) - np.amin(n_2)
        if np.amin(n_2) > 0: assert np.amax(state['x']) == np.sum(x_2)
        assert np.amax(state['n']) == max(np.amax(n_2) - np.amin(n_2), np.amin(n_2))

    @pytest.mark.parametrize("n_in, n_out", [
        pytest.param(1, np.array([1, 0])),
        pytest.param(2, np.array([1, 1])),
        pytest.param(3, np.array([2, 1])),
    ])
    def test_single_collision_same_n(self, n_in, n_out):
        # Arrange
        sut = SDM(StubKernel(), dt=0, dv=1, n_sd=2, n_cell=1, backend=backend)
        sut.compute_gamma = lambda backend, prob, rand: backend_fill(backend, prob, 1)
        state = State.state_0d(n=np.full(2, n_in), extensive={'x': np.full(2, 1.)}, intensive={}, backend=backend)

        # Act
        sut(state)

        # Assert
        np.testing.assert_array_equal(sorted(state.backend.to_ndarray(state.n)), sorted(n_out))

    @pytest.mark.parametrize("p", [
        pytest.param(2),
        pytest.param(4),
        pytest.param(5),
        pytest.param(7),
    ])
    def test_multi_collision(self, x_2, n_2, p):
        # Arrange
        sut = SDM(StubKernel(), dt=0, dv=1, n_sd=len(n_2), n_cell=1, backend=backend)
        sut.compute_gamma = lambda backend, prob, rand: backend_fill(backend, prob, p)
        state = State.state_0d(n=n_2, extensive={'x': x_2}, intensive={}, backend=backend)

        # Act
        sut(state)

        # Assert
        gamma = min(p, max(n_2[0] // n_2[1], n_2[1] // n_2[1]))
        assert np.amin(state['n']) >= 0
        assert np.sum(state['n'] * state['x']) == np.sum(n_2 * x_2)
        assert np.sum(state['n']) == np.sum(n_2) - gamma * np.amin(n_2)
        assert np.amax(state['x']) == gamma * x_2[np.argmax(n_2)] + x_2[np.argmax(n_2) - 1]
        assert np.amax(state['n']) == max(np.amax(n_2) - gamma * np.amin(n_2), np.amin(n_2))

    @pytest.mark.parametrize("x, n, p", [
        pytest.param(np.array([1., 1, 1]), np.array([1, 1, 1]), 2),
        pytest.param(np.array([1., 1, 1, 1, 1]), np.array([5, 1, 2, 1, 1]), 1),
        pytest.param(np.array([1., 1, 1, 1, 1]), np.array([5, 1, 2, 1, 1]), 6),
    ])
    def test_multi_droplet(self, x, n, p):
        # Arrange
        sut = SDM(StubKernel(), dt=0, dv=1, n_sd=len(n), n_cell=1, backend=backend)
        sut.compute_gamma = lambda backend, prob, rand: backend_fill(backend, prob, p, odd_zeros=True)
        state = State.state_0d(n=n, extensive={'x': x}, intensive={}, backend=backend)

        # Act
        sut(state)

        # Assert
        assert np.amin(state['n']) >= 0
        assert np.sum(state['n'] * state['x']) == np.sum(n * x)

    # TODO integration test?
    def test_multi_step(self):
        # Arrange
        SD_num = 256
        n = np.random.randint(1, 64, size=SD_num)
        x = np.random.uniform(size=SD_num)

        sut = SDM(StubKernel(), dt=0, dv=1, n_sd=SD_num, n_cell=1, backend=backend)

        sut.compute_gamma = lambda backend, prob, rand: backend_fill(
            backend,
            prob,
            backend.to_ndarray(rand) > 0.5,
            odd_zeros=True
        )
        state = State.state_0d(n=n, extensive={'x': x}, intensive={}, backend=backend)

        # Act
        for _ in range(32):
            sut(state)

        # Assert
        assert np.amin(state['n']) >= 0
        actual = np.sum(state['n'] * state['x'])
        desired = np.sum(n * x)
        np.testing.assert_almost_equal(actual=actual, desired=desired)

    @staticmethod
    def test_compute_gamma():
        # Arrange
        n = 87
        prob = np.linspace(0, 3, n, endpoint=True)
        rand = np.linspace(0, 1, n, endpoint=False)

        from PySDM.backends.default import Default
        backend = Default()

        expected = lambda p, r: p // 1 + (r < p - p // 1)

        for p in prob:
            for r in rand:
                # Act
                prob_arr = backend.from_ndarray(np.full((1,), p))
                rand_arr = backend.from_ndarray(np.full((1,), r))
                SDM.compute_gamma(backend, prob_arr, rand_arr)

                # Assert
                assert expected(p, r) == backend.to_ndarray(prob_arr)[0]

    # TODO test_compute_probability