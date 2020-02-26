def toDot(automate):
	file = open("Graph.dot","w")
	file.write("digraph automate {")
	for state in automate.E:
		for transition in state.transitions:
			dep = transition.v
			arr = transition.o
			file.write("{} -> {};".format(v,o))
	file.write("}")