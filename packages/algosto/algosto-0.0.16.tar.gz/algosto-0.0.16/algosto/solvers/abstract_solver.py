from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt

from algosto.constraints import AbstractConstraint, RdConstraint

class AbstractSolver(ABC):
    def __init__(self, d: int, objective: callable, cst: AbstractConstraint = None, random_state: int = None) -> None:
        super().__init__()

        if cst is None:
            cst = RdConstraint(2, self)

        self._d = d
        self._objective = objective
        self._cst = cst
        self._random_state = random_state
        
        self._trajectory = list()

    @abstractmethod
    def fit(self, x_start: npt.NDArray = None, n_iter: int = 1000):
        pass

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
