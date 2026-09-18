# Two constructions of finite-time blowup for the same forced Navier–Stokes vortex

First draft of a mathematical paper, 18 September 2026.

## Compile

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

If `latexmk` is unavailable:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Contents

The manuscript is split across:

| File | Section |
| --- | --- |
| `main.tex` | Preamble, title, abstract, table of contents |
| `macros.tex` | Notation |
| `sec_intro.tex` | Introduction |
| `sec_setup.tex` | Residual calculus, energy, rescaling, periodisation |
| `sec_model.tex` | Common inner model and scaling lemmas |
| `sec_methodI.tex` | Oscillatory residual-stress realisation |
| `sec_methodII.tex` | Certified similarity dynamics |
| `sec_comparison.tex` | Comparison of the two cores |
| `sec_remarks.tex` | Euler, viscosity, open problems |
| `sec_appendix.tex` | Heat exterior, axis profiles, stress cone |
| `references.bib` | Bibliography |

## Status of the draft

Complete proofs are given for the Clay residual criterion, energy bound, viscosity rescaling, periodisation, inner-model geometry, and localisation from rest. The two blowup constructions are written as complete schemes. Their remaining high-order estimates are isolated as Assumption A (pulse iteration) and Assumption B (profile remainder), which a later version must expand.

The paper addresses Clay alternatives (C) and (D) (smooth forced blowup). It does not address unforced Navier–Stokes (A) and (B).
