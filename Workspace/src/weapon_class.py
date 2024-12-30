import json
import math
import os

class Weapon:
    """
    Represents a firearm with specific properties such as barrel length and muzzle velocity.
    """

    def __init__(self, weapon_type):
        self.weapon_type = weapon_type
        self.data = self._load_data()

        self.barrel_length = self.data['barrel_length']
        self.muzzle_velocity = self.data['muzzle_velocity']

    def _load_data(self):
        """
        Loads weapon data from a JSON file or dictionary.
        """
        weapons = {
            "glock_17": "data/weapon_data/glock_17.json",
        }
        self.data_path = weapons[self.weapon_type]
        with open(self.data_path, 'r') as file:
            return json.load(file)

    def to_dict(self):
        """
        Returns weapon properties as a dictionary.
        """
        return {
            "type": self.weapon_type,
            "barrel_length": self.barrel_length,
            "muzzle_velocity": self.muzzle_velocity,
        }
