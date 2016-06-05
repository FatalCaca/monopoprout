__author__ = 'simon.ballu@gmail.com'


from monopoly.Text import Text
from monopoly.Player import Player
from monopoly.Board import Board
import monopoly.Cell as Cell

import random

random.seed()

class GameState:
    NOT_STARTED = 1
    ASKING_WHOS_PLAYING = 2
    GAME_STARTED = 3


class Game:
    MAX_PLAYER = 8
    SALARY = 200
    STARTING_MONEY = 1000
    JAIL_TOLL = 200
    MAX_TURNS_IN_JAIL = 3

    def __init__(self, game_over_callback=None):
        self.game_state = GameState.NOT_STARTED

        self.command_bindings = {
                         "startgame": self.start_game_command,
                         "iplay": self.register_player_command,
                         "roll": self.roll_command,
                         "buy": self.buy_estate_command,
                         "select": self.select_cell_command,
                         "upgrade": self.upgrade_estate_command,
                         "testroll": self.test_roll_command,
                         "payforjail": self.pay_for_jail_command,
                         "endturn": self.end_turn_command,
                         "money": self.money_command,
                         "info": self.info_command,
                         }
        self.board = Board()
        self.players = []
        self.playing_player = None
        self.output_channel = None
        self.private_output_channel = None
        self.busy = False
        self.game_over = False

        if game_over_callback:
            self.game_over_callback = game_over_callback
        else:
            self.game_over_callback = self.dummy_game_over

    def send_command(self, command_text):
        while self.busy:
            print("caca")
            pass

        self.busy = True

        caller = self.extract_command_nickname(command_text)
        args = self.extract_command_args(command_text)
        command_name = self.extract_command_name(command_text)

        if caller == None or command_name == None:
            self.busy = False
            return

        try:
            self.command_bindings[command_name.lower()](caller, args)
        except KeyError:
            print("Error: command binding missing for [" + command_name + "]")

        self.busy = False

    def money_command(self, caller, args):
        player = self.get_player_from_nickname(caller)

        if not player:
            return

        self.send_private_message(player, Text.YOU_HAVE_THAT_MUCH_MONEY % player.money)

    def info_command(self, caller, args):
        player = self.get_player_from_nickname(caller)

        if not player:
            return

        cell_index = player.position

        if len(args):
            cell_index = int(args[0])

        cell_index -= 1

        try:
            self.send_private_message(player, (Text.THE_CELL % cell_index) + " " + self.board.cells[cell_index].get_full_description())
        except KeyError:
            print("Error: Wrong cell index for info request")


    def end_turn_command(self, caller, args):
        player = self.get_player_from_nickname(caller)

        if player != self.playing_player:
            print("END_TURN pas bon joueur")
            return

        if player.can_roll:
            self.send_private_message(self.playing_player, Text.MUST_ROLL_BEFORE_END_TURN)
            return

        if player.money < 0:
            self.output_message(Text.PLAYER_GOES_BANKRUPT % str(player))
            new_playing_player_index = self.players.index(self.playing_player) - 1

            if new_playing_player_index < 0:
                new_playing_player_index = len(self.players) - 2

            self.playing_player = self.players[new_playing_player_index]
            self.players.remove(player)

        if len(self.players) == 1:
            self.end_game()

        self.next_turn()

    def pay_for_jail_command(self, caller, args):
        player = self.get_player_from_nickname(caller)
        if player != self.playing_player:
            return

        if not player.is_in_jail:
            return

        if player.money < Game.JAIL_TOLL:
            self.tell_player_he_doesnt_have_enough_money(player, Game.JAIL_TOLL)
            return

        player.money -= Game.JAIL_TOLL
        player.is_in_jail = False
        self.output_message(Text.GOES_OUT_OF_JAIL_BY_PAYING % str(player))

    def upgrade_estate_command(self, caller, args):
        player = self.get_player_from_nickname(caller)
        if player != self.playing_player:
            return

        if not isinstance(player.selected_cell, Cell.EstateCell):
            self.send_private_message(player, Text.NOT_AN_ESTATE_CELL % str(player.selected_cell))
            return

        estate = player.selected_cell.estate

        if estate.upgrade_level == 5:
            self.send_private_message(player, Text.ALREADY_MAX_LEVEL % str(estate))
            return

        if estate.upgrade_level == 4 and self.board.hotels_available <= 0:
            self.send_private_message(player, Text.NO_MORE_HOTEL)
            return

        if estate.upgrade_level < 4 and self.board.houses_available <= 0:
            self.send_private_message(player, Text.NO_MORE_HOUSE)
            return

        estates_in_same_group = [cell.estate for cell in self.board.cells
                                    if isinstance(cell, Cell.EstateCell)
                                    and hasattr(cell.estate, 'city')
                                    and cell.estate.city == estate.city]

        estates_in_group_but_not_owned = [e for e in estates_in_same_group
                                            if e.owner != estate.owner]

        if estates_in_group_but_not_owned:
            estates_not_owned_names = [str(e) for e in estates_in_group_but_not_owned]
            self.send_private_message(player, Text.NOT_ALL_GROUP_IS_OWNED % ', '.join(estates_not_owned_names))
            return

        minimum_upgrade_level = min([e.upgrade_level for e in estates_in_same_group])

        if estate.upgrade_level > minimum_upgrade_level:
            self.send_private_message(player, Text.ESTATE_TOO_HIGH_LEVEL_COMPARED_TO_GROUP)
            return

        if estate.upgrade_price > player.money:
            self.tell_player_he_doesnt_have_enough_money(player, estate.upgrade_price)
            return

        estate.upgrade_level += 1
        self.output_message(Text.PLAYER_UPGRADES_ESTATE % (str(player), str(estate), estate.upgrade_level))

    def tell_player_he_doesnt_have_enough_money(self, player, required_amount):
        self.send_private_message(player, Text.NOT_ENOUGH_MONEY % (required_amount, player.money))

    def get_current_cell(self):
        """
            return the cell where the playing_player is
            return None in case of IndexError
        """
        try:
            return self.board.cells[self.playing_player.position - 1]
        except IndexError:
            return None

    def buy_estate_command(self, caller, args):
        if self.playing_player.nickname != caller:
            return

        cell = self.get_current_cell()

        if not isinstance(cell, Cell.EstateCell):
            self.output_message(Text.IS_NOT_ESTATE_CELL)
            return

        if cell.estate.owner:
            self.output_message(Text.ALREADY_OWNED_BY % str(cell.estate.owner))
            return

        if self.playing_player.money < cell.estate.sell_price:
            self.output_message(Text.NOT_ENOUGH_MONEY_TO_BUY_ESTATE)
            return

        cell.estate.owner = self.playing_player
        self.playing_player.money -= cell.estate.sell_price
        self.output_message(Text.SOMEONE_BUYS_ESTATE % (str(self.playing_player), str(cell.estate),
                                                        cell.estate.sell_price, self.playing_player.money))

    def start_game_command(self, caller, args):
        if self.game_state == GameState.NOT_STARTED:
            self.output_message(Text.START_GAME)
            self.game_state = GameState.ASKING_WHOS_PLAYING
            return

        if self.game_state == GameState.ASKING_WHOS_PLAYING:
            if len(self.players) == 0:
                self.output_message(Text.GAME_CANT_START_WITHOUT_PLAYER)
                return

            for player in self.players:
                player.money = Game.STARTING_MONEY

            self.output_message(Text.END_OF_REGISTRATION + ", ".join([p.nickname for p in self.players]))
            self.output_message(Text.GAME_STARTING)
            self.game_state = GameState.GAME_STARTED

            self.playing_player = self.players[-1]
            self.next_turn()

    def next_turn(self):
        if self.game_over:
            return

        index = self.players.index(self.playing_player) + 1

        if index >= len(self.players):
            index = 0

        self.playing_player = self.players[index]
        self.output_message(Text.IT_IS_SOMEONES_TURN % self.playing_player.nickname)
        self.playing_player.can_roll = True

    def extract_command_nickname(self, command):
        return command.split(": ")[0]

    def extract_command_args(self, command):
        if len(command.split(": ")) < 2:
            return []

        return [arg for arg in command.split(": ")[1].split(" ")[1:] if arg != '']

    def extract_command_name(self, command):
        if len(command.split(": ")) < 2:
            return None

        return command.split(": ")[1].split(" ")[0]

    def register_player_command(self, caller, args):
        if len(self.players) >= Game.MAX_PLAYER:
            self.output_message(Text.TOO_MUCH_PLAYER_REGISTERED)
            return

        if [p for p in self.players if p.nickname == caller]:
            return

        self.players.append(Player(caller))

    def test_roll_command(self, caller, args):
        if caller != self.playing_player.nickname:
            return

        roll_score = (0, 0)

        try:
            roll_score = (int(args[0]), int(args[1]))
        except Exception:
            print("ERROR during test_roll_command")
            return

        self.validate_roll(roll_score)

    def roll_command(self, caller, args):
        if caller != self.playing_player.nickname:
            return

        roll_score = (random.randint(1, 6), random.randint(1, 6))
        self.validate_roll(roll_score)

    def validate_roll(self, roll_score):
        if not self.playing_player.can_roll:
            self.output_message(Text.NO_ROLL_LEFT)
            return

        self.playing_player.can_roll = False
        self.output_message(Text.ROLL_RESULT % (self.playing_player.nickname, sum(roll_score), roll_score[0], roll_score[1]))

        if roll_score[0] == roll_score[1]:
            self.output_message(Text.PLAYER_SCORED_A_DOUBLE % (self.playing_player.nickname))
            self.playing_player.can_roll = True

            if self.playing_player.is_in_jail:
                self.output_message(Text.GOES_OUT_OF_JAIL_WITH_DOUBLE % str(self.playing_player))
                self.playing_player.is_in_jail = False

        if not self.playing_player.is_in_jail:
            self.playing_player.position += sum(roll_score)

            if self.playing_player.position > len(self.board.cells):
                self.playing_player.position -= len(self.board.cells)

            self.output_message(Text.NEW_POSITION % (self.playing_player.nickname, self.playing_player.position))

        else:
            self.playing_player.turns_to_wait_in_jail -= 1

            if self.playing_player.turns_to_wait_in_jail <= 0:
                self.output_message(Text.GOES_OUT_OF_JAIL_BY_WAITING % str(self.playing_player))
                self.playing_player.is_in_jail = False
            else:
                self.output_message(Text.MISSES_DOUBLE_TO_GET_OUT_OF_JAIL % (str(self.playing_player), self.playing_player.turns_to_wait_in_jail))


    def output_message(self, message):
        if(self.output_channel != None):
            self.output_channel(message)
        else:
            print("ERROR: No output message set")

    def give_money_to_player(self, player, amount, reason):
        player.money += amount

        if amount > 0:
            message = Text.RECEIVES_MONEY
        if amount < 0:
            message = Text.LOSES_MONEY

        self.output_message(message % (player.nickname, amount, reason, player.money))

    def player_gives_money_to_player(self, player_from, amount, player_to, reason):
        if player_from == None or player_to == None or player_from == player_to or amount <= 0:
            return

        player_from.money -= amount
        player_to.money += amount
        self.output_message(Text.PLAYER_GIVES_MONEY_TO_PLAYER % (str(player_from), amount,
                                                                 str(player_to), reason,
                                                                 player_from.money, player_to.money))

    def forward_player(self, player, amount):
        if self.playing_player != player or amount == 0:
            return

        player.position += amount
        if player.position >= len(self.board.cells):
            player.position -= len(self.board.cells)
            self.give_money_to_player(player, Game.SALARY, Text.SALARY)

        self.arrival_at_cell(player)

    def send_private_message(self, player, message):
        if self.private_output_channel != None:
            if isinstance(player, str):
                self.private_output_channel(player, message)
                return

            if isinstance(player, Player):
                self.private_output_channel(player.nickname, message)
                return

            print("Error for player type in send_private_message")
        print("ERROR: no private output message set")

    def get_player_from_nickname(self, nickname):
        try:
            return [p for p in self.players if p.nickname == nickname][0]
        except IndexError:
            print("Trying to get a player whose nickname is unknown")
            return None

    def get_player_cell(self, player):
        try:
            return self.board.cells[player.position - 1]
        except IndexError:
            print("ERROR: A player is not in a cell")
            return None

    def select_cell_command(self, caller, args):
        cell = None
        player = self.get_player_from_nickname(caller)

        if len(args) == 0:
            cell = self.get_player_cell(player)
        else:
            try:
                index = int(args[0])
                try:
                    cell = self.board.cells[index - 1]
                except IndexError:
                    print("IndexError in select_cell_command")
                    return
            except ValueError:
                print("Wrong argument in select_cell_command")
                return

        player.selected_cell = cell
        self.send_private_message(player, Text.CELL_SELECTED_INFOS % str(cell))

    def arrival_at_cell(self, player):
        cell = self.get_player_cell(player)

        self.output_message(Text.ARRIVAL_AT_CELL % (str(player), player.position, str(cell)))

        if isinstance(cell, Cell.FreeParkingCell):
            if self.board.bank_money == 0:
                self.output_message(Text.BUT_FREE_PARKING_EMPTY)
            else:
                self.give_money_to_player(player, self.board.bank_money, Text.FREE_PARKING_FOR % str(player))
                self.board.bank_money = 0

        if isinstance(cell, Cell.MoneyCell):
            self.give_money_to_player(player, cell.money_amount, str(cell))

        if isinstance(cell, Cell.EstateCell):
            estate = cell.estate
            if estate.owner != None:
                self.player_gives_money_to_player(player,
                                                  estate.get_current_rent(),
                                                  estate.owner,
                                                  Text.RENT_FOR % (estate.get_name_and_level()))

        if isinstance(cell, Cell.GoToJailCell):
            prison_cell = next(c for c in self.board.cells if isinstance(c, Cell.JailCell))
            self.output_message(Text.SOMEONE_GOES_IN_PRISON % str(player))
            player.position = self.board.cells.index(prison_cell) + 1
            player.is_in_jail = True
            player.turns_to_wait_in_jail = Game.MAX_TURNS_IN_JAIL

    def end_game(self):
        self.output_message(Text.GAME_OVER % (str(self.players[0]), str(self.players[0])))
        self.game_over = True
        self.game_over_callback()

    def dummy_game_over(self):
        self.output_message("No gameover callback specified")
        print("No gameover callback specified")
