"""
PPO Agent module
"""

import torch as th
from numpy import ndarray
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure

from ostatslib.agents.agent import Agent
from ostatslib.environments import GymEnvironment

POLICY = "MultiInputPolicy"
POLICY_KWARGS = {
    'activation_fn': th.nn.ReLU,
    'share_features_extractor': False
}

TRAINING_LOGS_PATH = "./.logs/"


class PPOAgent(Agent):
    """
    Agent built on PPO algorithm model
    """

    def __init__(self,
                 path: str | None = None,
                 training_envs_count: int = 3,
                 environment_kwargs: dict | None = None) -> None:
        self.__environment_kwargs = environment_kwargs
        self.__model = self.__init__model(path, training_envs_count)

    def train(self, steps: int = 1000000, save_freq: int = 100000) -> None:
        n_envs = self.__model.n_envs if self.__model.n_envs is not None else 1
        save_freq = max(save_freq // n_envs, 1)
        checkpoint_callback = CheckpointCallback(save_freq=save_freq,
                                                 save_path=TRAINING_LOGS_PATH,
                                                 save_replay_buffer=True)
        logger = configure(TRAINING_LOGS_PATH,
                           ["stdout", "csv", "tensorboard"])
        self.__model.set_logger(logger)
        self.__model.learn(total_timesteps=steps, callback=checkpoint_callback)

    def save(self, path: str) -> None:
        self.__model.save(path)

    def _predict(self, observation: dict) -> ndarray:
        action, _ = self.__model.predict(observation, deterministic=True)
        return action[0]

    def __init__model(self, path: str | None, training_envs_count: int) -> PPO:
        environments = make_vec_env(GymEnvironment,
                                    training_envs_count,
                                    env_kwargs=self.__environment_kwargs,
                                    vec_env_cls=SubprocVecEnv)
        if path is None:
            return PPO(POLICY,
                       environments,
                       verbose=1,
                       n_steps=2048,
                       policy_kwargs=POLICY_KWARGS)

        return PPO.load(path,
                        environments,
                        custom_objects={
                            'observation_space': environments.observation_space,
                            'action_space': environments.action_space
                        })
