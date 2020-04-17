from Automate import *
import os
import sys

# read input file .txt, words to test
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

# list of character : 
# word : 1001 -> listChar = [1,0] 
def getListChar(word):
	listChar = list()
	for c in word:
		if c not in listChar:
			listChar.append(c)
	return listChar

# test the alphabet, if the word matches to the alphabet
def testAlphabet(alpha, word):
	rep = True
	listChar = getListChar(word)
	for c in listChar:
		if c not in alpha:
			rep = False
			with open(pathLogFile, "a+") as logFile:
				logFile.write("\nError : {} not in alphabet : V -> {}".format(c, alpha))
	return rep

# test if the transition exist
def testTransition(word, stateDep, auto, output):
	for charactere in word:
		stateArr, characterEcris = stateDep.transitTo(charactere)
		if (stateArr == -1):
			with open(pathLogFile, "a+") as logFile:
				logFile.write("\nError: transition not found for state {} with {}".format(stateDep.name,charactere))
				logFile.write("\nWord \"{}\" is not recognized.".format(word))
				sys.exit()
		stateArr = auto.E[stateArr]
		if characterEcris != auto.M :
			output.append(characterEcris)
		with open(pathLogFile, "a+") as logFile:
			logFile.write("{} -> {}/{} -> {}\n".format(stateDep.name, charactere, characterEcris, stateArr.name))
		stateDep = stateArr
	return stateArr, output

# analyse the word
def analyse(auto, word):
	output = list() 		# sortie
	result = False  		# mot appartient au langage ou pas
	resultAlpha = True 		# mot correspond à l'alphabet de l'automate
	k = 0;					# compteur
	notinf = list()			# liste contenant les états d'arrivé n'appartenance pas aux états finaux

	# on test pour tous les états initiaux
	while (k < len(auto.getInitialStates()) and result==False and resultAlpha==True):
		# test alphabet
		if testAlphabet(auto.V, word):
			stateDep = auto.getInitialStates()[k]
			etatFinal, output = testTransition(word,stateDep, auto, output) 
			# test pour savoir si l'état d'arrivé est un état final
			if etatFinal.name not in auto.F:
				result = False
				# état arrivé pas dans les états finaux : ajout de l'état à notinf
				if (etatFinal.name not in notinf):
					notinf.append(etatFinal.name)
			else :
				result = True
		else:
			resultAlpha = False
		k+=1

	if result == False:
		for i in range(len(notinf)):
			with open(pathLogFile, "a+") as logFile:
				logFile.write("\nError : {} not in final states : F -> {}".format(notinf[i], auto.F))

	return output, result



print("\nBienvenu sur notre moteur d'automate !")

# création des dossiers output / logs / dotImage
try:
    os.mkdir("output")
    os.mkdir("logs")
    os.mkdir("dotImage")
except FileExistsError: pass

pathLogFile = "logs/{}.log".format(sys.argv[1].split("/")[-1][:-6])
outputFile = "output/{}.txt".format(sys.argv[1].split("/")[-1][:-6])

### INPUT ###
filepath_input = sys.argv[2]
words = readFile(filepath_input)

## INIT FILE ##
with open(pathLogFile, "w") as logFile:
	logFile.write("")
with open(outputFile, "w") as out:
	out.write("")

### AUTOMATON ###
filepath_automate = sys.argv[1]
auto = Automate(filepath_automate)
auto.toDot("graphInitial.dot")

## DETERMINISE ##
auto = auto.determinise()
auto.toDot("graphDeter.dot")


### TREATMENT ###
for word in words:
	output, result = analyse(auto, word)
	textOut = ""
	for c in output:
		textOut += c

	with open(pathLogFile, "a+") as logFile:
		if result :
			logFile.write("\n\"{}\"\t Is a word from the language of the automaton\n".format(word))
			logFile.write("Sortie : {} ; {}\n".format(output, textOut))
			with open(outputFile, "a+") as out:
				out.write("\nInput {} -> Output {}".format(word,output))
		else :
			logFile.write("\n\"{}\"\t Is not a word from the language of the automaton\n".format(word))
			logFile.write("Sortie : {} ; {}\n".format(output, textOut))
		logFile.write("\n")
		
print("Automate créé, allez voir le fichier de log, faire un make graph")
