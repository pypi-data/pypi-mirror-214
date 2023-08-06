from abc import abstractmethod
from typing import Protocol

import reverb
from numpy.typing import NDArray


class Agent(Protocol):
    @abstractmethod
    def predict(self, observation: NDArray) -> NDArray:
        ...

    # FIXME: Unfinished
