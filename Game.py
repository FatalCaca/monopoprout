__author__ = "Simon"


from Text import Text
from Player import Player

class GameState:
    NOT_STARTED = 1
    ASKING_WHOS_PLAYING = 2


class Game:
    board = None
    players = []
    playing_player = None
    output_channel = None
    busy = False

    def __init__(self):
        self.game_state = GameState.NOT_STARTED

        self.commands = {"StartGame": self.start_game,
                         "IPlay": self.register_player,
                         "Roll": self.roll}

    """
    Commands format : "nickname: arg1 arg2 argn"
    """
    def send_command(self, command_text):
        while self.busy:
            pass

        self.busy = True

        caller = self.extract_command_nickname(command_text)
        args = self.extract_command_args(command_text)
        command_name = self.extract_command_name(command_text)

        if caller == None or command_name == None:
            return

        self.commands[command_name](caller, args)

        self.busy = False

    def start_game(self, caller, args):
        self.output_message(Text.START_GAME)
        self.game_state = GameState.ASKING_WHOS_PLAYING

    def extract_command_nickname(self, command):
        return command.split(": ")[0]

    def extract_command_args(self, command):
        if len(command.split(": ")) < 2:
            return []

        return command.split(": ")[1].split(" ")[1:]

    def extract_command_name(self, command):
        if len(command.split(": ")) < 2:
            return None

        return command.split(": ")[1].split(" ")[0]

    def register_player(self, caller, args):
        if len([p for p in self.players if p.nickname == caller]) > 0:
            return

        self.players.append(Player(caller))

    def roll(self):
        self.output_message("rolling")

    def output_message(self, message):
        if(self.output_channel != None):
            self.output_channel(message)
        else:
            print(message)