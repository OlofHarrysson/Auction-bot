import configparser

import requests

from .GameObject import GameObject

VERSION = '0.1.1'


class ApiClient:
    def __init__(self, config_file="config.ini"):
        """
        Creates ApiClient object.
        :param config_file: path to config.ini file
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        self.server_url = config["server"]["server_url"]
        self.username = config["user"]["username"]
        self.password = config["user"]["password"]
        self.session_id = "0"

    def communicate_api(self, h_id, game_object=GameObject()):
        """
        Sends game data to API and returns new game data.
        The method automatically fills all needed credentials configured by the config file.
        The method also automatically converts GameObject instance to json string and back.
        :param h_id: id of homework
        :param game_object: instance of GameObject
        :return: instance of GameObject as a response from server
        """
        r = requests.post(
            self.server_url + "/homework/%s/api?user=%s&password=%s&version=%s" %
                (str(h_id), self.username, self.password, VERSION),
                json={"session_id": self.session_id, "game_object": game_object.to_json_str()})
        if r.status_code == 500:
            print("Unknown error. Contact us on email (tomas.sabata@fit.cvut.cz). Add your script as attachment")
            exit()
        if r.status_code != 201:
            print("Error: %d, %s" % (r.status_code, r.json()['error']))
            exit()
        else:
            self.session_id = r.json()['session_id']
            return GameObject(r.json()['game_object'])
