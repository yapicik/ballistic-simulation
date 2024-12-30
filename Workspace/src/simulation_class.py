import json
import math
import os


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