__author__ = "Simon"


import test_helper
import monopoly.Cell as Cell
from monopoly.Game import Game
from monopoly.Command import Command
from monopoly.Text import Text
from monopoly.Player import Player
from monopoly.Game import GameState

import pytest
import re
from pprint import pprint

DEBUG = True

get_roll_score_from_message = test_helper.get_roll_score_from_message

message_received = ''
message_received_history = []
private_message_received = ''
private_message_received_history = []

def mock_output_channel(message):
    global message_received, message_received_history
    message_received = message
    message_received_history.append(message)

    if DEBUG:
        print("global : " + message)

def mock_private_output_channel(nickname, message):
    global private_message_received, private_message_received_history
    private_message_received = (nickname, message)
    private_message_received_history.append((nickname, message))

    if DEBUG:
        print("to %s : %s" % (nickname, message))

def clear_messages_received():
    global message_received, message_received_history, private_message_received, private_message_received_history
    message_received = ''
    message_received_history = []
    private_message_received = ('','')
    private_message_received_history = []

@pytest.fixture()
def game():
    clear_messages_received()
    game = Game()
    game.output_channel = mock_output_channel
    game.private_output_channel = mock_private_output_channel
    return game

@pytest.fixture()
def registered_game(game):
    test_register_players(game)
    clear_messages_received()
    return game 

@pytest.fixture()
def registered_game_with_owners(registered_game):
    player = registered_game.playing_player
    registered_game.board.cells[1].owner = player
    registered_game.board.cells[3].owner = player
    return registered_game

@pytest.fixture()
def jail_game(registered_game_with_owners):
    game = registered_game_with_owners
    player = registered_game_with_owners.playing_player
    player.position = 21
    game.forward_player(player, 10)
    clear_messages_received()
    return game

def test_set_output_channel(game):
    message_send = "onche onche"

    game.output_channel = mock_output_channel
    game.output_message(message_send)

    assert message_send == message_received

def test_extract_command_args(game):
    args = game.extract_command_args("bro: pouet lol fuck")

    assert args == ["lol", "fuck"]

def test_extract_command_args_with_no_args(game):
    assert game.extract_command_args("bro: pouet") == []
    assert game.extract_command_args("bro: pouet ") == []
    assert game.extract_command_args("bro: pouet     ") == []
    assert game.extract_command_args("bro:             ") == []

def test_extract_command_name(game):
    command_name = game.extract_command_name("bro: pouet lol fuck")

    assert "pouet" == command_name

def test_extract_command_nickname(game):
    nickname = game.extract_command_nickname("broski: pouet fuck")

    assert nickname == "broski"

def test_start_game(game):
    Command.START_GAME().as_caller('hurr').send(game)

    assert game.game_state == GameState.ASKING_WHOS_PLAYING
    assert Text.START_GAME == message_received

def test_register_players(game):
    test_start_game(game)

    Command.REGISTER_PLAYER().as_caller("broski").send(game)
    Command.REGISTER_PLAYER().as_caller("coincoin").send(game)
    Command.REGISTER_PLAYER().as_caller("GrosPoil").send(game)
    Command.REGISTER_PLAYER().as_caller("Salami").send(game)

    assert 4 == len(game.players)
    assert 1 == len([p for p in game.players if p.nickname == "coincoin"])
    assert 1 == len([p for p in game.players if p.nickname == "broski"])
    assert 1 == len([p for p in game.players if p.nickname == "GrosPoil"])
    assert 1 == len([p for p in game.players if p.nickname == "Salami"])

    Command.START_GAME().as_caller('hurr').send(game)

    assert Text.END_OF_REGISTRATION in message_received_history[-3]
    assert "coincoin" in message_received_history[-3]
    assert "broski" in message_received_history[-3]
    assert Text.GAME_STARTING == message_received_history[-2]
    assert game.game_state == GameState.GAME_STARTED

def test_register_same_player_twice(game):
    test_start_game(game)

    Command.REGISTER_PLAYER().as_caller("broski").send(game)
    assert len(game.players) == 1

    message_received_history = []
    Command.REGISTER_PLAYER().as_caller("broski").send(game)
    assert len(game.players) == 1
    assert len(message_received_history) == 0


def test_register_players_too_much_player(game):
    test_start_game(game)

    Command.REGISTER_PLAYER().as_caller("broski").send(game)
    Command.REGISTER_PLAYER().as_caller("broski2").send(game)
    Command.REGISTER_PLAYER().as_caller("broski3").send(game)
    Command.REGISTER_PLAYER().as_caller("broski4").send(game)
    Command.REGISTER_PLAYER().as_caller("broski5").send(game)
    Command.REGISTER_PLAYER().as_caller("broski6").send(game)
    Command.REGISTER_PLAYER().as_caller("broski7").send(game)
    Command.REGISTER_PLAYER().as_caller("broski8").send(game)
    Command.REGISTER_PLAYER().as_caller("broskiCACA").send(game)

    assert len(game.players) == 8
    assert message_received == Text.TOO_MUCH_PLAYER_REGISTERED

def test_game_initial_state(game):
    assert game.game_state == GameState.NOT_STARTED

def test_start_game_with_no_player(game):
    test_start_game(game)

    Command.START_GAME().as_caller('hurr').send(game)

    assert Text.GAME_CANT_START_WITHOUT_PLAYER == message_received

def test_roll_dice_not_your_turn(game):
    test_register_players(game)

    assert game.players

    player = next(p for p in game.players if p != game.playing_player)
    message_received_history = []
    Command.ROLL().as_caller(player.nickname).send(game)

    assert not message_received_history

def test_roll(game):
    test_register_players(game)
    clear_messages_received()

    assert game.players

    player = game.playing_player
    origin_position = player.position
    Command.ROLL().as_caller(player.nickname).send(game)

    if len(message_received_history) == 2:
        assert message_received_history[-2].startswith(Text.ROLL_RESULT.split("%i")[0] % player.nickname)
        roll_score = get_roll_score_from_message(message_received_history[-2])
        new_expected_position = origin_position + roll_score
        assert message_received_history[-1] == Text.NEW_POSITION % (player.nickname, new_expected_position)

    elif len(message_received_history) == 3:
        assert message_received_history[-3].startswith(Text.ROLL_RESULT.split("%i")[0] % player.nickname)
        roll_score = get_roll_score_from_message(message_received_history[-3])
        new_expected_position = origin_position + roll_score
        assert message_received_history[-1] == Text.NEW_POSITION % (player.nickname, new_expected_position)

def test_roll_at_end_of_board(game):
    test_register_players(game)
    roll_score = 0
    player = game.playing_player

    clear_messages_received()
    player.position = 40
    Command.TEST_ROLL().with_args([1, 2]).as_caller(player).send(game)
    if len(message_received_history) == 2:
        roll_score = get_roll_score_from_message(message_received_history[-2])
        assert player.position == get_roll_score_from_message(message_received_history[-2])
    elif len(message_received_history) == 3:
        roll_score = get_roll_score_from_message(message_received_history[-3])
        assert player.position == get_roll_score_from_message(message_received_history[-3])

    clear_messages_received()
    Command.ROLL().as_caller(player).send(game)
    if len(message_received_history) == 2:
        roll_score += get_roll_score_from_message(message_received_history[-2])
    elif len(message_received_history) == 3:
        roll_score += get_roll_score_from_message(message_received_history[-3])

    clear_messages_received()
    Command.ROLL().as_caller(player).send(game)
    if len(message_received_history) == 2:
        roll_score += get_roll_score_from_message(message_received_history[-2])
    elif len(message_received_history) == 3:
        roll_score += get_roll_score_from_message(message_received_history[-3])

    assert player.position == 40 + roll_score - len(game.board.cells)

def test_give_money_to_player(game):
    test_register_players(game)

    player = game.playing_player
    player.money = 10
    game.give_money_to_player(player, 100, 'il fait caca')

    assert player.money == 110
    assert message_received == Text.RECEIVES_MONEY % (player.nickname, 100, 'il fait caca', player.money)

    player.money = 10
    game.give_money_to_player(player, -100, 'Chaussette au fromage')

    assert player.money == -90
    assert message_received == Text.LOSES_MONEY % (player.nickname, -100, 'Chaussette au fromage', player.money)

def test_salary_when_passing_start_cell(registered_game):
    player = registered_game.playing_player

    player.position = 39
    player.money = 200
    registered_game.forward_player(player, 4)

    assert player.position == 3
    assert player.money == 200 + Game.SALARY

def test_double_salary_when_landing_on_start_cell(registered_game):
    player = registered_game.playing_player

    player.position = 39
    player.money = 300
    registered_game.forward_player(player, 2)
    Command.ROLL().as_caller(player).send(registered_game)

    assert player.money == 300 + Game.SALARY * 2

def test_free_parking_cell(registered_game):
    player = registered_game.playing_player

    player.position = 11
    player.money = 10
    registered_game.board.bank_money = 5000
    registered_game.forward_player(player, 10)

    assert Text.FREE_PARKING_FOR % str(player) in message_received
    assert player.money == 10 + 5000

    registered_game.forward_player(player, -2)
    registered_game.forward_player(player, 2)

    assert message_received == Text.BUT_FREE_PARKING_EMPTY
    assert player.money == 10 + 5000

def test_buy_estate_not_the_one_playing(registered_game):
    player = registered_game.players[-1]

    message_received = ''
    Command.BUY_ESTATE().as_caller(player).send(registered_game)
    assert message_received == ''

def test_buy_estate_not_enough_money(registered_game):
    player = registered_game.playing_player

    player.money = 0
    player.position = 2
    Command.BUY_ESTATE().as_caller(player).send(registered_game)
    assert message_received == Text.NOT_ENOUGH_MONEY_TO_BUY_ESTATE
    assert player.money == 0

def test_buy_estate_not_estate_cell(registered_game):
    global message_received
    player = registered_game.playing_player

    player.position = 1
    Command.BUY_ESTATE().as_caller(player).send(registered_game)
    assert message_received == Text.IS_NOT_ESTATE_CELL

    message_received = ''
    player.position = 3
    Command.BUY_ESTATE().as_caller(player).send(registered_game)
    assert message_received == Text.IS_NOT_ESTATE_CELL

    message_received = ''
    player.position = 11
    Command.BUY_ESTATE().as_caller(player).send(registered_game)
    assert message_received == Text.IS_NOT_ESTATE_CELL

def test_buy_estate_already_owned(registered_game):
    player = registered_game.playing_player
    owner = registered_game.players[-1]
    registered_game.board.cells[3].estate.owner = owner

    player.position = 4
    Command.BUY_ESTATE().as_caller(player).send(registered_game)

    assert registered_game.board.cells[3].estate.owner == owner
    assert message_received == Text.ALREADY_OWNED_BY % str(owner)

def test_buy_estate(registered_game):
    player = registered_game.playing_player

    player.position = 4
    player.money = 1000
    Command.BUY_ESTATE().as_caller(player).send(registered_game)

    estate_bought = registered_game.board.cells[3].estate
    assert message_received == (Text.SOMEONE_BUYS_ESTATE % (str(player), str(estate_bought),
                                                            estate_bought.sell_price, player.money))
    assert estate_bought.owner == player

def test_arrival_at_owned_estate(registered_game):
    player = registered_game.playing_player
    owner = registered_game.players[-2]

    player.position = 1
    player.money = 1000
    owned_estate = registered_game.board.cells[3].estate
    owned_estate.owner = owner

    registered_game.forward_player(player, 3)
    assert player.money == 1000 - owned_estate.get_current_rent()
    assert str(player) in message_received
    assert str(owner) in message_received
    assert repr(owned_estate.get_current_rent()) in message_received
    assert owned_estate.name in message_received

def test_send_private_message(game):
    global private_message_received, private_message_received_history
    clear_messages_received()

    game.send_private_message(Player("coincoin"), "caca suce")
    assert private_message_received == ("coincoin", "caca suce")
    assert ("coincoin", "caca suce") in private_message_received_history

    game.send_private_message(Player("FESSE"), "123")
    assert private_message_received == ("FESSE", "123")
    assert ("FESSE", "123") in private_message_received_history

    assert len(private_message_received_history) == 2

def test_get_player_from_nickname(game):
    Command.REGISTER_PLAYER().as_caller("Sauce").send(game)
    Command.REGISTER_PLAYER().as_caller("Etronaute").send(game)
    Command.REGISTER_PLAYER().as_caller("123").send(game)

    assert isinstance(game.get_player_from_nickname("Sauce"), Player)
    assert isinstance(game.get_player_from_nickname("Etronaute"), Player)
    assert isinstance(game.get_player_from_nickname("123"), Player)

    assert game.get_player_from_nickname("Sauce").nickname == "Sauce" 
    assert game.get_player_from_nickname("Etronaute").nickname == "Etronaute" 
    assert game.get_player_from_nickname("123").nickname == "123" 

    assert game.get_player_from_nickname("CAckA") == None
    assert game.get_player_from_nickname("GUICK") == None
    assert game.get_player_from_nickname("qsqsdsqd") == None

def test_select_cell(registered_game):
    clear_messages_received()
    player = registered_game.playing_player

    cell_that_should_be_selected = registered_game.board.cells[1]
    Command.SELECT_CELL().as_caller(player.nickname).with_args(['2']).send(registered_game)

    assert player.selected_cell == cell_that_should_be_selected
    assert private_message_received[0] == player.nickname
    assert cell_that_should_be_selected.estate.name in private_message_received[1]
    assert repr(cell_that_should_be_selected.estate.upgrade_level) in private_message_received[1]

def test_select_cell_no_argument(registered_game):
    clear_messages_received()
    player = registered_game.playing_player

    player.position = 10
    cell_that_should_be_selected = registered_game.board.cells[9]
    Command.SELECT_CELL().as_caller(player).send(registered_game)

    assert player.selected_cell == cell_that_should_be_selected
    assert private_message_received[0] == player.nickname
    assert cell_that_should_be_selected.estate.name in private_message_received[1]
    assert repr(cell_that_should_be_selected.estate.upgrade_level) in private_message_received[1]

def test_upgrade_estate_not_estate_cell(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player

    Command.SELECT_CELL().as_caller(player).with_args(1).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == player.nickname
    assert private_message_received[1] == Text.NOT_AN_ESTATE_CELL % str(game.board.cells[0])

def test_upgrade_estate_already_max_level(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    game.board.cells[1].estate.upgrade_level = 5

    Command.SELECT_CELL().as_caller(player).with_args(2).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == player.nickname
    assert private_message_received[1] == Text.ALREADY_MAX_LEVEL % str(game.board.cells[1].estate)

def test_upgrade_estate_no_more_hotel(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    game.board.cells[1].estate.upgrade_level = 4
    game.board.hotels_available = 0

    Command.SELECT_CELL().as_caller(player).with_args(2).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == player.nickname
    assert private_message_received[1] == Text.NO_MORE_HOTEL

def test_upgrade_estate_no_more_house(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    game.board.houses_available = 0  

    Command.SELECT_CELL().as_caller(player).with_args(2).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == player.nickname
    assert private_message_received[1] == Text.NO_MORE_HOUSE

def test_upgrade_estate_not_own_every_land(registered_game):
    game = registered_game
    player = game.playing_player

    cell = game.board.cells[1]
    cell.estate.owner = player
    missing_cell = game.board.cells[3]
    clear_messages_received()

    Command.SELECT_CELL().as_caller(player).with_args(2).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == game.playing_player.nickname
    assert private_message_received[1] == Text.NOT_ALL_GROUP_IS_OWNED % str(missing_cell.estate)
    assert cell.estate.upgrade_level == 0

    cell = game.board.cells[6]
    cell.estate.owner = player
    missing_cells = [game.board.cells[8], game.board.cells[9]]
    clear_messages_received()

    Command.SELECT_CELL().as_caller(player).with_args(7).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == game.playing_player.nickname
    assert private_message_received[1] == Text.NOT_ALL_GROUP_IS_OWNED % ', '.join([str(c.estate) for c in missing_cells])
    assert cell.estate.upgrade_level == 0

def test_upgrade_estate_with_gap(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    clear_messages_received()
    cell1 = game.board.cells[1]
    cell2 = game.board.cells[3]
    clear_messages_received()

    cell1.estate.upgrade_level = 1
    cell2.estate.upgrade_level = 0

    Command.SELECT_CELL().as_caller(player).with_args(2).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == game.playing_player.nickname
    assert private_message_received[1] == Text.ESTATE_TOO_HIGH_LEVEL_COMPARED_TO_GROUP
    assert cell1.estate.upgrade_level == 1

def test_upgrade_estate_not_enough_money(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    clear_messages_received()

    player.money = 10

    Command.SELECT_CELL().as_caller(player).with_args(2).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == ""
    assert private_message_received[0] == game.playing_player.nickname
    assert private_message_received[1] == Text.NOT_ENOUGH_MONEY % (game.board.cells[1].estate.upgrade_price, player.money)

def test_upgrade_estate(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    clear_messages_received()

    game.board.cells[6].estate.owner = player
    game.board.cells[8].estate.owner = player
    cell = game.board.cells[9]
    estate = cell.estate
    estate.owner = player

    Command.SELECT_CELL().as_caller(player).with_args(10).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == (Text.PLAYER_UPGRADES_ESTATE % (player.nickname, str(estate), 1))
    assert estate.upgrade_level == 1


    clear_messages_received()

    game.board.cells[16].estate.owner = player
    game.board.cells[16].estate.upgrade_level = 2
    game.board.cells[18].estate.owner = player
    game.board.cells[18].estate.upgrade_level = 2
    game.board.cells[19].estate.owner = player
    game.board.cells[19].estate.upgrade_level = 2
    cell = game.board.cells[18]
    estate = cell.estate
    estate.owner = player
    player.money = 1000

    Command.SELECT_CELL().as_caller(player).with_args(19).send(game)
    Command.UPGRADE_ESTATE().as_caller(player).send(game)

    assert message_received == (Text.PLAYER_UPGRADES_ESTATE % (player.nickname, str(estate), 3))
    assert estate.upgrade_level == 3

def test_goto_jail(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player
    clear_messages_received()

    player.position = 21
    game.forward_player(player, 10)

    assert message_received == Text.SOMEONE_GOES_IN_PRISON % str(player)
    assert player.position == 11
    assert player.is_in_jail == True

def test_roll_double(registered_game):
    game = registered_game
    player = game.playing_player
    origin_position = player.position

    Command.TEST_ROLL().with_args([1, 1]).as_caller(player).send(game)

    assert message_received_history[-3].startswith(Text.ROLL_RESULT.split("%i")[0] % player.nickname)

    roll_score = get_roll_score_from_message(message_received_history[-3])
    new_expected_position = origin_position + roll_score

    assert Text.NEW_POSITION % (player.nickname, new_expected_position) in message_received_history
    assert Text.PLAYER_SCORED_A_DOUBLE % (player.nickname) in message_received_history

def test_roll_already_rolled(registered_game):
    game = registered_game
    player = game.playing_player
    clear_messages_received()

    Command.TEST_ROLL().with_args([1, 2]).as_caller(player).send(game)
    Command.TEST_ROLL().with_args([2, 3]).as_caller(player).send(game)

    assert message_received_history[-1] == Text.NO_ROLL_LEFT

def test_get_out_of_jail_by_dice(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player

    player.position = 21
    game.forward_player(player, 10)

    Command.TEST_ROLL().as_caller(player).with_args([2, 2]).send(game)

    assert Text.NEW_POSITION % (player.nickname, player.position) in message_received_history
    assert Text.PLAYER_SCORED_A_DOUBLE % (player.nickname) in message_received_history
    assert Text.GOES_OUT_OF_JAIL_WITH_DOUBLE % str(player) in message_received_history
    assert game.playing_player.can_roll
    assert not game.playing_player.is_in_jail

def test_get_out_of_jail_by_paying_not_enough_money(jail_game):
    game = jail_game
    player = game.playing_player
    player.money = Game.JAIL_TOLL - 10

    Command.PAY_FOR_JAIL().as_caller(player).send(game)

    assert private_message_received[0] == str(player)
    assert private_message_received[1] == Text.NOT_ENOUGH_MONEY % (Game.JAIL_TOLL, player.money)

def test_get_out_of_jail_by_paying(jail_game):
    game = jail_game
    player = game.playing_player
    player.money = Game.JAIL_TOLL + 100

    Command.PAY_FOR_JAIL().as_caller(player).send(game)

    assert Text.GOES_OUT_OF_JAIL_BY_PAYING % str(player) in message_received_history
    assert player.money == 100
    assert not player.is_in_jail

def test_next_turn(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player

    Command.TEST_ROLL().as_caller(player).with_args([1, 2]).send(game)
    Command.END_MY_TURN().as_caller(player).send(game)

    assert player != game.playing_player
    assert message_received == Text.IT_IS_SOMEONES_TURN % game.playing_player

def test_next_turn_without_rolling(registered_game_with_owners):
    game = registered_game_with_owners
    player = game.playing_player

    Command.END_MY_TURN().as_caller(player).send(game)

    assert player == game.playing_player
    assert private_message_received_history[-1][1] == Text.MUST_ROLL_BEFORE_END_TURN

def test_get_out_of_jail_by_waiting(game):
    playerA = Player('plox')
    playerB = Player('poil')

    Command.START_GAME().as_caller(playerA).send(game)
    Command.REGISTER_PLAYER().as_caller(playerA).send(game)
    Command.REGISTER_PLAYER().as_caller(playerB).send(game)
    Command.START_GAME().as_caller(playerA).send(game)

    playerA = game.players[0]
    playerB = game.players[1]

    Command.END_MY_TURN().as_caller(playerA).send(game)
    Command.END_MY_TURN().as_caller(playerA).send(game)
    Command.END_MY_TURN().as_caller(playerA).send(game)
    Command.END_MY_TURN().as_caller(playerA).send(game)
    Command.TEST_ROLL().as_caller(playerA).with_args([1, 2]).send(game)
    playerA.position = 30
    game.forward_player(playerA, 1)
    Command.END_MY_TURN().as_caller(playerA).send(game)

    Command.TEST_ROLL().as_caller(playerB).with_args([1, 2]).send(game)
    Command.END_MY_TURN().as_caller(playerB).send(game)

    # 1st turn
    Command.TEST_ROLL().as_caller(playerA).with_args([1, 2]).send(game)
    Command.END_MY_TURN().as_caller(playerA).send(game)

    Command.TEST_ROLL().as_caller(playerB).with_args([1, 2]).send(game)
    Command.END_MY_TURN().as_caller(playerB).send(game)

    # 2nd turn
    Command.TEST_ROLL().as_caller(playerA).with_args([1, 2]).send(game)
    Command.END_MY_TURN().as_caller(playerA).send(game)

    Command.TEST_ROLL().as_caller(playerB).with_args([1, 2]).send(game)
    Command.END_MY_TURN().as_caller(playerB).send(game)

    # 3rd turn
    Command.TEST_ROLL().as_caller(playerA).with_args([1, 2]).send(game)

    assert message_received == Text.GOES_OUT_OF_JAIL_BY_WAITING % str(playerA)
    assert not game.playing_player.is_in_jail
    assert game.playing_player.turns_to_wait_in_jail == 0
