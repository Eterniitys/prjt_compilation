from Transition import *
import sys

class Etat:
	def __init__(self, name):
		self.name = name
		self.transitions = list()

	def addTransition(self, v, e, o):
		transition = Transition(v, e, o)
		self.transitions.append(transition)

	def transitTo(self, v):
		for transition in self.transitions:
			if (transition.v == v):
				return transition.e, transition.o

		print("Erreur: il pas de transition trouvée de l'état {} avec pour caractère lu {}".format(self.name,v))
		sys.exit()