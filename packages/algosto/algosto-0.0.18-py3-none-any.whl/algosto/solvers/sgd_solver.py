from typing import Callable
import numpy as np
import numpy.typing as npt

from algosto.solvers import AbstractSolver
from algosto.constraints import AbstractConstraint

class SGDSolver(AbstractSolver):
    """
    The solver for the Stochastic Gradient Descent (SGD) algorithm.

    Parameters
    ----------
    ct : AbstractConstraint
        A constraint object that inherits from ``AbstractConstraint``.
    objective : function
        The objective function to minimize. This function must be able to handle
        a 1-D array of several points.
    grad : function
        The gradient of the objective.
    batch_size : float
        The rate of dimensions kept to compute the gradient.
    gamma : float
        The learning rate.
    """
    
    name = "SGD Solver"
    
    def __init__(self, d: int, N: int, objective: callable, grad: callable, gamma: float = 0.1, cst: AbstractConstraint = None, random_state: int = None) -> None:
        super().__init__(d, objective, cst, random_state)
        
        self._N = N
        self._grad = grad
        self._gamma = gamma
    
    def fit(self, x_start: np.ndarray = None, n_iter: int = 1000):
        """
        Run the SGD solver to approximate the solution of the optimization problem.

        Parameters
        ----------
        x_start : array_like
            The point where the algorithm will start running.
        n_iter : int
            The number of iterations. The solver will run exactly this number of times.

        Raises
        ------
        ValueError
            It raises a ``ValueError`` if the dimension of ``x_start`` does not 
            match the dimension of the ``constraint``.
        """
        x = super().fit(x_start, n_iter)

        for n in range(1, self._n_iter):
            batch_filter = self._make_batch_filter()

            x = x - self._gamma * self._grad(x, batch_filter=batch_filter)

            self._trajectory.append(x)
            
    def _make_batch_filter(self, idx=None) -> np.array:
        batch_filter = np.zeros(self._N, dtype=int)
        idx = np.random.randint(0, self._N) if idx is None else idx
        batch_filter[idx] = 1
        
        return batch_filter
