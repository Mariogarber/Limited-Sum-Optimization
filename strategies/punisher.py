from game.game import Game
from game.player import Player

class InfernalPunisher(Player):
    """
    Adaptive strategy for the limited-sum game that balances coordination and self-protection.

    Strategy:
    - Starts trying to coordinate on i+j=5 (efficient outcome)
    - Monitors opponent's cooperation patterns and adapts accordingly
    - Uses graduated punishment for greedy behavior
    - Attempts forgiveness and cooperation recovery
    - Adjusts strategy based on opponent's consistency
    """

    def __init__(self, game: Game, name: str = ""):
        super().__init__(game, name)
        self.cooperation_score = 0  # Track opponent's cooperative behavior
        self.punishment_mode = False
        self.punishment_rounds = 0

    def strategy(self, opponent: Player) -> int:
        """
        Adaptive strategy with cooperation tracking and graduated response
        """
        # First round: start with 2 (middle ground)
        if not self.history:
            return 2

        last_opponent = opponent.history[-1]

        # Update cooperation tracking
        if last_opponent <= 3:
            self.cooperation_score += 1
        else:
            self.cooperation_score -= 2

        # Analyze opponent's recent pattern (last 5 rounds)
        recent_rounds = min(5, len(opponent.history))
        recent_actions = opponent.history[-recent_rounds:]
        avg_recent = sum(recent_actions) / len(recent_actions)

        # Simplified punishment mechanism
        if self.punishment_mode:
            self.punishment_rounds += 1
            # Simple punishment: play 0 for 2 rounds, then try to recover
            if self.punishment_rounds <= 2:
                return 0
            else:
                # Reset and try to recover cooperation
                self.punishment_mode = False
                self.punishment_rounds = 0
                return 2

        # Detect consistently greedy behavior
        if last_opponent > 3 and avg_recent > 3.5:
            self.punishment_mode = True
            self.punishment_rounds = 0
            return 0

        # Normal coordination attempt
        if last_opponent <= 3:
            # Try to maintain sum=5
            return max(0, min(5, 5 - last_opponent))

        # Default fallback
        return 2
