__author__  = 'Simon'


import socket
import random
import threading
from ping_pong import PingPong

random.seed()

channel = "#monosourcil"
nickname = "Chibronski"

probabilite_adverbe = 50

noms = [
		'Joseph',
		'Johnny',
		'Sadam Hussein',
		'Didier Super',
		'Le caca volant',
		'Pikachu',
		'Harry Potter',
		'Adolf',
		'Un goral',
		'Chibronski',
		'Le caca sur la table',
		'Jesus',
		'Potofion',
		'Mister T',
		'Jacky Chan',
		'Le melon jaune']

verbes = ['découvre',
		  's\'étonne de',
		  'soulève',
		  'pleure',
		  'imite avec son ventre',
		  'fait comme si il parlait comme',
		  'saute sur',
		  'débranche',
		  'suce',
		  'chie',
		  'n\'en peut plus de',
		  'voudrait plus de',
		  'regarde fixement',
		  'se touche en regardant',
		  'tourne le dos à'
		  'retourne',
		  'décapite',
		  'renifle',
		  'aime',
		  'fait dada sur',
		  'fait un câlin à',
		  'fait un câlin à',
		  'fait l\'hélicobite avec',
		  'tate les parties de',
		  'falsifie',
		  'interpelle',
		  'développe',
		  'sodomise']

adverbes = ['vachement',
			'amoureusement',
			'tendrement',
			'salement',
			'amicalement',
			'fichtrement',
			]

cods = ['le parquet',
		'un chaton',
		'la brosse à dents',
		'le serveur IRC',
		'le PHP',
		'une bouse de vache',
		'la table',
		'la pesée',
		'la coulante',
		'les m&m\'s',
		'Joseph',
		'Johnny',
		'Sadam Hussein',
		'l\'airbus A380',
		'Christophe Germain',
		'Bill Gates',
		'Didier Super',
		'Le caca volant',
		'Pikachu',
		'Harry Potter',
		'Adolf',
		'Chibronski',
		'Le caca sur la table',
		'Jesus',
		'Potofion',
		'Le melon jaune',
		'les fesses']

ponctuations = ['.',
				'...',
				'?',
				'!']

hello_said = False

def ping():
	irc_socket.send(bytes("PONG :PONG", 'UTF-8'))

def send_simple_message(msg):
	send_msg(channel, msg)

def send_msg(chan, msg):
	irc_socket.send(bytes("PRIVMSG " + chan + " :" + msg + '\r\n', 'UTF-8'))

def hello(new_nick):
	irc_socket.send(bytes("PRIVMSG " + channel + " :ATTENTION, IL Y A DU CACA SUR LA TABLE !!!\r\n", 'UTF-8'))

irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc_socket.connect(('kdvr.fr', 6667))
pouet = 'NICK ' + nickname + '\r\n'
irc_socket.send(bytes(pouet, 'UTF-8'))
pouet = 'USER ' + nickname + ' ' + nickname + ' ' + nickname + ' :' + nickname + ' Script\r\n'
irc_socket.send(bytes(pouet, 'UTF-8'))
pouet = 'JOIN ' + channel + '\r\n'
irc_socket.send(bytes(pouet, 'UTF-8'))

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
				adverbes[random.randint(0, len(adverbes) - 1)] if random.randint(0, 100) <= probabilite_adverbe else '',
				cods[random.randint(0, len(cods) - 1)],
				ponctuations[random.randint(0, len(ponctuations) - 1)]
			)))

	if irc_message.find(bytes(nickname, 'UTF-8')) != -1\
		and irc_message.find(bytes('ajoute', 'UTF-8')) != -1\
		and irc_message.find(bytes('noms')) != -1:

		send_msg(channel, 'sayé c ajouter hihihi')

	if irc_message.find(bytes("PING :", 'UTF-8')) != -1:
		ping()

	if irc_message.find(bytes('start ping-pong', 'UTF-8')) != -1:
		pp = PingPong(send_simple_message)
		t = threading.Thread(target=pp.run)
		t.daemon = True
		t.start()

