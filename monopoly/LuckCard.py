__author__ = 'Simon'


class LuckCard:
    def __init__(self, text, money_variation=0, position_variation=0, new_position=0):
        self.text = text
        self.money_variation = money_variation
        self.position_variation = position_variation
        self.new_position = new_position

    def pick_effect(self, game, player):
        game.give_money_to_player(player, self.money_variation)
        game.move_player(player, self.position_variation)
        game.set_player_position(player, self.new_position)


class LuckCardFactory:
    def get_default_luck_cards():
        cards = [
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
        ]

        jail_card = LuckCard("prout")

        return cards

    def get_default_community_chest_cards():
        cards = [
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
        ]

        jail_card = LuckCard("prout")

        return cards