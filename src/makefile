entries_folder := entrees/
descr_folder := testMoteur/
DESCR_FILES := $(patsubst $(descr_folder)%.descr, %, $(wildcard testMoteur/*.descr))

all: help

help:
	@echo "Fichier de log:"
	@echo "    - automate.log"
	@echo "    - moteur.log"
	@echo "Commandes : "
	@echo "   'all'   - génére un automate puis lance le moteur"
	@echo "   'test'  - génére un automate depuis un autre fichier"
	@echo "   'graph' - génére un fichier png à partir de graph.dot"
	@echo "   'list'  - Liste des automates disponible"
	@echo "             s'utilise avec la commande make"
	@echo "             ex: make AS"

list:
	@echo $(DESCR_FILES)

graph:
	dot -Tpng dotImage/graph.dot > dotImage/graph.png

%: $(wildcard $(descr_folder)%.descr)
	python code/moteur.py $(descr_folder)$@.descr $(entries_folder)$@.txt
