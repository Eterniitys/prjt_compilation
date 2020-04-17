from Transition import *
import sys

class Etat:
	def __init__(self, name):
		self.name = name
		self.transitions = list()
		self.hasLambdaTrans = False
	
	def __repr__(self):
		return "<{}>".format(str(self.name))

	# add transition to state
	def addTransition(self, v, e, o):
		transition = Transition(v, e, o)
		self.transitions.append(transition)

	# transit to function, return -1 if transition dont exist
	def transitTo(self, v):
		for transition in self.transitions:
			if (transition.v == v):
				return transition.e, transition.o
		return -1, -1
	
	# get lambda transition
	def getLambdaT(self):
		trans = list()
		if (self.hasLambdaTrans):
			for transition in self.transitions:
				if transition.v == '#' and transition.o == '#':
					trans.append(transition)
		return trans

	# get transistion
	def getTransition(self, a):
		trans = list()
		for transition in self.transitions:
			if transition.v == a:
				trans.append(transition)
		return trans
