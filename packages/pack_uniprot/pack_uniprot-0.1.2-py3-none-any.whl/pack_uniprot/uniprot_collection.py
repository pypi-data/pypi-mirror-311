from . uniprot import Uniprot 
from matplotlib import figure
import math
class Collection:
	'''
	Cette classe permettra de créer un objet contenant des objets de la classe
	Uniprot et de les manipuler à l'aide des fonctions de la classe.
	'''
	def __init__(self, allLines: str):
		'''
		__init__ vous permettra de créer une list contenant des objets de la classe Uniprot.
		Autrement dit, les données protéiques en tant qu'objets seront des éléments de la list.
		'''
		self.dicti = []
		array = []
		allLines = allLines.split('\n')
		for line in allLines:
			array.append(line)
			if "//" == line[0:2]:
				stringLine = '\n'.join(array)
				self.dicti.append(Uniprot(stringLine))
				array = []
				continue

	def __iter__(self):
		'''
		__iter__ permettra itérer sur un objet uniprot
		'''
		for elem in self.dicti:
			yield elem

	def create(path_file):
		'''
		create - une fonction qui vous permettra de créer un objet de la classe Collection
		lorsque vous entrez le nom d'un fichier contenant des informations textuelles décrivant des protéines.
		'''
		with open(path_file, 'r') as f:
			text_content=f.read()
		return Collection(text_content)

	def add(self, contenu_uniprot:str):
		'''
		add - une fonction qui permettra, si cette protéine n'est pas dans notre objet Collection,
		d'ajouter notre protéine à notre objet classe Collection.
		'''
		newProtObj = Uniprot(contenu_uniprot)
		for i in range(0, len(self.dicti)):
			if newProtObj.id == self.dicti[i].id:
				raise Exception("can't add, already exists")
			else:
				print("adding a new object")
				self.dicti.append(newProtObj)
				return self

	def delProt(self, uniprot_id: str):
		'''
		delProt - une fonction qui permettra, si cette protéine est présente dans notre objet collection,
		de supprimer la protéine dont nous avons besoin de notre objet classe Collection
		'''
		for i in range(0, len(self.dicti)):
			if uniprot_id == self.dicti[i].id:
				del self.dicti[i]
				return self
		raise Exception("can't delite, not exists")

	def sort_by_length(self):
		'''
		sort_by_length - une fonction qui vous permet de renvoyer une liste de protéines triées
		par ordre croissant selon la longueur de leur séquence d'acides aminés.
		'''
		newKeyVa = {}
		sortedProt = []
		for i in self.dicti:
			newKeyVa[i] = ''
			lenAC = len(i.sq)
			newKeyVa[i] = lenAC
		sortedD = dict(sorted(newKeyVa.items(), key=lambda x: x[1]))
		print(sortedD)
		final = list(sortedD)
		return final

	def filter_for_hydrophobic(self, min_hydro:int) -> dict:
		'''
		filter_for_hydrophobic - cette fonction permettra de renvoyer un objet Collection
		avec des objets sous forme de protéines dont le niveau d'hydrophobie est supérieur
		au nombre que nous saisissons.
		'''
		dico_hydro=[]
		for prot in self.dicti:
			hydroph = prot.average_hydrophobicity()
			if hydroph>min_hydro:
				dico_hydro.append(prot)
		return dico_hydro

	def __add__(self, coll2):
		'''
		__add__ cette fonction permettra d'ajouter des protéines d'un autre objet Collection
		à un objet Collection avec des objets sous forme de protéines s'ils n'existent pas.
		renverra un nouvel objet Collection avec toutes les protéines uniques.
		'''
		result_dict = self.dicti.copy()
		arra = []
		for f in self.dicti:
			arra.append(f.id)
		print(arra)
		for prot2 in coll2.dicti:
			if prot2.id not in arra:
				print("new protein")
				result_dict.append(prot2)
			else:
				print("existe")

		return result_dict

	def go_view(self):
		'''
		go_view - retournera le dictionnaire des nombres d'occurrences des mots-clés GO
		portés par toutes les membres de la Collection
		'''

		dico_go_coll={}
		for uniprot in self.dicti:
			dico_go_coll[uniprot.id] = len(uniprot.dico_GO)
		return dico_go_coll

	def draw_ABRL(self, uniprot_id:str):
		"""
		1) calculer table de fréquence des aa dans la protéine
		2) calculer table de fréquence moyenne des aa dans la collection
		3) calculer la table de ratio par aa: log (fq_aa_prot/fq_moye_aa_coll)
		"""
		aa_table_coll=self.get_table_aa_coll()
		aa_log_table={}
		for uniprot in self.dicti:
			if uniprot.id==uniprot_id:
				aa_table_prot=self.calc_aa_ratio(uniprot.sq)
		for aa in aa_table_prot:
			if aa in aa_table_coll:
				if (aa_table_coll[aa]==0 or aa_table_prot[aa]==0):
					continue
				else:
					log_aa=math.log(aa_table_prot[aa]/aa_table_coll[aa])
					aa_log_table[aa]=log_aa

		fig = figure.Figure()
		ax   = fig.subplots(1, 1)
		ax.bar(list(aa_log_table.keys()), list(aa_log_table.values()))
		fig.savefig(uniprot_id+".png")
		return aa_log_table

	def get_table_aa_coll(self):
		'''
		Calcule la table de fréquence des acides aminés pour la collection
		La somme des fréquences vaut 1
		'''
		aa_table_coll={}
		for uniprot in self.dicti:
			aa_table_prot=self.calc_aa_ratio(uniprot.sq)
			for aa in aa_table_prot:
				if aa not in aa_table_coll:
					aa_table_coll[aa]=aa_table_prot[aa]
				else:
					aa_table_coll[aa]+=aa_table_prot[aa]
		total=sum(aa_table_coll.values())
		for aa in aa_table_coll:
			aa_table_coll[aa]/=total
		return aa_table_coll

	def calc_aa_ratio(self, sequence:str):
		'''
		Calcule la table de fréquence des acides aminés pour une séquence
		La somme des fréquences vaut 1
		'''
		aa_freq={}
		for aa in sequence:
			if aa not in aa_freq:
				aa_freq[aa]=1
			else:
				aa_freq[aa]+=1
		total=sum(aa_freq.values())
		for aa in aa_freq:
			aa_freq[aa]/=total
		return aa_freq
