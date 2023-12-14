from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


def nim_sum(chips: list[int]):  # считаем ним-сумму
    ns = chips[0]
    for i in range(1, len(chips)):
        ns = ns ^ chips[i]
    return ns


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        if not (level in [i.value for i in AgentLevels]):
            raise ValueError
        self._level = level

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        if self._level == AgentLevels.EASY.value:
            h = choice([i+1 for i in range(len(state_curr)) if state_curr[i] != 0])
            d = randint(1, state_curr[h-1])
            w = NimStateChange(h, d)
            return w

        if self._level == AgentLevels.HARD.value:
            maxd = 1
            maxh = 0
            for i in range(len(state_curr)):
                if state_curr[i] != 0:
                    maxh = i
                    break

            for i in range(maxh, len(state_curr)):
                for j in range(1, state_curr[i]+1):
                    state_curr[i] -= j
                    if nim_sum(state_curr) == 0:
                        maxd = max(maxd, j)
                        maxh = max(maxh, i)

                    state_curr[i] += j
            # if state_curr[maxh-1] < maxd or maxh == 0:
                # maxh += 1
            return NimStateChange(heap_id=maxh+1, decrease=maxd)

        if self._level == AgentLevels.NORMAL.value:
            q = Agent(choice([AgentLevels.HARD, AgentLevels.EASY]))
            return q.make_step(state_curr)
