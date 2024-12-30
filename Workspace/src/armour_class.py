import json
import math
import os

class Armour:
    def __init__(self, armour_type):
        """
        Initialize the Armour object.
        :param armour_type: The type of armour (e.g., "NIJ_Level_2", "NIJ_Level_4").
        """
        self.armour_type = armour_type
        self.data = self._load_data()

        self.material = self.data['material']
        self.thickness = self.data['thickness_meters']
        self.energy_absorption = self.data['energy_absorption_joules_per_m2']
        self.density = self.data.get('density_g_per_cm3', None)
        self.test_standard = self.data['test_standard']

    def _load_data(self):
        """
        Loads the armour data from a JSON file or dictionary.
        :return: Parsed data as a Python dictionary
        """
        armours = {
            "class_2": "data/armour_data/class_2_armour.json",
        }
        self.data_path = armours[self.armour_type]
        with open(self.data_path, 'r') as file:
            return json.load(file)

    def to_dict(self):
        """
        Returns armour properties as a dictionary.
        """
        return {
            "type": self.armour_type,
            "material": self.material,
            "thickness": self.thickness,
            "energy_absorption": self.energy_absorption,
            "density": self.density,
            "test_standard": self.test_standard,
        }