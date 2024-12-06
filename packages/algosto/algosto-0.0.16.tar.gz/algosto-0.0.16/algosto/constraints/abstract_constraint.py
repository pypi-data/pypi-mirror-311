from typing import Tuple
import numpy.typing as npt
from abc import abstractmethod, ABC
import numpy as np
from typing import Tuple

class AbstractConstraint(ABC):
    def __init__(self, d: int) -> None:
        super().__init__()
        self._d = d

    @abstractmethod
    def get_one_element(self):
        pass
    
    def get_grid(self, x_lim: Tuple[int, int], y_lim: Tuple[int, int], num: int) -> Tuple[npt.NDArray, npt.NDArray]:
        if x_lim[1] - x_lim[0] > y_lim[1] - y_lim[0]:
            distance = ((x_lim[1] - x_lim[0]) - (y_lim[1] - y_lim[0])) / 2
            y_lim = ((y_lim[0] - distance, y_lim[1] + distance))
        else:
            distance = ((y_lim[1] - y_lim[0]) - (x_lim[1] - x_lim[0])) / 2
            x_lim = ((x_lim[0] - distance, x_lim[1] + distance))
        
        x = np.linspace(x_lim[0], x_lim[1], num)
        y = np.linspace(y_lim[0], y_lim[1], num)
        
        return np.meshgrid(x, y)

    def get_dimension(self) -> int:
        """
        Gives the dimension of the constraint.

        Returns
        -------
            out : int
                The dimension of the constraint.
        """
        return self._d
