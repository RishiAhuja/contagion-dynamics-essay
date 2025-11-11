#!/usr/bin/env python3
"""
Quick Test Script for Section 4 SIR Simulation

This is a fast test version that runs fewer simulations to verify
everything works before running the full 100-run experiment.

Usage:
    python test_sir_simulation.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_sir_simulation import (
    run_multiple_simulations, plot_epidemic_curves, 
    plot_infected_comparison, plot_r0_validation
)
import networkx as nx


def main():
    print("\n" + "="*70)
    print("QUICK TEST: SIR Simulation (Section 4)")
    print("Running with reduced parameters for fast testing")
    print("="*70)
    
    # Reduced parameters for testing
    N = 500  # Smaller network
    avg_degree = 10
    beta = 0.05
    gamma = 0.1
    num_runs = 5  # Much fewer runs
    
    print(f"\nTest Parameters:")
    print(f"  Network size (N): {N}")
    print(f"  Average degree: {avg_degree}")
    print(f"  Transmission (β): {beta}")
    print(f"  Recovery (γ): {gamma}")
    print(f"  Runs per topology: {num_runs}")
    print(f"  Expected R₀: {(beta * avg_degree) / gamma:.2f}")
    
    # Create R0 diagram
    print("\nCreating R₀ validation diagram...")
    plot_r0_validation(beta, gamma, avg_degree, 
                      filename='figures/test_sir_r0_validation.png')
    
    # Define network generators
    results = {}
    
    # 1. ER
    p_er = avg_degree / (N - 1)
    results['ER'] = run_multiple_simulations(
        network_generator=nx.erdos_renyi_graph,
        network_params={'n': N, 'p': p_er},
        beta=beta, gamma=gamma, num_runs=num_runs,
        description="ER (Test)"
    )
    
    # 2. WS
    results['WS'] = run_multiple_simulations(
        network_generator=nx.watts_strogatz_graph,
        network_params={'n': N, 'k': avg_degree, 'p': 0.1},
        beta=beta, gamma=gamma, num_runs=num_runs,
        description="WS (Test)"
    )
    
    # 3. BA
    results['BA'] = run_multiple_simulations(
        network_generator=nx.barabasi_albert_graph,
        network_params={'n': N, 'm': avg_degree // 2},
        beta=beta, gamma=gamma, num_runs=num_runs,
        description="BA (Test)"
    )
    
    # Generate plots
    print("\nGenerating test visualizations...")
    plot_epidemic_curves(results, filename='figures/test_sir_epidemic_curves.png')
    plot_infected_comparison(results, filename='figures/test_sir_infected_comparison.png')
    
    print("\n" + "="*70)
    print("✓ Test complete! Check figures/test_* files")
    print("If these look good, run the full simulation with:")
    print("  python src/generate_sir_simulation.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
