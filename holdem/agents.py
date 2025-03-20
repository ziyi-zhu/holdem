from .models import Action, ActionType, Player, Table


class RandomAgent(Player):
    def make_decision(self, table: Table) -> Action:
        return Action(
            type=ActionType.BET,
            amount=10,
            street=table.current_street,
            player=self,
        )
