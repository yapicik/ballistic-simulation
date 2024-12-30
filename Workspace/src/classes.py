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


class Simulation:
    def __init__(self, weapon, bullet):
        self.weapon = weapon
        self.bullet = bullet
        self.air_result = None
        self.armour_result = None
        self.tissue_result = None

    def simulate(self, medium, distance_meters, initial_velocity=None, initial_position=0, initial_vertical_velocity=0, initial_vertical_position=0, initial_time=0):
        """
        Verilen koşullar altında merminin hareketini simüle eder.
        """
        velocity = initial_velocity if initial_velocity is not None else self.weapon.muzzle_velocity
        position = initial_position
        vertical_velocity = initial_vertical_velocity
        vertical_position = initial_vertical_position
        time = initial_time
        time_step = 0.0000001

        density = medium.density
        drag_coefficient = medium.drag_coefficient
        cross_sectional_area = self.bullet.cross_sectional_area()

        gravity = 9.81

        initial_kinetic_energy = self.bullet.kinetic_energy(velocity)
        target_position = position + distance_meters

        while position < target_position:
            drag_force = 0.5 * density * drag_coefficient * cross_sectional_area * velocity ** 2

            acceleration = -drag_force / (self.bullet.mass / 1000.0)

            velocity += acceleration * time_step
            position += velocity * time_step

            vertical_velocity -= gravity * time_step
            vertical_position += vertical_velocity * time_step

            time += time_step

            if velocity <= 0:
                break

        final_kinetic_energy = self.bullet.kinetic_energy(velocity)
        energy_loss = initial_kinetic_energy - final_kinetic_energy

        return {
            "initial_energy": initial_kinetic_energy,
            "final_velocity": velocity,
            "time_elapsed": time,
            "final_position": position,
            "final_vertical_position": vertical_position,
            "final_vertical_velocity": vertical_velocity,
            "final_kinetic_energy": final_kinetic_energy,
            "vertical_drop": abs(vertical_position - initial_vertical_position),
            "energy_loss": energy_loss,
        }

    def air_simulation(self, medium, distance_meters):
        """
        Havada simülasyon. İlk ortam.
        """
        result = self.simulate(
            medium=medium,
            distance_meters=distance_meters,
            initial_velocity=self.weapon.muzzle_velocity,
            initial_position=0,
            initial_vertical_velocity=0,
            initial_vertical_position=0,
            initial_time=0
        )
        self.air_result = result
        return result

    def armour_simulation(self, medium):
        """
        Simulates the interaction between the bullet and the armor using improved ballistic resistance principles.

        Reference:
        - DiMaio, V. J. M. (1999). Gunshot wounds: Practical aspects of firearms, ballistics, and forensic techniques. CRC Press.
        """
        if self.air_result is None:
            raise ValueError("Run air_simulation() first to get initial conditions.")

        # Initial parameters
        initial_velocity = self.air_result["final_velocity"]
        cross_sectional_area = self.bullet.cross_sectional_area()
        kinetic_energy = self.bullet.kinetic_energy(initial_velocity)

        # Armor resistance calculation
        energy_absorption = medium.energy_absorption  # in Joules/m²
        cross_sectional_area = max(cross_sectional_area, 1e-4)  # Avoid too small areas
        armour_resistance = max(energy_absorption * cross_sectional_area, 350)  # Min threshold

        # Penetration logic
        if kinetic_energy > armour_resistance:
            penetration = True
            remaining_energy = kinetic_energy - armour_resistance
        else:
            penetration = False
            remaining_energy = 0

        # Deformation estimate
        deformation = (
            medium.thickness * (1 - (armour_resistance / max(kinetic_energy, 1e-4)) ** 0.5)
            if penetration
            else 0
        )

        # Result
        self.armour_result = {
            "initial_velocity": initial_velocity,
            "kinetic_energy": kinetic_energy,
            "armour_resistance": armour_resistance,
            "penetration": penetration,
            "remaining_energy": remaining_energy,
            "deformation": deformation,
        }

        return self.armour_result


    def tissue_simulation(self, medium, distance_meters):
        """
        Doku simülasyonu. Zırhtan çıkan verileri kullanır.
        """
        if self.armour_result is None:
            raise ValueError("Önce armour_simulation() metodunu çalıştırın.")

        if not self.armour_result["penetration"]:
            return {
                "message": "Mermi zırhı delmedi."
            }

        result = self.simulate(
            medium=medium,
            distance_meters=distance_meters,
            initial_velocity=math.sqrt(2 * self.armour_result["remaining_energy"] / (self.bullet.mass / 1000.0)),
            initial_position=self.air_result["final_position"],
            initial_vertical_velocity=self.air_result["final_vertical_velocity"],
            initial_vertical_position=self.air_result["final_vertical_position"],
            initial_time=self.air_result["time_elapsed"]
        )
        self.tissue_result = result
        return result
    
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

class Plot:
    """
    A utility class for creating plots related to ballistic simulations.
    """

    @staticmethod
    def plot_energy_loss_pie(air_result, armour_result, tissue_result):
        """
        Creates a pie chart showing energy losses across different mediums.

        :param air_result: Results from the air simulation.
        :param armour_result: Results from the armour simulation.
        :param tissue_result: Results from the tissue simulation.
        """
        # Extract energy values
        initial_energy = air_result["initial_energy"]
        air_loss = air_result["energy_loss"]
        armour_loss = armour_result["kinetic_energy"] - armour_result["remaining_energy"]
        tissue_loss = tissue_result["energy_loss"]

        # Remaining energy (final kinetic energy in the tissue)
        remaining_energy = tissue_result["final_kinetic_energy"]

        # Define labels and values
        labels = ["Air Loss", "Armour Loss", "Tissue Loss", "Remaining Energy"]
        values = [air_loss, armour_loss, tissue_loss, remaining_energy]
        colors = ["skyblue", "orange", "lightgreen", "lightcoral"]

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, 
                                           colors=colors, wedgeprops={"edgecolor": "black"})
        
        # Add a legend
        plt.legend(wedges, labels, title="Energy Components", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Title
        plt.title("Energy Distribution Across Mediums")
        
        # Show the plot
        plt.show()



# Gerekli sınıfları ve ortamları oluştur
glock_17 = Weapon("glock_17")
mm9_bullet = Bullet("9mm")
air = Medium("unc_air")
tissue = Medium("unc_tissue")
armour = Armour("class_2")

# Simülasyonu başlat
sim = Simulation(glock_17, mm9_bullet)

# Adım 1: Hava simülasyonu
air_result = sim.air_simulation(air, 25)
print("Hava Simülasyonu Sonucu:")
print(json.dumps(air_result, indent=4))

# Adım 2: Zırh simülasyonu
armour_result = sim.armour_simulation(armour)
print("Zırh Simülasyonu Sonucu:")
print(json.dumps(armour_result, indent=4))

# Adım 3: Doku simülasyonu
tissue_result = sim.tissue_simulation(tissue, 0.4)
print("Doku Simülasyonu Sonucu:")
print(json.dumps(tissue_result, indent=4))

# Example usage
# Assuming air_result, armour_result, and tissue_result are dictionaries with the required keys
plotter = Plot()
plotter.plot_energy_loss_pie(air_result, armour_result, tissue_result)