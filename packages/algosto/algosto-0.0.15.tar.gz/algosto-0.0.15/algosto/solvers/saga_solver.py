from typing import Any
import numpy as np

from algosto.constraints import AbstractConstraint
from algosto.solvers import SGDSolver

class SAGASolver(SGDSolver):
    def __init__(self, d: int, N: int, objective: callable, grad: callable, gamma: float = 0.1, alpha: float = 1., cst: AbstractConstraint = None, random_state: int = None) -> None:
        super().__init__(d, N, objective, grad, gamma, cst, random_state)
        
        self._alpha = alpha
        self._grad_memory = None
    
    def fit(self, x_start: np.ndarray[Any, np.dtype] = None, n_iter: int = 1000):
        d = self._d
        N = self._N

        if x_start is not None and x_start.shape[0] != d:
            raise ValueError(f"The starting point must have the same "
                             f"dimension as the constraint."
                             f"Start point has {x_start.shape[0]} and constraint as {d}")
            
        if self._random_state is not None:
            np.random.seed(self._random_state)

        x = self._cst.get_one_element() if x_start is None else x_start
        self._trajectory.append(x)

        self._grad_memory = np.zeros((N, d))
        for k in range(N):
            batch_filter = self._make_batch_filter(k)
            self._grad_memory[k,] = self._grad(x, batch_filter=batch_filter)

        for n in range(1, n_iter):
            batch_filter = self._make_batch_filter()
            u = np.argmax(batch_filter)
            
            grad = self._grad(x, batch_filter=batch_filter)
            
            x = x - self._gamma * (grad - self._alpha * (self._grad_memory[u] - (1/N) * np.sum(self._grad_memory, axis=0)))
            
            self._grad_memory[k,] = grad

            self._trajectory.append(x)

    def get_grad_memory(self) -> np.array:
        return self._grad_memory

    def set_grad_memory(self, new_grad_memory: np.array) -> None:
        self._grad_memory = new_grad_memory
