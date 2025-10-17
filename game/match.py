import random

from .player import Player
from .game import ACTIONS

class Match:

    # Este método ya está implementado
    def __init__(self, player_1: Player,
                       player_2: Player,
                       n_rounds: int = 100,
                       error: float = 0.0):
        """
        Match class to represent an iterative limited-sum game

        Parameters:
            - player_1 (Player): first player of the match
            - player_2 (Player): second player of the match
            - n_rounds (int = 100): number of rounds in the match
            - error (float = 0.0): error probability (on a 0-1 scale).
        """

        assert n_rounds > 0, "'n_rounds' should be greater than 0"

        self.player_1 = player_1
        self.player_2 = player_2
        self.n_rounds = n_rounds
        self.error = error

        self.score = (0.0, 0.0)  # this variable will store the final result of
                                 # the match, once the 'play()' function has
                                 # been called. The two values of the tuple
                                 # correspond to the points scored by the first
                                 # and second player, respectively.


    def play(self, do_print: bool = False) -> None:
        """
        Main call of the class. Play the match.
        Stores the final result in 'self.score'

        Parameters
            - do_print (bool = False): if True, should print the ongoing
            results at the end of each round (i.e. print round number, last
            actions of both players and ongoing score).
        """
        self.player_1.clean_history()
        self.player_2.clean_history()

        score_1 = 0.0
        score_2 = 0.0

        for round in range(self.n_rounds):
            action_1 = self.player_1.strategy(self.player_2)
            action_2 = self.player_2.strategy(self.player_1)

            # Introduce error with probability 'self.error'
            if random.random() < self.error:
                action_1 = random.choice(ACTIONS)
            if random.random() < self.error:
                action_2 = random.choice(ACTIONS)

            self.player_1.history.append(action_1)
            self.player_2.history.append(action_2)

            round_score_1, round_score_2 = self.player_1.compute_scores(self.player_2)
            score_1 += round_score_1
            score_2 += round_score_2

            if do_print:
                print(f"Round {round + 1}:")
                print(f"  Player 1 chose: {action_1}, Player 2 chose: {action_2}")
                print(f"  Current score -> Player 1: {score_1}, Player 2: {score_2}")

        self.score = (score_1, score_2)