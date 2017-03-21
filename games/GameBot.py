from games.ApiClient import ApiClient


class GameBot:
    def __init__(self, h_id, strategy):
        """
        Creates new GameBot instance.
        :param h_id: id of homework (can be found in website url)
        :param strategy: Instance of Strategy class.
        """
        self.h_id = h_id
        self.session_id = "0"
        self.last_response = None
        self._api_client = ApiClient()
        self.strategy = strategy
        self.game_running = True

    def _initiate(self, game_object):
        """
        Initiate communication with server.
        :param game_object: Default instance of GameObject
        """
        self.last_response = self._api_client.communicate_api(self.h_id, game_object=game_object)

    def _send_data(self, game_object):
        """
        Sends data stored in GameObject to the server.
        :param game_object: Instance of GameObject
        :return: GameObject instance as a response from server.
        """
        self.last_response = self._api_client.communicate_api(self.h_id, game_object=game_object)

    def _end_game(self):
        """
        Indicates end of the game. Stops while loop in run method.
        """
        self.game_running = False

    def _run(self, game_object):
        """
        Main loop of the game.
        :param game_object: Default gameObject for the problem.
        """
        self._initiate(game_object)
        while self.game_running:
            game_object = self.last_response
            if not game_object.get('game_active'):
                self._end_game()
                continue
            game_object = self._game_loop()
            self._send_data(game_object)
        print("Game ended after %d rounds.\nYour score: %d\nOpponents' score: %s" % (
            game_object.get('round'), game_object.get('score')[0], str(game_object.get('score')[1:])))

    def start(self, game_object):
        """
        Starts the game loop.
        :param game_object: Default gameObject for the problem.
        """
        self._run(game_object)

    def _game_loop(self):
        return self.strategy.move(self.last_response)
