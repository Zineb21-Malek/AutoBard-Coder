# Chapitre 1 — Les suites réelles (module M114)

Support LaTeX pour le cours de **Mathématiques appliquées à la gestion**, Licence MGE, semestre 1, Université Mundiapolis Business School (Pr. Rajae Malek).

## Fichiers

| Fichier | Contenu |
| --- | --- |
| `Chapitre1_Suites_reelles_Cours.tex` | Support de cours (définitions, théorèmes, exemples de gestion) |
| `Chapitre1_Suites_reelles_TD3h.tex` | Travaux dirigés calés sur **3 heures** |
| `Chapitre1_Suites_reelles_Exercices.tex` | Feuille d'entraînement / travail personnel |
| `Chapitre1_Suites_reelles_Corrections.tex` | Corrigés détaillés (TD + exercices + applications du cours) |
| `preambule-mge.tex` | Préambule commun (charte, boîtes pédagogiques) |

## Compilation

Depuis ce dossier, avec une distribution TeX Live récente :

```bash
latexmk -pdf Chapitre1_Suites_reelles_Cours.tex
latexmk -pdf Chapitre1_Suites_reelles_TD3h.tex
latexmk -pdf Chapitre1_Suites_reelles_Exercices.tex
latexmk -pdf Chapitre1_Suites_reelles_Corrections.tex
```

Ou simplement : `make`.
