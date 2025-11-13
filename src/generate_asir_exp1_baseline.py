#!/usr/bin/env python3
"""
ASIR Experiment 1: Baseline Comparison (Static vs. Adaptive)

Tests Hypothesis 1 (peak reduction) and Hypothesis 2 (duration extension)
by comparing static SIR (α=0, μ=0) with adaptive ASIR (α>0, μ>0).

Usage:
    python generate_asir_exp1_baseline.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from asir_core import run_multiple_asir_simulations, average_time_series
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_comparison(static_results, adaptive_results, topology_name, filename):
    """
    Plot side-by-side comparison of static vs adaptive epidemic curves.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Get averaged time series
    static_ts = average_time_series(static_results['all_series'])
    adaptive_ts = average_time_series(adaptive_results['all_series'])
    
    # Color scheme
    color_static = '#E63946'
    color_adaptive = '#06A77D'
    
    # Plot 1: Infected curves comparison
    ax = axes[0, 0]
    ax.plot(static_ts['t'], static_ts['I_mean'], 
           color=color_static, linewidth=3, label='Static (α=0, μ=0)', alpha=0.9)
    ax.fill_between(static_ts['t'], 
                    static_ts['I_mean'] - static_ts['I_std'],
                    static_ts['I_mean'] + static_ts['I_std'],
                    color=color_static, alpha=0.2)
    
    ax.plot(adaptive_ts['t'], adaptive_ts['I_mean'], 
           color=color_adaptive, linewidth=3, label='Adaptive (α=0.10, μ=0.03)', alpha=0.9)
    ax.fill_between(adaptive_ts['t'], 
                    adaptive_ts['I_mean'] - adaptive_ts['I_std'],
                    adaptive_ts['I_mean'] + adaptive_ts['I_std'],
                    color=color_adaptive, alpha=0.2)
    
    ax.set_xlabel('Time Step', fontsize=12, fontweight='bold')
    ax.set_ylabel('Infected Nodes', fontsize=12, fontweight='bold')
    ax.set_title('Infected Over Time', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    # Add peak markers
    static_peak = np.max(static_ts['I_mean'])
    adaptive_peak = np.max(adaptive_ts['I_mean'])
    static_peak_t = np.argmax(static_ts['I_mean'])
    adaptive_peak_t = np.argmax(adaptive_ts['I_mean'])
    
    ax.plot(static_peak_t, static_peak, 'o', color=color_static, markersize=10)
    ax.plot(adaptive_peak_t, adaptive_peak, 'o', color=color_adaptive, markersize=10)
    
    # Plot 2: All three compartments (S/I/R) - Adaptive only
    ax = axes[0, 1]
    ax.plot(adaptive_ts['t'], adaptive_ts['S_mean'], 
           color='#457B9D', linewidth=2.5, label='Susceptible', alpha=0.9)
    ax.plot(adaptive_ts['t'], adaptive_ts['I_mean'], 
           color='#E63946', linewidth=2.5, label='Infected', alpha=0.9)
    ax.plot(adaptive_ts['t'], adaptive_ts['R_mean'], 
           color='#06A77D', linewidth=2.5, label='Recovered', alpha=0.9)
    
    ax.set_xlabel('Time Step', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Nodes', fontsize=12, fontweight='bold')
    ax.set_title('Adaptive ASIR Dynamics', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Peak comparison bar chart
    ax = axes[1, 0]
    categories = ['Static', 'Adaptive']
    peaks = [static_results['peak_mean'], adaptive_results['peak_mean']]
    errors = [static_results['peak_std'], adaptive_results['peak_std']]
    colors = [color_static, color_adaptive]
    
    bars = ax.bar(categories, peaks, yerr=errors, capsize=10,
                  color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Add value labels
    for i, (bar, peak) in enumerate(zip(bars, peaks)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{peak:.0f}',
               ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Calculate reduction
    reduction = (static_results['peak_mean'] - adaptive_results['peak_mean']) / static_results['peak_mean'] * 100
    ax.text(0.5, max(peaks) * 0.9, 
           f'Peak Reduction:\n{reduction:.1f}%',
           ha='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.7))
    
    ax.set_ylabel('Peak Infected', fontsize=12, fontweight='bold')
    ax.set_title('Peak Infection Comparison', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Duration and final size comparison
    ax = axes[1, 1]
    
    # Duration bars
    x = np.array([0, 1])
    width = 0.35
    
    durations = [static_results['duration_mean'], adaptive_results['duration_mean']]
    duration_errors = [static_results['duration_std'], adaptive_results['duration_std']]
    
    bars1 = ax.bar(x - width/2, durations, width, yerr=duration_errors,
                   label='Duration (steps)', color='#A8DADC', 
                   alpha=0.8, edgecolor='black', linewidth=1.5, capsize=5)
    
    # Final size bars (scaled up for visibility)
    sizes = [static_results['size_mean'] * 100, adaptive_results['size_mean'] * 100]
    size_errors = [static_results['size_std'] * 100, adaptive_results['size_std'] * 100]
    
    ax2 = ax.twinx()
    bars2 = ax2.bar(x + width/2, sizes, width, yerr=size_errors,
                    label='Final Size (%)', color='#F1FAEE',
                    alpha=0.8, edgecolor='black', linewidth=1.5, capsize=5)
    
    ax.set_ylabel('Epidemic Duration (steps)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Final Outbreak Size (%)', fontsize=11, fontweight='bold')
    ax.set_title('Duration and Final Size', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    # Main title
    fig.suptitle(f'Static vs. Adaptive Comparison: {topology_name}\n' +
                r'N=5000, $\beta$=0.05, $\gamma$=0.1',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close()


def main():
    """
    Run Experiment 1: Static vs. Adaptive baseline comparison.
    """
    print("\n" + "="*70)
    print("ASIR EXPERIMENT 1: BASELINE COMPARISON")
    print("Testing Hypotheses 1 & 2 (Peak Reduction & Duration Extension)")
    print("="*70)
    
    # Common parameters
    N = 5000
    avg_degree = 10
    beta = 0.05
    gamma = 0.1
    num_runs = 50
    
    # Adaptive parameters - MIDDLE GROUND for sweet spot
    alpha_adaptive = 0.10  # Moderate isolation (balanced)
    mu_adaptive = 0.03     # Moderate clustering
    
    # Static parameters
    alpha_static = 0.0
    mu_static = 0.0
    
    print(f"\nGlobal Parameters:")
    print(f"  Network: N={N}, ⟨k⟩={avg_degree}")
    print(f"  Epidemic: β={beta}, γ={gamma}")
    print(f"  Static: α={alpha_static}, μ={mu_static}")
    print(f"  Adaptive: α={alpha_adaptive}, μ={mu_adaptive}")
    print(f"  Runs per condition: {num_runs}")
    
    # Test on all three topologies
    topologies = [
        ('ER', 'Erdős-Rényi (Random)', 
         nx.erdos_renyi_graph, {'n': N, 'p': avg_degree / (N - 1)}),
        ('WS', 'Watts-Strogatz (Small-World)', 
         nx.watts_strogatz_graph, {'n': N, 'k': avg_degree, 'p': 0.1}),
        ('BA', 'Barabási-Albert (Scale-Free)', 
         nx.barabasi_albert_graph, {'n': N, 'm': avg_degree // 2})
    ]
    
    summary_results = []
    
    for short_name, full_name, generator, params in topologies:
        print(f"\n{'='*70}")
        print(f"Testing on {full_name}")
        print(f"{'='*70}")
        
        # Run static simulations
        static_results = run_multiple_asir_simulations(
            network_generator=generator,
            network_params=params,
            beta=beta, gamma=gamma,
            alpha=alpha_static, mu=mu_static,
            num_runs=num_runs,
            description=f"{short_name} Static",
            track_network=False
        )
        
        # Run adaptive simulations
        adaptive_results = run_multiple_asir_simulations(
            network_generator=generator,
            network_params=params,
            beta=beta, gamma=gamma,
            alpha=alpha_adaptive, mu=mu_adaptive,
            num_runs=num_runs,
            description=f"{short_name} Adaptive",
            track_network=False
        )
        
        # Calculate improvements
        peak_reduction = ((static_results['peak_mean'] - adaptive_results['peak_mean']) / 
                         static_results['peak_mean'] * 100)
        size_reduction = ((static_results['size_mean'] - adaptive_results['size_mean']) / 
                         static_results['size_mean'] * 100)
        duration_increase = adaptive_results['duration_mean'] - static_results['duration_mean']
        
        summary_results.append({
            'topology': short_name,
            'peak_reduction': peak_reduction,
            'size_reduction': size_reduction,
            'duration_increase': duration_increase,
            'static': static_results,
            'adaptive': adaptive_results
        })
        
        print(f"\n{short_name} Summary:")
        print(f"  Peak reduction: {peak_reduction:.1f}%")
        print(f"  Final size reduction: {size_reduction:.1f}%")
        print(f"  Duration increase: {duration_increase:.1f} steps")
        
        # Generate visualization
        plot_comparison(static_results, adaptive_results, full_name,
                       f'figures/asir_exp1_comparison_{short_name}.png')
    
    # Create summary table
    print("\n" + "="*70)
    print("SUMMARY TABLE")
    print("="*70)
    print(f"{'Topology':<12} {'Peak Reduction':<18} {'Size Reduction':<18} {'Duration Change':<15}")
    print("-" * 70)
    
    for result in summary_results:
        print(f"{result['topology']:<12} {result['peak_reduction']:>15.1f}% "
              f"{result['size_reduction']:>15.1f}% {result['duration_increase']:>12.1f} steps")
    
    # Create combined comparison plot
    create_summary_plot(summary_results)
    
    print("\n" + "="*70)
    print("✓ Experiment 1 Complete!")
    print("="*70 + "\n")


def create_summary_plot(summary_results):
    """Create a summary plot comparing all three topologies."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    topologies = [r['topology'] for r in summary_results]
    peak_reductions = [r['peak_reduction'] for r in summary_results]
    size_reductions = [r['size_reduction'] for r in summary_results]
    duration_increases = [r['duration_increase'] for r in summary_results]
    
    colors = ['#2E86AB', '#06A77D', '#E63946']
    
    # Plot 1: Peak reduction
    ax = axes[0]
    bars = ax.bar(topologies, peak_reductions, color=colors, alpha=0.8, 
                  edgecolor='black', linewidth=2)
    ax.set_ylabel('Peak Reduction (%)', fontsize=12, fontweight='bold')
    ax.set_title('Peak Infection Reduction', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    for bar, val in zip(bars, peak_reductions):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.1f}%', ha='center', va='bottom', 
               fontsize=11, fontweight='bold')
    
    # Plot 2: Size reduction
    ax = axes[1]
    bars = ax.bar(topologies, size_reductions, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2)
    ax.set_ylabel('Final Size Reduction (%)', fontsize=12, fontweight='bold')
    ax.set_title('Total Infection Reduction', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    for bar, val in zip(bars, size_reductions):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.1f}%', ha='center', va='bottom',
               fontsize=11, fontweight='bold')
    
    # Plot 3: Duration increase
    ax = axes[2]
    bars = ax.bar(topologies, duration_increases, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2)
    ax.set_ylabel('Duration Increase (steps)', fontsize=12, fontweight='bold')
    ax.set_title('Epidemic Duration Change', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    for bar, val in zip(bars, duration_increases):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.0f}', ha='center', va='bottom',
               fontsize=11, fontweight='bold')
    
    fig.suptitle('Adaptive Behavior Effects Across Network Topologies\n' +
                r'(α=0.05, μ=0.02 vs. Static Baseline)',
                fontsize=15, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/asir_exp1_summary_all.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: figures/asir_exp1_summary_all.png")
    plt.close()


if __name__ == "__main__":
    main()
