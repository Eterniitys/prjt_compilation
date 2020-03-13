from Automate import *


if len(sys.argv)< 3:
	print("You should set paramaters as folow:")
	sys.exit()

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
			with open(pathLogFile, "a+") as logFile:
				logFile.write("\nError : {} not in O->".format(c, alpha))
	return rep

def testTransition(word, stateDep, auto, output):
	for charactere in word:
		stateArr, characterEcris = stateDep.transitTo(charactere)
		stateArr = auto.E[stateArr]
		if characterEcris != auto.M :
			output.append(characterEcris)
		with open(pathLogFile, "a+") as logFile:
			#logFile.write("\nConfig: Etat départ = {} | Caractère lu = {} | Caractère écris = {} | Etat arrivé = {}".format(stateDep.name, charactere, characterEcris, stateArr.name))
			logFile.write("\n {} -> {}/{} -> {}".format(stateDep.name, charactere, characterEcris, stateArr.name))
		stateDep = stateArr
	return stateArr

def analyse(auto, word):
	output = list() # sorties
	result = True # mot appartient au langage ou pas

	## verification alphabet d'entree ##
	if testAlphabet(auto.V, word):


		stateDep = auto.getInitialState()[0] #TODO plrs etats initiaux

		etatFinal = testTransition(word,stateDep, auto, output)

		if etatFinal.name not in auto.F:
			result = False
			with open(pathLogFile, "a+") as logFile:
				#logFile.write("\nErreur : {} ne correspond pas à un état final de l'automate".format(etatFinal.name))
				logFile.write("\nErreur : {} not in final states : F->{}".format(etatFinal.name, auto.F))
			return output, result
	else:
		result = False


	return output, result


print("\nBienvenu sur notre moteur d'automate !\n")

pathLogFile = "{}.log".format(sys.argv[1].split("/")[-1][:-6])

### INPUT ###
filepath_input = sys.argv[2]
words = readFile(filepath_input)

### AUTOMATE ###
filepath_automate = sys.argv[1]
auto = Automate(filepath_automate)
auto.toDot()

### fichier de log
with open(pathLogFile, "w") as logFile:
	logFile.write("")

### TREATMENT ###
for word in words:
	output, result = analyse(auto, word)
	textOut = ""
	for c in output:
		textOut += c

	with open(pathLogFile, "a+") as logFile:
		if result :
			logFile.write("\n{}\t ==\tmot du langage de l'automate".format(word))
			logFile.write("Sortie : {} ; {}".format(output, textOut))
		else :
		
			logFile.write("\n{}\t !=\tmot du langage de l'automate".format(word))
			logFile.write("Sortie : {} ; {}".format(output, textOut))
		logFile.write("\n")

print("Automate créé, allez voir le fichier de log, faire un make graph\n")