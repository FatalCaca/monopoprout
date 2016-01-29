__author__ = 'Simon'


from monopoly.Text import Text
from monopoly.Player import Player

import random

random.seed()

class GameState:
    NOT_STARTED = 1
    ASKING_WHOS_PLAYING = 2
    GAME_STARTED = 3


class Game:
    def __init__(self):
        self.game_state = GameState.NOT_STARTED

        self.commands = {"StartGame": self.start_game,
                         "IPlay": self.register_player,
                         "Roll": self.roll}
        self.board = None
        self.players = []
        self.playing_player = None
        self.output_channel = None
        self.busy = False


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
        if self.game_state == GameState.NOT_STARTED:
            self.output_message(Text.START_GAME)
            self.game_state = GameState.ASKING_WHOS_PLAYING
            return

        if self.game_state == GameState.ASKING_WHOS_PLAYING:
            if len(self.players) == 0:
                self.output_message(Text.GAME_CANT_START_WITHOUT_PLAYER)
                return

            self.output_message(Text.END_OF_REGISTRATION + ", ".join([p.nickname for p in self.players]))
            self.output_message(Text.GAME_STARTING)
            self.game_state = GameState.GAME_STARTED

            self.playing_player = self.players[0]
            self.output_message(Text.IT_IS_SOMEONES_TURN.replace("&1", self.playing_player.nickname))

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

    def roll(self, caller, args):
        if caller != self.playing_player.nickname:
            return

        roll_score = random.randint(1, 12)
        self.playing_player.position += roll_score  





        self.output_message(Text.ROLL_RESULT.replace("&1", self.playing_player.nickname).replace("&2", repr(roll_score)))
        self.output_message(Text.NEW_POSITION.replace("&1", self.playing_player.nickname).replace("&2", repr(self.playing_player.position)))

    def output_message(self, message):
        if(self.output_channel != None):
            self.output_channel(message)
        else:
            print(message)