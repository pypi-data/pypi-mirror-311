import random

amino = "ACDEFGHIKLMNPQRSTVWY"

class Protein:
    def __init__(self, sequence):
        self.sequence = list(sequence)  # Ensure sequence is a list for mutability
        self.structure = self._predict_structure()
        self.stability = self._calculate_stability()

    def mutate(self, environment):
        # Choose a random position to mutate
        position = random.randint(0, len(self.sequence) - 1)

        # Get a random new amino acid
        new_aa = random.choice(amino)

        # Create new sequence with the mutation
        new_sequence = self.sequence[:position] + [new_aa] + self.sequence[position + 1:]

        # Create a new protein with the mutated sequence
        mutated_protein = Protein(''.join(new_sequence))

        # Adjust stability based on environmental factors
        stability_factor = environment._calculate_stability_factor()
        mutated_protein.stability *= stability_factor

        # Update structure based on new environment
        mutated_protein.structure = mutated_protein._predict_structure(environment)

        return mutated_protein

    def _predict_structure(self, environment=None):
        # Simplified structure prediction
        # You can make this more complex by considering environmental factors
        return "".join(random.choice(["H", "E", "C"]) for _ in self.sequence)

    def _calculate_stability(self):
        # Simplified stability calculation
        return sum(aa in "ACFGILMPVW" for aa in self.sequence) / len(self.sequence)

    def __str__(self):
        return f"Sequence: {''.join(self.sequence)}\nStructure: {self.structure}\nStability: {self.stability:.2f}"

    def add_amino_acid(self, amino_acid: str):
        """
        Add an amino acid to the protein sequence.
        Amino acids are represented by their single-letter codes.
        """
        valid_amino_acids = amino  # Standard 20 amino acids
        if amino_acid.upper() not in valid_amino_acids:
            raise ValueError(f"{amino_acid} is not a valid amino acid.")

        # Add the amino acid to the sequence
        self.sequence.append(amino_acid.upper())

        # Recalculate structure and stability after the addition
        self.structure = self._predict_structure()
        self.stability = self._calculate_stability()

    def get_sequence(self) -> str:
        """
        Return the amino acid sequence as a string.
        """
        return "".join(self.sequence)

    def render(self, connector: str = "--%"):
        """
        Render the protein sequence as an ASCII chain.
        Amino acids are represented as '@', and connectors link them.
        If amino acids are lost due to oxidative stress, they will not be rendered.
        """
        ascii_representation = ""
        for index, amino_acid in enumerate(self.sequence):
            if amino_acid != '-':  # Only render if the amino acid is not lost (i.e., not '-')
                ascii_representation += "@"  # Represent amino acids with '@'
                if index < len(self.sequence) - 1:
                    ascii_representation += connector
        return ascii_representation

    def apply_ox_stress(self, stress_level, marker="-"):
        effects = []

        # Loop through the sequence and apply oxidative stress
        for i in range(len(self.sequence)):
            aa = self.sequence[i]

            # Probability of loss is directly proportional to stress_level
            if random.random() < stress_level:
                # Replace the amino acid with a marker (e.g., '-')
                self.sequence[i] = marker
                effects.append(f"{aa} lost due to oxidative stress (stress level {stress_level:.2f})")

        # Return the modified sequence and effects observed
        return self.get_sequence(), effects

    def __repr__(self):
        """
        String representation of the protein.
        """
        return f"<Protein sequence={self.get_sequence()}>"
