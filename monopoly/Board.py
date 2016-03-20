__author__ = 'simon.ballu@gmail.com'

from random import shuffle
from monopoly.LuckCard import LuckCardFactory
from monopoly.Cell import CellFactory, Cell


class Board:
    def __init__(self):
        self.bank_money = 0
        self.cells = CellFactory.get_default_cells()
        Cell.ask_board_for_index = self.get_cell_index
        self._renew_luck_card_deck()
        self._renew_community_chest_deck()
        self.houses_available = 50
        self.hotels_available = 10

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, position):
        return self.cell[position]

    def get_cell_index(self, cell):
        return self.cells.index(cell)

    def draw_luck_card(self):
        if not self.luck_cards_deck:
            self._renew_luck_card_deck()

        return self.luck_cards_deck.pop(0)

    def draw_community_chest_card(self):
        if not self.community_chest_deck:
            self._renew_community_chest_deck()

        return self.community_chest_deck.pop(0)

    def _renew_luck_card_deck(self):
        self.luck_cards_deck = LuckCardFactory.get_default_luck_cards()
        shuffle(self.luck_cards_deck)

    def _renew_community_chest_deck(self):
        self.community_chest_deck = LuckCardFactory.get_default_community_chest_cards()
        shuffle(self.community_chest_deck)
