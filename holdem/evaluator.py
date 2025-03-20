from collections import Counter
from enum import IntEnum
from typing import List, Tuple

from pydantic import BaseModel

from .models import Card, Rank


class HandType(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


class HandEvaluation(BaseModel):
    hand_type: HandType
    score: int
    ranks: List[Rank]


class Evaluator:
    @classmethod
    def evaluate(
        cls, hole_cards: List[Card], community_cards: List[Card]
    ) -> HandEvaluation:
        """
        Evaluate a poker hand and return a HandEvaluation object.
        Higher scores represent better hands.

        Args:
            hole_cards: A player's two hole cards
            community_cards: The community cards on the table

        Returns:
            HandEvaluation: Contains hand_type, score and ranks

        Raises:
            ValueError: If the total number of cards is less than 5
        """
        all_cards = hole_cards + community_cards

        if len(all_cards) < 5:
            raise ValueError("Cannot evaluate poker hand with fewer than 5 cards")

        hand_type, ranks = cls._get_hand_type(all_cards)
        score = cls._get_hand_score(all_cards)

        return HandEvaluation(hand_type=hand_type, score=score, ranks=ranks)

    @classmethod
    def _get_hand_score(cls, cards: List[Card]) -> int:
        """Calculate the score for the best 5-card hand from the given cards."""
        # Check for each hand type, from best to worst
        hand_type, hand_ranks = cls._get_hand_type(cards)

        # Base score is the hand type multiplied by a large number to ensure
        # a better hand type always beats a lesser hand type
        base_score = hand_type.value * 10**15

        # Add additional points based on the ranks within the hand
        # (this handles ties within the same hand type)
        rank_score = 0
        for i, rank in enumerate(hand_ranks):
            # Multiply by decreasing powers of 100 to prioritize higher cards
            rank_score += int(rank) * (100 ** (5 - i))

        return base_score + rank_score

    @classmethod
    def _get_hand_type(cls, cards: List[Card]) -> Tuple[HandType, List[Rank]]:
        """
        Determine the type of hand and return hand type and relevant ranks.

        Returns:
            tuple: (hand_type, [ranks]) where ranks are ordered
                  by importance for breaking ties
        """
        # Count occurrences of each rank
        rank_counts = Counter([card.rank for card in cards])
        most_common = rank_counts.most_common()

        # Get unique ranks
        unique_ranks = sorted(set([card.rank for card in cards]), reverse=True)

        # Check for flush
        suits = [card.suit for card in cards]
        is_flush = any(suits.count(suit) >= 5 for suit in set(suits))

        # Check for straight
        is_straight = cls._is_straight(unique_ranks)

        # Special case: A-5 straight (Ace counts as 1)
        wheel_straight = False
        if not is_straight and len(unique_ranks) >= 5:
            if Rank.ACE in unique_ranks:  # Ace present
                # Check for Ace, 2, 3, 4, 5
                if all(
                    r in unique_ranks
                    for r in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]
                ):
                    is_straight = True
                    wheel_straight = True

        # Determine the hand type and rank values for tiebreakers
        if is_straight and is_flush:
            # Check for royal flush (10-A of same suit)
            royal_ranks = {Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE}
            for suit in set(suits):
                suit_cards = [card for card in cards if card.suit == suit]
                if len(suit_cards) >= 5:
                    suit_ranks = {card.rank for card in suit_cards}
                    if royal_ranks.issubset(suit_ranks):
                        return HandType.ROYAL_FLUSH, [
                            Rank.ACE,
                            Rank.KING,
                            Rank.QUEEN,
                            Rank.JACK,
                            Rank.TEN,
                        ]

            # Get the ranks in the straight flush
            flush_suit = next(suit for suit in set(suits) if suits.count(suit) >= 5)
            flush_cards = [card for card in cards if card.suit == flush_suit]
            flush_ranks = sorted(set([card.rank for card in flush_cards]), reverse=True)

            # Check for wheel straight flush
            if (
                wheel_straight
                and Rank.ACE in flush_ranks
                and all(
                    r in flush_ranks
                    for r in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]
                )
            ):
                return HandType.STRAIGHT_FLUSH, [
                    Rank.FIVE,
                    Rank.FOUR,
                    Rank.THREE,
                    Rank.TWO,
                    Rank.ACE,
                ]

            straight_flush_ranks = cls._get_straight_ranks(flush_ranks)

            return HandType.STRAIGHT_FLUSH, straight_flush_ranks[:5]

        if most_common[0][1] == 4:  # Four of a kind
            quads_rank = most_common[0][0]
            kicker = next(
                r for r in sorted(unique_ranks, reverse=True) if r != quads_rank
            )
            return HandType.FOUR_OF_A_KIND, [quads_rank, kicker]

        # Check for full house
        # First, check explicit three of a kind + pair
        if most_common[0][1] == 3 and most_common[1][1] >= 2:
            return HandType.FULL_HOUSE, [most_common[0][0], most_common[1][0]]

        # If we have three pairs, we can form a full house by using the two highest pairs
        # By poker rules, we can choose which cards to use to make our best 5-card hand
        # So from three pairs, we can use the highest pair twice (making a "trips") and the second highest as a pair
        if (
            len(most_common) >= 3
            and most_common[0][1] == 2
            and most_common[1][1] == 2
            and most_common[2][1] == 2
        ):
            # Get the ranks of the three pairs in descending order
            pair_ranks = sorted(
                [rank for rank, count in most_common[:3] if count == 2], reverse=True
            )
            # Use the highest pair as trips and second highest as the pair part of the full house
            return HandType.FULL_HOUSE, [pair_ranks[0], pair_ranks[1]]

        if is_flush:
            # Get the 5 highest cards of the flush suit
            flush_suit = next(suit for suit in set(suits) if suits.count(suit) >= 5)
            flush_cards = [card for card in cards if card.suit == flush_suit]
            flush_ranks = sorted([card.rank for card in flush_cards], reverse=True)
            return HandType.FLUSH, flush_ranks[:5]

        if is_straight:
            if wheel_straight:
                return HandType.STRAIGHT, [
                    Rank.FIVE,
                    Rank.FOUR,
                    Rank.THREE,
                    Rank.TWO,
                    Rank.ACE,
                ]
            straight_ranks = cls._get_straight_ranks(unique_ranks)
            return HandType.STRAIGHT, straight_ranks[:5]

        if most_common[0][1] == 3:  # Three of a kind
            trips_rank = most_common[0][0]
            kickers = sorted(
                [r for r in unique_ranks if r != trips_rank], reverse=True
            )[:2]
            return HandType.THREE_OF_A_KIND, [trips_rank] + kickers

        if most_common[0][1] == 2 and most_common[1][1] == 2:  # Two pair
            high_pair = most_common[0][0]
            low_pair = most_common[1][0]
            kicker = next(
                r
                for r in sorted(unique_ranks, reverse=True)
                if r != high_pair and r != low_pair
            )
            return HandType.TWO_PAIR, [high_pair, low_pair, kicker]

        if most_common[0][1] == 2:  # One pair
            pair_rank = most_common[0][0]
            kickers = sorted([r for r in unique_ranks if r != pair_rank], reverse=True)[
                :3
            ]
            return HandType.PAIR, [pair_rank] + kickers

        # High card
        return HandType.HIGH_CARD, sorted(unique_ranks, reverse=True)[:5]

    @classmethod
    def _is_straight(cls, sorted_unique_ranks: List[Rank]) -> bool:
        """Check if the given unique ranks form a straight."""
        if len(sorted_unique_ranks) < 5:
            return False

        # Check for any 5 consecutive cards
        for i in range(len(sorted_unique_ranks) - 4):
            if (int(sorted_unique_ranks[i]) - int(sorted_unique_ranks[i + 4])) == 4:
                return True

        # Check for wheel straight: A-5-4-3-2
        if Rank.ACE in sorted_unique_ranks and all(  # Ace
            r in sorted_unique_ranks
            for r in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]
        ):
            return True

        return False

    @classmethod
    def _get_straight_ranks(cls, sorted_unique_ranks: List[Rank]) -> List[Rank]:
        """Get the ranks that form a straight, in descending order."""
        for i in range(len(sorted_unique_ranks) - 4):
            if (int(sorted_unique_ranks[i]) - int(sorted_unique_ranks[i + 4])) == 4:
                return sorted_unique_ranks[i : i + 5]

        # Check for A-5 straight
        if Rank.ACE in sorted_unique_ranks and all(  # Ace
            r in sorted_unique_ranks
            for r in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]
        ):
            return [Rank.FIVE, Rank.FOUR, Rank.THREE, Rank.TWO, Rank.ACE]

        return []
