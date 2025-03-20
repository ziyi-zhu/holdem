from __future__ import annotations

import random
from enum import Enum, IntEnum
from typing import List

from pydantic import BaseModel, Field


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @classmethod
    def all(cls) -> List["Rank"]:
        return list(cls)


class Suit(str, Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

    @classmethod
    def all(cls) -> List["Suit"]:
        return list(cls)


class Card(BaseModel):
    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        rank_str = str(self.rank.value)
        if self.rank == Rank.JACK:
            rank_str = "J"
        elif self.rank == Rank.QUEEN:
            rank_str = "Q"
        elif self.rank == Rank.KING:
            rank_str = "K"
        elif self.rank == Rank.ACE:
            rank_str = "A"
        return f"{rank_str}{self.suit.value}"


class Deck(BaseModel):
    cards: List[Card] = Field(
        default_factory=lambda: [
            Card(rank=rank, suit=suit) for rank in Rank.all() for suit in Suit.all()
        ]
    )

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()

    def deal(self, n: int) -> List[Card]:
        return [self.draw() for _ in range(n)]

    def deal_hand(self) -> List[Card]:
        return self.deal(2)

    def deal_flop(self) -> List[Card]:
        return self.deal(3)

    def deal_turn(self) -> List[Card]:
        return self.deal(1)

    def deal_river(self) -> List[Card]:
        return self.deal(1)

    def reset(self):
        self.cards = [
            Card(rank=rank, suit=suit) for rank in Rank.all() for suit in Suit.all()
        ]


class ActionType(str, Enum):
    FOLD = "fold"
    CHECK = "check"
    BET = "bet"


class Street(str, Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class Action(BaseModel):
    type: ActionType
    street: Street
    amount: float
    player: Player


class Player(BaseModel):
    name: str
    chips: int
    hand: List[Card] = Field(default_factory=list)
    is_active: bool = True

    def reset(self):
        self.hand = []

    def make_decision(self, table: Table) -> Action:
        raise NotImplementedError("Subclasses must implement this method")


class Table(BaseModel):
    players: List[Player]
    deck: Deck = Field(default_factory=Deck)
    community_cards: List[Card] = Field(default_factory=list)
    dealer_index: int = 0
    small_blind: int = 1
    big_blind: int = 2
    current_player_index: int = 0
    current_street: Street = Street.PREFLOP
    action_history: List[Action] = Field(default_factory=list)
    pot: int = 0

    def reset(self):
        self.deck.reset()
        self.deck.shuffle()
        self.community_cards = []
        for player in self.players:
            player.reset()
        self.dealer_index = random.randint(0, len(self.players) - 1)
        self.current_street = Street.PREFLOP

    def deal_hands(self):
        for player in self.players:
            player.hand = self.deck.deal_hand()

    def deal_flop(self):
        self.community_cards = self.deck.deal_flop()
        self.current_street = Street.FLOP

    def deal_turn(self):
        self.community_cards.extend(self.deck.deal_turn())
        self.current_street = Street.TURN

    def deal_river(self):
        self.community_cards.extend(self.deck.deal_river())
        self.current_street = Street.RIVER

    def post_blinds(self) -> List[Action]:
        actions = []
        self.current_player_index = self.dealer_index
        actions.append(
            Action(
                type=ActionType.BET,
                street=Street.PREFLOP,
                amount=self.small_blind,
                player=self.next_player(),
            )
        )
        actions.append(
            Action(
                type=ActionType.BET,
                street=Street.PREFLOP,
                amount=self.big_blind,
                player=self.next_player(),
            )
        )
        self.action_history.extend(actions)
        return actions

    def next_player(self) -> Player:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def take_actions(self) -> List[Action]:
        actions = []
        for player in self.players:
            if player.is_active:
                action = player.make_decision(self)
                if not self.validate_action(action):
                    raise ValueError(f"Invalid action: {action}")
                actions.append(action)

        self.action_history.extend(actions)
        return actions

    def validate_action(self, action: Action) -> bool:
        return True
