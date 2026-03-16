from dsl_constructor.interface_classifier import classify_param
from dsl_constructor.placeholder_types import PLACEHOLDERS


def choose_placeholder(param_name: str) -> str:
    return PLACEHOLDERS[classify_param(param_name)]
