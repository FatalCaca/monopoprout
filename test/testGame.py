__author__ = 'Simon'


import unittest
from Game import Game, GameState
from Text import Text
from Command import Command
from C import C
import re


class GameTest(unittest.TestCase):
    def setUp(self):
        self.message_received = None
        self.game = Game()
        self.message_received = ""
        self.message_received_history = []
        self.game.output_channel = self.mock_output_channel

    def tearDown(self):
        self.game = None

    def mock_output_channel(self, message):
        self.message_received = message
        self.message_received_history.append(message)

    def test_set_output_channel(self):
        message_send = "onche onche"

        self.game.output_channel = self.mock_output_channel
        self.game.output_message(message_send)

        self.assertEqual(message_send, self.message_received, "Message sent should be the same as the one received")

    def test_extract_command_args(self):
        args = self.game.extract_command_args("bro: pouet lol fuck")
        
        self.assertEqual(args, ["lol", "fuck"])

    def test_extract_command_args_with_no_args(self):
        args = self.game.extract_command_args("bro: pouet")
        
        self.assertEqual(args, [])

    def test_extract_command_name(self):
        command_name = self.game.extract_command_name("bro: pouet lol fuck")
        
        self.assertEqual("pouet", command_name)

    def test_extract_command_nickname(self):
        nickname = self.game.extract_command_nickname("broski: pouet fuck")
        
        self.assertEqual(nickname, "broski")

    def test_start_game(self):
        self.game.send_command("hurr: " + Command.START_GAME)

        self.assertEqual(Text.START_GAME, self.message_received, "Starting game message should be sent")
        self.assertEqual(self.game.game_state, GameState.ASKING_WHOS_PLAYING, "The game state should be updated")

    def test_register_players(self):
        self.test_start_game()

        self.game.send_command("broski: " + Command.REGISTER_PLAYER)
        self.game.send_command("coincoin: " + Command.REGISTER_PLAYER)

        self.assertEqual(2, len(self.game.players), "New players should be added")
        self.assertEqual(1, len([p for p in self.game.players if p.nickname == "coincoin"]), "coincoin should be in the game")
        self.assertEqual(1, len([p for p in self.game.players if p.nickname == "broski"]), "broski should be in the game")

        self.game.send_command("hurr: " + Command.START_GAME)

        self.assertTrue(Text.END_OF_REGISTRATION in self.message_received_history[-3], "End of registration message should be displayed")
        self.assertTrue("coincoin" in self.message_received_history[-3], "coincoin should be annouced as playing")
        self.assertTrue("broski" in self.message_received_history[-3], "broski should be annouced as playing")
        self.assertEqual(Text.GAME_STARTING, self.message_received_history[-2], "Start of game message should be displayed")
        self.assertEqual(self.game.game_state, GameState.GAME_STARTED, "The game state should be updated")

    def test_game_initial_state(self):
        self.assertEqual(self.game.game_state, GameState.NOT_STARTED, "The game should be at the NOT_STARTED state at the begining")

    def test_start_game_with_no_player(self):
        self.test_start_game()

        self.game.send_command("hurr: " + Command.START_GAME)

        self.assertEqual(Text.GAME_CANT_START_WITHOUT_PLAYER, self.message_received, "A message saying that the game can't start without player should be displayed")

    def test_roll_dice_not_your_turn(self):
        self.test_register_players()

        if not self.game.players:
            self.fail("There are no player registered")

        player = next(p for p in self.game.players if p != self.game.playing_player)

        self.message_received_history = []
        C(Command.ROLL).as_caller(player.nickname).send(self.game)

        self.assertTrue(not self.message_received_history, "Nothing should happen if you try to roll while it's not your turn")

    def test_roll(self):
        self.test_register_players()

        if not self.game.players:
            self.fail("There are no player registered") 

        player = self.game.playing_player
        origin_position = player.position

        C(Command.ROLL).as_caller(player.nickname).send(self.game)

        self.assertTrue(self.message_received_history[-2].startswith(Text.ROLL_RESULT.split("&2")[0].replace("&1", player.nickname)),
            "A message stating that someone has rolled the dice (with result) should be displayed")

        roll_score = int(re.search("\d+", self.message_received_history[-2]).group(0))
        new_expected_position = origin_position + roll_score

        self.assertEqual(self.message_received_history[-1],
                         Text.NEW_POSITION.replace("&1", player.nickname).replace("&2", repr(new_expected_position)),
                         "A message with the new position should be shown")