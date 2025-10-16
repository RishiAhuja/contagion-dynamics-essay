# Running the Phase Transition Visualization

## Quick Start

```bash
# Generate figures with default size (N=250)
python3 src/generate_phase_transition.py
```

## Changing Network Size

Edit `src/generate_phase_transition.py` and change the `NETWORK_SIZE` variable:

```python
NETWORK_SIZE = 250   # Fast, good for paper figures (default)
# NETWORK_SIZE = 1000  # Moderate size
# NETWORK_SIZE = 5000  # Large network
```

## Network Size Guide

### N = 250 (Recommended for paper)
- **Time**: ~5-10 seconds
- **Quality**: Excellent visualization
- **Requirements**: Just networkx and matplotlib
- **Best for**: Academic paper figures

### N = 1000
- **Time**: ~30-60 seconds
- **Quality**: Good, but nodes become smaller
- **Requirements**: scipy recommended
- **Best for**: Demonstrations

### N = 5000
- **Time**: 2-5 minutes
- **Quality**: Nodes are very small
- **Requirements**: **Must install scipy first**
- **Best for**: Statistical analysis

## Installing scipy (Required for N > 500)

```bash
# In your virtual environment
pip install scipy

# Or add to requirements.txt and reinstall
pip install -r requirements.txt
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'scipy'"
**Solution**: Install scipy:
```bash
pip install scipy
```

### Visualization is too slow
**Solution**: Reduce network size in the script
- Change `NETWORK_SIZE = 250` for faster generation

### Nodes are too small
**Solution**: The script automatically adjusts node size based on N
- For large networks, nodes must be smaller to avoid overlap
- Use N=250 for best visualization quality

### Layout looks messy
The script uses different layout algorithms based on network properties:
- **Spring layout**: N ≤ 500 (best looking, slow)
- **Kamada-Kawai**: N > 500 with giant component (faster)
- **Random layout**: Fragmented networks (fastest)

## Output

All figures are saved to `figures/` directory:
- `phase_transition_lambda_0.5.png`
- `phase_transition_lambda_0.8.png`
- `phase_transition_lambda_1.0.png`
- `phase_transition_lambda_1.2.png`
- `phase_transition_lambda_2.0.png`
- `phase_transition_curve.png` (analysis)

## Example Output

```
============================================================
Generating Phase Transition Visualizations
============================================================
Network size: N = 250
Lambda values: [0.5, 0.8, 1.0, 1.2, 2.0]
============================================================

Generating network for λ = 0.5...
  Edge probability p = 0.002008
Saved: figures/phase_transition_lambda_0.5.png
  - Total nodes: 250
  - Total edges: 65
  - Giant component size: 7 (2.8%)

...
```

## Tips for Paper Quality

1. **Use N = 250**: Best balance of clarity and speed
2. **High DPI**: Figures are saved at 300 DPI (publication quality)
3. **Consistent seed**: Random seed is fixed (seed=42) for reproducibility
4. **Color scheme**: Red for giant component, gray for isolated clusters
