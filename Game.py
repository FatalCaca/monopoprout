__author__ = "Simon"

from Command import Command, CommandFactory


class GameState:
    NOT_STARTED = 1
    ASKING_WHOS_PLAYING = 2


class Game:
    board = None
    players = []
    playing_player = None
    output_channel = None

    def __init__(self):
        self.commands = CommandFactory().get_all_commands()
        self.game_state = GameState.NOT_STARTED

    """
    Commands format : "nickname: arg1 arg2 argn"
    """
    def input_command(self, command):
        commander_nickname = self.extract_commander_nickname(command)
        args = self.extract_command_args(command)

        for command in [c for c in self.commands if c.text == args[0]]:
            command.execute(self, commander_nickname, args[1:])

    def start_game(self):
        self.output_message

    def extract_command_nickname(self, command):
        return command.split(": ")[0]

    def extract_command_args(self, command):
        return command.split(": ")[1].split(" ")

    def roll(self):
        self.output_message("rolling")

    def output_message(self, message):
        if(self.output_channel != None):
            self.output_channel(message)
        else:
            print(message)