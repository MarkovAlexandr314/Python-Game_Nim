from random import randint

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]       # кучки

    def __init__(self, heaps_amount: int) -> None:
        if heaps_amount < 2 or heaps_amount > 10:
            raise ValueError
        self._heaps = [randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX) for _ in range(heaps_amount)]

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек
        :return: копия списка с кучек
        """
        return self._heaps

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния

        """
        if state_change.heap_id < 1 or state_change.heap_id > len(self._heaps):
            raise ValueError

        if (state_change.decrease < STONE_AMOUNT_MIN or
            state_change.decrease > self._heaps[state_change.heap_id-1]):
            raise ValueError

        self._heaps[state_change.heap_id-1] -= state_change.decrease
