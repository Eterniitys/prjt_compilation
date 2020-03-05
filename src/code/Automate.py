import re
from Etat import *

class Automate:
	def __init__(self, filepath):
		self.I = ["0"]	# etats initiaux
		self.E = []	# tableau des etats
		self.F = []	# etats finaux
		self.V = []	# alpabet entrée
		self.O = []	# alpabet sortie
		self.M = "#"

		f = open(filepath, "r")
		for line in f:
			if re.match(r"^C\s+", line):
					pass

			elif re.match(r"^M\s+(.)\s*$", line):
				groups = re.match(r"^M\s+(.)\s*$", line)
				self.M = groups.group(0)
				self.M = self.M.split(" ")[1]

			elif re.match(r"^V\s+\"(\S+)\"\s*$", line):
				groups = re.match(r"^V\s+\"(\S+)\"\s*$", line)
				rep = list()
				for a in groups.group(0):
					rep.append(a.split("\n")[0])
				i = 3
				while (rep[i] != "\""):
					self.V.append(rep[i])
					i+=1

			elif re.match(r"^O\s+\"(\S+)\"\s*$", line):
				groups = re.match(r"^O\s+\"(\S+)\"\s*$", line)
				rep = list()
				for a in groups.group(0):
					rep.append(a.split("\n")[0])
				i = 3
				while (rep[i] != "\""):
					self.O.append(rep[i])
					i+=1

			elif re.match(r"^E\s+(\d+)\s*$", line):
				groups = re.match(r"^E\s+(\d+)\s*$", line)
				for nb in range(int(groups.group(0).split(" ")[1])): # split + 1 + int 
					self.E.append(Etat(str(nb)))

			elif re.match(r"^I\s+(?P<init>\d+(?:\s+\d+)*)\s*$",line):
				groups = re.match(r"^I\s+(?P<init>\d+(?:\s+\d+)*)\s*$",line)
				#self.I = []
				for nb in groups.group("init").split("\s"):
					self.I.append(nb)

			elif re.match(r"F\s+(?P<final>\d*(?:\s+\d+)*)\s*$",line):
				groups = re.match(r"^F\s+(?P<final>\d*(?:\s+\d+)*)\s*$",line)
				#self.I = []
				for nb in groups.group("final").split("\s+"):
					self.F.append(nb)

			elif re.match(r"^T\s+(?P<etatOrigine>\d+)\s+'(?P<v>.)'\s+(?P<etatSortie>\d+)(\s+'(?P<o>.)')?\s*$",line):
				groups = re.match(r"^T\s+(?P<etatOrigine>\d+)\s+'(?P<v>.)'\s+(?P<etatSortie>\d+)(\s+'(?P<o>.)')?\s*$",line)
				e1 = groups.group("etatOrigine")
				e2 = groups.group("etatSortie")
				a1 = groups.group("v")
				a2 = groups.group("o")
				if a1 == None:
					a1 = self.M
				if a2 == None:
					a2 = self.M
				self.E[int(e1)].addTransition(a1, e2, a2)

			else:
				print("Error : bad description file :" + line)

		if len(self.E) == 0 or len(self.V) == 0 or len(self.F) == 0:
			print("Error : Missing decription line. (E, V, F)")

	def toDot(self):
		file = open("dotImage/graph.dot","w")
		file.write("digraph automate {\n")
		for state in self.E:
			for transition in state.transitions:
				dep = state.name
				arr = transition.e
				file.write("\t{} -> {} [label=\"{}/{}\"];\n".format(dep,arr,transition.v,transition.o))
		file.write("}")


		
"""
<AEF> ::= [<ligneC>] [<ligneM>] <ligneV> [<ligneO>] <ligneE> [<ligneI>] <ligneF> [<ligneT>]* (1)

ligne C (commentaire) ::= C 
ligne M (méta)   ::= M µ        : le méta-caractère représentant lambda (défaut : #) (ici : µ)
ligne V (entrée) ::= V "c[c]*"    : le vocabulaire d'entrée (pas de défaut) (2)
ligne O (sortie) ::= O "c[c]*"    : le vocabulaire de sortie (défaut : pas de sortie) (2)
ligne E (nbre)   ::= E i        : nombre d'états (E = 0..N-1) (pas de défaut)
ligne I (init)   ::= I i[ i]*   : les états initiaux (défaut : 0)
ligne F (final)  ::= F [i[ i]*] : les états acceptants (pas de défaut) (5)
ligne T (trans)  ::= i 'x' i 'x'    : une transition de ExVxExO (3) (4)

(0) Les lignes entre crochets sont facultatives, les autres (V, E, F) sont obligatoires.
(1) <ligneT> ne peut être suivie que par <ligneT>. Le fichier peut éventuellement se terminer par une ligne vide, ou non.
(2) "c[c]*" doit être fourni entre guillemets.
(3) i 'x' i 'µ' peut aussi s'écrire i 'x' i
(4) i 'c' j 'x' représente la transition de i vers j par c avec sortie de x (ou rien si x=µ)
    i 'µ' j 'x' représente la transition de i vers j par lambda avec sortie de x (ou rien si x=µ)
(5) En cas d'états multiples, ceux-ci sont séparés par un espace.

Légende :
i représente un entier sans signe
c représente un caractère quelconque, différent de la représentation du méta-caractère lambda
x représente un caractère quelconque, ou le méta-caractère ( x    ::= c | µ )
[q] indique que q est facultatif                            ( [q]  ::= q | µ )
[q]* indique que q peut être fourni 0 ou plusieurs fois     ( [q]* ::= q[q]* | µ )

Note : 
- les espaces ne sont pas considérés. Ils doivent être ignorés lors de l'analyse.

Notes :
 - I 0 est sous-entendue.
 - on aurait pu écrire T 0 '1' 1 au lieu de T 0 '1' 1 '#'.
 """
