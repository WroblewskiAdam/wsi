import itertools
import numpy as np
from typing import Iterable, List, Optional
from game import Game
from move import Move
from player import Player
from state import State
from game import Game


class Pick(Game):
    """Class that represents the Pick game"""
    FIRST_PLAYER_DEFAULT_CHAR = '1'
    SECOND_PLAYER_DEFAULT_CHAR = '2'

    def __init__(self, first_player: Player = None, second_player: Player = None, n: int = 4):
        """
        Initializes game.

        Parameters:
            first_player: the player that will go first (if None is passed, a player will be created)
            second_player: the player that will go second (if None is passed, a player will be created)
            n: the subset size of picked numbers that should sum up to aim value
        """
        self.first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        self.second_player = second_player or Player(self.SECOND_PLAYER_DEFAULT_CHAR)

        state = PickState(self.first_player, self.second_player, n)

        super().__init__(state)


class PickMove(Move):
    """
    Class that represents a move in the PickMove game

    Variables:
        number: selected number (from 1 to n^2)
    """

    def __init__(self, number: int):
        self.number = number

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, PickMove):
            return False
        return self.number == o.number


class PickState(State):
    """Class that represents a state in the PickState game"""

    def __init__(self,
                 current_player: Player, other_player: Player, n,
                 current_player_numbers: List[int] = None,
                 other_player_numbers: List[int] = None):
        """Creates the state. Do not call directly."""

        if current_player_numbers is None:
            current_player_numbers = []
        if other_player_numbers is None:
            other_player_numbers = []

        self.current_player_numbers = current_player_numbers
        self.other_player_numbers = other_player_numbers
        self.selected_numbers = set(self.current_player_numbers).union(self.other_player_numbers)
        self.n = n
        self.max_number = n ** 2
        self.aim_value = int((n ** 2 * (n ** 2 + 1)) / (2 * n))
        super().__init__(current_player, other_player)

    def get_moves(self) -> Iterable[PickMove]:
        return [PickMove(number) for number in range(1, self.max_number + 1) if number not in self.selected_numbers]

    def make_move(self, move: PickMove) -> 'PickState':
        if move.number > self.max_number or move.number in self.selected_numbers:
            raise ValueError("Invalid move")
        else:
            next_player = self._other_player
            next_player_numbers = self.other_player_numbers

            other_player = self._current_player
            other_player_numbers = self.current_player_numbers + [move.number]

        return PickState(
            next_player, other_player, self.n, next_player_numbers, other_player_numbers
        )

    def is_finished(self) -> bool:
        return self._check_if_sums_to_aim_value(self.current_player_numbers) or \
               self._check_if_sums_to_aim_value(self.other_player_numbers) or \
               len(self.selected_numbers) == self.max_number

    def get_winner(self) -> Optional[Player]:
        if not self.is_finished():
            return None
        if self._check_if_sums_to_aim_value(self.current_player_numbers):
            return self._current_player
        elif self._check_if_sums_to_aim_value(self.other_player_numbers):
            return self._other_player
        else:
            return None

    def __str__(self) -> str:
        return f"n: {self.n}, aim_value: {self.aim_value}" \
               f"\nCurrent player: {self._current_player.char}, Numbers: " \
               f"{'[]' if not self.current_player_numbers else sorted(self.current_player_numbers)}," \
               f"\nOther player: {self._other_player.char}, Numbers: " \
               f"{'[]' if not self.other_player_numbers else sorted(self.other_player_numbers)}"

    # below are helper methods for the public interface

    def _check_if_sums_to_aim_value(self, numbers: List[int]) -> bool:
        return self.aim_value in [sum(i) for i in itertools.combinations(numbers, self.n)]

    
    def heuristic(self) -> int:
        # matrices definitions
        magic_square = np.array([[2,16,13,3],
						         [11,5,8,10],
						         [7,9,12,6],
						         [14,4,1,15]])

        field_values = np.array([[3, 2, 2, 3],
                                 [2, 3, 3, 2],
                                 [2, 3, 3, 2],
                                [3, 2, 2, 3]])
    
        numsMax = self.current_player_numbers if self._current_player.char == "1" else self.other_player_numbers
        numsMin = self.current_player_numbers if self._current_player.char == "2" else self.other_player_numbers
        
        sumMax = 0
        for num in numsMax:
            index = np.where(magic_square == num)
            row = int(index[0])
            col = int(index[1])
            sumMax += field_values[row, col]
        
        sumMin = 0
        for num in numsMin:
            index = np.where(magic_square == num)
            row = int(index[0])
            col = int(index[1])
            sumMin += field_values[row, col]
        
        score = sumMax - sumMin
        
        if self._current_player.char == "1":
            return score
        else :
            return -score
        


