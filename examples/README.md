# Synthetic demonstration

Run from the repository root:

```bash
python examples/synthetic_demo.py
```

The script constructs 24 synthetic companies, two historical steps, four random source groups and three ring-relation channels. It freezes a **randomly initialized** intrinsic encoder and classifier, verifies the initial graph residual numerically, and performs one graph-only BCE optimization step.

Expected structural output includes:

```text
Synthetic demo completed
nodes=24, relations=3
initial graph-residual max abs=0.000000
```

Loss and attention numbers are smoke-check output, not accuracy claims. No FiGraph data, actual company labels, pretrained checkpoint or thesis prediction is loaded.

See [the implementation boundary](../docs/implementation.md) before interpreting the code as a reproduction. Run software tests with `python -m unittest discover -s tests -v`.
