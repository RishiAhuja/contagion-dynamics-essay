#!/usr/bin/env python3
"""
SIR Epidemic Simulation Framework (Section 4)

This script implements the complete SIR model as described in Section 4 of the paper.
It follows the predicate logic formalization and generates the main epidemic curves
comparing ER, WS, and BA network topologies.

The implementation matches the pseudocode in Section 4.5 exactly.

Usage:
    python generate_sir_simulation.py
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict
from tqdm import tqdm


# ============================================================================
# SIR Model Implementation (Following Section 4's Predicate Logic)
# ============================================================================

class SIRSimulation:
    """
    Implements the SIR epidemic model with discrete-time, synchronous updates.
    
    States:
        - SUSCEPTIBLE (S): Can become infected
        - INFECTED (I): Currently infectious, can transmit to neighbors
        - RECOVERED (R): Immune, terminal state
    
    Parameters:
        - beta (β): Transmission probability per infected neighbor
        - gamma (γ): Recovery probability per time step
    """
    
    # State constants
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    
    def __init__(self, graph, beta, gamma, seed=None):
        """
        Initialize SIR simulation on a given network.
        
        Args:
            graph: NetworkX graph
            beta: Transmission probability (0 < β < 1)
            gamma: Recovery probability (0 < γ < 1)
            seed: Random seed for reproducibility
        """
        self.G = graph
        self.beta = beta
        self.gamma = gamma
        self.N = len(graph.nodes())
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Initialize all nodes as susceptible
        self.state = {node: self.SUSCEPTIBLE for node in self.G.nodes()}
        
        # Time series storage
        self.time_series = {
            'S': [],
            'I': [],
            'R': [],
            't': []
        }
    
    def infect_random_node(self):
        """Select a random node as patient zero."""
        patient_zero = random.choice(list(self.G.nodes()))
        self.state[patient_zero] = self.INFECTED
        return patient_zero
    
    def count_states(self):
        """Count nodes in each state."""
        counts = {self.SUSCEPTIBLE: 0, self.INFECTED: 0, self.RECOVERED: 0}
        for node in self.G.nodes():
            counts[self.state[node]] += 1
        return counts[self.SUSCEPTIBLE], counts[self.INFECTED], counts[self.RECOVERED]
    
    def step(self):
        """
        Execute one time step of the SIR simulation.
        
        Implements the two predicate logic rules from Section 4.2:
        1. Infection Rule: P(infection) = 1 - (1-β)^k_I
        2. Recovery Rule: P(recovery) = γ
        
        Uses synchronous updates: all state changes are marked first,
        then applied simultaneously to avoid order-dependent artifacts.
        """
        # Track nodes to change state
        to_infect = set()
        to_recover = set()
        
        # Process infections (S → I)
        for node in self.G.nodes():
            if self.state[node] == self.SUSCEPTIBLE:
                # Count infected neighbors (k_I)
                infected_neighbors = [n for n in self.G.neighbors(node) 
                                    if self.state[n] == self.INFECTED]
                k_I = len(infected_neighbors)
                
                if k_I > 0:
                    # Infection probability: 1 - (1-β)^k_I
                    p_infection = 1 - (1 - self.beta) ** k_I
                    
                    if random.random() < p_infection:
                        to_infect.add(node)
        
        # Process recoveries (I → R)
        for node in self.G.nodes():
            if self.state[node] == self.INFECTED:
                if random.random() < self.gamma:
                    to_recover.add(node)
        
        # Apply state changes simultaneously
        for node in to_infect:
            self.state[node] = self.INFECTED
        
        for node in to_recover:
            self.state[node] = self.RECOVERED
        
        return len(to_infect), len(to_recover)
    
    def run(self, max_steps=1000):
        """
        Run the epidemic until no infected nodes remain.
        
        Returns:
            dict: Time series of S(t), I(t), R(t)
        """
        t = 0
        self.time_series = {'S': [], 'I': [], 'R': [], 't': []}
        
        while t < max_steps:
            # Count current state
            S, I, R = self.count_states()
            
            # Record time series
            self.time_series['S'].append(S)
            self.time_series['I'].append(I)
            self.time_series['R'].append(R)
            self.time_series['t'].append(t)
            
            # Stop if no infected nodes remain
            if I == 0:
                break
            
            # Execute one time step
            self.step()
            t += 1
        
        return self.time_series
    
    def get_final_size(self):
        """Return the fraction of nodes that were eventually infected."""
        if len(self.time_series['R']) == 0:
            return 0.0
        return self.time_series['R'][-1] / self.N
    
    def get_peak_infected(self):
        """Return the maximum number of simultaneously infected nodes."""
        if len(self.time_series['I']) == 0:
            return 0
        return max(self.time_series['I'])


# ============================================================================
# Multi-Run Experiments with Averaging
# ============================================================================

def run_multiple_simulations(network_generator, network_params, beta, gamma, 
                            num_runs=100, description=""):
    """
    Run multiple SIR simulations and average the results.
    
    Args:
        network_generator: Function to generate network (e.g., nx.erdos_renyi_graph)
        network_params: Dict of parameters for network generation
        beta: Transmission probability
        gamma: Recovery probability
        num_runs: Number of simulation runs
        description: Network description for progress bar
    
    Returns:
        dict: Averaged time series and statistics
    """
    print(f"\n{'='*70}")
    print(f"Running {num_runs} simulations: {description}")
    print(f"Parameters: β={beta}, γ={gamma}")
    print(f"Network: {network_params}")
    print(f"{'='*70}")
    
    # Storage for all runs
    all_time_series = []
    final_sizes = []
    peak_infected = []
    
    for run in tqdm(range(num_runs), desc=f"{description}"):
        # Generate network
        G = network_generator(**network_params, seed=run)
        
        # Run simulation
        sim = SIRSimulation(G, beta, gamma, seed=run*1000)
        sim.infect_random_node()
        time_series = sim.run()
        
        all_time_series.append(time_series)
        final_sizes.append(sim.get_final_size())
        peak_infected.append(sim.get_peak_infected())
    
    # Compute average time series
    # First, find maximum time across all runs
    max_time = max(len(ts['t']) for ts in all_time_series)
    
    # Initialize arrays
    S_avg = np.zeros(max_time)
    I_avg = np.zeros(max_time)
    R_avg = np.zeros(max_time)
    S_std = np.zeros(max_time)
    I_std = np.zeros(max_time)
    R_std = np.zeros(max_time)
    
    # For each time step, average across all runs
    for t in range(max_time):
        S_values = []
        I_values = []
        R_values = []
        
        for ts in all_time_series:
            if t < len(ts['S']):
                S_values.append(ts['S'][t])
                I_values.append(ts['I'][t])
                R_values.append(ts['R'][t])
            else:
                # Epidemic has ended, use final values
                S_values.append(ts['S'][-1])
                I_values.append(ts['I'][-1])
                R_values.append(ts['R'][-1])
        
        S_avg[t] = np.mean(S_values)
        I_avg[t] = np.mean(I_values)
        R_avg[t] = np.mean(R_values)
        S_std[t] = np.std(S_values)
        I_std[t] = np.std(I_values)
        R_std[t] = np.std(R_values)
    
    # Print statistics
    print(f"\nResults:")
    print(f"  Average final outbreak size: {np.mean(final_sizes):.3f} ± {np.std(final_sizes):.3f}")
    print(f"  Average peak infected: {np.mean(peak_infected):.1f} ± {np.std(peak_infected):.1f}")
    print(f"  Average epidemic duration: {np.mean([len(ts['t']) for ts in all_time_series]):.1f} steps")
    
    return {
        'time': np.arange(max_time),
        'S_mean': S_avg,
        'I_mean': I_avg,
        'R_mean': R_avg,
        'S_std': S_std,
        'I_std': I_std,
        'R_std': R_std,
        'final_sizes': final_sizes,
        'peak_infected': peak_infected,
        'all_series': all_time_series
    }


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_epidemic_curves(results_dict, filename='figures/sir_epidemic_curves.png'):
    """
    Plot epidemic curves for all three network topologies.
    
    Args:
        results_dict: Dictionary with keys 'ER', 'WS', 'BA' containing results
        filename: Output filename
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    networks = [
        ('ER', 'Erdős-Rényi (Random Network)', '#2E86AB'),
        ('WS', 'Watts-Strogatz (Small-World Network)', '#06A77D'),
        ('BA', 'Barabási-Albert (Scale-Free Network)', '#E63946')
    ]
    
    for idx, (key, title, color) in enumerate(networks):
        ax = axes[idx]
        results = results_dict[key]
        
        # Plot mean curves
        ax.plot(results['time'], results['S_mean'], 
               color='#457B9D', linewidth=2.5, label='Susceptible', alpha=0.9)
        ax.plot(results['time'], results['I_mean'], 
               color='#E63946', linewidth=2.5, label='Infected', alpha=0.9)
        ax.plot(results['time'], results['R_mean'], 
               color='#06A77D', linewidth=2.5, label='Recovered', alpha=0.9)
        
        # Add confidence bands (±1 std)
        ax.fill_between(results['time'], 
                        results['I_mean'] - results['I_std'],
                        results['I_mean'] + results['I_std'],
                        color='#E63946', alpha=0.2)
        
        # Formatting
        ax.set_xlabel('Time Step', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Nodes', fontsize=12, fontweight='bold')
        ax.set_title(f'{title}', fontsize=14, fontweight='bold', pad=10)
        ax.legend(fontsize=11, loc='right', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, results['S_mean'][0] * 1.05])
        
        # Add statistics annotation
        peak_I = np.max(results['I_mean'])
        peak_t = np.argmax(results['I_mean'])
        final_R = results['R_mean'][-1]
        
        stats_text = f"Peak: {peak_I:.0f} at t={peak_t}\nFinal: {final_R:.0f} infected"
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved epidemic curves: {filename}")
    plt.close()


def plot_infected_comparison(results_dict, filename='figures/sir_infected_comparison.png'):
    """
    Plot only the infected curves for direct comparison.
    """
    plt.figure(figsize=(14, 8))
    
    networks = [
        ('ER', 'Random (ER)', '#2E86AB', 'o'),
        ('WS', 'Small-World (WS)', '#06A77D', 's'),
        ('BA', 'Scale-Free (BA)', '#E63946', '^')
    ]
    
    for key, label, color, marker in networks:
        results = results_dict[key]
        # Normalize to fraction
        I_fraction = results['I_mean'] / results['S_mean'][0]
        
        plt.plot(results['time'], I_fraction, 
                color=color, linewidth=3, label=label, 
                marker=marker, markersize=4, markevery=5, alpha=0.85)
        
        # Add confidence band
        I_std_frac = results['I_std'] / results['S_mean'][0]
        plt.fill_between(results['time'], 
                        I_fraction - I_std_frac,
                        I_fraction + I_std_frac,
                        color=color, alpha=0.15)
    
    plt.xlabel('Time Step', fontsize=14, fontweight='bold')
    plt.ylabel('Fraction of Population Infected', fontsize=14, fontweight='bold')
    plt.title('Epidemic Dynamics Across Network Topologies\n' + 
             r'$N=5000$, $\beta=0.05$, $\gamma=0.1$, $R_0 \approx 5$',
             fontsize=16, fontweight='bold', pad=15)
    plt.legend(fontsize=13, loc='best', framealpha=0.9)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim([0, None])
    
    # Add annotation about scale-free explosion
    plt.annotate('Scale-Free:\nExplosive cascade\nfrom hubs',
                xy=(15, 0.12), xytext=(30, 0.18),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='mistyrose', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Saved infected comparison: {filename}")
    plt.close()


def plot_r0_validation(beta, gamma, avg_degree, filename='figures/sir_r0_validation.png'):
    """
    Create a visual diagram explaining R0 calculation.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Calculate R0
    R0 = (beta * avg_degree) / gamma
    T_inf = 1 / gamma
    
    # Title
    fig.text(0.5, 0.95, r'Basic Reproduction Number ($R_0$) Calculation',
            ha='center', fontsize=18, fontweight='bold')
    
    # Formula derivation
    y_pos = 0.80
    line_height = 0.10
    
    formulas = [
        (r'$R_0 = \frac{\beta \langle k \rangle}{\gamma}$', 
         'Expected secondary infections per infected individual'),
        
        (r'$T_{\text{inf}} = \frac{1}{\gamma} = ' + f'{T_inf:.1f}' + r'$ time steps', 
         'Expected infectious period'),
        
        (r'Transmissions per step $= \beta \langle k \rangle = ' + 
         f'{beta * avg_degree:.2f}$', 
         'Expected infections per time step'),
        
        (r'$R_0 = ' + f'{T_inf:.1f}' + r' \times ' + f'{beta * avg_degree:.2f}' + 
         r' = ' + f'{R0:.1f}$',
         'Total expected transmissions over infectious period')
    ]
    
    for i, (formula, explanation) in enumerate(formulas):
        y = y_pos - i * line_height
        fig.text(0.15, y, formula, fontsize=14, fontweight='bold',
                family='monospace', bbox=dict(boxstyle='round', 
                facecolor='lightblue', alpha=0.3))
        fig.text(0.15, y - 0.04, explanation, fontsize=11, 
                style='italic', color='#444')
    
    # Interpretation box
    fig.text(0.5, 0.25, 'Interpretation', ha='center', 
            fontsize=16, fontweight='bold')
    
    interpretation = (
        f"With R₀ = {R0:.1f} > 1, each infected individual will infect\n"
        f"~{R0:.0f} others on average, causing exponential growth.\n\n"
        f"The epidemic will spread through the network until\n"
        f"susceptible depletion or intervention stops transmission."
    )
    
    fig.text(0.5, 0.15, interpretation, ha='center', fontsize=12,
            bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', 
            alpha=0.8), family='monospace')
    
    # Parameter box
    param_text = (
        f"Parameters:\n"
        f"β (transmission) = {beta}\n"
        f"γ (recovery) = {gamma}\n"
        f"⟨k⟩ (avg degree) = {avg_degree}"
    )
    
    fig.text(0.85, 0.75, param_text, fontsize=11,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
            verticalalignment='top', family='monospace')
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Saved R₀ validation diagram: {filename}")
    plt.close()


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Execute the complete SIR simulation experiment as described in Section 4.
    """
    print("\n" + "="*70)
    print("SIR EPIDEMIC SIMULATION FRAMEWORK")
    print("Section 4: The Simulation Framework")
    print("="*70)
    
    # Parameters from Section 4.4
    N = 5000
    avg_degree = 10
    beta = 0.05
    gamma = 0.1
    num_runs = 100
    
    print(f"\nGlobal Parameters:")
    print(f"  Network size (N): {N}")
    print(f"  Average degree (⟨k⟩): {avg_degree}")
    print(f"  Transmission probability (β): {beta}")
    print(f"  Recovery probability (γ): {gamma}")
    print(f"  Number of runs per topology: {num_runs}")
    print(f"  Expected R₀: {(beta * avg_degree) / gamma:.2f}")
    
    # Create R0 validation diagram
    plot_r0_validation(beta, gamma, avg_degree)
    
    # Define network generators
    results = {}
    
    # 1. Erdős-Rényi (Random)
    p_er = avg_degree / (N - 1)
    results['ER'] = run_multiple_simulations(
        network_generator=nx.erdos_renyi_graph,
        network_params={'n': N, 'p': p_er},
        beta=beta,
        gamma=gamma,
        num_runs=num_runs,
        description="Erdős-Rényi (Random Network)"
    )
    
    # 2. Watts-Strogatz (Small-World)
    results['WS'] = run_multiple_simulations(
        network_generator=nx.watts_strogatz_graph,
        network_params={'n': N, 'k': avg_degree, 'p': 0.1},
        beta=beta,
        gamma=gamma,
        num_runs=num_runs,
        description="Watts-Strogatz (Small-World Network)"
    )
    
    # 3. Barabási-Albert (Scale-Free)
    results['BA'] = run_multiple_simulations(
        network_generator=nx.barabasi_albert_graph,
        network_params={'n': N, 'm': avg_degree // 2},
        beta=beta,
        gamma=gamma,
        num_runs=num_runs,
        description="Barabási-Albert (Scale-Free Network)"
    )
    
    # Generate visualizations
    print("\n" + "="*70)
    print("Generating Visualizations...")
    print("="*70)
    
    plot_epidemic_curves(results)
    plot_infected_comparison(results)
    
    # Summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    
    for name, key in [('Random (ER)', 'ER'), 
                      ('Small-World (WS)', 'WS'), 
                      ('Scale-Free (BA)', 'BA')]:
        peak_I = np.max(results[key]['I_mean'])
        peak_t = np.argmax(results[key]['I_mean'])
        final_R = results[key]['R_mean'][-1]
        final_frac = final_R / N
        duration = len(results[key]['time'])
        
        print(f"\n{name}:")
        print(f"  Peak infected: {peak_I:.0f} nodes at t={peak_t}")
        print(f"  Final outbreak size: {final_R:.0f} / {N} ({final_frac:.1%})")
        print(f"  Epidemic duration: {duration} time steps")
    
    print("\n" + "="*70)
    print("✓ All simulations complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
