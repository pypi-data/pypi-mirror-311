import numpy as np
from typing import Tuple

def mean_of_quadratics() -> Tuple[callable, callable]:
    def f(x: np.array) -> float:
        return 1/x.shape[0] * np.sum(x**2)

    def grad(x, batch_filter) -> np.array:
        return 1/x.shape[0] * (2 * x) * batch_filter

    return f, grad
