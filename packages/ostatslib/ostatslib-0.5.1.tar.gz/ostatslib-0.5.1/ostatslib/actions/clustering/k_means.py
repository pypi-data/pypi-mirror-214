"""
K-Means module
"""

import operator
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from ostatslib import config

from ostatslib.states import State
from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     update_state_score,
                     validate_state)

_ACTION_NAME = "K-Means"
_VALIDATIONS = [('response_variable_label', operator.eq, ''),
                ('clusters_count', operator.gt, 0)]


@reward_cap
def _action(state: State, data: DataFrame) -> ActionResult[KMeans]:
    """
    Fits data to a KMeans cluster

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[KMeans]: action result
    """
    if not validate_state(state, _VALIDATIONS):
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_action,
                                                    model=None,
                                                    raised_exception=False)

    clusters_count: int = state.get("clusters_count")
    kmeans = KMeans(n_clusters=clusters_count)
    kmeans.fit(data)

    score: float = silhouette_score(data, kmeans.labels_)

    reward: float = calculate_score_reward(score)
    update_state_score(state, score)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_action,
                                     model=kmeans,
                                     raised_exception=False)


k_means: Action[KMeans] = _action
