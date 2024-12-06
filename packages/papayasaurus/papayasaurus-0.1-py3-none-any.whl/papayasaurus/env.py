import random
from papayasaurus import Protein  # Assuming the Protein class is imported here

class Environment:
    def __init__(self, temperature=25, pH=7, salt_concentration=0.1):
        self.temperature = temperature
        self.pH = pH
        self.salt_concentration = salt_concentration

    def affect_protein(self, protein):
        """
        Simulate environmental effects on the protein by applying mutation
        based on the current environmental conditions.
        """
        affected_protein = protein.mutate(self)
        return affected_protein


    def _calculate_stability_factor(self):
        """
        Calculate a stability factor based on the environmental conditions:
        Temperature, pH, and Salt concentration.
        """
        temp_factor = 1 - abs(self.temperature - 37) / 100  # Optimal temperature at 37°C
        pH_factor = 1 - abs(self.pH - 7) / 7  # Optimal pH at 7
        salt_factor = 1 - abs(self.salt_concentration - 0.1) / 0.5  # Optimal salt concentration at 0.1M

        return (temp_factor + pH_factor + salt_factor) / 3

    def change_conditions(self, temperature=None, pH=None, salt_concentration=None):
        """
        Dynamically change the environmental conditions.
        """
        if temperature is not None:
            self.temperature = temperature
        if pH is not None:
            self.pH = pH
        if salt_concentration is not None:
            self.salt_concentration = salt_concentration

    def __str__(self):
        """
        Return a string representation of the environment's conditions.
        """
        return f"Environment: Temperature={self.temperature}°C, pH={self.pH}, Salt Concentration={self.salt_concentration}M"
