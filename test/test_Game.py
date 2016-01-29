__author__ = "Simon"


from monopoly.Game import Game
from monopoly.Command import Command
from monopoly.C import C
from monopoly.Text import Text
from monopoly.Game import GameState
import pytest
import re

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
    game.send_command("hurr: " + Command.START_GAME)

    assert game.game_state == GameState.ASKING_WHOS_PLAYING
    assert Text.START_GAME == message_received

def test_register_players(game):
    test_start_game(game)

    game.send_command("broski: " + Command.REGISTER_PLAYER)
    game.send_command("coincoin: " + Command.REGISTER_PLAYER)

    assert 2 == len(game.players)
    assert 1 == len([p for p in game.players if p.nickname == "coincoin"])
    assert 1 == len([p for p in game.players if p.nickname == "broski"])

    game.send_command("hurr: " + Command.START_GAME)

    assert Text.END_OF_REGISTRATION in message_received_history[-3]
    assert "coincoin" in message_received_history[-3]
    assert "broski" in message_received_history[-3]
    assert Text.GAME_STARTING == message_received_history[-2]
    assert game.game_state == GameState.GAME_STARTED

def test_game_initial_state(game):
    assert game.game_state == GameState.NOT_STARTED

def test_start_game_with_no_player(game):
    test_start_game(game)

    game.send_command("hurr: " + Command.START_GAME)

    assert Text.GAME_CANT_START_WITHOUT_PLAYER == message_received

def test_roll_dice_not_your_turn(game):
    test_register_players(game)

    assert game.players

    player = next(p for p in game.players if p != game.playing_player)

    message_received_history = []
    C(Command.ROLL).as_caller(player.nickname).send(game)

    assert not message_received_history

def test_roll(game):
    test_register_players(game)

    assert game.players

    player = game.playing_player
    origin_position = player.position

    C(Command.ROLL).as_caller(player.nickname).send(game)

    assert message_received_history[-2].startswith(Text.ROLL_RESULT.split("&2")[0].replace("&1", player.nickname))

    roll_score = int(re.search("\d+", message_received_history[-2]).group(0))
    new_expected_position = origin_position + roll_score

    assert message_received_history[-1] == Text.NEW_POSITION.replace("&1", player.nickname).replace("&2", repr(new_expected_position))