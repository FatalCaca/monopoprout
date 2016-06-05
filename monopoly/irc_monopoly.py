__author__ = 'simon.ballu@gmail.com'


from monopoly.Game import Game
from monopoly.IrcConnector import IrcConnector
from monopoly.IrcStub import IrcStub

server = "127.0.0.1"
port = 7777
nickname = "monopoprout"

#irc = IrcConnector()
irc = IrcStub()

game = Game()
game.output_channel = irc.send_message
game.private_output_channel = irc.send_private_message

irc.connect(server, port, nickname)


