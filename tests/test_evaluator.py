import pytest

from holdem.evaluator import Evaluator, HandType
from holdem.models import Card, Rank, Suit


def test_high_card():
    # A-K-Q-9-7 high card
    hand = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.HIGH_CARD
    assert evaluation.ranks == [Rank.ACE, Rank.KING, Rank.QUEEN, Rank.NINE, Rank.SEVEN]


def test_pair():
    # Pair of Kings
    hand = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.PAIR
    assert evaluation.ranks[0] == Rank.KING  # Kings are the pair
    assert len(evaluation.ranks) == 4  # Pair + 3 kickers


def test_two_pair():
    # Two pair: Kings and Nines
    hand = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.NINE, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.TWO_PAIR
    assert evaluation.ranks[:2] == [Rank.KING, Rank.NINE]  # Kings and Nines
    assert len(evaluation.ranks) == 3  # Two pairs + 1 kicker


def test_three_of_a_kind():
    # Three Kings
    hand = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.THREE_OF_A_KIND
    assert evaluation.ranks[0] == Rank.KING  # Kings
    assert len(evaluation.ranks) == 3  # Trips + 2 kickers


def test_straight():
    # 9-8-7-6-5 straight
    hand = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.SIX, suit=Suit.CLUBS),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.STRAIGHT
    assert evaluation.ranks == [Rank.NINE, Rank.EIGHT, Rank.SEVEN, Rank.SIX, Rank.FIVE]


def test_wheel_straight():
    # A-5-4-3-2 wheel straight
    hand = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.FOUR, suit=Suit.DIAMONDS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.STRAIGHT
    assert evaluation.ranks == [
        Rank.FIVE,
        Rank.FOUR,
        Rank.THREE,
        Rank.TWO,
        Rank.ACE,
    ]  # Ace is low in this case


def test_flush():
    # Spades flush
    hand = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
    ]
    community = [
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.FLUSH
    assert evaluation.ranks == [
        Rank.ACE,
        Rank.TEN,
        Rank.SEVEN,
        Rank.FIVE,
        Rank.TWO,
    ]  # Ace-high flush


def test_full_house():
    # Kings full of Nines
    hand = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.FULL_HOUSE
    assert evaluation.ranks == [Rank.KING, Rank.NINE]  # Kings full of Nines


def test_four_of_a_kind():
    # Four Kings
    hand = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.CLUBS),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.FOUR_OF_A_KIND
    assert evaluation.ranks[0] == Rank.KING  # Kings
    assert len(evaluation.ranks) == 2  # Quads + 1 kicker


def test_straight_flush():
    # 9-8-7-6-5 straight flush in Spades
    hand = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.SPADES),
    ]
    community = [
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.SIX, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.STRAIGHT_FLUSH
    assert evaluation.ranks == [Rank.NINE, Rank.EIGHT, Rank.SEVEN, Rank.SIX, Rank.FIVE]


def test_royal_flush():
    # Royal flush in Hearts
    hand = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.TEN, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.ROYAL_FLUSH
    assert evaluation.ranks == [Rank.ACE, Rank.KING, Rank.QUEEN, Rank.JACK, Rank.TEN]


def test_hand_comparisons():
    # Define various hands from worst to best
    high_card = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    pair = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    two_pair = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.NINE, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    three_kind = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    straight = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.HEARTS),
        Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.SIX, suit=Suit.CLUBS),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    flush = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    full_house = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    four_kind = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.CLUBS),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    straight_flush = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.SPADES),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.SIX, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    royal_flush = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.TEN, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    hands = [
        high_card,
        pair,
        two_pair,
        three_kind,
        straight,
        flush,
        full_house,
        four_kind,
        straight_flush,
        royal_flush,
    ]

    evaluations = [Evaluator.evaluate(hand[:2], hand[2:]) for hand in hands]

    # Verify that each hand beats all previous hands
    for i in range(1, len(evaluations)):
        assert evaluations[i] > evaluations[i - 1], f"Hand {i} should beat hand {i - 1}"


def test_tie_breaker_kickers():
    # Two pair Kings and Nines with different kickers
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),  # Queen kicker
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.SPADES),  # Jack kicker
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),  # Makes a pair of Kings
        Card(rank=Rank.NINE, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),  # Makes a pair of Nines
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval2 < eval1, "Hand with Queen kicker should beat hand with Jack kicker"
    assert (
        eval1.hand_type == eval2.hand_type == HandType.TWO_PAIR
    ), "Both hands should be Two Pair"
    assert eval1.ranks[2] > eval2.ranks[2], "Queen kicker > Jack kicker"


def test_tie_breaker_pair_rank():
    # Two pair with different second pairs
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.DIAMONDS),  # Ten for second pair
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.NINE, suit=Suit.DIAMONDS),  # Nine for second pair
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),  # Makes a pair of Kings for both
        Card(rank=Rank.TEN, suit=Suit.CLUBS),  # Completes Ten pair for player 1
        Card(rank=Rank.NINE, suit=Suit.CLUBS),  # Completes Nine pair for player 2
        Card(rank=Rank.FIVE, suit=Suit.SPADES),  # Kicker
        Card(rank=Rank.THREE, suit=Suit.HEARTS),  # Unused
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval2 < eval1, "Kings and Tens should beat Kings and Nines"
    assert (
        eval1.hand_type == eval2.hand_type == HandType.TWO_PAIR
    ), "Both hands should be Two Pair"
    assert eval1.ranks[1] > eval2.ranks[1], "Tens > Nines in the second pair"


def test_fifth_card_kicker():
    # High card hands that differ only in the fifth card
    hole_cards1 = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),  # Higher fifth card
    ]

    hole_cards2 = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.SIX, suit=Suit.HEARTS),  # Lower fifth card
    ]

    # Common community cards with no pairs
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.QUEEN, suit=Suit.CLUBS),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval2 < eval1, "Hand with higher fifth card should win"
    assert eval1.hand_type == eval2.hand_type == HandType.HIGH_CARD
    assert eval1.ranks[4] > eval2.ranks[4], "Seven kicker > Six kicker"


def test_full_house_tie_breaker():
    # Kings full of Aces vs Kings full of Queens
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.CLUBS),  # Aces for the pair part
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.CLUBS),
        Card(rank=Rank.QUEEN, suit=Suit.CLUBS),  # Queens for the pair part
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),  # Makes three Kings for both
        Card(rank=Rank.ACE, suit=Suit.SPADES),  # Second Ace for player 1
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),  # Second Queen for player 2
        Card(rank=Rank.THREE, suit=Suit.HEARTS),  # Unused
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval2 < eval1, "Kings full of Aces should beat Kings full of Queens"
    assert eval1.hand_type == eval2.hand_type == HandType.FULL_HOUSE
    assert eval1.ranks[0] == eval2.ranks[0], "Both have Kings as trips"
    assert eval1.ranks[1] > eval2.ranks[1], "Aces > Queens in the pair part"


def test_four_of_a_kind_kicker():
    # Four Kings with different kickers
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.SPADES),  # Ace kicker
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),  # Same as player 1's first card
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),  # Queen kicker
    ]

    # Common community cards with the other three Kings
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.CLUBS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.FIVE, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.DIAMONDS),
    ]

    # We're using the same King of Spades for both players, which is fine
    # since we're just comparing the evaluations as independent hands
    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert (
        eval2 < eval1
    ), "Four Kings with Ace kicker should beat Four Kings with Queen kicker"
    assert eval1.hand_type == eval2.hand_type == HandType.FOUR_OF_A_KIND
    assert eval1.ranks[0] == eval2.ranks[0], "Both have Kings as quads"
    assert eval1.ranks[1] > eval2.ranks[1], "Ace kicker > Queen kicker"


def test_different_straight_ranks():
    # 9-high straight vs 8-high straight
    hole_cards1 = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.HEARTS),
    ]

    hole_cards2 = [
        Card(rank=Rank.EIGHT, suit=Suit.DIAMONDS),
        Card(rank=Rank.FOUR, suit=Suit.HEARTS),
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.SIX, suit=Suit.CLUBS),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    # Player 1 forms: 9-8-7-6-5
    # Player 2 forms: 8-7-6-5-4
    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval2 < eval1, "9-high straight should beat 8-high straight"
    assert eval1.hand_type == eval2.hand_type == HandType.STRAIGHT
    assert eval1.ranks[0] > eval2.ranks[0], "9-high > 8-high"


def test_wheel_vs_higher_straight():
    # Wheel straight (A-5-4-3-2) vs 6-high straight
    hole_cards1 = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.HEARTS),
    ]

    hole_cards2 = [
        Card(rank=Rank.SIX, suit=Suit.HEARTS),
        Card(rank=Rank.FIVE, suit=Suit.DIAMONDS),
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.FOUR, suit=Suit.DIAMONDS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
    ]

    # Player 1 forms: 5-4-3-2-A (wheel)
    # Player 2 forms: 6-5-4-3-2
    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval1 < eval2, "6-high straight should beat wheel straight (A-5-4-3-2)"
    assert eval1.hand_type == eval2.hand_type == HandType.STRAIGHT
    assert eval1.ranks[0] < eval2.ranks[0], "Wheel's high card (5) < 6-high straight"


def test_flush_comparison():
    # Two flush hands with different high cards
    hole_cards1 = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
    ]

    # Separate community cards since we need different suits for flushes
    community_cards1 = [
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
    ]

    community_cards2 = [
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.NINE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
    ]

    # For flush comparison, we need to use separate community cards
    # since we need different suits, but we'll make non-flush cards the same
    eval1 = Evaluator.evaluate(hole_cards1, community_cards1)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards2)

    assert eval2 < eval1, "Ace-high flush should beat King-high flush"
    assert eval1.hand_type == eval2.hand_type == HandType.FLUSH
    assert eval1.ranks[0] > eval2.ranks[0], "Ace > King as high card"


def test_evaluate_with_hole_and_community():
    # Test that the evaluate function correctly combines hole cards and community cards
    hole_cards = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]

    community_cards = [
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.TEN, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    # Should recognize a royal flush
    evaluation = Evaluator.evaluate(hole_cards, community_cards)

    assert evaluation.hand_type == HandType.ROYAL_FLUSH

    # The score should be higher than any other hand
    straight_flush_hole = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.SPADES),
    ]

    straight_flush_community = [
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.SIX, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    straight_flush_eval = Evaluator.evaluate(
        straight_flush_hole, straight_flush_community
    )

    assert evaluation > straight_flush_eval, "Royal flush should beat straight flush"


# Additional tests for ties, tie breakers, and edge cases


def test_identical_hands_tie():
    # Two identical high card hands
    hand1 = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
    ]

    hand2 = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.QUEEN, suit=Suit.CLUBS),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.SEVEN, suit=Suit.HEARTS),
    ]

    eval1 = Evaluator.evaluate(hand1[:2], hand1[2:])
    eval2 = Evaluator.evaluate(hand2[:2], hand2[2:])

    assert eval1 == eval2, "Identical hand ranks should tie"
    assert eval1.hand_type == eval2.hand_type, "Hand types should be the same"
    assert eval1.ranks == eval2.ranks, "Ranks should be identical"


def test_pydantic_model_serialization():
    # Test that the HandEvaluation model can be serialized to JSON
    hand = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.TEN, suit=Suit.HEARTS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    # Test that the model can be converted to dict
    eval_dict = evaluation.model_dump()

    assert eval_dict["hand_type"] == HandType.ROYAL_FLUSH
    assert isinstance(eval_dict["ranks"], list)
    # When serialized to dict, Enum values are converted to their integer values
    assert [int(r) for r in evaluation.ranks] == [14, 13, 12, 11, 10]


def test_wheel_straight_flush():
    # A-5-4-3-2 wheel straight flush in Spades
    hand = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
    ]
    community = [
        Card(rank=Rank.FOUR, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.SPADES),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.STRAIGHT_FLUSH
    assert evaluation.ranks == [
        Rank.FIVE,
        Rank.FOUR,
        Rank.THREE,
        Rank.TWO,
        Rank.ACE,
    ]  # Ace is low in this case


def test_full_house_three_pair():
    # Three pairs and a card, should form a full house with the best two pairs
    hand = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.CLUBS),
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.FULL_HOUSE
    assert evaluation.ranks == [Rank.ACE, Rank.KING]  # Aces full of Kings


def test_best_hand_selection():
    # Player has 7 cards that could make multiple hand types
    # The cards could make a flush and a three of a kind, but the flush is the best hand
    hand = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.ACE, suit=Suit.DIAMONDS),
    ]
    community = [
        Card(rank=Rank.ACE, suit=Suit.CLUBS),
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    # The player has three Aces (hearts, diamonds, clubs)
    # And also has 4 spades (but not enough for a flush)
    # The best hand is three of a kind: Aces with King, Queen kickers
    assert evaluation.hand_type == HandType.THREE_OF_A_KIND
    assert evaluation.ranks[0] == Rank.ACE  # Aces
    assert evaluation.ranks[1:3] == [Rank.KING, Rank.QUEEN]  # King, Queen kickers


def test_flush_vs_straight():
    # Player has both a flush and a straight, should choose the flush
    hand = [
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.EIGHT, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.SEVEN, suit=Suit.HEARTS),
        Card(rank=Rank.NINE, suit=Suit.CLUBS),
        Card(rank=Rank.SIX, suit=Suit.DIAMONDS),
        Card(rank=Rank.FOUR, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    # Player has a K-8-7-4-3 flush in hearts, and also a 9-8-7-6-x straight
    # Flush beats straight, so that's the hand that should be returned
    assert evaluation.hand_type == HandType.FLUSH
    assert evaluation.ranks[0] == Rank.KING  # King-high flush


def test_same_rank_different_full_house():
    # Tests a full house with the same high card but different pair card
    # Kings full of Queens vs Kings full of Jacks
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.QUEEN, suit=Suit.CLUBS),  # Queen for pair
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.CLUBS),  # Jack for pair
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.CLUBS),  # Makes trip Kings for both
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),  # Second Queen for player 1
        Card(rank=Rank.JACK, suit=Suit.SPADES),  # Second Jack for player 2
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval1 > eval2, "Kings full of Queens should beat Kings full of Jacks"
    assert eval1.hand_type == eval2.hand_type == HandType.FULL_HOUSE
    assert eval1.ranks[0] == eval2.ranks[0] == Rank.KING, "Both have Kings as trips"
    assert eval1.ranks[1] > eval2.ranks[1], "Queens > Jacks in the pair part"


def test_same_straight_different_suits():
    # Same straight with different suits should be a tie
    hole_cards1 = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.HEARTS),
    ]

    hole_cards2 = [
        Card(rank=Rank.NINE, suit=Suit.HEARTS),
        Card(rank=Rank.EIGHT, suit=Suit.DIAMONDS),
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.SIX, suit=Suit.CLUBS),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert eval1 == eval2, "Same straight values should tie regardless of suits"
    assert eval1.hand_type == eval2.hand_type == HandType.STRAIGHT
    assert eval1.ranks == eval2.ranks, "Ranks should be identical"


def test_higher_straight_flush():
    # King-high straight flush vs 9-high straight flush
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),
    ]

    hole_cards2 = [
        Card(rank=Rank.NINE, suit=Suit.HEARTS),
        Card(rank=Rank.EIGHT, suit=Suit.HEARTS),
    ]

    # Separate community cards for the two different straight flushes
    community_cards1 = [
        Card(rank=Rank.JACK, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    community_cards2 = [
        Card(rank=Rank.SEVEN, suit=Suit.HEARTS),
        Card(rank=Rank.SIX, suit=Suit.HEARTS),
        Card(rank=Rank.FIVE, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards1)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards2)

    assert eval1 > eval2, "King-high straight flush should beat 9-high straight flush"
    assert eval1.hand_type == eval2.hand_type == HandType.STRAIGHT_FLUSH
    assert eval1.ranks[0] > eval2.ranks[0], "King > 9 as high card"


def test_royal_flush_different_suits():
    # Royal flush in different suits should be a tie
    hole_cards1 = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.SPADES),
    ]

    hole_cards2 = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]

    # Separate community cards for the two different royal flushes
    community_cards1 = [
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),
        Card(rank=Rank.JACK, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.HEARTS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    community_cards2 = [
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.TEN, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
        Card(rank=Rank.TWO, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards1)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards2)

    assert eval1 == eval2, "Royal flushes in different suits should tie"
    assert eval1.hand_type == eval2.hand_type == HandType.ROYAL_FLUSH
    assert eval1.ranks == eval2.ranks, "Ranks should be identical"


def test_three_of_a_kind_kicker_comparison():
    # Three of a kind with different kickers
    hole_cards1 = [
        Card(rank=Rank.KING, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.CLUBS),  # Ace kicker
    ]

    hole_cards2 = [
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.CLUBS),  # Jack kicker
    ]

    # Common community cards
    community_cards = [
        Card(rank=Rank.KING, suit=Suit.DIAMONDS),
        Card(rank=Rank.KING, suit=Suit.CLUBS),  # Makes three Kings for both
        Card(rank=Rank.QUEEN, suit=Suit.SPADES),  # Common second kicker
        Card(rank=Rank.FIVE, suit=Suit.HEARTS),
        Card(rank=Rank.THREE, suit=Suit.DIAMONDS),
    ]

    eval1 = Evaluator.evaluate(hole_cards1, community_cards)
    eval2 = Evaluator.evaluate(hole_cards2, community_cards)

    assert (
        eval1 > eval2
    ), "Kings with Ace-Queen kickers should beat Kings with Jack-Queen kickers"
    assert eval1.hand_type == eval2.hand_type == HandType.THREE_OF_A_KIND
    assert eval1.ranks[0] == eval2.ranks[0], "Both have Kings as trips"
    assert eval1.ranks[1] > eval2.ranks[1], "Ace kicker > Jack kicker"


def test_edge_case_7_card_straight():
    # 7-card straight should use the highest 5 cards
    hand = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]
    community = [
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.JACK, suit=Suit.CLUBS),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
        Card(rank=Rank.NINE, suit=Suit.HEARTS),
        Card(rank=Rank.EIGHT, suit=Suit.DIAMONDS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    assert evaluation.hand_type == HandType.STRAIGHT
    assert evaluation.ranks == [
        Rank.ACE,
        Rank.KING,
        Rank.QUEEN,
        Rank.JACK,
        Rank.TEN,
    ], "Should use A-K-Q-J-10, not the lower cards"


def test_not_enough_cards_error():
    # Test that an error is raised when there are fewer than 5 cards
    hole_cards = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
    ]

    # Only 2 community cards (total 4 cards)
    community_cards = [
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.JACK, suit=Suit.CLUBS),
    ]

    # Should raise ValueError
    with pytest.raises(
        ValueError, match="Cannot evaluate poker hand with fewer than 5 cards"
    ):
        Evaluator.evaluate(hole_cards, community_cards)

    # Test with empty community cards
    with pytest.raises(
        ValueError, match="Cannot evaluate poker hand with fewer than 5 cards"
    ):
        Evaluator.evaluate(hole_cards, [])

    # Test with no hole cards and only 4 community cards
    community_cards_4 = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS),
        Card(rank=Rank.JACK, suit=Suit.CLUBS),
    ]

    with pytest.raises(
        ValueError, match="Cannot evaluate poker hand with fewer than 5 cards"
    ):
        Evaluator.evaluate([], community_cards_4)


def test_best_hand_selection_2():
    # Player has 7 cards that could make multiple hand types
    # The cards include a straight, a flush, and a pair, but the straight flush is the best hand
    hand = [
        Card(rank=Rank.NINE, suit=Suit.SPADES),
        Card(rank=Rank.EIGHT, suit=Suit.SPADES),
    ]
    community = [
        Card(rank=Rank.SEVEN, suit=Suit.SPADES),
        Card(rank=Rank.SIX, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.KING, suit=Suit.CLUBS),
    ]

    evaluation = Evaluator.evaluate(hand, community)

    # Player has a straight flush (9-8-7-6-5) as well as a pair of 9s
    # Straight flush is the better hand
    assert evaluation.hand_type == HandType.STRAIGHT_FLUSH
    assert evaluation.ranks == [
        Rank.NINE,
        Rank.EIGHT,
        Rank.SEVEN,
        Rank.SIX,
        Rank.FIVE,
    ], "9-high straight flush"
