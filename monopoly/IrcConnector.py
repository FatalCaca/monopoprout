__author__ = 'simon.ballu@gmail.com'


import socket


class IrcConnector():
    def __constructor__(self):
        self.irc_socket = None

    def connect(self, server, port, nickname):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.connect((server, port))
        pouet = 'NICK ' + nickname + '\r\n'
        self.irc_socket.send(bytes(pouet, 'UTF-8'))
        pouet = 'USER ' + nickname + ' ' + nickname + ' ' + nickname + ' :' + nickname + ' Script\r\n'
        self.irc_socket.send(bytes(pouet, 'UTF-8'))

    def join_channel(self, channel_name):
        pouet = 'JOIN ' + channel_name + '\r\n'
        self.irc_socket.send(bytes(pouet, 'UTF-8'))

    def send_message(self, message):
        pass

    def send_private_message(self, target, message):
        pass

def ping():
	irc_socket.send(bytes("PONG :PONG", 'UTF-8'))

def send_simple_message(msg):
	send_msg(channel, msg)

def send_msg(chan, msg):
	irc_socket.send(bytes("PRIVMSG " + chan + " :" + msg + '\r\n', 'UTF-8'))

def hello(new_nick):
	irc_socket.send(bytes("PRIVMSG " + channel + " :ATTENTION, IL Y A DU CACA SUR LA TABLE !!!\r\n", 'UTF-8'))


pp = None
t = None

while True:
	irc_message = irc_socket.recv(2048)
	irc_message = irc_message.strip(bytes('\n\r', 'UTF-8'))
	print(irc_message)

	if pp != None:
		pp.give_message(repr(irc_message).split(':')[2].replace('\'', ''))

	if not hello_said:
		send_msg(channel, "Bonjour les amis, je suis CHRIBRONSKIU")
		hello_said = True

	if irc_message.find(bytes('stop ping-pong', 'UTF-8')) != -1:
		pp.stop()
		t = None
		pp = None

	if irc_message.find(bytes(":Hello " + nickname, 'UTF-8')) != -1:
		print('bonjour')
		hello('qsd')

	if irc_message.find(bytes(nickname, 'UTF-8')) != -1:
		send_msg(channel,
			' '.join((
				noms[random.randint(0, len(noms) - 1)],
				verbes[random.randint(0, len(verbes) - 1)],
