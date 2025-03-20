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


class Player(BaseModel):
    name: str
    chips: int
    hand: List[Card] = Field(default_factory=list)

    def reset(self):
        self.hand = []


class Table(BaseModel):
    players: List[Player]
    deck: Deck = Field(default_factory=Deck)
    community_cards: List[Card] = Field(default_factory=list)

    def reset(self):
        self.deck.reset()
        self.deck.shuffle()
        self.community_cards = []
        for player in self.players:
            player.reset()

    def deal_hands(self):
        for player in self.players:
            player.hand = self.deck.deal_hand()

    def deal_flop(self):
        self.community_cards = self.deck.deal_flop()

    def deal_turn(self):
        self.community_cards.extend(self.deck.deal_turn())

    def deal_river(self):
        self.community_cards.extend(self.deck.deal_river())
