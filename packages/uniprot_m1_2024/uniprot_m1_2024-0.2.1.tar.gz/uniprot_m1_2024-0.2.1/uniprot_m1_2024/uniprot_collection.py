'''Import de fichiers et librairies'''

from uniprot_m1_2024.uniprot import Uniprot
from matplotlib import figure
import math


'''Class Collection:
	 pour organiser et opere sur plusieurs objets de type Uniprot'''

class Collection:

	'''Constructeur de la classe Collection:
			retourne un objet Collection contenant des objets Uniprot 
			à partir d'un fichier texte (entry_text)'''
	 
	def __init__ (self, entry_text):
		self.prot:list[Uniprot] = []
		prots = entry_text.split("//\n")
		for p in prots:
			if p.strip()!="":
				self.prot.append(Uniprot(p))


	'''Methode Add:
			ajoute un objet Uniprot à la collection'''

	def add(self, contenu_uniprot:str):
		if any(p.id == Uniprot(contenu_uniprot).id for p in self.prot):
			raise ValueError(f"La protéine avec l'ID '{contenu_uniprot.id}' existe déjà dans la collection.")
		else:
			self.prot.append(Uniprot(contenu_uniprot))
			print(f"La protéine avec l'ID '{Uniprot(contenu_uniprot).id}' a été ajoutée à la collection.")
		print(len(self.prot))
	 


	'''Methode Delete:
			supprime un objet Uniprot de la collection'''

	def delete(self, uniprot_id:str):
		for p in self.prot:
			if p.id == uniprot_id:
				self.prot.remove(p)
				print(f"La protéine avec l'ID '{uniprot_id}' a été supprimée de la collection.")
				return
			else:
				raise ValueError(f"Aucune protéine avec l'ID '{uniprot_id}' n'a été trouvée dans la collection.")


	'''Methode de triage:
			trie les objets Uniprot de la collection par longueur de séquence,
			de la plus courte à la plus longue'''

	def sort_by_length(self):
		return [p.id for p in sorted(self.prot, key=lambda p: len(p.sequence))]


	'''Methode de filtrage:
			filtre les objets Uniprot ayant une hydrophobicité supérieure au paramètre min_hydro'''

	def filter_for_hydrophobic(self,min_hydro:int):
		filtered_prot = []
		for p in self.prot:
			if p.average_hydrophobicity() > min_hydro:
				filtered_prot.append(p.id)
		return filtered_prot
		#dictionnaire ou dataframe pandas


	'''Methode magique __add__:
			addition entre deux objets Collection.
			Collection_1 + collection_2 produit un nouvel objet Collection 
			contenant l'union des contenus des deux termes. 
			Attention, si un object Uniprot existe dans les deux collections ajoutées, 
			il ne devra être présent qu'une seule fois dans la collection produit	e par l'addition.'''

	def __add__(self, other):
		if not isinstance(other, Collection):
			raise TypeError("L'opération '+' est uniquement définie entre des objets Collection.")

		total_collection = Collection([]) # total_collection = coll_1 + coll_2

		# 1. J'ajoute à total_collection tous les objets de la première collection
		added_ids = set()  # controller les doublons
		for p in self.prot:
			total_collection.prot.apped(p)
			added_ids.add(p.id)

		# 2. J'ajoute les objets de la deuxième collection (évite les doublons)
		for p in other.prot:
			if p.id not in added_ids:
				total_collection.prot.append(p)
				added_ids.add(p.id)
		
		return total_collection

	#def go_view:



	'''Visualisation de données'''


	'''Methode find_prot_by_id:
	 		recherche et retourne un objet Uniprot à partir de son ID'''

	def find_prot_by_id(self, uniprot_id:str):
		for p in self.prot:
			if p.id == uniprot_id:
				return p
		raise ValueError(f"Aucune protéine avec l'ID '{uniprot_id}' n'a été trouvée dans la collection.")


	'''Methode count_aa:
			retourne un dictionnaire avec l'occurrence de chaque acide aminé 
			dans la séquence de la protéine identifiée par son id en entrée'''

	def count_aa(self, uniprot_id:str):
		dict_abrl = {}
		p = self.find_prot_by_id(uniprot_id)
		for aa in p.sequence:
			if aa in dict_abrl:
				dict_abrl[aa] += 1
			else:
				dict_abrl[aa] = 1
		return dict_abrl


	'''Methode average:
			calcule l'occurence moyenne de l'acide aminé en entrée 
			dans la collection à laquelle appartient la protéine à étudier'''

	def average_aa(self, aa):
		tot_aa_coll = 0
		for p in self.prot:
			tot_aa_coll += self.count_aa(p.id)[aa]
		avg = tot_aa_coll / len(self.prot)
		return avg


	'''Methode draw_abrl:
			calcule l'ABondance ReLative des acides aminés naturels dans la protéine passée en argument 
			par rapport à la collection à laquelle elle appartient selon la formule abrl = ln(count_aa/average_aa).
			Le dessin de l'histogramme est realisé grace à la librairie matplotlib et sauvegardé dans un fichier .png'''

	def draw_ABRL(self, uniprot_id:str):
		dict_abrl = self.count_aa(uniprot_id)
		for cle, valeur in dict_abrl.items():
			dict_abrl[cle] = math.log(valeur / self.average_aa(cle))

		fig = figure.Figure()
		ax = fig.subplots(1, 1)
		ax.bar(range(len(dict_abrl)), dict_abrl.values(), tick_label = list(dict_abrl.keys()))
		fig.savefig("abrl.png")
		return fig