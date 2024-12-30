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
        initial_energy = air_result["initial_energy"]
        air_loss = air_result["energy_loss"]
        armour_loss = armour_result["kinetic_energy"] - armour_result["remaining_energy"]
        tissue_loss = tissue_result["energy_loss"]

        remaining_energy = tissue_result["final_kinetic_energy"]

        labels = ["Air Loss", "Armour Loss", "Tissue Loss", "Remaining Energy"]
        values = [air_loss, armour_loss, tissue_loss, remaining_energy]
        colors = ["skyblue", "orange", "lightgreen", "lightcoral"]

        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, 
                                           colors=colors, wedgeprops={"edgecolor": "black"})
        
        plt.legend(wedges, labels, title="Energy Components", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.title("Energy Distribution Across Mediums")
        
        plt.show()