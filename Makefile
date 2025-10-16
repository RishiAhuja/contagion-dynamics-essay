# Makefile for compiling the academic paper

# Variables
PAPER = paper
PYTHON = python3
SRC_DIR = src
FIG_DIR = figures

# Default target
all: figures pdf

# Generate all figures
figures:
	@echo "Generating phase transition visualizations..."
	$(PYTHON) $(SRC_DIR)/generate_phase_transition.py

# Compile PDF
pdf:
	@echo "Compiling LaTeX document..."
	pdflatex $(PAPER).tex
	pdflatex $(PAPER).tex  # Run twice for references

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	rm -f $(PAPER).aux $(PAPER).log $(PAPER).out $(PAPER).toc
	rm -f $(PAPER).bbl $(PAPER).blg $(PAPER).synctex.gz
	rm -f $(PAPER).fdb_latexmk $(PAPER).fls

# Clean everything including PDF and figures
cleanall: clean
	@echo "Cleaning PDF and figures..."
	rm -f $(PAPER).pdf
	rm -rf $(FIG_DIR)/*.png

# View the PDF (macOS)
view: pdf
	@echo "Opening PDF..."
	open $(PAPER).pdf

# Full rebuild
rebuild: cleanall all

# Help message
help:
	@echo "Available targets:"
	@echo "  all       - Generate figures and compile PDF (default)"
	@echo "  figures   - Generate all visualizations"
	@echo "  pdf       - Compile LaTeX to PDF"
	@echo "  clean     - Remove auxiliary LaTeX files"
	@echo "  cleanall  - Remove all generated files (PDF + figures)"
	@echo "  view      - Compile and open PDF (macOS)"
	@echo "  rebuild   - Clean everything and rebuild from scratch"
	@echo "  help      - Show this help message"

.PHONY: all figures pdf clean cleanall view rebuild help
