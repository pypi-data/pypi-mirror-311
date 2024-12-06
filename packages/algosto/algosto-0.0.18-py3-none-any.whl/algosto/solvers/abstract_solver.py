from abc import ABC
import numpy as np
import numpy.typing as npt

from algosto.constraints import AbstractConstraint, RdConstraint

class AbstractSolver(ABC):
    
    name = "Abstract Solver"
    
    def __init__(self, d: int, objective: callable, cst: AbstractConstraint = None, random_state: int = None) -> None:
        super().__init__()

        if cst is None:
            cst = RdConstraint(2, self)

        self._d = d
        self._objective = objective
        self._cst = cst
        self._random_state = random_state

        self._trajectory = list()
        self._n_iter = None
        self._x_start = None

    def fit(self, x_start: npt.NDArray = None, n_iter: int = 1000) -> np.array:
        self._n_iter = n_iter
        self._x_start = x_start if isinstance(x_start, np.ndarray) else np.array(x_start)
        
        if self._x_start is not None and self._x_start.shape[0] != self._d:
            raise ValueError(f"The starting point must have the same "
                             f"dimension as the constraint."
                             f"Start point has {self._x_start.shape[0]} and constraint as {self._d}")

        x = self._cst.get_one_element() if self._x_start is None else self._x_start
        self._trajectory.append(x)

        if self._random_state is not None:
            np.random.seed(self._random_state)
        
        return x

    def get_trajectory(self) -> npt.NDArray:
        """
        Returns the trajectory registered by the solver during the ``fit`` operation.
        
        It's a matrix of size ``(n_iter, d)``.

        Returns
        -------
            out : ndarray
                An array of dimension ``(n_iter, d)`` where d is the dimension defined in the constraint
        """
        return np.array(self._trajectory)
    
    def get_objective(self) -> callable:
        return self._objective
    
    def set_objective(self, new_objective: callable) -> None:
        self._objective = new_objective

    def get_constraint(self) -> AbstractConstraint:
        return self._cst
    
    def set_constraint(self, new_cst: AbstractConstraint) -> None:
        self._cst = new_cst
