import numpy as np
from game.game import Game, ACTIONS
from game.player import Player

class IndianStrategy(Player):
    """
    Implements the Indian strategy for a game-playing agent.
    The strategy uses an initial probability distribution for actions during the first `burnout_epochs` rounds.
    After the burnout period, it predicts the opponent's next move based on their recent history and counters it.
    Attributes:
        name (str): Name of the player.
        game (Game): Reference to the game instance.
        history (list): History of actions taken by this player.
        init_probabilities (dict): Initial probability distribution for actions.
        burnout_epochs (int): Number of epochs to use the initial probability strategy.
        k (int): Number of recent opponent actions to consider for prediction.
    Methods:
        strategy(opponent: Player) -> int:
            Determines the next action based on the opponent's history and the current strategy phase.
    """

    def __init__(self, game: Game, name: str = "", k=10, burnout_epochs=20):
        self.name = name
        self.game = game
        self.history  = []
        self.init_probabilities = {
            0: 0,
            1: 0.1,
            2: 0.2,
            3: 0.6,
            4: 0.1,
            5: 0
        }
        self.burnout_epochs = burnout_epochs
        self.k = k

    def strategy(self, opponent: Player) -> int:
        """
        Determines the next action for the player based on the opponent's history and internal strategy.

        The strategy works in two phases:
        1. Burnout phase: For the initial `burnout_epochs` rounds, selects an action randomly according to `init_probabilities`.
           Also updates conditional probabilities based on the last results.
        2. Adaptive phase: After the burnout phase, analyzes the opponent's last `k` actions to estimate their next move.
           Predicts the opponent's next action using empirical probabilities, then selects a counter-action.

        Args:
            opponent (Player): The opponent player object, which contains their action history.

        Returns:
            int: The chosen action for the current round.
        """
        opponent_history = opponent.history
        i = len(opponent_history)
        last_2_opponent_result = opponent_history[-2] if len(opponent_history) > 1 else 2
        last_my_result = self.history[-1] if len(self.history) > 0 else 2
        if i <= self.burnout_epochs:
            result=  np.random.choice(list(self.init_probabilities.keys()), p=list(self.init_probabilities.values()))
            self.cond_prob[last_my_result].append(last_2_opponent_result)
        else:
            last_opponent_history = opponent.history[-self.k:]
            prob = [last_opponent_history.count(a) / len(last_opponent_history) for a in ACTIONS]
            opponent_next = np.random.choice(ACTIONS, p=prob)
            result = max(1, min(5, 5 - opponent_next))
        return result

class IndianGreedyStrategy(Player):
    """
    Implements a greedy strategy inspired by Indian Poker for a limited-sum optimization game.
    The strategy uses initial action probabilities for the first `burnout_epochs` rounds,
    then adapts based on conditional probabilities of the opponent's recent moves.
    Attributes:
        name (str): Name of the player/strategy.
        game (Game): Reference to the game instance.
        history (list): History of actions taken by this player.
        init_probabilities (dict): Initial probabilities for actions during the burnout period.
        burnout_epochs (int): Number of initial rounds to use random strategy.
        k (int): Number of recent moves to consider for conditional probability calculation.
        cond_prob (dict): Conditional probability history for each action.
    Methods:
        strategy(opponent: Player) -> int:
            Determines the next action based on the opponent's history and the player's own history.
            Uses initial probabilities for the first `burnout_epochs` rounds, then adapts using
            conditional probabilities of the opponent's responses to the player's previous actions.
    """

    def __init__(self, game: Game, name: str = "", k=10, burnout_epochs=20):
        self.name = name
        self.game = game
        self.history  = []
        self.init_probabilities = {
            0: 0,
            1: 0.1,
            2: 0.2,
            3: 0.6,
            4: 0.1,
            5: 0
        }
        self.burnout_epochs = burnout_epochs
        self.k = k
        self.cond_prob = {a: [] for a in ACTIONS}

    def strategy(self, opponent: Player) -> int:
        """
        Determines the next action to take based on the opponent's history and the player's own history.

        This strategy uses conditional probabilities and a burn-in period to adapt its behavior:
        - During the initial `burnout_epochs`, it selects an action randomly according to `init_probabilities`.
        - After the burn-in period, it predicts the opponent's next move using the last `k` conditional probabilities,
          then selects an action in response.

        Args:
            opponent (Player): The opponent player instance, which contains the history of their actions.

        Returns:
            int: The chosen action for the current round.
        """
        opponent_history = opponent.history
        i = len(opponent_history)
        last_2_opponent_result = opponent_history[-2] if len(opponent_history) > 1 else 2
        last_my_result = self.history[-1] if len(self.history) > 0 else 2
        if i <= self.burnout_epochs:
            result=  np.random.choice(list(self.init_probabilities.keys()), p=list(self.init_probabilities.values()))
            self.cond_prob[last_my_result].append(last_2_opponent_result)
        else:
            last_opponent_history = self.cond_prob[last_my_result][-self.k:]
            prob = [last_opponent_history.count(a) / len(last_opponent_history) for a in ACTIONS]
            opponent_next = np.random.choice(ACTIONS, p=prob)
            result = max(1, min(5, 5 - opponent_next))
        return result