__author__ = 'Simon'

from monopoly.Text import Text


class Estate:
    def __init__(self, **kwds):
        self.city = ''
        self.name = ''
        self.owner = None
        self.upgrade_level = 0
        self.upgrade_price = 0
        self.sell_price = 0
        self.mortgage_price = 0
        self.rents = [0, 0, 0, 0, 0, 0]
        self.__dict__.update(kwds)

    def get_current_rent(self):
        return self.rents[self.upgrade_level]

    def __str__(self):
        return ' '.join((self.name, Text.AT, self.city))

    def get_full_description(self):
        return ' '.join((self.name, Text.AT, self.city, '[lvl', self.upgrade_level, 'rent', repr(self.get_current_rent))) + ']'

    def get_name_and_level(self):
        return str(self) + '[' + repr(self.upgrade_level) + ']'

class StationEstate(Estate):
    def __init__(self, **kwds):
        self.name = ''
        self.owner = None
        self.sell_price = 200
        self.mortgage_price = 100
        self.rents = [25, 50, 100, 200]
        self.city = ''
        self.upgrade_level = 0
        self.__dict__.update(kwds)


class DiceEstate(Estate):
    def __init__(self, **kwds):
        self.name = ''
        self.owner = None
        self.sell_price = 150
        self.mortgage_price = 75
        self.rents = [4, 10]
        self.city = ''
        self.upgrade_level = 0
        self.__dict__.update(kwds)


class EstateFactory:
    def get_default_estates():
        return [
        Estate(city='Laignelet',
               name='Station d\'epuration',
               rents=[2, 10, 30, 90, 160, 250],
               sell_price=60,
               upgrade_price=50,
               mortgage_price=30),
        Estate(city='Laignelet',
               name='Boulangerie',
               rents=[4, 20, 60, 180, 320, 450],
               sell_price=60,
               upgrade_price=50,
               mortgage_price=30),


        StationEstate(name='Gare Caca'),


        Estate(city='Laval',
               name='Le Quick',
               rents=[6, 30, 90, 270, 400, 550],
               sell_price=100,
               upgrade_price=50,
               mortgage_price=50),
        Estate(city='Laval',
               name='L\'arabe a cote de la gare',
               rents=[6, 30, 90, 270, 400, 550],
               sell_price=100,
               upgrade_price=50,
               mortgage_price=30),
        Estate(city='Laval',
               name='La pute sur la route de Loiron',
               rents=[8, 40, 100, 300, 450, 600],
               sell_price=120,
               upgrade_price=50,
               mortgage_price=60),


        Estate(city='Fougeres',
               name='Le Quick',
               rents=[10, 50, 150, 450, 625, 750],
               sell_price=140,
               upgrade_price=100,
               mortgage_price=70),

        DiceEstate(name='Eboueurs Bibi'),

        Estate(city='Fougeres',
               name='L\'arabe a cote de la gare',
               rents=[10, 50, 150, 450, 625, 750],
               sell_price=140,
               upgrade_price=100,
               mortgage_price=70),
        Estate(city='Fougeres',
               name='La pute sur la route de Loiron',
               rents=[12, 60, 180, 500, 700, 900],
               sell_price=160,
               upgrade_price=100,
               mortgage_price=80),


        StationEstate(name='Gare Prout'),


        Estate(city='Rennes',
               name='Le Quick',
               rents=[14, 70, 200, 550, 750, 950],
               sell_price=180,
               upgrade_price=100,
               mortgage_price=90),
        Estate(city='Rennes',
               name='L\'arabe a cote de la gare',
               rents=[14, 70, 200, 550, 750, 950],
               sell_price=180,
               upgrade_price=100,
               mortgage_price=90),
        Estate(city='Rennes',
               name='La pute sur la route de Loiron',
               rents=[12, 60, 180, 500, 700, 900],
               sell_price=200,
               upgrade_price=100,
               mortgage_price=100),


        Estate(city='Moncul',
               name='Le Quick',
               rents=[18, 90, 250, 700, 875, 1050],
               sell_price=220,
               upgrade_price=150,
               mortgage_price=110),
        Estate(city='Moncul',
               name='L\'arabe a cote de la gare',
               rents=[18, 90, 250, 700, 875, 1050],
               sell_price=220,
               upgrade_price=150,
               mortgage_price=110),
        Estate(city='Moncul',
               name='La pute sur la route de Loiron',
               rents=[20, 100, 300, 750, 925, 1100],
               sell_price=240,
               upgrade_price=150,
               mortgage_price=120),


        StationEstate(name='Gare Anus'),


        Estate(city='Chibroland',
               name='Le Quick',
               rents=[22, 110, 330, 800, 975, 1150],
               sell_price=260,
               upgrade_price=150,
               mortgage_price=130),
        Estate(city='Chibroland',
               name='L\'arabe a cote de la gare',
               rents=[22, 110, 330, 800, 975, 1150],
               sell_price=260,
               upgrade_price=150,
               mortgage_price=130),

        DiceEstate(name='Fosses Septiques Cacatron'),

        Estate(city='Chibroland',
               name='La pute sur la route de Loiron',
               rents=[24, 120, 360, 850, 1025, 1200],
               sell_price=280,
               upgrade_price=150,
               mortgage_price=150),


        Estate(city='Paris',
               name='Le Quick',
               rents=[26, 130, 390, 900, 1100, 1275],
               sell_price=100,
               upgrade_price=300,
               mortgage_price=150),
        Estate(city='Paris',
               name='L\'arabe a cote de la gare',
               rents=[26, 130, 390, 900, 1100, 1275],
               sell_price=100,
               upgrade_price=300,
               mortgage_price=150),
        Estate(city='Paris',
               name='La pute sur la route de Loiron',
               rents=[28, 150, 450, 1000, 1200, 1400],
               sell_price=100,
               upgrade_price=320,
               mortgage_price=160),


        StationEstate(name='Gare Fion'),


        Estate(city='St Berthevin',
               name='Univers Noz',
               rents=[35, 175, 500, 1100, 1300, 1500],
               sell_price=350,
               upgrade_price=200,
               mortgage_price=175),
        Estate(city='St Berthevin',
               name='Le kebab',
               rents=[50, 200, 600, 1400, 1700, 2000],
               sell_price=400,
               upgrade_price=200,
               mortgage_price=200),
        ]
