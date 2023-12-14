import pytest

from nim_game.common.models import NimStateChange
from nim_game.agents.agent import Agent


def test_init_raise_exception():
    with pytest.raises(ValueError):
        Agent('')


def test_make_step_return_value():
    state = list(range(5))
    print(state)

    agent = Agent(level='hard')
    step = agent.make_step(state)
    assert isinstance(step, NimStateChange)
    assert 0 <= step.heap_id <= len(state)
    print(state)
    print(step.decrease, state[step.heap_id-1])
    assert 1 <= step.decrease <= state[step.heap_id-1]
