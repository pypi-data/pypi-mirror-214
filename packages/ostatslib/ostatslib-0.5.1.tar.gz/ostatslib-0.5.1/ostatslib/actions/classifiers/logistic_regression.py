"""
Logistic regression module
"""

import operator
from pandas import DataFrame
from sklearn.linear_model import LogisticRegressionCV
from ostatslib import config
from ostatslib.states import State

from ..action import Action, ActionInfo, ActionResult
from ..utils import (calculate_score_reward,
                     reward_cap,
                     interpretable_model,
                     split_response_from_explanatory_variables,
                     update_state_score,
                     validate_state)

_ACTION_NAME = "Logistic Regression"
_VALIDATIONS = [('response_variable_label', operator.truth, None),
                ('is_response_dichotomous', operator.gt, 0),
                ('response_variable_label', operator.truth, None),
                ('logistic_regression_score_reward', operator.eq, 0)]


@reward_cap
@interpretable_model
def _action(state: State, data: DataFrame) -> ActionResult[LogisticRegressionCV]:
    """
    Fits data to a logistic regression model.

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[LogisticRegressionCV]: action result
    """
    if not validate_state(state, _VALIDATIONS):
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_action,
                                                    model=None,
                                                    raised_exception=False)

    y_values, x_values = split_response_from_explanatory_variables(state, data)
    regression = LogisticRegressionCV(cv=5)

    try:
        regression = regression.fit(x_values, y_values)
    except ValueError:
        state.set('logistic_regression_score_reward', config.MIN_REWARD)
        return state, config.MIN_REWARD, ActionInfo(action_name=_ACTION_NAME,
                                                    action_fn=_action,
                                                    model=None,
                                                    raised_exception=True)

    score: float = regression.score(x_values, y_values)
    update_state_score(state, score)
    reward: float = calculate_score_reward(score)
    state.set('logistic_regression_score_reward', reward)
    return state, reward, ActionInfo(action_name=_ACTION_NAME,
                                     action_fn=_action,
                                     model=regression,
                                     raised_exception=False)


logistic_regression: Action[LogisticRegressionCV] = _action
