all:
	@echo "Rien a compiler pour le moment."
	@echo "'make help' pour connaitre les commande utile"

help:
	@echo "'graph' - génére un fichier png à partir de graph.dot"

graph:
	dot -Tpng graph.dot > graph.png


