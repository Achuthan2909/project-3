#!/bin/bash

# Compile LaTeX paper
# Requires: pdflatex, bibtex (if using bibliography)

echo "Compiling paper.tex..."

# First pass
pdflatex -interaction=nonstopmode paper.tex

# BibTeX (if needed)
# bibtex paper

# Second pass for references
pdflatex -interaction=nonstopmode paper.tex

# Third pass to ensure everything is resolved
pdflatex -interaction=nonstopmode paper.tex

echo "Compilation complete. Check paper.pdf"

# Clean up auxiliary files (optional)
# rm -f paper.aux paper.log paper.out paper.bbl paper.blg


