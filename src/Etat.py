from Transition import *

class Etat:
    def __init__(self, name):
        self.name = name
        self.transitions = list()

    def addTransition(self, v, e, o):
        transition = Transition(v, e, o)
        self.transitions.append(transition)

    def transitTo(v):
        for transition in self.transitions:
            if transition.v == 'v':
                return transition.e, transition.o
        raise Exception("Transition not Found")
