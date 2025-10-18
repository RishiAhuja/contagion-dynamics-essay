#!/usr/bin/env python3
"""
Generate comprehensive visualizations for the Barabási-Albert model.

This script creates 6 experiments that demonstrate the unique properties
of scale-free networks, from degree distributions to attack simulations.

Usage:
    python generate_ba_analysis.py
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import random


# ============================================================================
# EXPERIMENT 1: Power-Law vs. Poisson Degree Distributions
# ============================================================================

def experiment1_degree_distributions():
    """
    Compare degree distributions of ER (Poisson) and BA (Power-law) networks.
    Shows the fundamental difference in network inequality.
    """
    print("Experiment 1: Degree Distribution Comparison")
    print("-" * 60)
    
    N = 1000
    avg_degree = 10
    
    # Generate networks
    print(f"Generating ER network (N={N}, avg_degree={avg_degree})...")
    p_er = avg_degree / (N - 1)
    er_network = nx.erdos_renyi_graph(N, p_er, seed=42)
    
    print(f"Generating BA network (N={N}, m={avg_degree//2})...")
    ba_network = nx.barabasi_albert_graph(N, m=avg_degree//2, seed=42)
    
    # Get degree sequences
    er_degrees = [d for n, d in er_network.degree()]
    ba_degrees = [d for n, d in ba_network.degree()]
    
    # Calculate statistics
    er_mean = np.mean(er_degrees)
    er_max = np.max(er_degrees)
    ba_mean = np.mean(ba_degrees)
    ba_max = np.max(ba_degrees)
    
    print(f"ER: mean degree = {er_mean:.2f}, max degree = {er_max}")
    print(f"BA: mean degree = {ba_mean:.2f}, max degree = {ba_max}")
    
    # Create figure with two panels
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # ===== Panel A: Regular histogram (shows the bell curve) =====
    ax1 = axes[0]
    
    # ER histogram
    er_hist, er_bins = np.histogram(er_degrees, bins=range(0, max(er_degrees)+2))
    er_centers = (er_bins[:-1] + er_bins[1:]) / 2
    ax1.plot(er_centers, er_hist, 'o-', color='#2E86AB', linewidth=2.5, 
             markersize=6, label='Erdős-Rényi (Random)', alpha=0.8)
    
    # BA histogram
    ba_hist, ba_bins = np.histogram(ba_degrees, bins=range(0, min(50, max(ba_degrees)+2)))
    ba_centers = (ba_bins[:-1] + ba_bins[1:]) / 2
    ax1.plot(ba_centers, ba_hist, 's-', color='#E63946', linewidth=2.5, 
             markersize=6, label='Barabási-Albert (Scale-Free)', alpha=0.8)
    
    ax1.axvline(er_mean, color='#2E86AB', linestyle='--', linewidth=2, alpha=0.5)
    ax1.axvline(ba_mean, color='#E63946', linestyle='--', linewidth=2, alpha=0.5)
    
    ax1.set_xlabel('Degree $k$', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Nodes', fontsize=14, fontweight='bold')
    ax1.set_title('(A) Linear Scale: The "Bell Curve" vs. "Long Tail"', 
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 50)
    
    # ===== Panel B: Log-log scale (shows the power law) =====
    ax2 = axes[1]
    
    # ER on log-log
    er_counter = Counter(er_degrees)
    er_k = sorted(er_counter.keys())
    er_pk = [er_counter[k] / N for k in er_k]
    ax2.loglog(er_k, er_pk, 'o-', color='#2E86AB', linewidth=2.5, 
               markersize=8, label='Erdős-Rényi (Poisson)', alpha=0.8)
    
    # BA on log-log
    ba_counter = Counter(ba_degrees)
    ba_k = sorted(ba_counter.keys())
    ba_pk = [ba_counter[k] / N for k in ba_k]
    ax2.loglog(ba_k, ba_pk, 's-', color='#E63946', linewidth=2.5, 
               markersize=8, label='Barabási-Albert (Power-Law)', alpha=0.8)
    
    # Fit power law line for BA (for reference)
    # P(k) ~ k^(-gamma), on log-log this is: log P(k) = -gamma * log(k)
    # Only fit the clean power-law region (avoid the peak and the noisy tail)
    ba_k_fit = np.array([k for k in ba_k if k >= 8 and k <= 40])  # Fit only clean region
    ba_pk_fit = np.array([ba_counter[k]/N for k in ba_k_fit])
    if len(ba_k_fit) > 5:
        # Linear fit on log-log scale
        coeffs = np.polyfit(np.log(ba_k_fit), np.log(ba_pk_fit), 1)
        gamma = -coeffs[0]
        # Create smooth line ONLY in the region where it's actually straight
        fit_k = np.logspace(np.log10(8), np.log10(40), 100)
        fit_line = np.exp(coeffs[1]) * fit_k ** coeffs[0]
        ax2.loglog(fit_k, fit_line, '--', color='darkred', linewidth=3, 
                   alpha=0.9, label=f'Power-Law Fit: $k^{{-{gamma:.2f}}}$', zorder=10)
    
    ax2.set_xlabel('Degree $k$ (log scale)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('P(k) = Fraction of Nodes (log scale)', fontsize=14, fontweight='bold')
    ax2.set_title('(B) Log-Log Scale: Signature of Scale-Free Networks', 
                  fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11, framealpha=0.9, loc='lower left')
    ax2.grid(True, alpha=0.3, which='both')
    
    # Add annotation explaining the straight line
    ax2.annotate('Power law:\nStraight line on log-log', 
                xy=(20, 0.01), xytext=(40, 0.05),
                fontsize=11, ha='left', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5),
                bbox=dict(boxstyle='round,pad=0.7', facecolor='mistyrose', 
                         alpha=0.9, edgecolor='darkred', linewidth=2))
    
    plt.tight_layout()
    plt.savefig('figures/ba_degree_distributions.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: figures/ba_degree_distributions.png")
    plt.close()


# ============================================================================
# EXPERIMENT 2: Hub Visualization - Three Network Comparison
# ============================================================================

def experiment2_hub_visualization():
    """
    Visual comparison of ER, WS, and BA network structures.
    Shows the emergence of hubs in scale-free networks.
    Creates THREE separate figures for proper visibility in two-column format.
    """
    print("\nExperiment 2: Hub Visualization Comparison")
    print("-" * 60)
    
    N = 100
    seed = 42
    
    # Generate networks
    print(f"Generating three networks (N={N})...")
    er = nx.erdos_renyi_graph(N, p=0.1, seed=seed)
    ws = nx.watts_strogatz_graph(N, k=10, p=0.1, seed=seed)
    ba = nx.barabasi_albert_graph(N, m=5, seed=seed)
    
    networks = [er, ws, ba]
    titles = ['Random Network (Erdős-Rényi)', 'Small-World Network (Watts-Strogatz)', 
              'Scale-Free Network (Barabási-Albert)']
    filenames = ['ba_network_er.png', 'ba_network_ws.png', 'ba_network_ba.png']
    
    for idx, (G, title, filename) in enumerate(zip(networks, titles, filenames)):
        # Create individual figure for each network
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        
        # Calculate degrees
        degrees = dict(G.degree())
        degree_values = list(degrees.values())
        max_degree = max(degree_values)
        min_degree = min(degree_values)
        
        # Create layout
        pos = nx.spring_layout(G, k=0.3, iterations=50, seed=seed)
        
        # Normalize degrees for coloring (0 to 1)
        norm_degrees = [(d - min_degree) / (max_degree - min_degree + 1) for d in degree_values]
        
        # Node sizes proportional to degree
        node_sizes = [100 + 600 * ((d - min_degree) / (max_degree - min_degree + 1)) 
                      for d in degree_values]
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.2, width=0.5, ax=ax)
        
        # Draw nodes with color gradient
        nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                                       node_color=norm_degrees, 
                                       cmap='YlOrRd', vmin=0, vmax=1,
                                       alpha=0.9, ax=ax)
        
        # Highlight top 5 hubs in BA network
        if idx == 2:  # BA network
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            top_pos = {n: pos[n] for n, d in top_nodes}
            nx.draw_networkx_nodes(G, top_pos, 
                                  nodelist=[n for n, d in top_nodes],
                                  node_size=[node_sizes[n] for n, d in top_nodes],
                                  node_color='red', 
                                  edgecolors='darkred', linewidths=4,
                                  alpha=1.0, ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
        ax.axis('off')
        
        # Add statistics
        avg_deg = np.mean(degree_values)
        max_deg = max_degree
        stats_text = f'Average Degree: {avg_deg:.1f}\nMaximum Degree: {max_deg}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=12, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, pad=0.7))
        
        # Add colorbar
        cbar = plt.colorbar(nodes, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Node Degree (normalized)', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'figures/{filename}', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: figures/{filename}")
        plt.close()


# ============================================================================
# EXPERIMENT 3: Degree Evolution Over Time
# ============================================================================

def experiment3_degree_evolution():
    """
    Track how node degrees evolve over time during network growth.
    Demonstrates the first-mover advantage and preferential attachment.
    """
    print("\nExperiment 3: Degree Evolution Over Time")
    print("-" * 60)
    
    N_final = 1000
    m = 5
    m0 = 5
    
    print(f"Building BA network step-by-step (N={N_final}, m={m})...")
    
    # We'll rebuild the network manually to track degree evolution
    # Start with m0 nodes in a complete graph
    G = nx.complete_graph(m0)
    degree_history = {i: [m0-1] for i in range(m0)}  # Initial degrees
    
    # Add nodes one by one
    for new_node in range(m0, N_final):
        # Get current degrees
        degrees = dict(G.degree())
        total_degree = sum(degrees.values())
        
        # Calculate probabilities for preferential attachment
        if total_degree > 0:
            probs = [degrees[node] / total_degree for node in G.nodes()]
            nodes_list = list(G.nodes())
            
            # Choose m nodes to connect to (without replacement)
            targets = np.random.choice(nodes_list, size=min(m, len(nodes_list)), 
                                      replace=False, p=probs)
        else:
            # Fallback (shouldn't happen)
            targets = list(G.nodes())[:m]
        
        # Add new node and edges
        G.add_node(new_node)
        for target in targets:
            G.add_edge(new_node, target)
        
        # Record degrees at this time step
        current_degrees = dict(G.degree())
        for node in G.nodes():
            if node not in degree_history:
                degree_history[node] = []
            degree_history[node].append(current_degrees[node])
        
        if (new_node + 1) % 100 == 0:
            print(f"  Progress: {new_node + 1}/{N_final} nodes", end='\r')
    
    print(f"  Progress: {N_final}/{N_final} nodes")
    print("Network construction complete!")
    
    # Select representative nodes to plot
    early_nodes = list(range(5))  # Nodes 0-4
    mid_nodes = list(range(250, 255))  # Nodes 250-254
    late_nodes = list(range(900, 905))  # Nodes 900-904
    
    # Create figure
    plt.figure(figsize=(12, 7))
    
    # Plot early nodes
    for node in early_nodes:
        time_steps = range(node, len(degree_history[node]) + node)
        plt.plot(time_steps, degree_history[node], '-', linewidth=2.5, 
                alpha=0.8, label=f'Node {node} (early)')
    
    # Plot mid nodes
    for i, node in enumerate(mid_nodes):
        time_steps = range(node, len(degree_history[node]) + node)
        plt.plot(time_steps, degree_history[node], '--', linewidth=2, 
                alpha=0.7, label=f'Node {node} (mid)' if i == 0 else '')
    
    # Plot late nodes
    for i, node in enumerate(late_nodes):
        time_steps = range(node, len(degree_history[node]) + node)
        plt.plot(time_steps, degree_history[node], ':', linewidth=1.5, 
                alpha=0.6, label=f'Node {node} (late)' if i == 0 else '')
    
    plt.xlabel('Time Step (Network Size)', fontsize=14, fontweight='bold')
    plt.ylabel('Node Degree', fontsize=14, fontweight='bold')
    plt.title('First-Mover Advantage: Degree Evolution in Growing Network', 
             fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=9, ncol=3, framealpha=0.9, loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Add annotations
    plt.annotate('Early nodes grow rapidly\ndue to preferential attachment',
                xy=(500, degree_history[0][-1]), xytext=(600, 140),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='darkblue', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    plt.annotate('Late nodes struggle\nto accumulate connections',
                xy=(950, degree_history[900][-1]), xytext=(700, 30),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='mistyrose', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('figures/ba_degree_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: figures/ba_degree_evolution.png")
    plt.close()


# ============================================================================
# EXPERIMENT 4: Robustness vs. Vulnerability (Attack Simulation)
# ============================================================================

def experiment4_attack_simulation():
    """
    Simulate random and targeted attacks on ER and BA networks.
    Demonstrates the robustness/vulnerability paradox.
    """
    print("\nExperiment 4: Attack Simulation (Robustness vs. Vulnerability)")
    print("-" * 60)
    
    N = 1000
    avg_degree = 10
    
    # Generate networks
    print(f"Generating networks (N={N})...")
    p_er = avg_degree / (N - 1)
    er = nx.erdos_renyi_graph(N, p_er, seed=42)
    ba = nx.barabasi_albert_graph(N, m=avg_degree//2, seed=42)
    
    def get_giant_component_size(G):
        """Return size of largest connected component as fraction of network."""
        if len(G) == 0:
            return 0.0
        if nx.is_connected(G):
            return 1.0
        components = list(nx.connected_components(G))
        largest = max(components, key=len)
        return len(largest) / N
    
    def random_attack(G):
        """Simulate random node removal."""
        G_copy = G.copy()
        nodes = list(G_copy.nodes())
        random.shuffle(nodes)
        
        fractions_removed = []
        giant_sizes = []
        
        for i in range(0, len(nodes), 5):  # Remove 5 nodes at a time
            # Remove nodes
            nodes_to_remove = nodes[i:i+5]
            G_copy.remove_nodes_from(nodes_to_remove)
            
            # Record state
            fraction_removed = (i + len(nodes_to_remove)) / N
            giant_size = get_giant_component_size(G_copy)
            
            fractions_removed.append(fraction_removed)
            giant_sizes.append(giant_size)
        
        return fractions_removed, giant_sizes
    
    def targeted_attack(G):
        """Simulate targeted removal of highest-degree nodes."""
        G_copy = G.copy()
        
        fractions_removed = []
        giant_sizes = []
        
        removed_count = 0
        while len(G_copy) > 0:
            # Find highest degree node
            degrees = dict(G_copy.degree())
            if not degrees:
                break
            
            # Remove top 5 nodes
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            nodes_to_remove = [n for n, d in top_nodes]
            G_copy.remove_nodes_from(nodes_to_remove)
            
            removed_count += len(nodes_to_remove)
            
            # Record state
            fraction_removed = removed_count / N
            giant_size = get_giant_component_size(G_copy)
            
            fractions_removed.append(fraction_removed)
            giant_sizes.append(giant_size)
            
            if removed_count >= N * 0.5:  # Stop at 50% for efficiency
                break
        
        return fractions_removed, giant_sizes
    
    print("Running random attack simulations...")
    er_random_x, er_random_y = random_attack(er)
    ba_random_x, ba_random_y = random_attack(ba)
    
    print("Running targeted attack simulations...")
    er_targeted_x, er_targeted_y = targeted_attack(er)
    ba_targeted_x, ba_targeted_y = targeted_attack(ba)
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel A: Random Attack
    ax1 = axes[0]
    ax1.plot(er_random_x, er_random_y, 'o-', color='#2E86AB', linewidth=2.5,
            markersize=5, label='ER (Random)', alpha=0.8)
    ax1.plot(ba_random_x, ba_random_y, 's-', color='#E63946', linewidth=2.5,
            markersize=5, label='BA (Scale-Free)', alpha=0.8)
    
    ax1.set_xlabel('Fraction of Nodes Removed', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Giant Component Size (fraction)', fontsize=14, fontweight='bold')
    ax1.set_title('(A) Random Node Removal', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=12, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.05, 1.05)
    
    ax1.annotate('BA more robust\nto random failures',
                xy=(0.3, 0.7), xytext=(0.4, 0.85),
                fontsize=11, ha='center',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='mistyrose', alpha=0.7))
    
    # Panel B: Targeted Attack
    ax2 = axes[1]
    ax2.plot(er_targeted_x, er_targeted_y, 'o-', color='#2E86AB', linewidth=2.5,
            markersize=5, label='ER (Random)', alpha=0.8)
    ax2.plot(ba_targeted_x, ba_targeted_y, 's-', color='#E63946', linewidth=2.5,
            markersize=5, label='BA (Scale-Free)', alpha=0.8)
    
    ax2.set_xlabel('Fraction of Nodes Removed', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Giant Component Size (fraction)', fontsize=14, fontweight='bold')
    ax2.set_title('(B) Targeted Hub Removal', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=12, framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    
    # Fix arrow position - BA starts fragmenting immediately when top hubs are removed
    # Point to the initial drop around 5% removal
    ax2.annotate('BA fragments\nimmediately when\ntop hubs removed',
                xy=(0.05, 0.95), xytext=(0.15, 0.6),
                fontsize=11, ha='center', color='darkred', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=3),
                bbox=dict(boxstyle='round,pad=0.6', facecolor='mistyrose', 
                         alpha=0.9, edgecolor='darkred', linewidth=2))
    
    plt.suptitle('The Achilles\' Heel: Robustness vs. Vulnerability in Scale-Free Networks',
                fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('figures/ba_attack_simulation.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: figures/ba_attack_simulation.png")
    plt.close()


# ============================================================================
# EXPERIMENT 5: Epidemic Threshold Comparison
# ============================================================================

def experiment5_epidemic_threshold():
    """
    Compare epidemic thresholds across ER, WS, and BA networks.
    Shows how topology affects outbreak potential.
    """
    print("\nExperiment 5: Epidemic Threshold Comparison")
    print("-" * 60)
    print("NOTE: This is a simplified SIR model for demonstration.")
    
    N = 1000
    avg_degree = 10
    
    # Generate networks
    print(f"Generating networks (N={N})...")
    p_er = avg_degree / (N - 1)
    er = nx.erdos_renyi_graph(N, p_er, seed=42)
    ws = nx.watts_strogatz_graph(N, k=10, p=0.1, seed=42)
    ba = nx.barabasi_albert_graph(N, m=avg_degree//2, seed=42)
    
    def run_simple_sir(G, beta, num_runs=10):
        """
        Run simplified SIR epidemic simulation.
        beta: transmission probability
        Returns: average final outbreak size
        """
        outbreak_sizes = []
        
        for run in range(num_runs):
            # Initialize: one random infected node
            infected = {random.choice(list(G.nodes()))}
            recovered = set()
            
            # Run until no more infections
            while infected:
                new_infected = set()
                
                for node in infected:
                    # Try to infect neighbors
                    for neighbor in G.neighbors(node):
                        if neighbor not in infected and neighbor not in recovered:
                            if random.random() < beta:
                                new_infected.add(neighbor)
                
                # Move current infected to recovered
                recovered.update(infected)
                infected = new_infected
            
            outbreak_sizes.append(len(recovered) / N)
        
        return np.mean(outbreak_sizes)
    
    # Test range of beta values
    beta_values = np.linspace(0.01, 0.5, 20)
    
    er_sizes = []
    ws_sizes = []
    ba_sizes = []
    
    print("Running epidemic simulations...")
    for i, beta in enumerate(beta_values):
        print(f"  Progress: {i+1}/{len(beta_values)} (β={beta:.3f})", end='\r')
        er_sizes.append(run_simple_sir(er, beta, num_runs=5))
        ws_sizes.append(run_simple_sir(ws, beta, num_runs=5))
        ba_sizes.append(run_simple_sir(ba, beta, num_runs=5))
    
    print(f"  Progress: {len(beta_values)}/{len(beta_values)} complete")
    
    # Create figure
    plt.figure(figsize=(12, 7))
    
    plt.plot(beta_values, er_sizes, 'o-', color='#2E86AB', linewidth=2.5,
            markersize=7, label='ER (Random)', alpha=0.8)
    plt.plot(beta_values, ws_sizes, 's-', color='#06A77D', linewidth=2.5,
            markersize=7, label='WS (Small-World)', alpha=0.8)
    plt.plot(beta_values, ba_sizes, '^-', color='#E63946', linewidth=2.5,
            markersize=7, label='BA (Scale-Free)', alpha=0.8)
    
    # Add threshold line at 10% outbreak
    plt.axhline(y=0.1, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    plt.xlabel('Transmission Probability $\\beta$', fontsize=14, fontweight='bold')
    plt.ylabel('Final Outbreak Size (fraction of network)', fontsize=14, fontweight='bold')
    plt.title('Epidemic Thresholds: Network Topology Determines Outbreak Potential',
             fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=12, framealpha=0.9, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.ylim(-0.05, 1.05)
    
    # Add annotations
    plt.annotate('BA: Lowest threshold\nEpidemics even at low β',
                xy=(0.1, ba_sizes[2]), xytext=(0.2, 0.7),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='mistyrose', alpha=0.8))
    
    plt.annotate('ER/WS: Higher threshold\nRequires more contagious pathogen',
                xy=(0.25, er_sizes[8]), xytext=(0.32, 0.3),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='darkblue', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('figures/ba_epidemic_threshold.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: figures/ba_epidemic_threshold.png")
    plt.close()


# ============================================================================
# EXPERIMENT 6: Hub Dominance Table/Chart
# ============================================================================

def experiment6_hub_dominance():
    """
    Quantify hub dominance in BA network.
    Shows numerical inequality in connectivity.
    """
    print("\nExperiment 6: Hub Dominance Analysis")
    print("-" * 60)
    
    N = 1000
    m = 5
    
    print(f"Generating BA network (N={N}, m={m})...")
    ba = nx.barabasi_albert_graph(N, m=m, seed=42)
    
    # Get degree distribution
    degrees = dict(ba.degree())
    total_edges = ba.number_of_edges()
    
    # Sort nodes by degree
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate statistics for top nodes
    top_10 = sorted_nodes[:10]
    top_50 = sorted_nodes[:50]
    top_100 = sorted_nodes[:100]
    
    # Sum of degrees (each edge counted twice)
    sum_degrees = sum(degrees.values())
    
    top_10_degree_sum = sum(d for n, d in top_10)
    top_50_degree_sum = sum(d for n, d in top_50)
    top_100_degree_sum = sum(d for n, d in top_100)
    
    top_10_percent = (top_10_degree_sum / sum_degrees) * 100
    top_50_percent = (top_50_degree_sum / sum_degrees) * 100
    top_100_percent = (top_100_degree_sum / sum_degrees) * 100
    
    print(f"Total edges: {total_edges}")
    print(f"Top 10 nodes (1%) control: {top_10_percent:.1f}% of connections")
    print(f"Top 50 nodes (5%) control: {top_50_percent:.1f}% of connections")
    print(f"Top 100 nodes (10%) control: {top_100_percent:.1f}% of connections")
    
    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel A: Bar chart of top 20 nodes
    ax1 = axes[0]
    top_20 = sorted_nodes[:20]
    node_labels = [f"{n}" for n, d in top_20]
    node_degrees = [d for n, d in top_20]
    
    bars = ax1.bar(range(20), node_degrees, color='#E63946', alpha=0.8, edgecolor='darkred', linewidth=1.5)
    
    # Highlight top 5
    for i in range(5):
        bars[i].set_color('darkred')
        bars[i].set_alpha(1.0)
    
    ax1.set_xlabel('Node Rank', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Degree (Number of Connections)', fontsize=14, fontweight='bold')
    ax1.set_title('(A) Top 20 Hub Nodes by Degree', fontsize=14, fontweight='bold')
    ax1.set_xticks(range(0, 20, 2))
    ax1.set_xticklabels(range(1, 21, 2))
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add statistics box
    stats_text = f"Top hub: {node_degrees[0]} connections\nTop 5 avg: {np.mean(node_degrees[:5]):.1f}"
    ax1.text(0.98, 0.98, stats_text, transform=ax1.transAxes,
            fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    # Panel B: Cumulative percentage
    ax2 = axes[1]
    
    percentiles = [1, 5, 10, 20, 50]
    percentages = []
    
    for p in percentiles:
        n_nodes = int(N * p / 100)
        top_n = sorted_nodes[:n_nodes]
        degree_sum = sum(d for n, d in top_n)
        percentage = (degree_sum / sum_degrees) * 100
        percentages.append(percentage)
    
    bars = ax2.bar(range(len(percentiles)), percentages, 
                   color=['darkred', '#E63946', '#FF6B6B', '#FFA07A', '#FFB6C1'],
                   alpha=0.8, edgecolor='darkred', linewidth=1.5)
    
    ax2.set_xlabel('Top X% of Nodes', fontsize=14, fontweight='bold')
    ax2.set_ylabel('% of Total Connections Controlled', fontsize=14, fontweight='bold')
    ax2.set_title('(B) Cumulative Hub Dominance', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(percentiles)))
    ax2.set_xticklabels([f'{p}%' for p in percentiles])
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim(0, 100)
    
    # Add percentage labels on bars
    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Add reference line at 50%
    ax2.axhline(y=50, color='gray', linestyle='--', linewidth=2, alpha=0.5)
    ax2.text(len(percentiles)-0.5, 52, '50% threshold', fontsize=10, ha='right', style='italic')
    
    plt.suptitle(f'Hub Dominance in Scale-Free Networks (N={N})',
                fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('figures/ba_hub_dominance.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: figures/ba_hub_dominance.png")
    plt.close()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all 6 experiments."""
    print("=" * 70)
    print("BARABÁSI-ALBERT MODEL: COMPREHENSIVE ANALYSIS")
    print("=" * 70)
    print()
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Run all experiments
    experiment1_degree_distributions()
    experiment2_hub_visualization()
    experiment3_degree_evolution()
    experiment4_attack_simulation()
    experiment5_epidemic_threshold()
    experiment6_hub_dominance()
    
    print()
    print("=" * 70)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 70)
    print()
    print("Generated figures:")
    print("  1. ba_degree_distributions.png  - Power-law vs. Poisson")
    print("  2. ba_hub_visualization.png     - Visual network comparison")
    print("  3. ba_degree_evolution.png      - Temporal growth dynamics")
    print("  4. ba_attack_simulation.png     - Robustness/vulnerability paradox")
    print("  5. ba_epidemic_threshold.png    - Outbreak potential comparison")
    print("  6. ba_hub_dominance.png         - Hub concentration statistics")
    print()
    print("To compile the paper with these figures:")
    print("  make pdf")
    print()


if __name__ == "__main__":
    main()
