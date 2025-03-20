from holdem.agents import RandomAgent
from holdem.engine import HoldemEngine
from holdem.models import Table


def main():
    """Execute the main functionality of the program."""
    table = Table(
        players=[
            RandomAgent(name="Player 1", chips=1000),
            RandomAgent(name="Player 2", chips=1000),
            RandomAgent(name="Player 3", chips=1000),
        ]
    )
    engine = HoldemEngine(table=table)
    engine.run()


if __name__ == "__main__":
    main()
