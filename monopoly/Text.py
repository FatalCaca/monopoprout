__author__ = "Simon"


class Text:
    START_GAME = "kikijou ? (IPlay)"
    END_OF_REGISTRATION = "Fin des inscriptions. Joueurs inscrits : "
    GAME_STARTING = "Debut de la partie !"
    IT_IS_SOMEONES_TURN = "C'est a %s de jouer"
    GAME_CANT_START_WITHOUT_PLAYER = "La partie ne peut pas commencer, il faut au moins un joueur d'inscrit !"
    ROLL_RESULT = "%s lance les des. Il fait un total de %i ! (%i et %i)"
    NEW_POSITION = "%s est maintenant a la case %i"
    TOO_MUCH_PLAYER_REGISTERED = "La partie est pleine !"
    RECEIVES_MONEY = "%s recoit %i (%s). Reste %i"
    LOSES_MONEY = "%s paie %i (%s). Reste %i"
    SALARY = "Salaire"
    COSTS = "(coute %i)"

    # Estate
    OWNED_BY = '(Possede par %s)'
    AT_LEVEL = '[Upgrade %i]'
    AT = 'a'
    RENT_AT = '[Loyer a %i]'
    SOMEONE_BUYS_ESTATE = '%s achete %s pour %i ! (reste %i)'
    RENT_FOR = "Loyer pour %s"
    NOT_AN_ESTATE_CELL = "%s n'est pas une case propriete"
    ALREADY_MAX_LEVEL = "%s est deja upgrade au maximum"

    ARRIVAL_AT_CELL = '%s arrive a la case %i (%s)'

    # Cells
    LUCK_CELL = "Case chance"
    COMMUNITY_CHEST_CELL = "Case caisse de communaute"
    FREE_PARKING_CELL = "Case maxiloot"
    JAIL_CELL = "Case prison"
    GO_TO_JAIL_CELL = "Case va prison connard'"
    FREE_PARKING_FOR = "Maxiloot pour %s !"
    BUT_FREE_PARKING_EMPTY = "Malheureusemtn c'est vide pd"

    # Actions
    NOT_ENOUGH_MONEY_TO_BUY_ESTATE = "Pas assez d'argent pour acheter !"
    IS_NOT_ESTATE_CELL = "Ce n'est pas une case achetable lole"
    ALREADY_OWNED_BY = "Cette propriete est deja possedee par %s !"
    PLAYER_GIVES_MONEY_TO_PLAYER = "%s donne %i a %s (%s). Reste %i et %i"
    CELL_SELECTED_INFOS = "Selection de %s"
    UPGRADED_ESTATE = "%s upgrade %s !"
    NO_MORE_HOTEL = "Il ne reste plus d'hotel disponible"
    NO_MORE_HOUSE = "Il ne reste plus de maison disponible"
    NOT_ALL_GROUP_IS_OWNED = "Vous ne possedez pas tous les terrains du groupe. Il vous manque : %s"
    ESTATE_TOO_HIGH_LEVEL_COMPARED_TO_GROUP = "Cette propriete a un niveau trop eleve par rapport au reste du groupe"
    NOT_ENOUGH_MONEY = "Pas assez d'argent (il faut %i, vous avez %i)"
    PLAYER_UPGRADES_ESTATE = "%s upgrade %s au niveau %i !"
    SOMEONE_GOES_IN_PRISON = "%s tombe à la case prison ! Bye bye PD"
    PLAYER_SCORED_A_DOUBLE = "%s a fait un double ! Il peut relancer les des !"
    NO_ROLL_LEFT = "Vous ne pouvez plus lancer les des pour ce tour !"
    GOES_OUT_OF_JAIL_WITH_DOUBLE = "%s sort de prison grace a son double"
    GOES_OUT_OF_JAIL_BY_PAYING = "%s sort de prison en payant"
    GOES_OUT_OF_JAIL_BY_WAITING = "%s sort de prison en arrivant à la limite de tour"
    MUST_ROLL_BEFORE_END_TURN = "Il faut roll avant de pouvoir terminer son tour"
    MISSES_DOUBLE_TO_GET_OUT_OF_JAIL = "%s rate son double, pas de sortie de prison ! (encore %i tours en prison)"
    PLAYER_GOES_BANKRUPT = "%s n'a plus de sousous et est elimine !"
    GAME_OVER = "La partie est terminee ! C est %s qui gagne ! BRAVAU %s"
