from Automate import *


def readFile(filepath):
	file = open(filepath,"r")
	ch = file.readline()
	words =  list()

	while(ch[:3] != "###"):
		ch = ch.split(" ")
		for word in ch:
			word = word.split('\n')[0]
			if word != "":
				words.append(word)
		ch = file.readline()
	return words

def getListChar(word):
	listChar = list()
	for c in word:
		if c not in listChar:
			listChar.append(c)
	return listChar

def testAlphabet(alpha, word):
	rep = True
	listChar = getListChar(word)
	for c in listChar:
		if c not in alpha:
			rep = False
			print("{} n'est pas dans alphabet entrée de l'automate".format(c))
	return rep

def getState(states, charactere):
	for state in states:
		if state.name == charactere:
			return state
	return -1

def testTransition(word, stateDep, auto, config, output, erreur):
	for charactere in word:
		find = False
		for transition in stateDep.transitions:
			if transition.v == charactere:
				find = True
				# Je prends cette transition car deterministe -> que celle la possible
				arrive = transition.e
				output.append(transition.o)
				config.append("Etat départ = {} | Caractère lu = {} | Caractère écris = {} | Etat arrivé = {}".format(stateDep.name, transition.v, transition.o, arrive))
				stateDep = getState(auto.E, arrive)
		#transition pas trouvé
		if not find:
			config.append("Etat départ = {} | Caractère lu = {} | Caractère écris = {} | Etat arrivé = {}".format(stateDep.name, None, None, None))
			erreur = "Erreur : La transition {}/? n'existe pas dans l'état {}".format(charactere, stateDep.name)
			result = False
			return config, output, result, erreur

	return stateDep

def analyse(auto, word):
	config = list() # liste des config successives de l'automate -> etat 0 prend transition a et ecris 1
	output = list() # sorties
	result = True # mot appartient au langage ou pas
	erreur = "" # messsage d'erreur

	## verification alphabet d'entree ##
	if testAlphabet(auto.V, word):

		# état de départ
		stateDep = getState(auto.E, auto.I[0]) #TODO plrs etats initiaux

		# test transitions
		etatFinal = testTransition(word,stateDep, auto, config, output, erreur)

		# test de l'état final du mot
		if etatFinal.name not in auto.F:
			result = False
			erreur = "Erreur : {} ne correspond pas à un état final de l'automate".format(etatFinal.name)
			return config, output, result, erreur

	else:
		result = False
		config.append("Etat départ = {} | Caractère lu = {} | Caractère écris = {} | Etat arrivé = {}".format(None, None, None, None))
		erreur = "Erreur : un caractère du mot ne correspond pas à l'alphabet d'entrée de l'automate"

	return config, output, result, erreur


print("\nBienvenu sur notre moteur d'automate !\n")

### INPUT ###
filepath_input = "entrees/entree.txt" # parametre
words = readFile(filepath_input)

### AUTOMATE ###
#filepath_automate = "automate_exemples/automate1.descr"
filepath_automate = "testMoteur/C0.descr"
auto = Automate(filepath_automate)
auto.toDot()

### TREATMENT ###
for word in words:
	config, output, result, erreur = analyse(auto, word)
	if result :
		print("{}\t ==\tmot du langage de l'automate".format(word))
		print("Sortie : {}".format(output))
		for conf in config:
			print("Config : {}".format(conf))
	else :
		print("{}\t <>\tmot du langage de l'automate".format(word))
		print("Sortie : {}".format(output))
		for conf in config:
			print("Config : {}".format(conf))
		print(erreur)
	print("\n")
