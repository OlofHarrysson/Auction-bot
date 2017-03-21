import json


class GameObject:
    def __init__(self, j_str='{}'):
        """
        Creates new GameObject.
        :param j_str: The object can be created from json string.
        """
        self._elements_dict = json.loads(j_str)

    def possible_keys(self):
        """
        Return list of object's keys.
        :return: list of possible keys.
        """
        return list(self._elements_dict.keys())

    def get(self, key):
        """
        Getter for game object. Raise a KeyError exception for unknown key.
        :param key: variable key
        :return: value of the variable
        """
        if key not in self.possible_keys():
            raise KeyError("Error: key is not defined in the GameObject")
        return self._elements_dict.get(key, None)

    def set(self, key, value):
        """
        Setter for game object. Raise a KeyError exception for unknown key.
        :param key: variable key
        :param value: variable value
        """
        if key not in self.possible_keys():
            raise KeyError("Error: key is not defined in the GameObject")
        self._elements_dict[key] = value

    def to_json_str(self):
        """
        Serialize object to json string.
        :return: json string
        """
        return json.dumps(self._elements_dict)
