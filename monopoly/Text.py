__author__ = "Simon"


class Text:
    START_GAME = "kikijou ? (IPlay)"
    END_OF_REGISTRATION = "Fin des inscriptions. Joueurs inscrits : "
    GAME_STARTING = "Debut de la partie !"
    IT_IS_SOMEONES_TURN = "C'est a &1 de jouer"
    GAME_CANT_START_WITHOUT_PLAYER = "La partie ne peut pas commencer, il faut au moins un joueur d'inscrit !"
    ROLL_RESULT = "&1 lance les des. Il fait un &2 !"
    NEW_POSITION = "&1 est maintenant a la case &2"
    TOO_MUCH_PLAYER_REGISTERED = "La partie est pleine !"
    RECEIVES_MONEY = "&1 recoit &2 (&3)"
    LOSES_MONEY = "&2 paie &2 (&3)"
    SALARY = "Salaire"
    COSTS = "(coute &1)"
    
    # Estate
    OWNED_BY = '(Possede par &1)'
    AT_LEVEL = '[Upgrade &1]'
    AT = 'a'
    RENT_AT = '[Loyer a &1]'
    SOMEONE_BUYS_ESTATE = '&1 achete &2 pour &3 ! (reste &4)'
    RENT_FOR = "Loyer pour &1"
    NOT_AN_ESTATE_CELL = "&1 n'est pas une case propriete"
    ALREADY_MAX_LEVEL = "&1 est deja upgrade au maximum"

    ARRIVAL_AT_CELL = '&1 arrive a la case &2 (&3)'

    # Cells
    LUCK_CELL = "Case chance"
    COMMUNITY_CHEST_CELL = "Case caisse de communaute"
    FREE_PARKING_CELL = "Case maxiloot"
    JAIL_CELL = "Case prison"
    GO_TO_JAIL_CELL = "Case 'vas en prison connard'"
    FREE_PARKING_FOR = "Maxiloot pour &1 !"
    BUT_FREE_PARKING_EMPTY = "Malheureusemtn c'est vide pd"

    # Actions
    NOT_ENOUGH_MONEY_TO_BUY_ESTATE = "Pas assez d'argent pour acheter !"
    IS_NOT_ESTATE_CELL = "Ce n'est pas une case achetable lole"
    ALREADY_OWNED_BY = "Cette propriete est deja possedee par &1 !"
    PLAYER_GIVES_MONEY_TO_PLAYER = "&1 donne &2 a &3 (&4). Reste &5 et &6"
    CELL_SELECTED_INFOS = "Selection de &1"
    UPGRADED_ESTATE = "&1 upgrade &2 !"
    NO_MORE_HOTEL = "Il ne reste plus d'hotel disponible"
    NO_MORE_HOUSE = "Il ne reste plus de maison disponible"
    NOT_ALL_GROUP_IS_OWNED = "Vous ne possedez pas tous les terrains du groupe. Il vous manque : &1"
    ESTATE_TOO_HIGH_LEVEL_COMPARED_TO_GROUP = "Cette propriete a un niveau trop eleve par rapport au reste du groupe"
    NOT_ENOUGH_MONEY = "Pas assez d'argent (il faut &1, vous avez &2)"
    PLAYER_UPGRADES_ESTATE = "&1 upgrade &2 au niveau &3 !"
    SOMEONE_GOES_IN_PRISON = "&1 tombe à la case prison ! Bye bye PD"