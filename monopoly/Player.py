class Player:
    def __init__(self, nickname):
        self.position = 1
        self.nickname = nickname
        self.has_jail_card = False
        self.money = 0
        self.selected_cell = None

    def __str__(self):
        return self.nickname