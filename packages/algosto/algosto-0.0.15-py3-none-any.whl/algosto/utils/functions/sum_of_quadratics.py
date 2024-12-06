import numpy as np

def sum_of_quadratics():
    def f(X):
        return 1/X.shape[1] * np.sum(X**2, axis=1)

    def grad(X):
        return 2/X.shape[1] * np.sum(X, axis=1)

    return f, grad
