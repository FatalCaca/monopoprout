__author__ = 'simon.ballu@gmail.com'


class IrcStub():
    GAME_MASTER_PREFIX = 'Game master'

    def __constructor__(self):
        pass

    def send_message(self):
        pass

    def send_private_message(self, target, message):
        print('%s [to %s]: %s' % (IrcStub.GAME_MASTER_PREFIX, target, message))

    def input_channel(self, emmitter, message):
        pass
