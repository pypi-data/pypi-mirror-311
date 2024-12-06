class Uniprot:
	'''
	une classe qui vous permet de créer et de manipuler des objets, en l'occurrence des données protéiques 
	'''
	def __init__(self, lineFileAll: str):
		'''
		__init__ est un constructeur qui vous permet de créer un objet de classe. Doit prendre un fichier sous
		forme de chaîne et renvoyer un objet où les clés sont les désignations codées et leurs valeurs sont les
		valeurs d'une protéine particulière.
		'''
		lineFileAll = lineFileAll.split('\n')
		osProt = ""
		gnProt = ""
		dico_GO ={}
		seqProt = ""
		acProt = ""
		acCounter = 0
		sqCounter = 0
		for lin in lineFileAll:
			lin_sep = lin.split(' ')
			if lin_sep[0] == "ID" or lin_sep[0] == "AC" or lin_sep[0] == "OS" or lin_sep[0] == "GN" or lin_sep[0] == "SQ" or lin_sep[0] == "" or lin_sep[0] == "DR":
				for word in lin_sep[1:]:
					if word != '':
						if lin_sep[0] == "ID":
							self.id = word.strip()
							break
						if lin_sep[0] == "AC" and acCounter == 0:
							acProt = word.strip()
							acCounter += 1
							break
						if lin_sep[0] == "OS":
							osProt += word.strip() + " "
						if lin_sep[0] == "GN":
							gnProt += word.strip() + " "
						if lin_sep[0] == "SQ":
							sqCounter += 1
						if lin_sep[0] == "" and sqCounter > 0 and lin_sep[0] != "//":
							seqProt += word.strip()
						if lin_sep[0] == "DR":
							DR_line=''.join(lin_sep[1:]).strip()
							DR_line=DR_line.split(';')
							if(DR_line[0]=='GO'):
								ID=DR_line[1].split(':')[1]
								Value=DR_line[2:]
								dico_GO[ID]= Value
		if ";" in acProt:
			self.ac = acProt[:-1]
		self.os = osProt
		self.gn = gnProt
		self.sq = seqProt
		self.dico_GO = dico_GO

	def __repr__(self):
		'''
		__repr__ - cette fonction permet afficher toutes les clés de valeur d’objet.
		'''
		return (f'''ID:{self.id}\n
			AC:{self.ac}\n
			OS:{self.os}\n
			GN:{self.gn}\n
			'''
			)

	def fasta_dump(self):
		'''
		fasta_dump - cette fonction permet d'écrire la séquence protéique sous forme de fichier fasta
		'''
		fasta_file=self.ac+'.fasta'
		with open(fasta_file, 'w') as f_out:
			header=f'>{self.id}|{self.os}|{self.gn}\n'
			f_out.write(header)
			f_out.write(f'{self.sq}\n')

	def molecular_weight(self)->float:
		'''
		moleculat_weight - cette fonction permet retourne le poids moléculaire de la protéine
		'''
		mol_weight=0
		for aa in self.sq:
			if aa not in amino_acids:
				continue
			mol_weight+=amino_acids[aa][0]
		return mol_weight

	def average_hydrophobicity(self)->float:
		'''
		average_hydrophobicity - cette fonction permet retourne l'hydrophobicité moyenne de la protéine
		'''
		av_hydro=0
		total_aa=0
		for aa in self.sq:
			if aa not in amino_acids:
				continue
			if 'P' or '+' or '-' or 'A' in aa[2]:
				av_hydro+=amino_acids[aa][1]
				total_aa+=1
		return av_hydro/total_aa

amino_acids = {
    'A': [89, 0.33, 'A'],
    'R': [174, 1.00, '+'],
    'N': [132, 0.43, 'P'],
    'D': [133, 2.41, '-'],
    'B': [133, 'n/a', 'n/a'],  # Asparagine ou acide aspartique
    'C': [121, 0.22, 'A or P'],
    'Q': [146, 0.19, 'P'],
    'E': [147, 1.61, '-'],
    'Z': [147, 'n/a', 'n/a'],  # Glutamine ou acide glutamique
    'G': [75, 1.14, 'P'],
    'H': [155, -0.06, 'P or +'],  # Ou 1.37 en fonction de la charge
    'I': [131, -0.81, 'A'],
    'L': [131, -0.69, 'A'],
    'K': [146, 1.81, '+'],
    'M': [149, -0.44, 'A'],
    'F': [165, -0.58, 'A'],
    'P': [115, -0.31, 'A'],
    'S': [105, 0.33, 'P'],
    'T': [119, 0.11, 'P'],
    'W': [204, -0.24, 'A'],
    'Y': [181, 0.23, 'P'],
    'V': [117, -0.53, 'A']
}
