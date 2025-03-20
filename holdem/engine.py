from typing import List

from loguru import logger
from pydantic import BaseModel

from .models import Card, Table


class HoldemEngine(BaseModel):
    table: Table

    def run(self):
        logger.info("Starting new game")
        self.table.reset()
        self.run_hand()

    def run_hand(self):
        logger.info("Starting new hand")
        logger.info(f"Dealer: {self.table.players[self.table.dealer_index].name}")
        logger.info("Dealing hands to players")
        self.table.deal_hands()

        for player in self.table.players:
            logger.debug(f"{player.name}: {self.print_cards(player.hand)}")

        logger.info("Posting blinds")
        self.post_blinds()
        self.take_actions()

        logger.info("Dealing flop")
        self.table.deal_flop()
        logger.info(f"Board: {self.print_cards(self.table.community_cards)}")
        self.take_actions()

        logger.info("Dealing turn")
        self.table.deal_turn()
        logger.info(f"Board: {self.print_cards(self.table.community_cards)}")
        self.take_actions()

        logger.info("Dealing river")
        self.table.deal_river()
        logger.info(f"Board: {self.print_cards(self.table.community_cards)}")
        self.take_actions()

    def post_blinds(self):
        actions = self.table.post_blinds()
        for action in actions:
            logger.info(f"{action.player.name} {action.type.value} {action.amount}")

    def take_actions(self):
        actions = self.table.take_actions()
        for action in actions:
            logger.info(f"{action.player.name} {action.type.value} {action.amount}")

    def print_cards(self, cards: List[Card]):
        return " ".join([str(card) for card in cards])
