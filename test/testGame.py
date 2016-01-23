__author__ = 'Simon'


import unittest
from Game import Game


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game = None

    def test_extract_command_args(self):
        args = self.game.extract_command_args("bro: pouet lol fuck")
        self.assertEqual(args, ["pouet", "lol", "fuck"])

    def test_extract_commander_nickname(self):
        nickname = self.game.extract_command_nickname("broski: pouet fuck")
        self.assertEqual(nickname, "broski")

    def test_set_output_channel(self):
        message_send = "onche onche"
        message_received = None

        def mock_output_channel(message):
            nonlocal message_received
            message_received = message_send

        self.game.output_channel = mock_output_channel
        self.game.output_message(message_send)

        self.assertEqual(message_send, message_received)