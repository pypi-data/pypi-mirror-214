"""
Actions validators module
"""

from inspect import signature
from typing import Any, Callable
from ostatslib.states import State


def validate_state(state: State, validator_fns: list[tuple[str, Callable[..., bool], Any]]) -> bool:
    """
    Validate state using list of validation functions

    Args:
        state (State): state
        validator_fns (list[tuple[str, Callable[..., bool], Any]]): validations

    Returns:
        bool: True if state is valid
    """
    for (feature_key, operator_fn, value) in validator_fns:
        if not _is_valid(state, feature_key, operator_fn, value):
            return False
    return True


def _is_valid(state: State,
              feature_key: str,
              operator_fn: Callable[..., bool], value: Any) -> bool:
    if value is None:
        operator_fn_signature = signature(operator_fn)
        if len(operator_fn_signature.parameters) == 1:
            return operator_fn(state.get(feature_key))

    return operator_fn(state.get(feature_key), value)
