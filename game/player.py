from abc import ABC, abstractmethod
from typing import Self

from .game import Game

class Player(ABC):

    # Este método ya está implementado
    @abstractmethod
    def __init__(self, game: Game, name: str = ""):
        """
        Abstract class that represents a generic player

        Parameters:
            - name (str): the name of the strategy
            - game (Game): the game that this player will play
        """

        self.name = name
        self.game = game

        self.history  = []  # This is the main variable of this class. It is
                            # intended to store all the history of actions
                            # performed by this player.
                            # Example: [0, 1, 2, 3] <- So far, the
                            # interaction lasts four rounds. In the first one,
                            # this player chose 0. In the second, 1. Etc.


    # Este método ya está implementado
    @abstractmethod
    def strategy(self, opponent: Self) -> int:
        """
        Main call of the class. Gives the action for the following round of the
        interaction, based on the history

        Parameters:
            - opponent (Player): is another instance of Player.

        Results:
            - An integer representing the action (0 to 5)
        """
        pass


    def compute_scores(self, opponent: Self) -> tuple[float, float]:
        """
        Compute the scores for a given opponent

        Parameters:
            - opponent (Player): is another instance of Player.

        Results:
            - A tuple of two floats, where the first value is the current
            player's payoff, and the second value is the opponent's payoff.
        """
        my_score = self.game.evaluate_result(self.history[-1], opponent.history[-1])[0]
        opponent_score = self.game.evaluate_result(self.history[-1], opponent.history[-1])[1]
        return my_score, opponent_score


    # Este método ya está implementado
    def clean_history(self):
        """Resets the history of the current player"""
        self.history = []

    def __str__(self) -> str:
        """String representation of the player"""
        return f"Player: {self.name}"
    
    def __repr__(self) -> str:
        """Representation of the player"""
        return f"Player({self.name})"