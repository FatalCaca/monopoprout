__author__ = 'simon.ballu@gmail.com'


from monopoly.Game import Game

irc  = IrcInterface()
irc.connect(server, port, nickname)

game = Game()
game.output_channel = irc.send_message
game.private_output_channel = irc.send_private_message

