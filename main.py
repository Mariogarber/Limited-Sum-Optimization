from game.tournament import Tournament
from strategies.basic import Always0, Always3, UniformRandom, Focal5
from game.game import Game

def example_tournament():
    game = Game()
    participants = (Always0(game, "always0"),
                    Always3(game, "always3"),
                    UniformRandom(game, "uniform_random"),
                    Focal5(game, "focal5"))

    tournament = Tournament(participants, n_rounds=100, error=0.01,
                            repetitions=2)
    tournament.play()
    tournament.plot_results()

    return tournament

if __name__ == "__main__":
    _ = example_tournament()