import json
import math
import os

class Medium:
    def __init__(self, medium_type):
        self.medium_type = medium_type
        self.data = self._load_data()

        self.density = self.data['density']
        self.drag_coefficient = self.data['drag_coefficient']

    def _load_data(self):
        """
        Loads the medium data from a JSON file or dictionary.
        :return: Parsed data as a Python dictionary
        """
        mediums = {
            "unc_air": "data/air_data/unc_air.json",
            "unc_tissue": "data/tissue_data/unc_tissue.json",
            "class_1_armour": "data/armour_data/class_1_armour.json",
        }
        self.data_path = mediums[self.medium_type]
        with open(self.data_path, 'r') as file:
            return json.load(file)

    def to_dict(self):
        """
        Returns medium properties as a dictionary.
        """
        return {
            "type": self.medium_type,
            "density": self.density,
            "drag_coefficient": self.drag_coefficient,
        }
