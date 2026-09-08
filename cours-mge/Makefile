# Compile les quatre documents du chapitre 1 (suites réelles)
TEX = latexmk
FLAGS = -pdf -interaction=nonstopmode -halt-on-error

SOURCES = \
	Chapitre1_Suites_reelles_Cours.tex \
	Chapitre1_Suites_reelles_TD3h.tex \
	Chapitre1_Suites_reelles_Exercices.tex \
	Chapitre1_Suites_reelles_Corrections.tex

.PHONY: all clean

all: $(SOURCES:.tex=.pdf)

%.pdf: %.tex preambule-mge.tex
	$(TEX) $(FLAGS) $<

clean:
	latexmk -C $(SOURCES)
