entries_folder := entrees/
descr_folder := testMoteur/


all:
	python code/moteur.py testMoteur/C0.descr entrees/entree.txt

test:
	python code/test.py
help:
	@echo "Fichier de log:"
	@echo "    - automate.log"
	@echo "    - moteur.log"
	@echo "Commandes : "
	@echo "   'all'      - génére un automate puis lance le moteur"
	@echo "   'test'  - génére un automate depuis un autre fichier"
	@echo "   'graph' - génére un fichier png à partir de graph.dot"

graph:
	dot -Tpng dotImage/graph.dot > dotImage/graph.png

	

