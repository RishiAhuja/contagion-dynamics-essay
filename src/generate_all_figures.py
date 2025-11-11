#!/usr/bin/env python3
"""
Master Script: Generate All Figures for the Paper

Runs all analysis and simulation scripts in the correct order.
Provides progress tracking and error handling.

Usage:
    python generate_all_figures.py
    python generate_all_figures.py --section 4  # Only Section 4
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            check=True,
            capture_output=False
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {script_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate all paper figures')
    parser.add_argument('--section', type=int, choices=[2, 3, 4], 
                       help='Generate figures for specific section only')
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("MASTER FIGURE GENERATION SCRIPT")
    print("Discrete Mathematics Paper - Network Contagion Dynamics")
    print("="*70)
    
    # Ensure figures directory exists
    figures_dir = Path(__file__).parent.parent / 'figures'
    figures_dir.mkdir(exist_ok=True)
    print(f"\nFigures will be saved to: {figures_dir}")
    
    # Track success
    all_success = True
    
    # Section 2: Graph Theory Primer (not applicable, no figures)
    
    # Section 3: Network Topologies
    section_3_scripts = [
        ('generate_phase_transition.py', 'Section 3.1: Erdős-Rényi Phase Transition'),
        ('generate_small_world_analysis.py', 'Section 3.2: Watts-Strogatz Small-World Analysis'),
        ('generate_ws_diagrams.py', 'Section 3.2: Watts-Strogatz Network Diagrams'),
        ('generate_ba_analysis.py', 'Section 3.3: Barabási-Albert Scale-Free Analysis'),
    ]
    
    # Section 4: SIR Simulation Framework
    section_4_scripts = [
        ('generate_sir_diagrams.py', 'Section 4: SIR Model Diagrams'),
        ('generate_sir_simulation.py', 'Section 4: SIR Epidemic Simulations'),
    ]
    
    # Determine which sections to run
    if args.section == 3:
        scripts_to_run = section_3_scripts
        print("\nGenerating Section 3 figures only...")
    elif args.section == 4:
        scripts_to_run = section_4_scripts
        print("\nGenerating Section 4 figures only...")
    else:
        scripts_to_run = section_3_scripts + section_4_scripts
        print("\nGenerating ALL figures...")
    
    # Run scripts
    for script, description in scripts_to_run:
        success = run_script(script, description)
        if not success:
            all_success = False
            response = input("\nContinue despite error? [y/N]: ")
            if response.lower() != 'y':
                print("\nAborting.")
                sys.exit(1)
    
    # Summary
    print("\n" + "="*70)
    if all_success:
        print("✓ ALL FIGURES GENERATED SUCCESSFULLY!")
    else:
        print("⚠ Some scripts encountered errors (see above)")
    print("="*70)
    
    # List generated files
    print("\nGenerated files:")
    for fig_file in sorted(figures_dir.glob('*.png')):
        size_mb = fig_file.stat().st_size / (1024 * 1024)
        print(f"  {fig_file.name:<50} ({size_mb:.2f} MB)")
    
    print("\n")


if __name__ == "__main__":
    main()
