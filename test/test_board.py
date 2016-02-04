__author__ = 'Simon'


from monopoly.Board import Board
import pytest


@pytest.fixture
def board():
    return Board()

def test_new_board(board):
    assert len(board.cells) == 40
    assert len(board.luck_cards_deck)
    assert len(board.community_chest_deck)

def test_deck_renew(board):
    origin_luck_cards_deck = board.luck_cards_deck[:]
    origin_community_chest_deck = board.community_chest_deck[:]

    end_luck_cards_deck = []
    end_community_chest_deck = []

    for i in range(len(origin_luck_cards_deck)):
        end_luck_cards_deck.append(board.draw_luck_card())

    for i in range(len(origin_community_chest_deck)):
        end_community_chest_deck.append(board.draw_community_chest_card())

    assert len(origin_luck_cards_deck) == len(end_luck_cards_deck)
    assert len(origin_community_chest_deck) == len(end_community_chest_deck)
    assert not board.luck_cards_deck
    assert not board.community_chest_deck

    renewed_draw = None
    renewed_draw = board.draw_luck_card()
    assert renewed_draw
    assert board.luck_cards_deck

    renewed_draw = None
    renewed_draw = board.draw_community_chest_card()
    assert renewed_draw
    assert board.community_chest_deck

def test_get_index_in_board(board):
    assert board.cells[10].get_index_in_board() == 10
    assert board.cells[0].get_index_in_board() == 0
    assert board.cells[20].get_index_in_board() == 20
    assert board.cells[39].get_index_in_board() == 39