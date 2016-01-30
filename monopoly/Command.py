__author__ = "Simon"

from monopoly.Player import Player


commands = {
    'START_GAME': "StartGame",
    'REGISTER_PLAYER': "IPlay",
    'ROLL': "Roll",
    }


class Command:
    def __init__(self, command_name):
        self.command_name = command_name
        self.caller = ""
        self.args = []

    def as_caller(self, caller):
        if isinstance(caller, Player):
            self.caller = caller.nickname
            return self
        if isinstance(caller, str):
            self.caller = caller
            return self

    def with_args(self, args):
        self.args = args
        return self

    def send(self, game):
        if self.command_name:
            game.send_command(self.caller + ": " + self.command_name + " " + " ".join(self.args))

for command_name, command_string in commands.items():
    setattr(Command, command_name, Command(command_string))
    
