'''
The script uniprot.py is composed of the Uniprot class which allows you to provide information on a "protein" object.

Author : Salma El AOUDATI, Elsa BALIGAND
Date : 2024-11-22
'''
import os

# Amino acid information dictionary
amino_acids = {
  "A": ["Alanine", "Ala", 89, "A", 0.33],
  "R": ["Arginine", "Arg", 174, "+", 1.00],
  "N": ["Asparagine", "Asn", 132, "P", 0.43],
  "D": ["Aspartic acid", "Asp", 133, "-", 2.41],
  "B": ["Asparagine or aspartic acid", "Asx", 133, "n/a", "n/a"],
  "C": ["Cysteine", "Cys", 121, "A or P", 0.22],
  "Q": ["Glutamine", "Gln", 146, "P", 0.19],
  "E": ["Glutamic acid", "Glu", 147, "-", 1.61],
  "Z": ["Glutamine or glutamic acid", "Glx", 147, "n/a", "n/a"],
  "G": ["Glycine", "Gly", 75, "P", 1.14],
  "H": ["Histidine", "His", 155, "P or +", -0.06], # hydrophobicity closest to neutral pH
  "I": ["Isoleucine", "Ile", 131, "A", -0.81],
  "L": ["Leucine", "Leu", 131, "A", -0.69],
  "K": ["Lysine", "Lys", 146, "+", 1.81],
  "M": ["Methionine", "Met", 149, "A", -0.44],
  "F": ["Phenylalanine", "Phe", 165, "A", -0.58],
  "P": ["Proline", "Pro", 115, "A", -0.31],
  "S": ["Serine", "Ser", 105, "P", 0.33],
  "T": ["Threonine", "Thr", 119, "P", 0.11],
  "W": ["Tryptophan", "Trp", 204, "A", -0.24],
  "Y": ["Tyrosine", "Tyr", 181, "P", 0.23],
  "V": ["Valine", "Val", 117, "A", -0.53]
}


class Uniprot:

  def __init__(self, uniprot_sheet):
    self.identification = ""
    self.ac_number = ""
    self.org_species = ""
    self.gene_name = ""
    self.peptide_seq = ""
    self.go_id = []

    for line in uniprot_sheet.split("\n"):
      if line.startswith("ID"):
        self.identification = line.strip().split()[1]
      elif line.startswith("AC") and not self.ac_number:
        self.ac_number = line.strip().split()[1].strip(";")
      elif line.startswith("OS"):
        self.org_species = line.strip()[5:-1]
      elif line.startswith("GN   Name"):
        self.gene_name = line.strip().split()[1][5:]
      elif line.startswith(" "):
        self.peptide_seq += line.strip().replace(" ", "")
      elif line.startswith("DR   GO;"):
        self.go_id.append(line.strip().split()[2][:-1])

  def __repr__(self):
    return f"{self.identification}\n{self.ac_number}\n{self.org_species}\n{self.gene_name}\n{self.peptide_seq}\n{self.go_id}"

  def fasta_dump(self):
    '''
    Saves the protein sequence in FASTA format.
    Arguments:
    - None (uses object's attributes).
    Returns:
    - None (writes a FASTA file in the "output" folder).
    '''
    os.makedirs("output", exist_ok=True)  # Create output folder if it does not exist
    output = os.path.join(os.curdir, f"output/{self.ac_number}.fasta")
    with open(output, 'w') as o:
      o.write(f"> {self.identification} {self.org_species} {self.gene_name}\n{self.peptide_seq}")

  def molecular_weight(self) -> float:
    '''
    Calculates the molecular weight of the protein.
    Arguments:
    - None (uses the object's peptide sequence).
    Returns:
    - float: The molecular weight of the peptide.
    '''
    mol_weight = 0
    for AA_1 in self.peptide_seq:
      for AA_2 in amino_acids:
        if AA_1 == AA_2:
          mol_weight += amino_acids[AA_2][2]
    return mol_weight

  def average_hydrophobicity(self) -> float:
    '''
    Calculates the average hydrophobicity of the peptide sequence.
    Arguments:
    - None (uses the object's peptide sequence).
    Returns:
    - float: The average hydrophobicity.
    '''
    length_peptide = len(self.peptide_seq)  # Sequence length
    sum_hydro = 0
    for AA_1 in self.peptide_seq:
      for AA_2 in amino_acids:
        if AA_1 == AA_2:
          sum_hydro += amino_acids[AA_2][4]  # Sum of hydrophobicity
    hydro_scale = sum_hydro / length_peptide  # Calculation of the average hydrophobicity for the protein
    return round(hydro_scale, 4)


