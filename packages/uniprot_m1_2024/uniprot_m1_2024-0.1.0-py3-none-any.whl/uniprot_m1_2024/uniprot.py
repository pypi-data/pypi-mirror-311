'''Class Uniprot:
	 stocke certaines informations des protéines contenues dans la base de données Uniprot'''

class Uniprot:

	'''Dictionnaire des masses moléculaires des acides aminés'''
	dict_mol_weight = {"A": 89, "R": 174, "N": 132, "D": 133, "B": 133,
						"C": 121, "Q": 146, "E": 147, "Z": 147, "G": 75,
						"H": 155, "I": 131, "L": 131, "K": 146, "M": 149,
						"F": 165, "P": 115, "S": 105, "T": 119, "W": 204,
						"Y": 181, "V": 117}

	'''Dictionnaire des hydrophobicity des acides aminés'''
	dict_hydrophobic = {"A": 0.33, "R": 1, "N": 0.43, "D": 2.41, "B": 0, "C": 0.22,
						"Q": 0.19, "E":0, "Z": 0, "G": 1.14, "H": -0.06, "I": -0.81, "L": -0.69,
						"K": 1.81, "M": -0.44, "F": -0.58, "P": -0.31, "S": 0.33,
						"T": 0.11, "W": -0.24, "Y": 0.23, "V": -0.53}


	'''Constructeur de la classe Uniprot:
			prend le contenu textuel d'une fiche uniprot en entrée (entry_text),
			parse le contenu, crée l'objet et renseigne les attributs'''

	def __init__ (self, entry_text):

		self.id = None
		self.ac_number = None
		self.organism = None
		self.gene_name = None
		self.sequence = None
		self.go_identifiers = []

		lines = entry_text.split("\n")
		flag1 = True
		flag2 = True

		for ln in lines[:-1]:
			element = ln.split() 
			if element[0] == "ID":
				self.id = element[1]

			if element[0] == "AC" and flag1 == True:
				self.ac_number = element[1][:-1]
				flag1 = False

			if element[0] == "OS":
				organism = " ".join(element[1:])
				self.organism = organism[:-1]

			if element[0] == "GN" and flag2 == True:
				self.gene_name = element[1][5:]
				flag2 = False

			if element[0] == "SQ":
				sq_line = lines.index(ln)

		sequence = "".join(lines[sq_line+1:-2])
		self.sequence = sequence.replace(" ", "")



	'''Methode fasta_dump: 
			écrit la sequence de la protéine au forma fasta dans un fichier'''

	def fasta_dump(self):
		fasta_filename = f"{self.ac_number}.fasta"
		with open(fasta_filename, "w") as fasta_file:
			header = f">{self.id} | {self.organism} | {self.gene_name}\n"
			fasta_file.write(header)
			for i in range(0, len(self.sequence), 60):
				fasta_file.write(self.sequence[i:i+60] + "\n")
		print(f"Fichier FASTA géneré : {fasta_filename}")



	'''Methode molecular_weight:
			calcule la masse moléculaire de la protéine'''

	def molecular_weight(self)->float:
		molecular_weight = 0
		if self.sequence == "":
			return 0
		for char in self.sequence:
			molecular_weight += self.dict_mol_weight[char]
		return molecular_weight



	'''Methode average_hydrophobicity:
			calcule la masse moléculaire de la protéine'''

	def average_hydrophobicity(self)->float:
		average_hydro = 0
		if self.sequence == "":
			return 0
		for char in self.sequence:
			average_hydro += self.dict_hydrophobic[char]
		return average_hydro