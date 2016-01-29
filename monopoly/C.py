__author__ = "Simon"

class C:
    def __init__(self, command_name):
        self.command_name = command_name
        self.caller = ""
        self.args = []

    def as_caller(self, caller):
        self.caller = caller
        return self

    def with_args(self, args):
        self.args = args
        return self

    def send(self, game):
        if self.command_name:
            game.send_command(self.caller + ": " + self.command_name + " " + " ".join(self.args))