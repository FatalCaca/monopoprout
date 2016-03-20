__author__ = 'simon.ballu@gmail.com'


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


class JailCard(LuckCard):
    pass


class LuckCardFactory:
    def get_default_luck_cards():
        cards = [
            LuckCard("Kevin vous invite pour un kebab ! RDV au kebZ de St Berth (36)", new_position=36),
            LuckCard("Allez à la gare de lyon", new_position=32),
            LuckCard("Allez en prison, pas de case départ etc.", new_position=32),
            LuckCard("Vous avez gagné un concours de transformisme, gagnez 100", money_variation=100),
            LuckCard("Croquettes pour chat : 20", money_variation=-20),
            LuckCard("Allez à la case départ", new_position=1),
            LuckCard("Votre bar à pute vous rapporte. Touchez 150", money_variation=150),
            LuckCard("Reparation de mobylette. 150", money_variation=-150),
            LuckCard("Amende pour vol de bebe", money_variation=-15),
            LuckCard("Vous trouvez un billet de 50 en sortant du mcdo", money_variation=50),
            LuckCard("RDV à ...", new_position=12),
            LuckCard("RDV à ...", new_position=22),
            LuckCard("Reculez de trois cases", position_variation=-3),
            LuckCard("Reparations de toutes vos upgrades. 25 par upgrade et 100 par lvl5", money_variation=1000),
            JailCard("Carte de liberation de prison"),
            LuckCard("Reparations blablacul, 40 par lvl et 115 par lvl5", money_variation=1200),
        ]

        return cards

    def get_default_community_chest_cards():
        cards = [
            LuckCard("Amende pour exces de vitesse sur mobylette. Payez 10", money_variation=10),
            LuckCard("C'est votre anniversaire, chaque joueur vous verse 10.", money_variation=20),
            LuckCard("RDV au premier terrain du jeu", new_position=2),
            LuckCard("Votre ferme de lama vous rapporte. Touchez 100", money_variation=100),
            LuckCard("Votre investissement dans les armes vous rapporte. Touchez 200", money_variation=200),
            LuckCard("Allez en prison, tralala", new_position=32),
            LuckCard("Vous vous achetez un nouveau pc de keke. Payez 50", money_variation=50),
            LuckCard("Votre bar a pute vous rapporte. Touchez 100", money_variation=100),
            LuckCard("Fracture du penis. Payez l'hopital 100", money_variation=-100),
            LuckCard("Votre vente de shit vous rapporte. Touchez 10", money_variation=10),
            LuckCard("Vous revendez votre chihuahua sur ebay. Touchez 10", money_variation=10),
            LuckCard("Votre nouvelle erotique se vend plutot bien. Touchez 20", money_variation=20),
            LuckCard("Vous vous faites allonger le penis. Payez 50", money_variation=50),
            LuckCard("Vous vous prostituez. Touchez 50", money_variation=50),
            LuckCard("Votre livret A vous rapporte. Touchez 25", money_variation=25),
            LuckCard("Placez vous sur la case depart.", new_position=1),
            #LuckCard("", new_position=1),
        ]

        return cards
