import json
import math
import os

class Bullet:
    """
    Represents a bullet with various properties and allows for ballistic calculations.
    """

    def __init__(self, bullet_type):
        """
        Initializes the Bullet object.
        :param bullet_type: Type of the bullet (e.g., '9mm')
        """
        self.bullet_type = bullet_type
        self.data = self._load_data()

        self.mass = self.data['bullet']['core_material']['mass']['value']  # grams
        self.caliber = self.data['bullet']['caliber']['value']  # mm
        self.core_density = self.data['bullet']['core_material']['density']['value']
        self.ballistic_coefficient = self.data['bullet']['ballistic_coefficient']
        self.muzzle_velocity = self.data['muzzle_velocity']['value']  # m/s

        self.shape = self.data['bullet']['shape']
        self.jacket_material = self.data['bullet']['jacket']['material']

    def _load_data(self):
        """
        Loads the bullet data from a JSON file or dictionary.
        :return: Parsed data as a Python dictionary
        """
        bullets = {
            "9mm": "data/bullet_data/9mm.json",
        }
        self.data_path = bullets[self.bullet_type]
        with open(self.data_path, 'r') as file:
            return json.load(file)

    def kinetic_energy(self, velocity=None):
        """
        Calculates the kinetic energy of the bullet.
        If velocity is not given, uses the muzzle_velocity.
        :return: Kinetic energy in Joules
        """
        mass_kg = self.mass / 1000
        if velocity is None:
            velocity = self.muzzle_velocity
        return 0.5 * mass_kg * velocity ** 2

    def cross_sectional_area(self):
        """
        Calculates the cross-sectional area of the bullet.
        :return: Cross-sectional area in square meters
        """
        radius_m = (self.caliber / 1000) / 2
        return math.pi * radius_m ** 2

    def to_dict(self):
        """
        Returns bullet properties as a dictionary.
        """
        return {
            "type": self.bullet_type,
            "mass": self.mass,
            "caliber": self.caliber,
            "muzzle_velocity": self.muzzle_velocity,
            "shape": self.shape,
            "jacket_material": self.jacket_material,
        }
