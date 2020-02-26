class Etat:
    def __init__(self, name):
        self.name = name
        self.transitions = []

    def addTransition(char v, Etat e, char o):
        transition = Transition(v,e,o)
        transitions.append(transition)

    def transitTo(char v):
        for transition in transitions:
            if transition.v == 'v':
                return transition.e, transition.o
        raise Exception("Transition not Found")

