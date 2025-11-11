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
├── paper.tex                    # Main LaTeX paper
├── paper.pdf                    # Compiled PDF (generated)
├── Makefile                     # Build automation
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── figures/                     # Generated visualizations
│   ├── phase_transition_*.png           # Section 3.1: ER phase transition
│   ├── ws_*.png                         # Section 3.2: WS diagrams
│   ├── small_world_*.png                # Section 3.2: WS analysis
│   ├── ba_*.png                         # Section 3.3: BA analysis
│   ├── sir_state_diagram.png            # Section 4: SIR model
│   ├── sir_algorithm_flowchart.png      # Section 4: Algorithm
│   ├── sir_parameters.png               # Section 4: Parameters
│   ├── sir_r0_validation.png            # Section 4: R₀ calculation
│   ├── sir_epidemic_curves.png          # Section 4: Main results
│   └── sir_infected_comparison.png      # Section 4: Comparison
└── src/                         # Python simulation scripts
    ├── generate_all_figures.py          # Master script (runs all)
    ├── generate_phase_transition.py     # Section 3.1
    ├── generate_ws_diagrams.py          # Section 3.2 (diagrams)
    ├── generate_small_world_analysis.py # Section 3.2 (analysis)
    ├── generate_ba_analysis.py          # Section 3.3
    ├── generate_sir_diagrams.py         # Section 4 (diagrams)
    ├── generate_sir_simulation.py       # Section 4 (simulations)
    └── test_sir_simulation.py           # Quick test (5 runs)
```

## Prerequisites

### For LaTeX Compilation

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required LaTeX packages (usually included):
  - amsmath, amssymb, graphicx, subcaption
  - hyperref, enumitem, multicol, caption
  - authblk, times, titlesec

### For Python Simulations

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
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

### Option 1: Quick Start (Using Makefile) ⭐ **RECOMMENDED**

The easiest way to generate everything:

```bash
make all          # Generate all figures and compile PDF
make view         # Compile and open PDF (macOS)
make help         # Show all available commands
```

### Option 2: Generate Specific Sections

```bash
make figures-section3    # Generate only Section 3 figures
make figures-section4    # Generate only Section 4 figures
```

### Option 3: Individual Figure Generation (for debugging)

```bash
make figures-phase            # ER phase transition
make figures-ws               # WS network diagrams
make figures-small-world      # WS analysis
make figures-ba               # BA analysis
make figures-sir-diagrams     # SIR model diagrams
make figures-sir-simulation   # SIR simulations (⚠️ takes ~10-15 min)
```

### Option 4: Manual Python Execution

#### Generate All Figures (Master Script)

```bash
python src/generate_all_figures.py
```

#### Or Generate by Section

```bash
# Section 3: Network Topologies
python src/generate_phase_transition.py
python src/generate_ws_diagrams.py
python src/generate_small_world_analysis.py
python src/generate_ba_analysis.py

# Section 4: SIR Simulation Framework
python src/generate_sir_diagrams.py
python src/generate_sir_simulation.py  # ⚠️ Takes 10-15 minutes
```

#### Quick Test (Before Full Simulation)

```bash
# Test SIR simulation with reduced parameters (5 runs instead of 100)
python src/test_sir_simulation.py
# If test results look good, run the full simulation
```

## Script Details

### Section 3: Network Topologies

#### `generate_phase_transition.py`
- **Purpose**: Visualize ER random graph phase transition
- **Runtime**: ~30 seconds
- **Generates**:
  - `phase_transition_lambda_*.png` (5 network snapshots)
  - `phase_transition_curve.png` (quantitative curve)

#### `generate_ws_diagrams.py`
- **Purpose**: WS ring lattice and rewired network diagrams
- **Runtime**: ~20 seconds
- **Generates**:
  - `ws_ring_lattice.png`
  - `ws_rewired_network.png`

#### `generate_small_world_analysis.py`
- **Purpose**: Comprehensive WS small-world transition analysis
- **Runtime**: ~2-3 minutes
- **Generates**:
  - `small_world_transition.png`
  - `absolute_metrics.png`
  - `phase_space_trajectory.png`
  - `small_world_metric.png`

#### `generate_ba_analysis.py`
- **Purpose**: Complete BA scale-free network analysis
- **Runtime**: ~2-3 minutes
- **Generates**:
  - `ba_degree_evolution.png` (preferential attachment)
  - `ba_degree_distribution.png` (power law vs Poisson)
  - `ba_network_*.png` (ER/WS/BA comparison)
  - `ba_hub_dominance.png`
  - `ba_attack_simulation.png`
  - `ba_epidemic_threshold.png`

### Section 4: SIR Simulation Framework

#### `generate_sir_diagrams.py`
- **Purpose**: Create explanatory diagrams for SIR model
- **Runtime**: ~10 seconds
- **Generates**:
  - `sir_state_diagram.png` (S→I→R with predicate logic)
  - `sir_algorithm_flowchart.png` (algorithm steps)
  - `sir_parameters.png` (parameter justifications)

#### `generate_sir_simulation.py` ⚠️ **LONG RUNTIME**
- **Purpose**: Run complete SIR epidemic simulations
- **Runtime**: ~10-15 minutes (100 runs × 3 topologies)
- **Parameters**: N=5000, ⟨k⟩=10, β=0.05, γ=0.1, runs=100
- **Generates**:
  - `sir_r0_validation.png` (R₀ calculation diagram)
  - `sir_epidemic_curves.png` (S/I/R curves for all topologies)
  - `sir_infected_comparison.png` (infected curves comparison)
- **Progress**: Shows progress bar with tqdm

#### `test_sir_simulation.py` ✅ **QUICK TEST**
- **Purpose**: Fast test version of SIR simulation
- **Runtime**: ~30 seconds (5 runs × 3 topologies)
- **Parameters**: N=500, runs=5 (reduced)
- **Use**: Verify implementation before running full simulation

## Compilation

### Compile PDF from LaTeX

```bash
pdflatex paper.tex
pdflatex paper.tex  # Run twice for references
```

Or use Makefile:

```bash
make pdf
```

### View PDF (macOS)

```bash
make view
```

Or manually:

```bash
open paper.pdf
```
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
