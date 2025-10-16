# A Graph-Theoretic Analysis of Contagion Dynamics on Simulated Network Topologies

A computational investigation into how network topology dictates the dynamics of contagion, using discrete mathematics and epidemiological models. **Professional two-column academic paper format.**

## Authors

- Rishi Ahuja (24124092)
- Anish Ranjan (24124015)
- Priyansh Kumar (24124086)
- Gaurav (24124034)
- Mohit Kumar (24124069)
- Hiten Janjua (24124041)

## Repository Structure

```
contagion-dynamics-essay/
├── paper.tex                    # Main LaTeX paper (single file)
├── paper.md                     # Markdown draft (work in progress)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── figures/                     # Generated figures and visualizations
│   ├── phase_transition_lambda_0.5.png
│   ├── phase_transition_lambda_0.8.png
│   ├── phase_transition_lambda_1.0.png
│   ├── phase_transition_lambda_1.2.png
│   ├── phase_transition_lambda_2.0.png
│   └── phase_transition_curve.png
├── src/                         # Python scripts for simulations
│   └── generate_phase_transition.py
└── sections/                    # LaTeX sections (optional organization)
    └── 01_introduction.tex
```

## Prerequisites

### For LaTeX Compilation

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required LaTeX packages (usually included):
  - amsmath
  - amssymb
  - graphicx
  - subcaption
  - hyperref
  - enumitem

### For Python Simulations

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
cd /path/to/your/workspace
git clone https://github.com/RishiAhuja/contagion-dynamics-essay
cd contagion-dynamics-essay
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Quick Start (Using Makefile)

The easiest way to generate figures and compile the paper:

```bash
make all          # Generate figures and compile PDF
make view         # Compile and open PDF (macOS)
make clean        # Remove auxiliary files
make help         # Show all available commands
```

### Manual Steps

#### Step 1: Generate Figures

Before compiling the paper, generate the phase transition visualizations:

```bash
python3 src/generate_phase_transition.py
```

This will:
1. Generate 5 network visualizations for λ = 0.5, 0.8, 1.0, 1.2, 2.0
2. Create a phase transition curve analysis
3. Save all figures to the `figures/` directory

**Expected output:**
```
============================================================
Generating Phase Transition Visualizations
============================================================
Network size: N = 250
Lambda values: [0.5, 0.8, 1.0, 1.2, 2.0]
============================================================

Generating network for λ = 0.5...
  Edge probability p = 0.002008
Saved: figures/phase_transition_lambda_0.5.png
  - Total nodes: 250
  - Total edges: ~62
  - Giant component size: ~15 (6%)

...
```

#### Step 2: Compile the Paper

##### Using pdflatex (recommended)

```bash
pdflatex paper.tex
pdflatex paper.tex  # Run twice for proper references
```

##### Using latexmk (automatic)

```bash
latexmk -pdf paper.tex
```

##### Using an IDE

- **Overleaf**: Upload all files including the `figures/` directory
- **TeXShop/TeXworks**: Open `paper.tex` and click "Typeset"
- **VS Code**: Use LaTeX Workshop extension

#### Step 3: View the Paper

After compilation, open `paper.pdf` in your PDF viewer.

## Project Overview

### Paper Format

The paper uses a **professional two-column academic format** with:
- 10pt font size optimized for readability
- Two-column layout (standard for conferences and journals)
- Professional title page with author affiliations
- Mathematical equations and formal notation
- IEEE/ACM-style references
- Figure spanning both columns for better visualization
- Structured sections with clear hierarchy

### Key Concepts Explored

1. **Graph Theory Fundamentals**
   - Nodes, edges, degree distribution
   - Path length and clustering coefficient
   - Network connectivity measures

2. **Network Topologies**
   - **Erdős-Rényi Random Networks**: Baseline null model
   - **Watts-Strogatz Small-World Networks**: Clustered social circles
   - **Barabási-Albert Scale-Free Networks**: Hub-dominated systems

3. **Phase Transition in Random Networks**
   - Subcritical phase (λ < 1): Fragmented network
   - Critical point (λ = 1): Emergence of giant component
   - Supercritical phase (λ > 1): Cohesive, connected network

4. **Epidemiological Modeling**
   - SIR (Susceptible-Infected-Recovered) model
   - Contagion dynamics on different topologies
   - Impact of network structure on epidemic spread

### Visualizations

The phase transition visualizations (Figure 1 in the paper) demonstrate:

- **λ = 0.5**: Disconnected archipelago of small clusters
- **λ = 0.8**: Growing components, still fragmented
- **λ = 1.0**: Critical point - giant component emerges
- **λ = 1.2**: Dominant giant component
- **λ = 2.0**: Nearly complete connectivity

Red nodes indicate membership in the giant component, gray nodes are in smaller isolated clusters.

## Development Workflow

### Adding New Content

1. **Draft in Markdown**: Write new sections in `paper.md`
2. **Convert to LaTeX**: Add the content to `paper.tex` with proper formatting
3. **Generate figures**: Create Python scripts in `src/` for any visualizations
4. **Update paper**: Reference figures using `\ref{fig:label}`

### Common LaTeX Commands Used

```latex
\section{Title}                  % Main section
\subsection{Title}               % Subsection
\subsubsection{Title}            % Sub-subsection

$inline math$                    % Inline equation
\[ display math \]               % Display equation

\textbf{bold text}               % Bold
\emph{emphasized}                % Italics

\begin{figure}...\end{figure}    % Figure environment
\label{fig:name}                 % Label for reference
\ref{fig:name}                   % Reference to label
```

## Troubleshooting

### LaTeX Issues

**Problem**: Missing figure warnings
```
LaTeX Warning: File `figures/phase_transition_lambda_0.5.png' not found
```
**Solution**: Run the Python script to generate figures first

**Problem**: Missing packages
```
! LaTeX Error: File `subcaption.sty' not found
```
**Solution**: Install the missing package via your LaTeX distribution's package manager

### Python Issues

**Problem**: Import errors
```
ModuleNotFoundError: No module named 'networkx'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

**Problem**: Permission errors when saving figures
**Solution**: Ensure the `figures/` directory exists or the script will create it

## Future Work

- [ ] Complete Watts-Strogatz small-world network section
- [ ] Complete Barabási-Albert scale-free network section
- [ ] Implement SIR epidemic simulations
- [ ] Add comparative analysis figures
- [ ] Include predicate logic formalization
- [ ] Add experimental results section
- [ ] Write conclusion and discussion

## Citation

If you use this work, please cite:

```bibtex
@article{ahuja2025contagion,
  title={A Graph-Theoretic Analysis of Contagion on Simulated Network Topologies},
  author={Ahuja, Rishi and Ranjan, Anish and Kumar, Priyansh and Gaurav and Kumar, Mohit and Janjua, Hiten},
  year={2025}
}
```

## Contact

For questions or collaboration:
- Primary Contact: Rishi Ahuja (24124092)
- Repository: https://github.com/RishiAhuja/contagion-dynamics-essay

---

**Last Updated**: October 14, 2025
