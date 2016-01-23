__author__ = "Simon"


class Command:
    def __init__(self, text, execute):
        self.text = text
        self.execute = execute


class CommandFactory:
    def get_all_commands(self):
        def start_game_execute(self, game, nickname, args):
            print("StartGame")

        def roll_execute(self, game, nickname, args):
            print("roll")

        return [Command("StartGame", start_game_execute),
                Command("Roll", roll_execute)]