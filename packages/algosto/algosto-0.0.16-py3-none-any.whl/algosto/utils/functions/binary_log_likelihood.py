import numpy as np

def binary_log_likelihood(X: np.array, y: np.array, batch_size: int, model: callable):
    def f(w: np.array):
        return -1/batch_size * np.sum(y[:, np.newaxis] * np.log(model(X, w)) + (1 - y[:, np.newaxis]) * np.log(1 - model(X, w)), axis=0)

    def grad(w: np.array, batch_filter: np.array):
        batch_filter = np.repeat(batch_filter, batch_size)[:X.shape[0]]

        return 1/batch_size * X.T @ ((model(X, w) - y) * batch_filter)

    return f, grad
