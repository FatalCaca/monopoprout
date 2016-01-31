__author__ = 'Simon'

from monopoly.Estate import EstateFactory
from monopoly.Text import Text



class MoneyCell:
    def __init__(self, text, money_amount):
        self.text = text
        self.money_amount = money_amount

    def __str__(self):
        return self.text


class LuckCell:
    def __str__(self):
        return Text.LUCK_CELL


class CommunityChestCell:
    def __str__(self):
        return Text.COMMUNITY_CHEST_CELL


class FreeParkingCell:
    def __str__(self):
        return Text.FREE_PARKING_CELL


class JailCell:
    def __str__(self):
        return Text.JAIL_CELL


class GoToJailCell:
    def __str__(self):
        return Text.GO_TO_JAIL_CELL


class EstateCell:
    def __init__(self, estate):
        self.estate = estate

    def __str__(self):
        return ' '.join((self.estate.name,
                         Text.AT,
                         self.estate.city,
                         Text.OWNED_BY.replace('&1', self.estate.owner) if self.estate.owner != None else '',
                         Text.AT_LEVEL.replace('&1', repr(self.estate.upgrade_level)),
                         Text.RENT_AT.replace('&1', repr(self.estate.get_current_rent()))))


class CellFactory:
    def get_default_cells():
        estates = EstateFactory.get_default_estates()

        return [
            MoneyCell('Case départ', 200),
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