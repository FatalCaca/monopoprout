__author__ = "simon.ballu@gmail.com"


from monopoly.Text import Text


class Player:
    def __init__(self, nickname):
        self.position = 1
        self.nickname = nickname
        self.jail_cards = 0
        self.is_in_jail = False
        self.money = 0
        self.selected_cell = None
        self.can_roll = True
        self.turns_to_wait_in_jail = 0
        self.curent_cell = None

    def __str__(self):
        return self.nickname

    def get_full_description(self):
        return Text.PLAYER_FULL_DESCRIPTION % (
            self.nickname,
            self.position,
            self.money
        )
