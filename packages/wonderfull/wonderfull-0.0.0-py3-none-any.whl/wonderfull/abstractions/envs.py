from abc import abstractmethod
from typing import Protocol, Sequence

from gymnasium import Env, Space
from numpy.typing import NDArray

from wonderfull import utils


class EnvGroup(Protocol):
    @property
    @abstractmethod
    def envs(self) -> tuple[Env, ...]:
        ...

    @property
    @abstractmethod
    def observation_space(self) -> Space:
        ...

    @property
    @abstractmethod
    def action_space(self) -> Space:
        ...

    @abstractmethod
    def reset(self) -> NDArray:
        ...

    @abstractmethod
    def step(self, actions: NDArray) -> NDArray:
        ...

    @staticmethod
    def join_spaces(spaces: Sequence[Space]) -> Space:
        try:
            typ = utils.unique([type(space) for space in spaces])
            shape = utils.unique([space.shape for space in spaces])
            dtype = utils.unique([space.dtype for space in spaces])
        except ValueError:
            raise ValueError("Cannot join spaces because they are not compatible.")

        return typ(shape=shape, dtype=dtype)

    def check_observation_shape(self, observation: NDArray) -> None:
        if self.observation_space != observation.shape:
            raise ValueError(
                "Illegal observation shape. "
                f"Expected: {self.observation_space.shape}. Received: {observation.shape}"
            )

    def check_action_shape(self, action: NDArray) -> None:
        if self.action_space != action.shape:
            raise ValueError(
                "Illegal action shape. "
                f"Expected: {self.action_space.shape}. Received: {action.shape}."
            )
