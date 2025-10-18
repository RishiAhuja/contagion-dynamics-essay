#!/usr/bin/env python3
"""
Generate comprehensive visualizations of the small-world transition.

This script analyzes how Watts-Strogatz network properties change with
the rewiring probability beta, creating four complementary visualizations:

1. Normalized metrics (L/L0 and C/C0 vs beta)
2. Absolute metrics (raw L and C values vs beta)
3. Phase space trajectory (C vs L, color-coded by beta)
4. Small-world coefficient (sigma vs beta)

Usage:
    python generate_small_world_analysis.py
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches


def watts_strogatz_metrics(N, k, beta, num_samples=5):
    """
    Calculate average path length and clustering coefficient for WS network.
    
    Parameters:
    -----------
    N : int
        Number of nodes
    k : int
        Each node connects to k/2 neighbors on each side
    beta : float
        Rewiring probability
    num_samples : int
        Number of network realizations to average over
        
    Returns:
    --------
    avg_path_length : float
        Average shortest path length
    clustering_coeff : float
        Average clustering coefficient
    """
    path_lengths = []
    clusterings = []
    
    for _ in range(num_samples):
        G = nx.watts_strogatz_graph(N, k, beta)
        
        # Average path length (only for connected graphs)
        if nx.is_connected(G):
            path_lengths.append(nx.average_shortest_path_length(G))
        
        # Clustering coefficient
        clusterings.append(nx.average_clustering(G))
    
    return np.mean(path_lengths), np.mean(clusterings)


def analyze_small_world_transition(N=1000, k=10, num_beta_points=30, num_samples=5):
    """
    Analyze how network properties change across the small-world transition.
    
    Parameters:
    -----------
    N : int
        Number of nodes
    k : int
        Each node connects to k/2 neighbors on each side
    num_beta_points : int
        Number of beta values to sample
    num_samples : int
        Number of network realizations per beta value
        
    Returns:
    --------
    results : dict
        Dictionary containing beta values and corresponding metrics
    """
    # Generate beta values logarithmically from 10^-4 to 1
    betas = np.logspace(-4, 0, num_beta_points)
    
    # Storage for results
    path_lengths = []
    clusterings = []
    
    print(f"Analyzing small-world transition (N={N}, k={k})...")
    print(f"Sampling {num_beta_points} beta values with {num_samples} realizations each...")
    print()
    
    for i, beta in enumerate(betas):
        print(f"Progress: {i+1}/{num_beta_points} (β = {beta:.6f})", end='\r')
        
        L, C = watts_strogatz_metrics(N, k, beta, num_samples)
        path_lengths.append(L)
        clusterings.append(C)
    
    print()  # New line after progress
    print("Analysis complete!")
    print()
    
    # Get baseline values (ordered lattice, beta=0)
    L0, C0 = watts_strogatz_metrics(N, k, 0, num_samples)
    
    # Get random graph baseline (beta=1)
    L_random, C_random = watts_strogatz_metrics(N, k, 1.0, num_samples)
    
    results = {
        'betas': betas,
        'path_lengths': np.array(path_lengths),
        'clusterings': np.array(clusterings),
        'L0': L0,
        'C0': C0,
        'L_random': L_random,
        'C_random': C_random,
        'N': N,
        'k': k
    }
    
    return results


def visualize_normalized_transition(results):
    """
    Create Figure 1: Normalized metrics showing the small-world transition.
    """
    betas = results['betas']
    L_normalized = results['path_lengths'] / results['L0']
    C_normalized = results['clusterings'] / results['C0']
    
    plt.figure(figsize=(10, 6))
    
    # Plot normalized metrics
    plt.semilogx(betas, L_normalized, 'o-', color='#2E86AB', linewidth=2.5, 
                 markersize=6, label='$L/L_0$ (Path Length)', alpha=0.8)
    plt.semilogx(betas, C_normalized, 's-', color='#E63946', linewidth=2.5, 
                 markersize=6, label='$C/C_0$ (Clustering)', alpha=0.8)
    
    # Highlight small-world regime (where both clustering is high and path length is low)
    # Find region where C/C0 > 0.5 and L/L0 < 0.5
    small_world_mask = (C_normalized > 0.5) & (L_normalized < 0.5)
    if np.any(small_world_mask):
        sw_start = betas[small_world_mask][0]
        sw_end = betas[small_world_mask][-1]
        plt.axvspan(sw_start, sw_end, alpha=0.15, color='green', 
                   label='Small-World Regime')
    
    plt.xlabel('Rewiring Probability $\\beta$', fontsize=14, fontweight='bold')
    plt.ylabel('Normalized Metric', fontsize=14, fontweight='bold')
    plt.title(f'Small-World Transition (N={results["N"]}, k={results["k"]})', 
              fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=12, framealpha=0.9, loc='right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim(-0.05, 1.1)
    
    # Add annotations
    plt.annotate('Ordered Lattice\n(High C, Long L)', xy=(1e-4, 0.95), 
                xytext=(1e-4, 1.05), fontsize=10, ha='left',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))
    plt.annotate('Random Graph\n(Low C, Short L)', xy=(1.0, 0.05), 
                xytext=(0.3, 0.2), fontsize=10, ha='right',
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('figures/small_world_transition.png', dpi=300, bbox_inches='tight')
    print("✓ Normalized transition plot saved to figures/small_world_transition.png")
    plt.close()


def visualize_absolute_metrics(results):
    """
    Create Figure 2: Absolute metrics showing raw values.
    """
    betas = results['betas']
    path_lengths = results['path_lengths']
    clusterings = results['clusterings']
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Plot path length on primary y-axis
    color1 = '#2E86AB'
    ax1.set_xlabel('Rewiring Probability $\\beta$', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Average Path Length $L$', fontsize=14, fontweight='bold', color=color1)
    line1 = ax1.semilogx(betas, path_lengths, 'o-', color=color1, linewidth=2.5, 
                         markersize=6, label='Path Length $L$', alpha=0.8)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Plot clustering on secondary y-axis
    ax2 = ax1.twinx()
    color2 = '#E63946'
    ax2.set_ylabel('Clustering Coefficient $C$', fontsize=14, fontweight='bold', color=color2)
    line2 = ax2.semilogx(betas, clusterings, 's-', color=color2, linewidth=2.5, 
                         markersize=6, label='Clustering $C$', alpha=0.8)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Title
    plt.title(f'Absolute Network Metrics (N={results["N"]}, k={results["k"]})', 
              fontsize=16, fontweight='bold', pad=15)
    
    # Combined legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, fontsize=12, framealpha=0.9, loc='center right')
    
    # Add reference lines for initial values
    ax1.axhline(y=results['L0'], color=color1, linestyle=':', alpha=0.5, linewidth=1.5)
    ax2.axhline(y=results['C0'], color=color2, linestyle=':', alpha=0.5, linewidth=1.5)
    
    fig.tight_layout()
    plt.savefig('figures/absolute_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ Absolute metrics plot saved to figures/absolute_metrics.png")
    plt.close()


def visualize_phase_space(results):
    """
    Create Figure 3: Phase space trajectory showing C vs L.
    """
    path_lengths = results['path_lengths']
    clusterings = results['clusterings']
    betas = results['betas']
    
    plt.figure(figsize=(10, 8))
    
    # Create scatter plot with color gradient based on beta
    scatter = plt.scatter(path_lengths, clusterings, c=np.log10(betas), 
                         cmap='viridis', s=100, alpha=0.8, edgecolors='black', linewidth=1)
    
    # Add trajectory line
    plt.plot(path_lengths, clusterings, '-', color='gray', alpha=0.3, linewidth=1.5, zorder=0)
    
    # Mark special points
    plt.scatter([results['L0']], [results['C0']], s=300, color='red', 
               marker='*', edgecolors='darkred', linewidth=2, 
               label='Ordered Lattice ($\\beta=0$)', zorder=10)
    plt.scatter([results['L_random']], [results['C_random']], s=300, color='blue', 
               marker='*', edgecolors='darkblue', linewidth=2, 
               label='Random Graph ($\\beta=1$)', zorder=10)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, label='$\\log_{10}(\\beta)$')
    cbar.set_label('$\\log_{10}(\\beta)$', fontsize=12, fontweight='bold')
    
    # Define regime regions with rectangles (approximate)
    # Small-world regime: short path, high clustering
    sw_rect = Rectangle((0, 0.4), 10, 0.3, linewidth=2, 
                        edgecolor='green', facecolor='green', alpha=0.1)
    plt.gca().add_patch(sw_rect)
    
    plt.xlabel('Average Path Length $L$', fontsize=14, fontweight='bold')
    plt.ylabel('Clustering Coefficient $C$', fontsize=14, fontweight='bold')
    plt.title(f'Phase Space Trajectory (N={results["N"]}, k={results["k"]})', 
              fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=11, framealpha=0.9, loc='upper right')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Add regime labels
    plt.text(0.95, 0.95, 'Ordered\nRegime', transform=plt.gca().transAxes,
            fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.text(0.05, 0.05, 'Random\nRegime', transform=plt.gca().transAxes,
            fontsize=11, verticalalignment='bottom', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    plt.text(0.25, 0.75, 'Small-World\nRegime', transform=plt.gca().transAxes,
            fontsize=12, verticalalignment='center', horizontalalignment='center',
            color='darkgreen', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('figures/phase_space_trajectory.png', dpi=300, bbox_inches='tight')
    print("✓ Phase space trajectory plot saved to figures/phase_space_trajectory.png")
    plt.close()


def visualize_small_world_coefficient(results):
    """
    Create Figure 4: Small-world coefficient sigma vs beta.
    
    The small-world coefficient is defined as:
    sigma = (C/C_random) / (L/L_random)
    
    Values > 1 indicate small-world properties.
    """
    betas = results['betas']
    
    # Calculate sigma
    C_ratio = results['clusterings'] / results['C_random']
    L_ratio = results['path_lengths'] / results['L_random']
    sigma = C_ratio / L_ratio
    
    plt.figure(figsize=(10, 6))
    
    # Plot sigma
    plt.semilogx(betas, sigma, 'o-', color='#A23E48', linewidth=2.5, 
                markersize=6, alpha=0.8)
    
    # Add reference line at sigma = 1
    plt.axhline(y=1, color='black', linestyle='--', linewidth=2, alpha=0.5, 
               label='$\\sigma = 1$ (threshold)')
    
    # Highlight small-world region (sigma > 1)
    small_world_region = sigma > 1
    if np.any(small_world_region):
        sw_betas = betas[small_world_region]
        sw_sigma = sigma[small_world_region]
        plt.fill_between(sw_betas, 1, sw_sigma, alpha=0.2, color='green', 
                        label='Small-World Region ($\\sigma > 1$)')
    
    # Find and mark peak
    peak_idx = np.argmax(sigma)
    peak_beta = betas[peak_idx]
    peak_sigma = sigma[peak_idx]
    plt.scatter([peak_beta], [peak_sigma], s=200, color='red', marker='*', 
               edgecolors='darkred', linewidth=2, zorder=10, 
               label=f'Peak: $\\beta={peak_beta:.4f}$, $\\sigma={peak_sigma:.2f}$')
    
    plt.xlabel('Rewiring Probability $\\beta$', fontsize=14, fontweight='bold')
    plt.ylabel('Small-World Coefficient $\\sigma$', fontsize=14, fontweight='bold')
    plt.title(f'Small-World Coefficient $\\sigma = (C/C_{{random}}) / (L/L_{{random}})$\n' +
              f'N={results["N"]}, k={results["k"]}', 
              fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=11, framealpha=0.9, loc='upper right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim(0, None)
    
    # Add annotation about interpretation
    plt.text(0.02, 0.98, 
            '$\\sigma > 1$: Small-world properties\n' +
            '$\\sigma \\approx 1$: Random-like\n' +
            '$\\sigma < 1$: Not small-world',
            transform=plt.gca().transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('figures/small_world_metric.png', dpi=300, bbox_inches='tight')
    print("✓ Small-world coefficient plot saved to figures/small_world_metric.png")
    plt.close()


def main():
    """Generate all small-world transition visualizations."""
    print("=" * 70)
    print("SMALL-WORLD TRANSITION ANALYSIS")
    print("=" * 70)
    print()
    
    # Parameters
    N = 1000  # Number of nodes
    k = 10    # Average degree (each node connects to k/2 neighbors on each side)
    num_beta_points = 30  # Number of beta values to sample
    num_samples = 5  # Number of network realizations per beta
    
    print(f"Parameters:")
    print(f"  N = {N} nodes")
    print(f"  k = {k} (average degree)")
    print(f"  Beta range: 10^-4 to 1")
    print(f"  Number of beta samples: {num_beta_points}")
    print(f"  Network realizations per beta: {num_samples}")
    print()
    
    # Run analysis
    results = analyze_small_world_transition(N, k, num_beta_points, num_samples)
    
    print()
    print("Generating visualizations...")
    print()
    
    # Generate all four visualizations
    visualize_normalized_transition(results)
    visualize_absolute_metrics(results)
    visualize_phase_space(results)
    visualize_small_world_coefficient(results)
    
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    print("Summary of results:")
    print(f"  Ordered lattice (β=0):   L={results['L0']:.2f}, C={results['C0']:.4f}")
    print(f"  Random graph (β=1):      L={results['L_random']:.2f}, C={results['C_random']:.4f}")
    print()
    print("Generated figures:")
    print("  1. small_world_transition.png  - Normalized metrics vs beta")
    print("  2. absolute_metrics.png        - Absolute L and C values")
    print("  3. phase_space_trajectory.png  - C vs L phase space")
    print("  4. small_world_metric.png      - Small-world coefficient sigma")
    print()
    print("These figures illustrate:")
    print("  • How path length drops dramatically with minimal rewiring")
    print("  • How clustering remains high even with significant rewiring")
    print("  • The trajectory through phase space from ordered to random")
    print("  • The quantification of 'small-worldness' via the sigma metric")
    print()
    print("To compile the paper with these figures:")
    print("  make pdf")
    print()


if __name__ == "__main__":
    main()
