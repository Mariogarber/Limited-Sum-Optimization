from abc import ABC, abstractmethod
from typing import Self, Sequence
import numpy as np

# Acciones del juego de suma limitada
ACTIONS = (0, 1, 2, 3, 4, 5)
THRESHOLD = 5  # Umbral de suma

class Game:

    def __init__(self, actions: Sequence[int] = ACTIONS, threshold: int = THRESHOLD):
        """
        Represents the limited-sum game.

        Parameters:
            - actions (list[int]): list of possible actions (default: [0,1,2,3,4,5])
            - threshold (int): sum threshold beyond which both get 0 (default: 5)
        """
        self.actions = actions
        self.threshold = threshold

    @property
    @abstractmethod
    def payoff_matrix(self) -> np.ndarray:
        """
        Payoff matrix of the game.

        Returns:
            - 6x6 np array of the matrix
        """
        return np.array([[self.evaluate_result(a_1, a_2) for a_2 in ACTIONS] for a_1 in ACTIONS])


    @abstractmethod
    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        """
        Given two actions, returns the payoffs of the two players.

        Parameters:
            - a_1 (int): action of player 1 (0 to 5)
            - a_2 (int): action of player 2 (0 to 5)

        Returns:
            - tuple of two floats, being the first and second values the payoff
            for the first and second player, respectively.
        """
        reward_matrix = np.array([[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)], 
                                  [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (0, 0)],
                                  [(2, 0), (2, 1), (2, 2), (2, 3), (0, 0), (0, 0)],
                                  [(3, 0), (3, 1), (3, 2), (0, 0), (0, 0), (0, 0)],
                                  [(4, 0), (4, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                                  [(5, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]])
        return reward_matrix[a_1, a_2]
