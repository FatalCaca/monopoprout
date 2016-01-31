__author__ = 'Simon'


from monopoly.Text import Text
from monopoly.Player import Player
from monopoly.Board import Board
import monopoly.Cell as Cell

import random
from pprint import pprint

random.seed()

class GameState:
    NOT_STARTED = 1
    ASKING_WHOS_PLAYING = 2
    GAME_STARTED = 3


class Game:
    MAX_PLAYER = 8
    SALARY = 200

    def __init__(self):
        self.game_state = GameState.NOT_STARTED

        self.command_bindings = {
                         "StartGame": self.start_game,
                         "IPlay": self.register_player,
                         "Roll": self.roll,
                         "Buy": self.buy_estate,
                         }
        self.board = Board()
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

        self.command_bindings[command_name](caller, args)

        self.busy = False

    def get_current_cell(self):
        try:
            return self.board.cells[self.playing_player.position - 1]
        except IndexError:
            return None

    def buy_estate(self, caller, args):
        if self.playing_player.nickname != caller:
            return

        cell = self.get_current_cell()

        if not isinstance(cell, Cell.EstateCell):
            self.output_message(Text.IS_NOT_ESTATE_CELL)
            return

        if cell.estate.owner:
            self.output_message(Text.ALREADY_OWNED_BY.replace('&1', str(cell.estate.owner)))
            return            

        if self.playing_player.money < cell.estate.sell_price:
            self.output_message(Text.NOT_ENOUGH_MONEY_TO_BUY_ESTATE)
            return

        cell.estate.owner = self.playing_player
        self.playing_player.money -= cell.estate.sell_price
        self.output_message(Text.SOMEONE_BUYS_ESTATE.replace('&1', str(self.playing_player))
                                                    .replace('&2', str(cell.estate))
                                                    .replace('&3', repr(cell.estate.sell_price))
                                                    .replace('&4', repr(self.playing_player.money)))

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
        if len(self.players) >= Game.MAX_PLAYER:
            self.output_message(Text.TOO_MUCH_PLAYER_REGISTERED)
            return

        if [p for p in self.players if p.nickname == caller]:
            return

        self.players.append(Player(caller))

    def roll(self, caller, args):
        if caller != self.playing_player.nickname:
            return

        roll_score = random.randint(1, 12)
        self.playing_player.position += roll_score  

        if self.playing_player.position > len(self.board.cells):
            self.playing_player.position -= len(self.board.cells)

        self.output_message(Text.ROLL_RESULT.replace("&1", self.playing_player.nickname).replace("&2", repr(roll_score)))
        self.output_message(Text.NEW_POSITION.replace("&1", self.playing_player.nickname).replace("&2", repr(self.playing_player.position)))

    def output_message(self, message):
        if(self.output_channel != None):
            self.output_channel(message)
        else:
            print(message)

    def give_money_to_player(self, player, amount, reason):
        player.money += amount

        if amount > 0:
            message = Text.RECEIVES_MONEY
        if amount < 0:
            message = Text.LOSES_MONEY

        self.output_message(message.replace('&1', player.nickname)
                                   .replace('&2', repr(amount))
                                   .replace('&3', reason)
                                   .replace('&4', repr(player.money)))

    def forward_player(self, player, amount):
        if self.playing_player != player or amount == 0:
            return

        player.position += amount
        if player.position >= len(self.board.cells):
            player.position -= len(self.board.cells)
            self.give_money_to_player(player, Game.SALARY, Text.SALARY)

        self.arrival_at_cell(player)

    def arrival_at_cell(self, player):
        cell = self.board.cells[player.position - 1]

        self.output_message(Text.ARRIVAL_AT_CELL.replace('&1', str(player))
                                                .replace('&2', repr(player.position))
                                                .replace('&3', str(cell)))

        if isinstance(cell, Cell.FreeParkingCell):
            if self.board.bank_money == 0:
                self.output_message(Text.BUT_FREE_PARKING_EMPTY)
            else:
                self.give_money_to_player(player, self.board.bank_money, Text.FREE_PARKING_FOR.replace('&1', str(player)))
                self.board.bank_money = 0

        if isinstance(cell, Cell.MoneyCell):
            self.give_money_to_player(player, cell.money_amount, str(cell))

