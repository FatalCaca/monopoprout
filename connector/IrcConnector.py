__author__ = "simon.ballu@gmail.com"


import socket
import threading
import re


class IrcConnector:
    PRIVMSG_SEPARATOR = 'PRIVMSG #%s :'

    def __init__(self, server, port=6667, channel='', nickname='branlix'):
        self.server = server
        self.port = port
        self.channel= channel
        self.nickname = nickname
        self.irc_socket = None
        self.find_sender_regex = re.compile(':(.*)!')

        self.on_message_received = None
        self.on_private_message_received = None

    def send_string(self, message):
        print('Sending:%s' % message)
        self.irc_socket.send(bytes(message, 'UTF-8'))

    def connect(self):
        print("Connecting to %s:%i %s as %s" % (self.server, self.port, self.channel, self.nickname))

        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.connect((self.server, self.port))

        irc_listener = IrcListener(self.irc_socket, self)
        irc_listener.start()

        self.send_string('NICK %s \r\n' % (self.nickname))
        self.send_string('USER %s %s %s :%s Script\r\n' % (self.nickname, self.nickname, self.nickname, self.nickname))

    def send_message(self, message):
        self.send_string('PRIVMSG %s :%s' % (self.channel, message))

    def send_private_message(self, message, target):
        self.send_string('PRIVMSG %s :%s' % (target, message))

    def handle_ping(self, param):
        self.send_string('PONG :%s\r\n' % param)

    def handle_message(self, message):
        message_elements = message.split(':')
        message_meta = ''
        message_content = ''

        if len(message_elements) >= 2:
            message_meta = message_elements[1]

        if len(message_elements) >= 3:
            message_content = message_elements[2]

        if 'welcome' in message_content.lower():
            self.on_connection_accepted()

        if message_meta:
            meta_elements = message_meta.split(' ')
            sender = ''
            operation = ''
            target = ''

            if meta_elements:
                sender = meta_elements[0].split('!')[0]

            if len(meta_elements) >= 2:
                operation = meta_elements[1]

            if len(meta_elements) >= 3:
                target = meta_elements[2]

            if operation == 'PRIVMSG':
                if target == self.channel:
                    try:
                        self.on_message_received(sender, message_content)
                    except TypeError as e:
                        print(e)
                        print('Error: on_message_received not set')

                if target == self.nickname:
                    try:
                        self.on_private_message_received(sender, message_content)
                    except TypeError:
                        print('Error: on_private_message_received not set')

    def on_connection_accepted(self):
        self.send_string('JOIN %s\r\n' % (self.channel))


class IrcListener(threading.Thread):
    def __init__(self, irc_socket, irc_connector):
        threading.Thread.__init__(self)
        self.irc_socket = irc_socket
        self.irc_connector = irc_connector

    def run(self):
        while True:
            irc_messages = self.irc_socket.recv(4096).split(bytes('\n', 'UTF-8'))

            for irc_message in irc_messages:
                irc_message = irc_message.decode('UTF-8')
                if not irc_message:
                    continue

                print("FROM SERVER:" + irc_message)
                irc_command = irc_message.split(':')[0].lower().strip()
                if not irc_command:
                    self.irc_connector.handle_message(irc_message)
                    continue

                try:
                    command_handler = getattr(self.irc_connector, 'handle_%s' % irc_command)
                    command_handler(irc_message.split(':')[1])
                except AttributeError:
                    print('Error: received unknown command: [%s]' % irc_command)
                except IndexError:
                    print('Error: received command with no parameter [%s]' % irc_command)


