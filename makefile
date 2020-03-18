entries_folder := entrees/
descr_folder := testMoteur/

DESCR_FILES := $(patsubst $(descr_folder)%.descr, %, $(wildcard $(descr_folder)*.descr))
AUTO_RULE := $(addprefix automate/,$(basename $(notdir $(wildcard $(descr_folder)*.descr))))

all: 
	@echo "Commandes : "
	@echo "   'graph' - génére un fichier png à partir de graph.dot"
	@echo "   'list'  - Liste des automates disponible"
	@echo "             s'utilise avec la commande make"
	@echo "             ex: make automate/AS"

list:
	@echo $(DESCR_FILES)

graph:
	dot -Tpng dotImage/graph.dot > dotImage/graph.png

$(AUTO_RULE): $(wildcard $(descr_folder)%.descr)
	python src/moteur.py $(descr_folder)$(notdir $@).descr $(entries_folder)$(notdir $@).txt
