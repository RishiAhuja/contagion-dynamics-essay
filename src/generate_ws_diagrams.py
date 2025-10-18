#!/usr/bin/env python3
"""
Generate Watts-Strogatz small-world network diagrams.

This script creates two visualizations:
1. Ring lattice initialization (beta=0) showing ordered local connections
2. Rewired network (beta>0) showing shortcuts and small-world property

Usage:
    python generate_ws_diagrams.py
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random


def create_ring_lattice(N=30, k=4):
    """
    Create a ring lattice network.
    
    Parameters:
    -----------
    N : int
        Number of nodes
    k : int
        Each node connects to k/2 neighbors on each side (must be even)
        
    Returns:
    --------
    G : networkx.Graph
        Ring lattice graph
    """
    G = nx.Graph()
    G.add_nodes_from(range(N))
    
    # Connect each node to k/2 neighbors on each side
    for i in range(N):
        for j in range(1, k//2 + 1):
            G.add_edge(i, (i + j) % N)
            G.add_edge(i, (i - j) % N)
    
    return G


def visualize_ring_lattice(N=30, k=4, highlight_node=0):
    """
    Visualize the ring lattice with a highlighted central node.
    
    Parameters:
    -----------
    N : int
        Number of nodes
    k : int
        Each node connects to k/2 neighbors on each side
    highlight_node : int
        Node to highlight to show local neighborhood structure
    """
    G = create_ring_lattice(N, k)
    
    # Create circular layout
    pos = {}
    for i in range(N):
        angle = 2 * np.pi * i / N
        pos[i] = (np.cos(angle), np.sin(angle))
    
    # Identify neighbors of highlighted node
    neighbors = set(G.neighbors(highlight_node))
    
    # Create figure
    plt.figure(figsize=(10, 10))
    
    # Draw edges
    # Regular edges (not connected to highlighted node)
    regular_edges = [(u, v) for u, v in G.edges() 
                     if u != highlight_node and v != highlight_node]
    # Edges connected to highlighted node
    highlight_edges = [(u, v) for u, v in G.edges() 
                       if u == highlight_node or v == highlight_node]
    
    # Draw regular edges in light gray
    nx.draw_networkx_edges(G, pos, edgelist=regular_edges, 
                          edge_color='lightgray', width=1.5, alpha=0.5)
    
    # Draw highlighted edges in blue
    nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, 
                          edge_color='blue', width=3, alpha=0.8)
    
    # Draw nodes
    # Regular nodes
    regular_nodes = [n for n in G.nodes() if n != highlight_node and n not in neighbors]
    nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes,
                          node_color='lightblue', node_size=300, alpha=0.6)
    
    # Neighbor nodes
    nx.draw_networkx_nodes(G, pos, nodelist=list(neighbors),
                          node_color='skyblue', node_size=400, alpha=0.8)
    
    # Highlighted central node
    nx.draw_networkx_nodes(G, pos, nodelist=[highlight_node],
                          node_color='red', node_size=500)
    
    # Add labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title(f'Ring Lattice (N={N}, k={k}, β=0)\nHighlighted node shows k/2={k//2} connections on each side', 
              fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    # Save figure
    plt.savefig('figures/ws_ring_lattice.png', dpi=300, bbox_inches='tight')
    print(f"Ring lattice diagram saved to figures/ws_ring_lattice.png")
    plt.close()


def create_watts_strogatz(N=30, k=4, beta=0.15, seed=42):
    """
    Create a Watts-Strogatz small-world network with controlled rewiring.
    
    Parameters:
    -----------
    N : int
        Number of nodes
    k : int
        Each node connects to k/2 neighbors on each side
    beta : float
        Rewiring probability
    seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    G : networkx.Graph
        Watts-Strogatz graph
    rewired_edges : list
        List of edges that were rewired (shortcuts)
    """
    random.seed(seed)
    np.random.seed(seed)
    
    # Start with ring lattice
    G = create_ring_lattice(N, k)
    
    # Track original edges and rewired edges
    original_edges = set(G.edges())
    rewired_edges = []
    
    # Rewire edges
    edges_to_process = list(G.edges())
    for u, v in edges_to_process:
        if random.random() < beta:
            # Remove this edge
            G.remove_edge(u, v)
            
            # Choose a new target node (avoiding self-loops and duplicates)
            possible_targets = [n for n in range(N) 
                              if n != u and not G.has_edge(u, n)]
            
            if possible_targets:
                new_target = random.choice(possible_targets)
                G.add_edge(u, new_target)
                rewired_edges.append((u, new_target))
    
    return G, rewired_edges


def visualize_ws_network(N=30, k=4, beta=0.15, highlight_node=0):
    """
    Visualize the Watts-Strogatz network showing shortcuts.
    
    Parameters:
    -----------
    N : int
        Number of nodes
    k : int
        Each node connects to k/2 neighbors on each side
    beta : float
        Rewiring probability
    highlight_node : int
        Node to highlight
    """
    G, rewired_edges = create_watts_strogatz(N, k, beta)
    
    # Create circular layout
    pos = {}
    for i in range(N):
        angle = 2 * np.pi * i / N
        pos[i] = (np.cos(angle), np.sin(angle))
    
    # Identify neighbors of highlighted node
    neighbors = set(G.neighbors(highlight_node))
    
    # Categorize edges
    all_edges = set(G.edges())
    rewired_set = set(rewired_edges)
    
    # Edges involving highlighted node
    highlight_rewired = [(u, v) for u, v in rewired_set 
                        if u == highlight_node or v == highlight_node]
    highlight_regular = [(u, v) for u, v in all_edges 
                        if (u == highlight_node or v == highlight_node) 
                        and (u, v) not in rewired_set]
    
    # Other edges
    other_rewired = [(u, v) for u, v in rewired_set 
                    if u != highlight_node and v != highlight_node]
    other_regular = [(u, v) for u, v in all_edges 
                    if u != highlight_node and v != highlight_node 
                    and (u, v) not in rewired_set]
    
    # Create figure
    plt.figure(figsize=(10, 10))
    
    # Draw regular edges (not rewired, not highlighted)
    nx.draw_networkx_edges(G, pos, edgelist=other_regular, 
                          edge_color='lightgray', width=1.5, alpha=0.4)
    
    # Draw other rewired edges (shortcuts, not connected to highlighted node)
    nx.draw_networkx_edges(G, pos, edgelist=other_rewired, 
                          edge_color='orange', width=2, alpha=0.6, style='dashed')
    
    # Draw highlighted regular edges
    nx.draw_networkx_edges(G, pos, edgelist=highlight_regular, 
                          edge_color='blue', width=3, alpha=0.8)
    
    # Draw highlighted rewired edges (shortcuts from/to highlighted node)
    nx.draw_networkx_edges(G, pos, edgelist=highlight_rewired, 
                          edge_color='red', width=3, alpha=0.9, style='dashed')
    
    # Draw nodes
    # Regular nodes
    regular_nodes = [n for n in G.nodes() if n != highlight_node and n not in neighbors]
    nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes,
                          node_color='lightblue', node_size=300, alpha=0.6)
    
    # Neighbor nodes
    nx.draw_networkx_nodes(G, pos, nodelist=list(neighbors),
                          node_color='skyblue', node_size=400, alpha=0.8)
    
    # Highlighted central node
    nx.draw_networkx_nodes(G, pos, nodelist=[highlight_node],
                          node_color='darkred', node_size=500)
    
    # Add labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Calculate and display network properties
    clustering = nx.average_clustering(G)
    avg_path = nx.average_shortest_path_length(G)
    
    plt.title(f'Small-World Network (N={N}, k={k}, β={beta})\n' + 
              f'Shortcuts (dashed) create small-world property\n' +
              f'Clustering: {clustering:.3f}, Avg Path Length: {avg_path:.2f}', 
              fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    # Save figure
    plt.savefig('figures/ws_rewired_network.png', dpi=300, bbox_inches='tight')
    print(f"Rewired network diagram saved to figures/ws_rewired_network.png")
    print(f"  - Number of shortcuts created: {len(rewired_edges)}")
    print(f"  - Average clustering coefficient: {clustering:.4f}")
    print(f"  - Average shortest path length: {avg_path:.2f}")
    plt.close()


def main():
    """Generate both Watts-Strogatz diagrams."""
    print("Generating Watts-Strogatz diagrams...")
    print()
    
    # Parameters
    N = 30  # Number of nodes
    k = 4   # Degree (connections to k/2 neighbors on each side)
    beta = 0.15  # Rewiring probability
    highlight_node = 0  # Node to highlight in visualizations
    
    # Generate ring lattice
    print(f"1. Creating ring lattice (N={N}, k={k}, β=0)...")
    visualize_ring_lattice(N=N, k=k, highlight_node=highlight_node)
    print()
    
    # Generate rewired small-world network
    print(f"2. Creating small-world network (N={N}, k={k}, β={beta})...")
    visualize_ws_network(N=N, k=k, beta=beta, highlight_node=highlight_node)
    print()
    
    print("All diagrams generated successfully!")
    print()
    print("To include these in your paper, compile with:")
    print("  make pdf")


if __name__ == "__main__":
    main()
