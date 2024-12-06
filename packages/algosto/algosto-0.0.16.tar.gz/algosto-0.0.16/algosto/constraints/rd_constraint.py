from typing import Tuple
import numpy as np
import numpy.typing as npt
from algosto.constraints import AbstractConstraint

class RdConstraint(AbstractConstraint):
    def __init__(self, d: int, solver) -> None:
        super().__init__(d)
        
        self._s = solver
    
    def get_one_element(self) -> npt.NDArray[np.float64]:
        raise NotImplementedError("The RdConstraint can't give an element."
                                  "If you don't know the starting point,"
                                  "you should consider an other constraint such"
                                  "RdSquareConstraint or RdBallConstraint")

    def get_grid(self, num: int) -> Tuple[npt.NDArray, npt.NDArray]:
        trajectory = self._s.get_trajectory()
        
        x_lim = (np.min(trajectory[:, 0]) - 0.5, np.max(trajectory[:, 0]) + 0.5)

        y_lim = (np.min(trajectory[:, 1]) - 0.5, np.max(trajectory[:, 1]) + 0.5)

        X, Y = super().get_grid(x_lim, y_lim, num)

        return X, Y

class RdBallConstraint(AbstractConstraint):
    """
    A constraint on the ball in Rd with center ``c`` and radius ``r``.

    Parameters
    ----------
    d : int
        The space dimension.
    c : array_like
        The center of the ball in Rd.
    r : float
        The radius of the ball.
        
    Raises
    ------
    ValueError
        If the array that gives the center of the ball has not the same length as `d`.
    """
    def __init__(self, d: int, c: npt.NDArray[np.float64], r: float) -> None:
        super().__init__(d)
        
        if d != c.shape[0]:
            raise ValueError("The center of the ball must be a 1-D numpy array of shape d.")

        self._c = c
        self._r = r
    
    def get_one_element(self) -> npt.NDArray[np.float64]:
        """
        Gives randomly one element which is inside the constraint.
        
        It follows a uniform law.

        Returns
        -------
        out : ndarray
            A vector in Rd inside the constraint.
        """
        x = np.random.rand(self._d) * 2 - 1
        x /= np.linalg.norm(x)
        
        return x * (self._r - np.random.uniform(0, self._r))
    
    def get_grid(self, num: int) -> Tuple[npt.NDArray, npt.NDArray]:
        """
        Gives a grid of `num` elements on ``X`` and ``Y``.

        Parameters
        ----------
            num : int
                The number of points on one axis to make the grid.

        Returns
        -------
            out : Tuple[ndarray, ndarray]
                returns X and Y.
        """
        X, Y = super().get_grid(num)
        
        norm = np.sqrt(X**2 + Y**2)
        
        X[norm > self._r] = np.nan
        Y[norm > self._r] = np.nan
        
        return X, Y
