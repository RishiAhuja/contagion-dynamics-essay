"""
Phase Transition Visualization for Erdős-Rényi Random Networks

This script generates visualizations of the phase transition in random networks,
showing the emergence of the giant component as the average degree λ crosses the
critical threshold of λ = 1.

Author: Network Analysis Team
Date: October 2025
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os


def generate_random_network(N, lambda_val):
    """
    Generate an Erdős-Rényi random network G(N, p).
    
    Parameters:
    -----------
    N : int
        Number of nodes in the network
    lambda_val : float
        Average degree (λ = p(N-1))
    
    Returns:
    --------
    G : networkx.Graph
        Generated random network
    p : float
        Edge probability used
    """
    # Calculate edge probability from average degree
    p = lambda_val / (N - 1)
    
    # Generate the random graph
    G = nx.erdos_renyi_graph(N, p, seed=42)
    
    return G, p


def find_giant_component(G):
    """
    Find the largest connected component (giant component) in the graph.
    
    Parameters:
    -----------
    G : networkx.Graph
        Input graph
    
    Returns:
    --------
    giant_component : set
        Set of nodes in the giant component
    """
    # Get all connected components
    components = list(nx.connected_components(G))
    
    # Find the largest one
    if components:
        giant_component = max(components, key=len)
    else:
        giant_component = set()
    
    return giant_component


def visualize_network(G, lambda_val, output_dir='figures'):
    """
    Visualize the network with giant component highlighted.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network to visualize
    lambda_val : float
        Average degree value (for labeling)
    output_dir : str
        Directory to save the figure
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find the giant component
    giant_component = find_giant_component(G)
    
    # Create node colors: red for giant component, gray for others
    node_colors = ['#d62728' if node in giant_component else '#7f7f7f' 
                   for node in G.nodes()]
    
    # Create layout using spring layout for aesthetic visualization
    # Use a fixed seed for reproducibility
    pos = nx.spring_layout(G, seed=42, iterations=50, k=0.5)
    
    # Create figure
    plt.figure(figsize=(10, 10))
    
    # Draw the network
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=30,
                          alpha=0.8)
    
    nx.draw_networkx_edges(G, pos, 
                          alpha=0.2,
                          width=0.5,
                          edge_color='gray')
    
    # Add title with statistics
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    giant_size = len(giant_component)
    giant_fraction = giant_size / num_nodes
    
    plt.title(f'λ = {lambda_val:.1f}\n'
              f'Giant Component: {giant_size}/{num_nodes} nodes ({giant_fraction:.1%})',
              fontsize=16, fontweight='bold')
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save figure
    filename = f'phase_transition_lambda_{lambda_val:.1f}.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Saved: {filepath}")
    print(f"  - Total nodes: {num_nodes}")
    print(f"  - Total edges: {num_edges}")
    print(f"  - Giant component size: {giant_size} ({giant_fraction:.1%})")
    print()


def generate_all_visualizations():
    """
    Generate visualizations for all λ values around the phase transition.
    """
    # Fixed network size
    N = 250
    
    # Lambda values to test
    lambda_values = [0.5, 0.8, 1.0, 1.2, 2.0]
    
    print("=" * 60)
    print("Generating Phase Transition Visualizations")
    print("=" * 60)
    print(f"Network size: N = {N}")
    print(f"Lambda values: {lambda_values}")
    print("=" * 60)
    print()
    
    for lambda_val in lambda_values:
        print(f"Generating network for λ = {lambda_val}...")
        
        # Generate network
        G, p = generate_random_network(N, lambda_val)
        
        print(f"  Edge probability p = {p:.6f}")
        
        # Visualize
        visualize_network(G, lambda_val)
    
    print("=" * 60)
    print("All visualizations generated successfully!")
    print("Figures saved in: figures/")
    print("=" * 60)


def analyze_phase_transition():
    """
    Analyze the phase transition by computing statistics across λ values.
    """
    N = 250
    lambda_range = np.linspace(0.1, 3.0, 30)
    
    giant_component_sizes = []
    
    print("\nAnalyzing phase transition across λ range...")
    
    for lambda_val in lambda_range:
        G, _ = generate_random_network(N, lambda_val)
        giant = find_giant_component(G)
        giant_fraction = len(giant) / N
        giant_component_sizes.append(giant_fraction)
    
    # Plot the phase transition curve
    plt.figure(figsize=(10, 6))
    plt.plot(lambda_range, giant_component_sizes, 'b-', linewidth=2)
    plt.axvline(x=1.0, color='r', linestyle='--', linewidth=2, label='Critical point (λ = 1)')
    plt.xlabel('Average Degree (λ)', fontsize=14)
    plt.ylabel('Fraction of Nodes in Giant Component', fontsize=14)
    plt.title('Phase Transition in Erdős-Rényi Networks', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Save the analysis plot
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/phase_transition_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Phase transition analysis saved: figures/phase_transition_curve.png")


if __name__ == "__main__":
    # Generate all required visualizations
    generate_all_visualizations()
    
    # Optional: Generate phase transition analysis curve
    analyze_phase_transition()
