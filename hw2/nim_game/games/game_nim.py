import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent
from nim_game.common.enumerations import Players


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        try:
            with open(path_to_config) as file:
                res = json.load(file)
                self._environment = EnvironmentNim(res["heaps_amount"])
                self._agent = Agent(res["opponent_level"])
        except FileNotFoundError:
            raise ValueError()

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """

        game_position = GameState()
        bot_move = None

        self._environment.change_state(player_step)
        if not self.is_game_finished():
            bot_move = self._agent.make_step(self.heaps_state)
            self._environment.change_state(bot_move)
        game_position = GameState(
            opponent_step=bot_move,
            heaps_state=self.heaps_state,
        )

        if self.is_game_finished():
            game_position.winner = Players.BOT if bot_move else Players.USER

        return game_position

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """

        return sum(self.heaps_state) == 0

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
