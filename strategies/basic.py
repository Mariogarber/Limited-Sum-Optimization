from abc import ABC, abstractmethod
import random

from game.player import Player
from game.game import Game, ACTIONS

class Always0(Player):

    def __init__(self, game: Game, name: str = ""):
        """Always chooses 0"""
        self.name = name
        self.game = game
        self.history  = []


    def strategy(self, opponent: Player) -> int:
        """Always chooses 0"""
        result = 0
        self.history.append(result)
        return result


class Always3(Player):

    def __init__(self, game: Game, name: str = ""):
        """Always chooses 3"""
        self.name = name
        self.game = game
        self.history  = []


    def strategy(self, opponent: Player) -> int:
        """Always chooses 3"""
        result = 3
        self.history.append(result)
        return result


class UniformRandom(Player):

    def __init__(self, game: Game, name: str = ""):
        """Chooses uniformly at random"""
        self.name = name
        self.game = game
        self.history  = []


    def strategy(self, opponent: Player) -> int:
        """Chooses uniformly at random"""
        result = random.choice(ACTIONS)
        self.history.append(result)
        return result


class Focal5(Player):

    def __init__(self, game: Game, name: str = ""):
        """Tries to coordinate on i+j=5. Several logics possible."""
        self.name = name
        self.game = game
        self.history  = []


    def strategy(self, opponent: Player) -> int:
        """First round: 2, then adapts based on opponent trying to maximize the
        chances of establishing a 5-way split in each round."""
        if len(self.history) == 0:
            result = 2
        else:
            last_opponent_action = opponent.history[-1]
            if last_opponent_action < 5:
                result = 5 - last_opponent_action
            else:
                result = random.choice(ACTIONS)
        self.history.append(result)
        return result


class TitForTat(Player):

    def __init__(self, game: Game, name: str = ""):
        """Tit-for-tat adapted to the JCMA. Several logics possible."""
        self.name = name
        self.game = game
        self.history  = []


    def strategy(self, opponent: Player) -> int:
        """Similar to Focal5, but reactive with opponent's actions above 3."""
        if len(self.history) == 0:
            result = 2
        else:
            last_opponent_action = opponent.history[-1]
            if last_opponent_action < 3:
                result = last_opponent_action
            else:
                result = 5 - last_opponent_action
        self.history.append(result)
        return result