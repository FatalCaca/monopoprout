__author__ = "Simon"


class Text:
    START_GAME = "kikijou ? (IPlay)"
    END_OF_REGISTRATION = "Fin des inscriptions. Joueurs inscrits : "
    GAME_STARTING = "Début de la partie !"
    IT_IS_SOMEONES_TURN = "C'est à &1 de jouer"
    GAME_CANT_START_WITHOUT_PLAYER = "La partie ne peut pas commencer, il faut au moins un joueur d'inscrit !"
    ROLL_RESULT = "&1 lance les dés. Il fait un &2 !"
    NEW_POSITION = "&1 est maintenant à la case &2"
    TOO_MUCH_PLAYER_REGISTERED = "La partie est pleine !"
    RECEIVES_MONEY = "&1 reçoit &2 (&3)"
    LOSES_MONEY = "&2 perd &2 (&3)"
    SALARY = "Salaire"
    
    # Estate
    OWNED_BY = '(Possédé par &1)'
    AT_LEVEL = '[Upgrade &1]'
    AT = 'à'
    RENT_AT = '[Loyer à &1]'
    SOMEONE_BUYS_ESTATE = '&1 achète &2 pour &3 ! (reste &4)'

    ARRIVAL_AT_CELL = '&1 arrive à la case &2 (&3)'

    # Cells
    LUCK_CELL = "Case chance"
    COMMUNITY_CHEST_CELL = "Case caisse de communauté"
    FREE_PARKING_CELL = "Case maxiloot"
    JAIL_CELL = "Case prison"
    GO_TO_JAIL_CELL = "Case 'vas en prison connard'"
    FREE_PARKING_FOR = "Maxiloot pour &1 !"
    BUT_FREE_PARKING_EMPTY = "Malheureusemtn c'est vide pd"

    # Actions
    NOT_ENOUGH_MONEY_TO_BUY_ESTATE = "Pas assez d'argent pour acheter !"
    IS_NOT_ESTATE_CELL = "Ce n'est pas une case achetable lole"
    ALREADY_OWNED_BY = "Cette propriété est déjà possédée par &1 !"