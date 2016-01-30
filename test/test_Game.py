__author__ = "Simon"


from monopoly.Game import Game
from monopoly.Command import Command
from monopoly.Text import Text
from monopoly.Game import GameState
import pytest
import re
import test_helper

get_roll_score_from_message = test_helper.get_roll_score_from_message

message_received = ''
message_received_history = []

def mock_output_channel(message):
    global message_received, message_received_history
    message_received = message
    message_received_history.append(message)

@pytest.fixture()
def game():
    global message_received
    global message_received_history
    message_received = ''
    message_received_history = []
    game = Game()
    game.output_channel = mock_output_channel
    return game

@pytest.fixture()
def registered_game(game):
    test_register_players(game)
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
    args = game.extract_command_args("bro: pouet")
    
    assert args == []

def test_extract_command_name(game):
    command_name = game.extract_command_name("bro: pouet lol fuck")
    
    assert "pouet" == command_name

def test_extract_command_nickname(game):
    nickname = game.extract_command_nickname("broski: pouet fuck")
    
    assert nickname == "broski"

def test_start_game(game):
    Command.START_GAME.as_caller('hurr').send(game)

    assert game.game_state == GameState.ASKING_WHOS_PLAYING
    assert Text.START_GAME == message_received

def test_register_players(game):
    test_start_game(game)

    Command.REGISTER_PLAYER.as_caller("broski").send(game)
    Command.REGISTER_PLAYER.as_caller("coincoin").send(game)

    assert 2 == len(game.players)
    assert 1 == len([p for p in game.players if p.nickname == "coincoin"])
    assert 1 == len([p for p in game.players if p.nickname == "broski"])

    Command.START_GAME.as_caller('hurr').send(game)

    assert Text.END_OF_REGISTRATION in message_received_history[-3]
    assert "coincoin" in message_received_history[-3]
    assert "broski" in message_received_history[-3]
    assert Text.GAME_STARTING == message_received_history[-2]
    assert game.game_state == GameState.GAME_STARTED

def test_register_same_player_twice(game):
    test_start_game(game)

    Command.REGISTER_PLAYER.as_caller("broski").send(game)
    assert len(game.players) == 1

    message_received_history = []
    Command.REGISTER_PLAYER.as_caller("broski").send(game)
    assert len(game.players) == 1
    assert len(message_received_history) == 0


def test_register_players_too_much_player(game):
    test_start_game(game)

    Command.REGISTER_PLAYER.as_caller("broski").send(game)
    Command.REGISTER_PLAYER.as_caller("broski2").send(game)
    Command.REGISTER_PLAYER.as_caller("broski3").send(game)
    Command.REGISTER_PLAYER.as_caller("broski4").send(game)
    Command.REGISTER_PLAYER.as_caller("broski5").send(game)
    Command.REGISTER_PLAYER.as_caller("broski6").send(game)
    Command.REGISTER_PLAYER.as_caller("broski7").send(game)
    Command.REGISTER_PLAYER.as_caller("broski8").send(game)
    Command.REGISTER_PLAYER.as_caller("broskiCACA").send(game)

    assert len(game.players) == 8
    assert message_received == Text.TOO_MUCH_PLAYER_REGISTERED

def test_game_initial_state(game):
    assert game.game_state == GameState.NOT_STARTED

def test_start_game_with_no_player(game):
    test_start_game(game)

    Command.START_GAME.as_caller('hurr').send(game)

    assert Text.GAME_CANT_START_WITHOUT_PLAYER == message_received

def test_roll_dice_not_your_turn(game):
    test_register_players(game)

    assert game.players

    player = next(p for p in game.players if p != game.playing_player)
    message_received_history = []
    Command.ROLL.as_caller(player.nickname).send(game)

    assert not message_received_history

def test_roll(game):
    test_register_players(game)

    assert game.players

    player = game.playing_player
    origin_position = player.position
    Command.ROLL.as_caller(player.nickname).send(game)

    assert message_received_history[-2].startswith(Text.ROLL_RESULT.split("&2")[0].replace("&1", player.nickname))

    roll_score = get_roll_score_from_message(message_received_history[-2])
    new_expected_position = origin_position + roll_score

    assert message_received_history[-1] == Text.NEW_POSITION.replace("&1", player.nickname).replace("&2", repr(new_expected_position))

def test_roll_at_end_of_board(game):
    test_register_players(game)

    player = game.playing_player
    player.position = 36
    Command.ROLL.as_caller(player).send(game)

    assert player.position == get_roll_score_from_message(message_received_history[-2])

    player.position = 35
    Command.ROLL.as_caller(player).send(game)
    roll_score = get_roll_score_from_message(message_received_history[-2])
    Command.ROLL.as_caller(player).send(game)
    roll_score += get_roll_score_from_message(message_received_history[-2])

    assert player.position == 35 + roll_score - len(game.cells)

def test_give_money_to_player(game):
    test_register_players(game)

    player = game.playing_player
    player.money = 10
    game.give_money_to_player(player, 100, 'il fait caca')

    assert player.money == 110
    assert message_received == (Text.RECEIVES_MONEY.replace('&1', player.nickname)
                                                  .replace('&2', repr(100))
                                                  .replace('&3', 'il fait caca'))

    player.money = 10
    game.give_money_to_player(player, -100, 'Chaussette au fromage')

    assert player.money == -90
    assert message_received == (Text.LOSES_MONEY.replace('&1', player.nickname)
                                                .replace('&2', repr(-100))
                                                .replace('&3', 'Chaussette au fromage'))

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
    Command.ROLL.as_caller(player).send(registered_game)

    assert player.money == 300 + Game.SALARY * 2