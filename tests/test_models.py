from holdem.models import Deck, Player, Table


def test_deck():
    deck = Deck()
    assert len(deck.cards) == 52
    assert len(deck.deal_hand()) == 2
    assert len(deck.deal_flop()) == 3
    assert len(deck.deal_turn()) == 1
    assert len(deck.deal_river()) == 1


def test_player():
    player = Player(name="Player 1", chips=1000)
    assert player.name == "Player 1"
    assert player.chips == 1000


def test_table():
    table = Table(
        players=[
            Player(name="Player 1", chips=1000),
            Player(name="Player 2", chips=1000),
        ]
    )
    assert len(table.players) == 2
    assert len(table.deck.cards) == 52

    assert all(player.hand == [] for player in table.players)
    assert len(table.community_cards) == 0

    table.deal_hands()

    assert all(len(player.hand) == 2 for player in table.players)
    assert len(table.deck.cards) == 52 - 2 * len(table.players)

    table.deal_flop()
    assert len(table.community_cards) == 3
    assert len(table.deck.cards) == 52 - 2 * len(table.players) - 3

    table.deal_turn()
    assert len(table.community_cards) == 4
    assert len(table.deck.cards) == 52 - 2 * len(table.players) - 4

    table.deal_river()
    assert len(table.community_cards) == 5
    assert len(table.deck.cards) == 52 - 2 * len(table.players) - 5
