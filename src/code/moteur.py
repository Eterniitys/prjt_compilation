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

def testTransition(word, stateDep, auto, output):
	for charactere in word:
		stateArr, characterEcris = stateDep.transitTo(charactere)
		stateArr = auto.E[stateArr]
		output.append(characterEcris)
		print("Config: Etat départ = {} | Caractère lu = {} | Caractère écris = {} | Etat arrivé = {}".format(stateDep.name, charactere, characterEcris, stateArr.name))
		stateDep = stateArr
	return stateArr

def analyse(auto, word):
	output = list() # sorties
	result = True # mot appartient au langage ou pas

	## verification alphabet d'entree ##
	if testAlphabet(auto.V, word):

		stateDep = auto.E[auto.I[0]] #TODO plrs etats initiaux
		etatFinal = testTransition(word,stateDep, auto, output)

		if etatFinal.name not in auto.F:
			result = False
			print("Erreur : {} ne correspond pas à un état final de l'automate".format(etatFinal.name))
			return output, result
	else:
		result = False
		print("Erreur : un caractère du mot ne correspond pas à l'alphabet d'entrée de l'automate")

	return output, result


print("\nBienvenu sur notre moteur d'automate !\n")

### INPUT ###
filepath_input = "entrees/entree.txt" # TODO parametre
words = readFile(filepath_input)

### AUTOMATE ###
#filepath_automate = "automate_exemples/automate1.descr"
filepath_automate = "testMoteur/C0.descr"
auto = Automate(filepath_automate)
auto.toDot()

### TREATMENT ###
for word in words:
	output, result = analyse(auto, word)

	if result :
		print("{}\t ==\tmot du langage de l'automate".format(word))
		print("Sortie : {}".format(output))
	else :
		print("{}\t <>\tmot du langage de l'automate".format(word))
		print("Sortie : {}".format(output))
	print("\n")
