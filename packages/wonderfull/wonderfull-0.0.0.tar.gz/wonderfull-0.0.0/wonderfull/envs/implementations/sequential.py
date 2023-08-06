from typing import Sequence

import numpy as np
from gymnasium import Env, Space
from numpy.typing import NDArray

from wonderfull.abstractions.envs import EnvGroup


class SequentialEnv(EnvGroup):
    def __init__(self, envs: Sequence[Env]) -> None:
        super().__init__()

        num_envs = len(envs)

        try:
            observation_space = self.join_spaces(
                [env.observation_space for env in envs]
            )
        except ValueError as ve:
            raise ValueError(
                "Given list of environments have different observation shapes."
            ) from ve

        try:
            action_space = self.join_spaces([env.action_space for env in envs])
        except ValueError as ve:
            raise ValueError(
                "Given list of environments have different action shapes."
            ) from ve

        self._envs = tuple(envs)

        # FIXME: This is here to silence mypy checks that shape might be None.
        assert observation_space.shape and action_space.shape
        self._observation_space: Space = Space(
            shape=(num_envs, *observation_space.shape), dtype=observation_space.dtype
        )
        self._action_space: Space = Space(
            shape=(num_envs, *action_space.shape), dtype=action_space.dtype
        )

    @property
    def envs(self) -> tuple[Env, ...]:
        return self._envs

    @property
    def action_space(self) -> Space:
        return self._action_space

    @property
    def observation_space(self) -> Space:
        return self._observation_space

    def step(self, actions: NDArray) -> NDArray:
        self.check_action_shape(actions)
        obs_raw = [env.step(act) for env, act in zip(self.envs, actions)]
        obs = np.array(obs_raw)
        self.check_action_shape(obs)
        return obs
