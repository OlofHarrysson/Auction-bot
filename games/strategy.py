class Strategy:
    def __init__(self, name):
        """
        Creates new strategy instance
        :param name: name of your strategy
        """
        self.name = name

    def move(self, game_object):
        """
        Method generates a move which reacts on opponents' moves stored in game_object.
        :param game_object: GameObject instance includes all relevant information about game state.
        :return: game_object with upgraded value 'last_move'
        """
        raise NotImplementedError("Strategy.move(): is not overridden")

    def first_move(self, game_object):
        """
        Returns a move in the beginning of the game.
        :param game_object: game_object that should be updated
        :return:  game_object with upgraded value of 'last_move'
        """
        raise NotImplementedError("Strategy.first_move(): is not overridden")

    def __str__(self):
        return str(self.name)
