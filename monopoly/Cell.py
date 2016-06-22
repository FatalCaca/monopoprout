__author__ = 'Simon'

from monopoly.Estate import EstateFactory
from monopoly.Text import Text


class Cell:
    ask_board_for_index = None

    def  __str__(self):
        return self.__class__.__name__

    def get_selection_infos(self):
        return str(self)

    def get_full_description(self):
        return str(self)

    def get_index_in_board(self):
        if self.ask_board_for_index != None and hasattr(self.ask_board_for_index, '__call__'):
            return self.ask_board_for_index(self)


class MoneyCell(Cell):
    def __init__(self, text, money_amount):
        self.text = text
        self.money_amount = money_amount
        super()

    def __str__(self):
        return self.text + ' ' + Text.COSTS.replace('&1', repr(self.money_amount))


class LuckCell(Cell):
    def __str__(self):
        return Text.LUCK_CELL


class CommunityChestCell(Cell):
    def __str__(self):
        return Text.COMMUNITY_CHEST_CELL


class FreeParkingCell(Cell):
    def __str__(self):
        return Text.FREE_PARKING_CELL


class JailCell(Cell):
    def __str__(self):
        return Text.JAIL_CELL


class GoToJailCell(Cell):
    def __str__(self):
        return Text.GO_TO_JAIL_CELL


class EstateCell(Cell):
    def __init__(self, estate):
        self.estate = estate

    def __str__(self):
        infos = [self.estate.name,
                 Text.AT,
                 self.estate.city,
                 '[' + repr(self.get_index_in_board()) + ']',
                 Text.AT_LEVEL % self.estate.upgrade_level]

        if self.estate.owner:
            infos.append(str(self.estate.owner))

        return ' '.join(infos)

    def get_full_description(self):
        infos = [self.estate.name,
                 Text.AT,
                 self.estate.city,
                 Text.OWNED_BY % str(self.estate.owner) if self.estate.owner != None else '',
                 Text.AT_LEVEL % self.estate.upgrade_level,
                 Text.RENT_AT % self.estate.get_current_rent(),
                 Text.COSTS % self.estate.sell_price]

        return ' '.join(infos)
class CellFactory:
    def get_default_cells():
        estates = EstateFactory.get_default_estates()

        return [
            MoneyCell('Case depart', 200),
            EstateCell(estates.pop(0)),
            CommunityChestCell(),
            EstateCell(estates.pop(0)),
            MoneyCell('Vidange de voiture', -200),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            LuckCell(),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            JailCell(),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            CommunityChestCell(),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            FreeParkingCell(),
            EstateCell(estates.pop(0)),
            LuckCell(),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            GoToJailCell(),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            CommunityChestCell(),
            EstateCell(estates.pop(0)),
            EstateCell(estates.pop(0)),
            LuckCell(),
            EstateCell(estates.pop(0)),
            MoneyCell('Croquettes pour le chat', -200),
            EstateCell(estates.pop(0)),
        ]
