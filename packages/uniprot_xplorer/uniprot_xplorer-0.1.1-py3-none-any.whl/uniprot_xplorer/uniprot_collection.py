'''
The script uniprot_collection.py is composed of the Collection class which allows you to provide information on a several "protein" object.

Author : Salma El AOUDATI, Elsa BALIGAND
Date : 2024-11-22
'''

from uniprot_xplorer.uniprot import Uniprot
from matplotlib import figure
import math

class Collection:
  def __init__(self):
    self.uniprot_list = []

  def __repr__(self):
    result = ""
    for uniprot in self.uniprot_list:
      result += f"{uniprot}\n\n"
    return result


  def add_uniprot(self, contenu_uniprot: str):
    '''
    Adds a Uniprot protein sheet to the collection.
    Arguments:
    - contenu_uniprot (str): The Uniprot data as a string.
    Returns:
    - None (updates the object's uniprot_list).
    Raises:
    - Exception: If the protein sheet is already in the collection.
    '''
    uniprot_sheet = contenu_uniprot.split("//\n")
    for line in uniprot_sheet:
      line = line.strip()
      if line:  # to skip empty line
        uniprot_obj = Uniprot(line)
        id_exists = False
        for uniprot in self.uniprot_list:
          if uniprot.identification == uniprot_obj.identification:
            id_exists = True
            break
        if id_exists:
          raise Exception(f"The protein sheet is already in the collection !")
        else:
          self.uniprot_list.append(uniprot_obj)

  def del_uniprot(self, uniprot_id: str):
    '''
    Deletes a Uniprot protein from the collection by its Id.
    Arguments:
    - uniprot_id (str): The Id of the Uniprot protein to delete.
    Returns:
    - None (removes the specified protein from uniprot_list).
    Raises:
    - Exception: If no protein with the given Id is found.
    '''
    for i in range(len(self.uniprot_list)):
      if self.uniprot_list[i].identification == uniprot_id:
        del self.uniprot_list[i]
        return  # to stop the function
    raise Exception(f"No protein found with the id : {uniprot_id}")

  def sort_by_length(self):
    '''
   Sorts the Uniprot proteins in the collection by the length of their peptide sequences.
   Arguments:
   - None (operates on the object's uniprot_list).
   Returns:
   - None (updates the uniprot_list in place).
   '''
    self.uniprot_list = sorted(self.uniprot_list, key=lambda uniprot: len(uniprot.peptide_seq))

  def filter_for_hydrophobic(self, min_hydro: int):
    '''
    Filters the Uniprot proteins, keeping only those with an average hydrophobicity above or equal to a given threshold.
    Arguments:
    - min_hydro (int): The minimum average hydrophobicity threshold.
    Returns:
    - None (updates the uniprot_list in place).
    '''
    self.uniprot_list = [uniprot for uniprot in self.uniprot_list if uniprot.average_hydrophobicity() >= min_hydro]

  def predicate_fn(self):
    '''
    Checks if each Uniprot protein in the collection has "HUMAN" in its identification.
    Arguments:
    - None (operates on the object's uniprot_list).
    Returns:
    - dict: A dictionary where keys are Uniprot Ids and values are booleans indicating if "HUMAN" is in the Id.
    '''
    results = {}
    for uniprot in self.uniprot_list:
        if "HUMAN" in uniprot.identification:
            results[uniprot.identification] = True
        else:
            results[uniprot.identification] = False
    return results

  def filter(self) -> list:
    '''
    Filters the Uniprot proteins, keeping only those that satisfy the predicate defined in 'predicate_fn'.
    Arguments:
    - None (uses 'predicate_fn' to evaluate the criteria).
    Returns:
    - list: A list of Uniprot objects that meet the predicate condition.
    '''
    results = self.predicate_fn()
    list_true = []
    for uniprot in self.uniprot_list:
        if results.get(uniprot.identification, True):
            list_true.append(uniprot)
    return list_true

  def __add__(self, collection2):
    '''
    Merges two Uniprot collections, keeping only unique proteins based on their identification.
    Arguments:
    - collection2 (Collection): The second collection to merge with the current one.
    Returns:
    - Collection: A new Collection object containing the merged unique proteins from both collections.
    '''
    merge_collection = Collection()  # new collection
    id_list = []
    for uniprot_col1 in self.uniprot_list:
      if uniprot_col1.identification not in id_list:
        merge_collection.uniprot_list.append(uniprot_col1)
        id_list.append(uniprot_col1.identification)
    for uniprot_col2 in collection2.uniprot_list:
      if uniprot_col2.identification not in id_list:
        merge_collection.uniprot_list.append(uniprot_col2)
        id_list.append(uniprot_col2.identification)
    return merge_collection

  def go_view(self):
    '''
    Creates a dictionary counting the occurrences of each GO Id across all Uniprot proteins in the collection.
    Arguments:
    - None (operates on the object's uniprot_list).
    Returns:
    - dict: A dictionary where keys are GO Ids and values are the count of occurrences in the collection.
    '''
    dict_go = {}
    for uniprot in self.uniprot_list:
      for goId in uniprot.go_id:
        if goId not in dict_go:
          dict_go[goId] = 1
        else:
          dict_go[goId] += 1
    return dict_go

  def count_protX(self, uniprot_id: str):
    '''
    Counts the occurrences of each amino acid in the peptide sequence of a specified Uniprot protein.
    Arguments:
    - uniprot_id (str): The id of the Uniprot protein.
    Returns:
    - dict: A dictionary where keys are amino acids and values are their counts in the peptide sequence.
    '''
    dict_protX = {}
    for i in range(len(self.uniprot_list)):
      if self.uniprot_list[i].identification == uniprot_id:
        for AA in self.uniprot_list[i].peptide_seq:
          if AA not in dict_protX:
            dict_protX[AA] = 1
          else:
            dict_protX[AA] += 1
    return dict_protX

  def count_collX(self):
    '''
    Calculates the relative frequency of each amino acid in the peptide sequences of the number of Uniprot proteins in the collection.
    Arguments:
    - None (operates on the object's uniprot_list).
    Returns:
    - dict: A dictionary where keys are amino acids and values are their relative frequencies in the entire collection.
    '''
    dict_collX = {}
    list_id = []
    for uniprot in self.uniprot_list:
      list_id.append(uniprot.identification) 
      for AA in uniprot.peptide_seq:
        if AA not in dict_collX:
          dict_collX[AA] = 1
        else:
          dict_collX[AA] += 1

    for AA in dict_collX:
      dict_collX[AA] /= len(list_id)

    return dict_collX

  def calculate_ABRL(self, dict_protX, dict_collX):
    '''
    Calculates the ABRL for each amino acid based on its frequency in a specific protein's peptide sequence
    and its frequency in the entire collection.
    Arguments:
    - dict_protX (dict): A dictionary containing the counts of amino acids in a specific protein's peptide sequence.
    - dict_collX (dict): A dictionary containing the relative frequencies of amino acids in the entire collection.
    Returns:
    - dict: A dictionary where keys are amino acids, and values are their ABRL (log of the ratio between the protein's frequency and the collection's frequency).
    '''
    dict_ABRL = {}
    for AA_prot in dict_protX:
      for AA_coll in dict_collX:
        if AA_prot == AA_coll:
          if dict_protX[AA_prot] == 0 or dict_collX[AA_coll] == 0: # to avoid zero division
            print("Warning : calcul impossible !")
          dict_ABRL[AA_prot] = math.log(dict_protX[AA_prot] / dict_collX[AA_coll])
    return dict_ABRL

  def draw_ABRL(self, uniprot_id: str):
    '''
    Draws a histogram of the ABRL for a specific protein, based on its amino acid composition
    and the amino acid frequencies in the entire collection.
    Arguments:
    - uniprot_id (str): The id of the Uniprot protein for which the ABRL histogram will be drawn.
    Returns:
    - None (saves the histogram as a PNG image file).
    '''
    dict_protX = self.count_protX(uniprot_id)
    dict_collX = self.count_collX()
    dict_ABRL = self.calculate_ABRL(dict_protX, dict_collX)

    fig = figure.Figure()
    ax = fig.subplots(1, 1)
    ax.set_xlabel("Amino acids")
    ax.set_ylabel("ABRL")
    ax.set_title(f"Histogram of the ABRL of the protein {uniprot_id}")
    ax.bar(dict_ABRL.keys(), dict_ABRL.values())
    fig.savefig(f"Histogram_ABRL_{uniprot_id}.png")
    return f"You will find the histogram in the file 'Histogram_ABRL_{uniprot_id}.png'"