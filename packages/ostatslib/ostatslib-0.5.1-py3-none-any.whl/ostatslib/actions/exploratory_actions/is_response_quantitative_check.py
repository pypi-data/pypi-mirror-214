"""
is_response_quantitative_check module
"""

import operator
from pandas import DataFrame, Series
import numpy as np
from ostatslib import config

from ostatslib.states import State
from ._get_exploratory_reward import get_exploratory_reward
from ..action import Action, ActionInfo, ActionResult
from ..utils import validate_state

_ACTION_NAME = "Is Response Quantitative Check"
_VALIDATIONS = [('response_variable_label', operator.truth, None)]


def _action(state: State, data: DataFrame) -> ActionResult[None]:
    """
    Check if response variable is quantitative

    Args:
        state (State): state
        data (DataFrame): data

    Returns:
        ActionResult[None]: action result
    """
    if not validate_state(state, _VALIDATIONS):
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_action,
                                                    model=None,
                                                    raised_exception=False)
    state_copy: State = state.copy()
    response_var_label: str = state.get("response_variable_label")
    response: Series = data[response_var_label]

    is_quantitative: bool = __is_quantitative_check(response)
    if is_quantitative:
        state.set("is_response_quantitative", 1)
    else:
        state.set("is_response_quantitative", -1)

    reward = get_exploratory_reward(state, state_copy)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_action,
                                     model=None,
                                     raised_exception=False)


def __is_quantitative_check(values: Series) -> bool:
    unique_values = values.unique()
    return np.issubdtype(unique_values.dtype, np.number)


is_response_quantitative_check: Action[None] = _action
