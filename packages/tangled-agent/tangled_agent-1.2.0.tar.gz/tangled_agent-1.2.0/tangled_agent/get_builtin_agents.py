from __future__ import annotations
import random
import logging

from typing import Tuple

from tangled_game_engine import GameAgentBase

def get_builtin_agents():
    """
    Find all implementations of the GameAgentBase class in the tangled_agent module and return their names.
    """

    subclasses = GameAgentBase.__subclasses__()
    # print(f"subclasses: {subclasses}")
    result = [cls.__name__ for cls in subclasses]
    # print(f"result: {result}")
    return result