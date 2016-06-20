__author__ = "simon.ballu@gmail.com"


import sys
from connector.IrcConnector import IrcConnector


irc_connector = None
server = 'kdvr.fr'
port = 6667
nickname = 'Monopoprout'
channel = '#monosourcil'


if '-c' in sys.argv:
    try:
        channel = sys.argv[sys.argv.index('-c') + 1]
    except:
        print("Error with channel (-c) argument")

if '-p' in sys.argv:
    try:
        port = sys.argv[sys.argv.index('-p') + 1]
    except:
        print("Error with port (-p) argument")

if '-n' in sys.argv:
    try:
        nickname = sys.argv[sys.argv.index('-n') + 1]
    except:
        print("Error with nickname (-n) argument")

if '-s' in sys.argv:
    try:
        server = sys.argv[sys.argv.index('-s') + 1]
    except:
        print("Error with server (-s) argument")


irc_connector = IrcConnector(server, port, channel, nickname)

def repeat_message(sender, message):
    global irc_connector
    irc_connector.send_message(message)

def repeat_private_message(sender, message):
    global irc_connector
    irc_connector.send_private_message(message, sender)

irc_connector.on_message_received = repeat_message
irc_connector.on_private_message_received = repeat_private_message
irc_connector.connect()
