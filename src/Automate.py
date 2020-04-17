import re
from Etat import *

pathAutomateLogFile = "automate.log"
pathToDeterminised = "generatedAutomate.descr"

class Automate:
	def __init__(self, filepath):
		self.I = [0]	# etats initiaux
		self.E = []		# tableau des etats
		self.F = []		# etats finaux
		self.V = []		# alpabet entrée
		self.O = []		# alpabet sortie
		self.M = "#"

		self.initLog()
		with open(filepath, "r") as f:
			check = self.check_file(f)
			if check != 0:
				exit(check)
		with open(filepath, "r") as f:
			self.init(f)

	# initialize the log file : Automate.log
	def initLog(self):
		with open(pathAutomateLogFile, "w") as logFile:
			logFile.write("")

	# ckeck if there are all lines
	def check_file(self, f):
		cmpt = 0
		state_checker = 0
		hasLine = {
			0 : False,
			1 : False,
			2 : False,
			3 : False,
			4 : False,
			5 : False,
			6 : False,
			7 : False
		}
		typeLine = {
			0 : "C",
			1 : "M",
			2 : "V",
			3 : "O",
			4 : "E",
			5 : "I",
			6 : "F",
			7 : "T"
		}
		for l in f:
			if l[0] =="C" and state_checker < 1:
				state_checker = 1
				hasLine[state_checker-1] = True
			elif l[0] == "M" and state_checker < 2:
				state_checker = 2
				hasLine[state_checker-1] = True
			elif l[0] == "V" and state_checker < 3:
				state_checker = 3
				hasLine[state_checker-1] = True
			elif l[0] == "O" and state_checker == 3:
				state_checker = 4
				hasLine[state_checker-1] = True
			elif l[0] == "E" and state_checker >= 3 and state_checker <= 4:
				state_checker = 5
				hasLine[state_checker-1] = True
			elif l[0] == "I" and state_checker == 5:
				state_checker = 6
				hasLine[state_checker-1] = True
			elif l[0] == "F" and state_checker >= 5 and state_checker <= 6:
				state_checker = 7
				hasLine[state_checker-1] = True
			elif l[0] == "T" and state_checker == 7:
				state_checker = 8
				hasLine[state_checker-1] = True
			elif state_checker == 8 and l[0] != "T" :
				hasLine[state_checker-1] = False
			cmpt += 1
			
		for i in range (len(hasLine)):
			if not hasLine[i]:
				if i == 2 or i == 4 or i == 6:
					self.logWrite(">Error< there is no line {}\n".format(typeLine[i]))
					return 50+i
				else:
					self.logWrite("Warning there is no line {}\n".format(typeLine[i]))
		return 0

	# create the automaton, and ckeck the syntaxe with regex
	def init(self, f):
		cmpt = 0
		for line in f:
			cmpt += 1
			if re.match(r"^C\s+", line):
				pass
			elif re.match(r"^M\s+(.)\s*$", line):
				groups = re.match(r"^M\s+(.)\s*$", line)
				self.M = groups.group(1)

			elif re.match(r"^V\s+\"(\S+)\"\s*$", line):
				groups = re.match(r"^V\s+\"(\S+)\"\s*$", line)
				for a in groups.group(1):
					self.V.append(a)

			elif re.match(r"^O\s+\"(\S+)\"\s*$", line):
				groups = re.match(r"^O\s+\"(\S+)\"\s*$", line)
				for a in groups.group(1):
					self.O.append(a)

			elif re.match(r"^E\s+(\d+)\s*$", line):
				groups = re.match(r"^E\s+(\d+)\s*$", line)
				for nb in range(int(groups.group(1))):
					self.E.append(Etat(nb))

			elif re.match(r"^I\s+(?P<init>\d+(?:\s+\d+)*)\s*$",line):
				groups = re.match(r"^I\s+(?P<init>\d+(?:\s+\d+)*)\s*$",line)
				self.I = []
				for nb in re.split("\s", groups.group("init")):
					self.I.append(int(nb))

			elif re.match(r"F\s+(?P<final>\d*(?:\s+\d+)*)\s*$",line):
				groups = re.match(r"^F\s+(?P<final>\d*(?:\s+\d+)*)\s*$",line)
				for nb in re.split("\s", groups.group("final")):
					self.F.append(int(nb))

			elif re.match(r"^T\s+(?P<etatOrigine>\d+)\s+'(?P<v>.)'\s+(?P<etatSortie>\d+)(\s+'(?P<o>.)')?\s*$",line):
				groups = re.match(r"^T\s+(?P<etatOrigine>\d+)\s+'(?P<v>.)'\s+(?P<etatSortie>\d+)(\s+'(?P<o>.)')?\s*$",line)
				e1 = groups.group("etatOrigine")
				e2 = groups.group("etatSortie")
				a1 = groups.group("v")
				a2 = groups.group("o")
				if a2 == None:
					a2 = '#'
				if a1 == None:
					a1 = self.M
				if a2 == None:
					a2 = self.M
				if (a2  == '#' and a1 == '#'):
					self.E[int(e1)].hasLambdaTrans = True
				self.E[int(e1)].addTransition(a1, int(e2), a2)

			else:
				self.logWrite("Error line {} ; bad description file ; {}\n".format(cmpt, line))

	# write log : automate.log
	def logWrite(self , ch):
		with open(pathAutomateLogFile, "a+") as logFile:
			logFile.write(str(ch))

	# toDot function
	def toDot(self,name):
		file = open("dotImage/"+name,"w")
		file.write("digraph automate {\n")
		for state_nb in self.I:
			file.write("\t{} [peripheries=2];\n".format(state_nb))
		for state_nb in self.F:
			file.write("\t{} [color=black, style=filled, fontcolor=white];\n".format(state_nb))
		for state in self.E:
			for transition in state.transitions:
				dep = state.name
				arr = transition.e
				file.write("\t{} -> {} [label=\"{}/{}\"];\n".format(dep, arr, transition.v, transition.o))
		file.write("}")


	# Getters
	def getStates(self, sArray):
		stateArray = []
		for state in sArray:
			stateArray.append(self.E[state])
		return stateArray
		
	def getInitialStates(self):
		return self.getStates(self.I)
		

	### DETERMINISE ###

	# get lambda closure
	def getLambdaClosure(self , origineStates):
		p = self.getStates(origineStates)
		lClosure = []
		while len(p) != 0:
			state = p.pop(0)
			if state not in lClosure:
				lClosure.append(state)
				for lTransition in state.getLambdaT():
					p.append(self.E[lTransition.e])
		return lClosure

	# transit function
	def transiter(self, T, a):
		F = list()
		rw = list()
		for t in T:
			trans = t.getTransition(a)
			if (len(trans) > 0):
				for p in trans:
					rw.append((p.v, p.o))

					if p.e not in F:
						F.append(p.e)

		if len(rw) == 0:
			rw.append((a,'#'))
		return F, rw

	# determinise function
	def determinise(self):
		p = [self.getLambdaClosure(self.I)]
		L = [] # tous les états
		D = [] # toutes les transition
		while len(p) != 0:
			stateBundle = p.pop(0)  # groupe d'états
			if stateBundle not in L:
				L.append(stateBundle)
				for alpha in self.V:
					F, rw = self.transiter(stateBundle, alpha)
					newStates = self.getLambdaClosure(F)
					if newStates in L:
						D.append([stateBundle, rw[0][0], rw[0][1] , L[L.index(newStates)]])
					elif newStates in p:
						D.append([stateBundle, rw[0][0], rw[0][1], p[p.index(newStates)]])
					else:
						D.append([stateBundle, rw[0][0], rw[0][1] , newStates])
						p.append(newStates)
		self.determiniseToFile(L, D)
		return Automate(pathToDeterminised)
		
	# create the new deterministic automaton : generatedAutomate.descr
	def determiniseToFile(self, L, D):
		cmpt = 1
		for etats in L:
			if etats == []:
				etats.append([0, False, False]) # 0 et le numéro par du puits
			else:
				etats.append([cmpt, False, False])
				cmpt+=1
			for initial in self.getInitialStates():
				if initial in etats:
					etats[-1][1] = True
			for final in self.getStates(self.F):
				if final in etats:
					etats[-1][2] = True

		with open(pathToDeterminised, "w+") as g:
			g.write("C Autogenerated File, from determinise call\n")
			g.write("V \"")
			for v in self.V:
				g.write(v)
			g.write("\"\n")
			if len(self.O) != 0:
				g.write("O \"")
				for o in self.O:
					g.write(o)
				g.write("\"\n")
			g.write("E {}\n".format(len(L)+1))
			init = "I"
			final = "F"
			for etats in L:
				if etats[-1][1]:
					init += " {}".format(etats[-1][0])
				if etats[-1][2]:
					final += " {}".format(etats[-1][0])
			g.write(init+"\n")
			g.write(final+"\n")
			for t in D:
				if t[3] != []:
					#g.write("T {} '{}' {} '{}'\n".format(t[0][-1][0], t[1], t[3][-1][0], t[2]))
					g.write("T {} '{}' {} '{}'\n".format(t[0][-1][0], t[1], t[3][-1][0], t[2]))
				else:
					g.write("T {} '{}' {} '{}'\n".format(t[0][-1][0], t[1], 0, t[2]))		
