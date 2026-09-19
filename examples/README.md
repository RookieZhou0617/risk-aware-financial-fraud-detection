# Synthetic demo

Run from the repository root:

```bash
python examples/synthetic_demo.py
```

The script creates random company features, two historical observations, three synthetic peer relations, and binary labels. It exercises the frozen-anchor path, deterministic top-half peer selection, binary cross-entropy, and one graph-only optimization step. No FiGraph or thesis data is used, and the output is not a benchmark result.
