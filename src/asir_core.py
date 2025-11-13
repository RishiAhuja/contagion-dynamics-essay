#!/usr/bin/env python3
"""
ASIR Core Implementation - Adaptive SIR Model

This module implements the Adaptive SIR (ASIR) model with network co-evolution
as described in Section 5 of the paper.

Classes:
    AdaptiveSIRSimulation: Main ASIR simulation with edge cutting and triadic closure
"""

import networkx as nx
import numpy as np
import random
from collections import defaultdict


class AdaptiveSIRSimulation:
    """
    Adaptive SIR epidemic model with dynamic network topology.
    
    Implements two behavioral rules:
    1. Edge Cutting (α): Susceptible nodes cut connections to infected neighbors
    2. Triadic Closure (μ): Susceptible nodes form pods with friends-of-friends
    
    States:
        - SUSCEPTIBLE (0): Can become infected
        - INFECTED (1): Currently infectious, can transmit
        - RECOVERED (2): Immune, terminal state
    
    Parameters:
        - beta (β): Transmission probability per infected neighbor
        - gamma (γ): Recovery probability per time step
        - alpha (α): Edge cutting probability (isolation)
        - mu (μ): Triadic closure probability (clustering)
    """
    
    # State constants
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    
    def __init__(self, graph, beta, gamma, alpha, mu, seed=None):
        """
        Initialize ASIR simulation.
        
        Args:
            graph: NetworkX graph (will be modified during simulation)
            beta: Transmission probability
            gamma: Recovery probability
            alpha: Edge cutting probability (0 = no cutting, 1 = always cut)
            mu: Triadic closure probability (0 = no closure, 1 = always close)
            seed: Random seed for reproducibility
        """
        self.G = graph.copy()  # Create copy to avoid modifying original
        self.beta = beta
        self.gamma = gamma
        self.alpha = alpha
        self.mu = mu
        self.N = len(graph.nodes())
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Initialize all nodes as susceptible
        self.state = {node: self.SUSCEPTIBLE for node in self.G.nodes()}
        
        # Time series storage - epidemic
        self.time_series = {
            'S': [],
            'I': [],
            'R': [],
            't': []
        }
        
        # Time series storage - network metrics
        self.network_metrics = {
            'avg_degree': [],
            'clustering': [],
            'num_edges': [],
            'num_components': []
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
    
    def compute_network_metrics(self):
        """Compute current network topology metrics."""
        metrics = {}
        
        # Average degree
        if self.G.number_of_edges() > 0:
            metrics['avg_degree'] = 2 * self.G.number_of_edges() / self.G.number_of_nodes()
        else:
            metrics['avg_degree'] = 0
        
        # Clustering coefficient (can be slow, use sampling for large networks)
        try:
            metrics['clustering'] = nx.average_clustering(self.G)
        except:
            metrics['clustering'] = 0
        
        # Number of edges
        metrics['num_edges'] = self.G.number_of_edges()
        
        # Number of connected components
        metrics['num_components'] = nx.number_connected_components(self.G)
        
        return metrics
    
    def adaptive_step(self):
        """
        Execute adaptive network updates (Rules 1 and 2).
        
        Rule 1 (Edge Cutting): Remove S-I edges with probability α
        Rule 2 (Triadic Closure): Add S-S edges that close triangles with probability μ
        
        Returns:
            tuple: (num_edges_cut, num_edges_added)
        """
        edges_cut = 0
        edges_added = 0
        
        # ========================================================================
        # RULE 1: Edge Cutting (Fear-Based Isolation)
        # ========================================================================
        edges_to_remove = []
        
        for u, v in list(self.G.edges()):
            # Check if one is S and other is I
            if ((self.state[u] == self.SUSCEPTIBLE and self.state[v] == self.INFECTED) or
                (self.state[v] == self.SUSCEPTIBLE and self.state[u] == self.INFECTED)):
                
                # Cut edge with probability alpha
                if random.random() < self.alpha:
                    edges_to_remove.append((u, v))
        
        self.G.remove_edges_from(edges_to_remove)
        edges_cut = len(edges_to_remove)
        
        # ========================================================================
        # RULE 2: Triadic Closure (Pod Formation)
        # ========================================================================
        edges_to_add = []
        
        # Get all susceptible nodes
        susceptible_nodes = [n for n in self.G.nodes() 
                           if self.state[n] == self.SUSCEPTIBLE]
        
        # For computational efficiency, we use a heuristic:
        # Only check pairs where at least one node was involved in edge cutting
        # OR randomly sample pairs if no cutting occurred
        
        nodes_to_check = set()
        for u, v in edges_to_remove:
            if self.state[u] == self.SUSCEPTIBLE:
                nodes_to_check.add(u)
            if self.state[v] == self.SUSCEPTIBLE:
                nodes_to_check.add(v)
        
        # If no edges were cut, randomly sample some susceptible nodes
        if len(nodes_to_check) == 0 and len(susceptible_nodes) > 0:
            sample_size = min(50, len(susceptible_nodes))
            nodes_to_check = set(random.sample(susceptible_nodes, sample_size))
        
        # Check for triadic closure opportunities
        for u in nodes_to_check:
            if u not in self.G:
                continue
                
            # Get neighbors of u
            u_neighbors = set(self.G.neighbors(u))
            
            for v in u_neighbors:
                if self.state[v] != self.SUSCEPTIBLE:
                    continue
                
                # Get neighbors of v
                v_neighbors = set(self.G.neighbors(v))
                
                # Find common neighbors (potential third point of triangle)
                for w in v_neighbors:
                    if (w == u or 
                        self.state[w] != self.SUSCEPTIBLE or
                        self.G.has_edge(u, w)):
                        continue
                    
                    # We have an open triangle: u-v-w with u and w not connected
                    # Close it with probability mu
                    if random.random() < self.mu:
                        edges_to_add.append((u, w))
                        break  # Only add one edge per node u to avoid explosion
        
        # Add edges (avoid duplicates)
        edges_to_add = list(set(edges_to_add))
        self.G.add_edges_from(edges_to_add)
        edges_added = len(edges_to_add)
        
        return edges_cut, edges_added
    
    def epidemic_step(self):
        """
        Execute one time step of SIR epidemic dynamics.
        
        Uses the same rules as Section 4:
        - Infection: P = 1 - (1-β)^k_I
        - Recovery: P = γ
        
        Returns:
            tuple: (num_infections, num_recoveries)
        """
        to_infect = set()
        to_recover = set()
        
        # Process infections (S → I)
        for node in self.G.nodes():
            if self.state[node] == self.SUSCEPTIBLE:
                # Count infected neighbors
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
    
    def run(self, max_steps=500, track_network=True):
        """
        Run the ASIR simulation until epidemic ends.
        
        Args:
            max_steps: Maximum number of time steps
            track_network: Whether to compute network metrics (can be slow)
        
        Returns:
            dict: Combined time series of epidemic and network metrics
        """
        t = 0
        self.time_series = {'S': [], 'I': [], 'R': [], 't': []}
        self.network_metrics = {
            'avg_degree': [],
            'clustering': [],
            'num_edges': [],
            'num_components': []
        }
        
        while t < max_steps:
            # Count current epidemic state
            S, I, R = self.count_states()
            
            # Record epidemic time series
            self.time_series['S'].append(S)
            self.time_series['I'].append(I)
            self.time_series['R'].append(R)
            self.time_series['t'].append(t)
            
            # Record network metrics if requested
            if track_network:
                metrics = self.compute_network_metrics()
                self.network_metrics['avg_degree'].append(metrics['avg_degree'])
                self.network_metrics['clustering'].append(metrics['clustering'])
                self.network_metrics['num_edges'].append(metrics['num_edges'])
                self.network_metrics['num_components'].append(metrics['num_components'])
            
            # Stop if no infected nodes remain
            if I == 0:
                break
            
            # CRITICAL: Adaptive updates BEFORE epidemic spread
            # This gives adaptation a "head start" - best case scenario
            self.adaptive_step()
            
            # Then epidemic spreads on the modified network
            self.epidemic_step()
            
            t += 1
        
        return {
            'epidemic': self.time_series,
            'network': self.network_metrics
        }
    
    def get_final_size(self):
        """Return fraction of nodes that were eventually infected."""
        if len(self.time_series['R']) == 0:
            return 0.0
        return self.time_series['R'][-1] / self.N
    
    def get_peak_infected(self):
        """Return maximum number of simultaneously infected nodes."""
        if len(self.time_series['I']) == 0:
            return 0
        return max(self.time_series['I'])
    
    def get_epidemic_duration(self):
        """Return total duration of epidemic."""
        return len(self.time_series['t'])


# ============================================================================
# Helper Functions for Running Multiple Simulations
# ============================================================================

def run_multiple_asir_simulations(network_generator, network_params, 
                                   beta, gamma, alpha, mu,
                                   num_runs=50, description="",
                                   track_network=False):
    """
    Run multiple ASIR simulations and collect statistics.
    
    Args:
        network_generator: Function to generate network (e.g., nx.barabasi_albert_graph)
        network_params: Dict of parameters for network generation
        beta, gamma, alpha, mu: ASIR model parameters
        num_runs: Number of simulation runs
        description: Description for progress output
        track_network: Whether to track network metrics (slower)
    
    Returns:
        dict: Aggregated results with means and standard deviations
    """
    from tqdm import tqdm
    
    print(f"\n{'='*70}")
    print(f"Running {num_runs} ASIR simulations: {description}")
    print(f"Epidemic: β={beta}, γ={gamma}")
    print(f"Adaptive: α={alpha}, μ={mu}")
    print(f"Network: {network_params}")
    print(f"{'='*70}")
    
    results = {
        'peak_infected': [],
        'final_size': [],
        'duration': [],
        'all_series': []
    }
    
    if track_network:
        results['network_metrics'] = []
    
    for run in tqdm(range(num_runs), desc=description):
        # Generate network
        G = network_generator(**network_params, seed=run)
        
        # Run ASIR simulation
        sim = AdaptiveSIRSimulation(G, beta, gamma, alpha, mu, seed=run*1000)
        sim.infect_random_node()
        output = sim.run(track_network=track_network)
        
        # Collect metrics
        results['peak_infected'].append(sim.get_peak_infected())
        results['final_size'].append(sim.get_final_size())
        results['duration'].append(sim.get_epidemic_duration())
        results['all_series'].append(output['epidemic'])
        
        if track_network:
            results['network_metrics'].append(output['network'])
    
    # Compute statistics
    results['peak_mean'] = np.mean(results['peak_infected'])
    results['peak_std'] = np.std(results['peak_infected'])
    results['size_mean'] = np.mean(results['final_size'])
    results['size_std'] = np.std(results['final_size'])
    results['duration_mean'] = np.mean(results['duration'])
    results['duration_std'] = np.std(results['duration'])
    
    print(f"\nResults:")
    print(f"  Peak infected: {results['peak_mean']:.1f} ± {results['peak_std']:.1f}")
    print(f"  Final size: {results['size_mean']:.3f} ± {results['size_std']:.3f}")
    print(f"  Duration: {results['duration_mean']:.1f} ± {results['duration_std']:.1f} steps")
    
    return results


def average_time_series(all_series, max_length=None):
    """
    Average epidemic time series across multiple runs.
    
    Args:
        all_series: List of time series dicts
        max_length: Maximum time to average over (None = use longest)
    
    Returns:
        dict: Averaged time series with mean and std
    """
    if max_length is None:
        max_length = max(len(ts['t']) for ts in all_series)
    
    S_all = np.zeros((len(all_series), max_length))
    I_all = np.zeros((len(all_series), max_length))
    R_all = np.zeros((len(all_series), max_length))
    
    for i, ts in enumerate(all_series):
        length = len(ts['S'])
        S_all[i, :length] = ts['S']
        I_all[i, :length] = ts['I']
        R_all[i, :length] = ts['R']
        
        # Fill remaining with final values
        if length < max_length:
            S_all[i, length:] = ts['S'][-1]
            I_all[i, length:] = ts['I'][-1]
            R_all[i, length:] = ts['R'][-1]
    
    return {
        't': np.arange(max_length),
        'S_mean': np.mean(S_all, axis=0),
        'S_std': np.std(S_all, axis=0),
        'I_mean': np.mean(I_all, axis=0),
        'I_std': np.std(I_all, axis=0),
        'R_mean': np.mean(R_all, axis=0),
        'R_std': np.std(R_all, axis=0)
    }
