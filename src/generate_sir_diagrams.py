#!/usr/bin/env python3
"""
Generate visual diagrams for Section 4 (SIR Model Framework)

Creates:
1. SIR state transition diagram with predicate logic annotations
2. Algorithm flowchart
3. Parameter justification visualization

Usage:
    python generate_sir_diagrams.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np


def create_sir_state_diagram(filename='figures/sir_state_diagram.png'):
    """
    Create a visual state transition diagram for the SIR model.
    Shows S → I → R with transition probabilities and predicate logic.
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    fig.text(0.5, 0.95, 'SIR Model: State Transitions with Predicate Logic',
            ha='center', fontsize=18, fontweight='bold')
    
    # Define state positions
    states = {
        'S': (2, 5),
        'I': (5, 5),
        'R': (8, 5)
    }
    
    # Draw states as circles
    state_radius = 0.6
    state_colors = {
        'S': '#457B9D',  # Blue - susceptible
        'I': '#E63946',  # Red - infected
        'R': '#06A77D'   # Green - recovered
    }
    
    state_labels = {
        'S': 'Susceptible\n(S)',
        'I': 'Infected\n(I)',
        'R': 'Recovered\n(R)'
    }
    
    state_descriptions = {
        'S': 'Healthy\nNo immunity\nCan be infected',
        'I': 'Infectious\nCan transmit\nto neighbors',
        'R': 'Immune\nTerminal state\nNo transmission'
    }
    
    for state, (x, y) in states.items():
        # Draw state circle
        circle = Circle((x, y), state_radius, color=state_colors[state], 
                       alpha=0.7, ec='black', linewidth=3)
        ax.add_patch(circle)
        
        # State label
        ax.text(x, y + 0.1, state_labels[state], ha='center', va='center',
               fontsize=16, fontweight='bold', color='white')
        
        # Description below
        ax.text(x, y - 1.2, state_descriptions[state], ha='center', va='top',
               fontsize=10, style='italic', 
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # Draw transitions (arrows)
    arrow_y = 5
    arrow_props = dict(arrowstyle='->', lw=4, color='black', 
                      connectionstyle="arc3,rad=0")
    
    # S → I transition
    arrow1 = FancyArrowPatch((states['S'][0] + state_radius, arrow_y),
                            (states['I'][0] - state_radius, arrow_y),
                            **arrow_props)
    ax.add_patch(arrow1)
    
    # Transition label (above arrow)
    ax.text(3.5, 6.2, r'Infection', ha='center', fontsize=13, 
           fontweight='bold', color='darkred')
    ax.text(3.5, 5.7, r'$P = 1 - (1-\beta)^{k_I}$', ha='center', 
           fontsize=12, family='monospace',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='mistyrose', alpha=0.9))
    
    # I → R transition
    arrow2 = FancyArrowPatch((states['I'][0] + state_radius, arrow_y),
                            (states['R'][0] - state_radius, arrow_y),
                            **arrow_props)
    ax.add_patch(arrow2)
    
    # Transition label (above arrow)
    ax.text(6.5, 6.2, r'Recovery', ha='center', fontsize=13, 
           fontweight='bold', color='darkgreen')
    ax.text(6.5, 5.7, r'$P = \gamma$', ha='center', fontsize=12,
           family='monospace',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.9))
    
    # Add predicate logic rules at bottom
    logic_y = 2.5
    
    # Box for infection rule
    infection_rule = (
        r"$\forall y \ ((\mathrm{Susceptible}(y,t) \land "
        r"(\exists x \ \mathrm{Infected}(x,t) \land \mathrm{Neighbor}(x,y)))$"
        r"\n"
        r"$\rightarrow P(\mathrm{Infected}(y, t+1)) = 1-(1-\beta)^{k_I})$"
    )
    
    ax.text(3.5, logic_y, 'Infection Rule:', ha='center', fontsize=11, 
           fontweight='bold', color='darkred')
    ax.text(3.5, logic_y - 0.6, infection_rule, ha='center', fontsize=9,
           family='monospace',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFE6E6', alpha=0.9))
    
    # Box for recovery rule
    recovery_rule = (
        r"$\forall x \ (\mathrm{Infected}(x,t)$"
        r"\n"
        r"$\rightarrow P(\mathrm{Recovered}(x, t+1)) = \gamma)$"
    )
    
    ax.text(6.5, logic_y, 'Recovery Rule:', ha='center', fontsize=11, 
           fontweight='bold', color='darkgreen')
    ax.text(6.5, logic_y - 0.6, recovery_rule, ha='center', fontsize=9,
           family='monospace',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#E6FFE6', alpha=0.9))
    
    # Add parameter definitions
    param_text = (
        r"Parameters:" + "\n"
        r"β = transmission probability" + "\n"
        r"γ = recovery probability" + "\n"
        r"$k_I$ = number of infected neighbors"
    )
    
    ax.text(9.5, 8, param_text, ha='right', va='top', fontsize=10,
           bbox=dict(boxstyle='round,pad=0.8', facecolor='wheat', alpha=0.8),
           family='monospace')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Created SIR state diagram: {filename}")
    plt.close()


def create_algorithm_flowchart(filename='figures/sir_algorithm_flowchart.png'):
    """
    Create a flowchart showing the simulation algorithm structure.
    """
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 18)
    ax.axis('off')
    
    # Title
    fig.text(0.5, 0.98, 'SIR Simulation Algorithm Flowchart',
            ha='center', fontsize=18, fontweight='bold')
    
    # Box drawing helper
    def draw_box(x, y, width, height, text, color, shape='round'):
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                            boxstyle=f'{shape},pad=0.1',
                            facecolor=color, edgecolor='black', 
                            linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10,
               fontweight='bold', wrap=True)
    
    def draw_arrow(x1, y1, x2, y2, label=''):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle='->', lw=2, color='black',
                               mutation_scale=20)
        ax.add_patch(arrow)
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.5, mid_y, label, fontsize=9, 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white'))
    
    # Flowchart elements
    y = 16.5
    x_center = 5
    
    # Start
    draw_box(x_center, y, 2, 0.8, 'START', '#90EE90', 'round')
    y -= 1.2
    draw_arrow(x_center, y + 1.2, x_center, y + 0.4)
    
    # Initialize
    draw_box(x_center, y, 3.5, 1.2, 
            'Initialize Network G\nSet all nodes to SUSCEPTIBLE', 
            '#ADD8E6', 'round')
    y -= 1.6
    draw_arrow(x_center, y + 1.6, x_center, y + 0.6)
    
    # Select patient zero
    draw_box(x_center, y, 3.5, 1.0,
            'Select random node\nSet to INFECTED (patient zero)',
            '#FFE4B5', 'round')
    y -= 1.4
    draw_arrow(x_center, y + 1.4, x_center, y + 0.5)
    
    # Initialize time
    draw_box(x_center, y, 2, 0.8, 't ← 0', '#E6E6FA', 'round')
    y -= 1.2
    draw_arrow(x_center, y + 1.2, x_center, y + 0.4)
    
    # Main loop start (decision diamond)
    decision_y = y
    diamond_points = [(x_center, y + 0.6), (x_center + 1, y), 
                     (x_center, y - 0.6), (x_center - 1, y)]
    diamond = mpatches.Polygon(diamond_points, closed=True,
                              facecolor='#FFD700', edgecolor='black',
                              linewidth=2, alpha=0.8)
    ax.add_patch(diamond)
    ax.text(x_center, y, 'I(t) > 0?', ha='center', va='center',
           fontsize=11, fontweight='bold')
    
    # No branch (end)
    draw_arrow(x_center + 1, y, x_center + 3, y)
    draw_box(x_center + 4.5, y, 2, 0.8, 'END', '#FFB6C1', 'round')
    ax.text(x_center + 2, y + 0.3, 'No', fontsize=10, fontweight='bold')
    
    # Yes branch (continue)
    y -= 1.2
    draw_arrow(x_center, decision_y - 0.6, x_center, y + 0.8)
    ax.text(x_center - 0.5, decision_y - 0.9, 'Yes', fontsize=10, fontweight='bold')
    
    # Process infections
    draw_box(x_center, y, 3.8, 1.4,
            'For each SUSCEPTIBLE node:\n' + 
            r'Count infected neighbors $k_I$' + '\n' +
            r'If rand() < $1-(1-\beta)^{k_I}$:' + '\n' +
            '  Mark for infection',
            '#FFCCCC', 'round')
    y -= 1.8
    draw_arrow(x_center, y + 1.8, x_center, y + 0.7)
    
    # Process recoveries
    draw_box(x_center, y, 3.8, 1.2,
            'For each INFECTED node:\n' +
            r'If rand() < $\gamma$:' + '\n' +
            '  Mark for recovery',
            '#CCFFCC', 'round')
    y -= 1.6
    draw_arrow(x_center, y + 1.6, x_center, y + 0.6)
    
    # Apply updates
    draw_box(x_center, y, 3.8, 1.0,
            'Apply all marked state changes\n(Synchronous update)',
            '#CCCCFF', 'round')
    y -= 1.4
    draw_arrow(x_center, y + 1.4, x_center, y + 0.5)
    
    # Record data
    draw_box(x_center, y, 3.5, 1.0,
            'Record S(t), I(t), R(t)\nt ← t + 1',
            '#E6E6FA', 'round')
    y -= 1.4
    draw_arrow(x_center, y + 1.4, x_center, y + 0.5)
    
    # Loop back
    draw_arrow(x_center, y, x_center - 2.5, y)
    draw_arrow(x_center - 2.5, y, x_center - 2.5, decision_y)
    draw_arrow(x_center - 2.5, decision_y, x_center - 1, decision_y)
    
    # Add note box
    note_text = (
        "Key Implementation Details:\n\n"
        "• Synchronous updates prevent\n  order-dependent artifacts\n\n"
        "• Infection depends on network\n  structure (neighbors)\n\n"
        "• Recovery is independent\n  of neighbors"
    )
    ax.text(1, 8, note_text, ha='left', va='center', fontsize=9,
           bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', 
                    edgecolor='orange', linewidth=2, alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Created algorithm flowchart: {filename}")
    plt.close()


def create_parameter_justification(filename='figures/sir_parameters.png'):
    """
    Create a visual explanation of parameter choices.
    """
    fig = plt.figure(figsize=(14, 10))
    
    # Title
    fig.text(0.5, 0.96, 'SIR Model Parameters: Choices and Justifications',
            ha='center', fontsize=18, fontweight='bold')
    
    # Create grid for parameter cards
    params = [
        {
            'name': r'Network Size: $N = 5000$',
            'color': '#E3F2FD',
            'reasons': [
                '✓ Large enough for statistical robustness',
                '✓ Exhibits emergent network phenomena',
                '✓ Computationally tractable (100 runs feasible)',
                '✓ Representative of real communities',
                '✓ Allows clear observation of hubs and clusters'
            ],
            'position': (0.08, 0.65, 0.28, 0.25)
        },
        {
            'name': r'Average Degree: $\langle k \rangle = 10$',
            'color': '#F3E5F5',
            'reasons': [
                '✓ Moderate connectivity (not sparse/dense)',
                '✓ Consistent with real contact networks',
                '✓ Same across all topologies (fair comparison)',
                '✓ Enables meaningful epidemic dynamics',
                '✓ Typical of social networks (Dunbar estimate)'
            ],
            'position': (0.38, 0.65, 0.28, 0.25)
        },
        {
            'name': r'Transmission: $\beta = 0.05$',
            'color': '#FFEBEE',
            'reasons': [
                '✓ 5% per-contact transmission (moderate)',
                '✓ Ensures R₀ > 1 (viable epidemic)',
                '✓ Not too high (allows structure effects)',
                '✓ Similar to respiratory infections',
                '✓ Low enough for stochastic variation'
            ],
            'position': (0.68, 0.65, 0.28, 0.25)
        },
        {
            'name': r'Recovery: $\gamma = 0.1$',
            'color': '#E8F5E9',
            'reasons': [
                '✓ Average infectious period: 10 days',
                '✓ Realistic for viral infections',
                '✓ γ = 2β (recovery faster than transmission)',
                '✓ Allows multi-hop spread before recovery',
                '✓ Standard epidemiological timescale'
            ],
            'position': (0.08, 0.35, 0.28, 0.25)
        },
        {
            'name': r'Number of Runs: $100$',
            'color': '#FFF9C4',
            'reasons': [
                '✓ Accounts for network randomness',
                '✓ Accounts for patient zero variation',
                '✓ Accounts for transmission stochasticity',
                '✓ Produces smooth averaged curves',
                '✓ Standard for statistical significance'
            ],
            'position': (0.38, 0.35, 0.28, 0.25)
        },
        {
            'name': r'Basic Reproduction Number',
            'color': '#FFE0B2',
            'reasons': [
                r'$R_0 = \frac{\beta \langle k \rangle}{\gamma}$',
                r'$R_0 = \frac{0.05 \times 10}{0.1} = 5$',
                '',
                '✓ Well above threshold (R₀ > 1)',
                '✓ Ensures substantial outbreaks',
                '✓ Comparable to real diseases (flu~1.3, measles~15)'
            ],
            'position': (0.68, 0.35, 0.28, 0.25)
        }
    ]
    
    for param in params:
        x, y, w, h = param['position']
        
        # Draw box
        box = FancyBboxPatch((x, y), w, h,
                            boxstyle='round,pad=0.02',
                            transform=fig.transFigure,
                            facecolor=param['color'],
                            edgecolor='black',
                            linewidth=2,
                            alpha=0.8)
        fig.add_artist(box)
        
        # Title
        fig.text(x + w/2, y + h - 0.03, param['name'],
                ha='center', va='top', fontsize=13, fontweight='bold',
                transform=fig.transFigure)
        
        # Reasons
        reasons_text = '\n'.join(param['reasons'])
        fig.text(x + 0.02, y + h - 0.06, reasons_text,
                ha='left', va='top', fontsize=9,
                transform=fig.transFigure, family='monospace')
    
    # Bottom explanation box
    explanation = (
        "Design Principle: All parameters are chosen to create a controlled experiment where the ONLY variable\n"
        "changing across simulations is the network topology (ER vs WS vs BA). This isolates the effect of\n"
        "network structure on epidemic dynamics, allowing clear comparison of cascade behavior."
    )
    
    fig.text(0.5, 0.15, explanation,
            ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=1', facecolor='lightcyan', 
                     edgecolor='darkblue', linewidth=2, alpha=0.9),
            style='italic')
    
    # Comparison table
    table_data = [
        ['Topology', 'N', '⟨k⟩', 'β', 'γ', 'Runs'],
        ['ER (Random)', '5000', '10', '0.05', '0.1', '100'],
        ['WS (Small-World)', '5000', '10', '0.05', '0.1', '100'],
        ['BA (Scale-Free)', '5000', '10', '0.05', '0.1', '100']
    ]
    
    fig.text(0.5, 0.06, 'Parameter Consistency Across Topologies',
            ha='center', fontsize=12, fontweight='bold')
    
    # Simple table
    table_text = ''
    for row in table_data:
        table_text += '  '.join(f'{cell:>15}' for cell in row) + '\n'
    
    fig.text(0.5, 0.01, table_text,
            ha='center', va='bottom', fontsize=9, family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                     edgecolor='gray', linewidth=1))
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Created parameter justification: {filename}")
    plt.close()


def main():
    """Generate all Section 4 diagrams."""
    print("\n" + "="*70)
    print("GENERATING SECTION 4 DIAGRAMS")
    print("="*70 + "\n")
    
    create_sir_state_diagram()
    create_algorithm_flowchart()
    create_parameter_justification()
    
    print("\n" + "="*70)
    print("✓ All Section 4 diagrams generated successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
