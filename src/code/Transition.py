class Transition(object):

	def __init__(self, v, e, o):
		self.v = v # caractere lu
		self.e = e # etat arrivé
		self.o = o # caratere ecris
		
	def __repr__(self):
		return "'{}' {} '{}'".format
