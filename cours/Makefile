# Chapitre 2 — Fonction d'une variable réelle (Beamer)
# Usage : make        (depuis ce dossier)
#         make clean

MAIN = Chapitre2_Fonction_variable_reelle
LATEX = pdflatex
FLAGS = -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex munidia.png honoris.jpg
	$(LATEX) $(FLAGS) $(MAIN).tex
	$(LATEX) $(FLAGS) $(MAIN).tex

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).nav $(MAIN).out \
	      $(MAIN).snm $(MAIN).toc $(MAIN).vrb $(MAIN).fls \
	      $(MAIN).fdb_latexmk $(MAIN).synctex.gz
