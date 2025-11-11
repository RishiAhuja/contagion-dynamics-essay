# Makefile for compiling the academic paper

# Variables
PAPER = paper
PYTHON = python3
SRC_DIR = src
FIG_DIR = figures

# Default target
all: figures pdf

# Generate all figures (using master script)
figures:
	@echo "Generating all figures using master script..."
	$(PYTHON) $(SRC_DIR)/generate_all_figures.py

# Generate figures for specific sections
figures-section3:
	@echo "Generating Section 3 figures only..."
	$(PYTHON) $(SRC_DIR)/generate_all_figures.py --section 3

figures-section4:
	@echo "Generating Section 4 figures only..."
	$(PYTHON) $(SRC_DIR)/generate_all_figures.py --section 4

# Individual figure generation scripts (for debugging)
figures-phase:
	@echo "Generating phase transition visualizations..."
	$(PYTHON) $(SRC_DIR)/generate_phase_transition.py

figures-ws:
	@echo "Generating Watts-Strogatz diagrams..."
	$(PYTHON) $(SRC_DIR)/generate_ws_diagrams.py

figures-small-world:
	@echo "Generating small-world transition analysis..."
	$(PYTHON) $(SRC_DIR)/generate_small_world_analysis.py

figures-ba:
	@echo "Generating Barabási-Albert analysis..."
	$(PYTHON) $(SRC_DIR)/generate_ba_analysis.py

figures-sir-diagrams:
	@echo "Generating SIR model diagrams..."
	$(PYTHON) $(SRC_DIR)/generate_sir_diagrams.py

figures-sir-simulation:
	@echo "Generating SIR simulation results..."
	$(PYTHON) $(SRC_DIR)/generate_sir_simulation.py

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
	@echo "  all                  - Generate figures and compile PDF (default)"
	@echo "  figures              - Generate all visualizations (all sections)"
	@echo "  figures-section3     - Generate Section 3 figures only"
	@echo "  figures-section4     - Generate Section 4 figures only"
	@echo "  figures-phase        - Generate phase transition diagrams only"
	@echo "  figures-ws           - Generate WS network diagrams only"
	@echo "  figures-small-world  - Generate small-world analysis only"
	@echo "  figures-ba           - Generate BA analysis only"
	@echo "  figures-sir-diagrams - Generate SIR model diagrams only"
	@echo "  figures-sir-simulation - Generate SIR simulation results only"
	@echo "  pdf                  - Compile LaTeX to PDF"
	@echo "  clean                - Remove auxiliary LaTeX files"
	@echo "  cleanall             - Remove all generated files (PDF + figures)"
	@echo "  view                 - Compile and open PDF (macOS)"
	@echo "  rebuild              - Clean everything and rebuild from scratch"
	@echo "  help                 - Show this help message"

.PHONY: all figures figures-section3 figures-section4 figures-phase figures-ws \
        figures-small-world figures-ba figures-sir-diagrams figures-sir-simulation \
        pdf clean cleanall view rebuild help
