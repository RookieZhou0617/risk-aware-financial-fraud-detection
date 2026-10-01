# Public implementation · 代码与复现边界

[Home](../README.md) · [Formal method](methodology.md)

## A readable demonstration, not the private pipeline

This repository exposes the structural idea with native PyTorch: a multi-source anchor, deterministic peer selection, risk-aware messages, relation reliability, NULL-aware fusion, and a zero-initialized hidden residual.

| Component | Public code |
| :--- | :--- |
| Multi-source current/history encoder | [multi_source_risk_encoder.py](../src/models/multi_source_risk_encoder.py) |
| Peer selection and relation messages | [relational_message.py](../src/models/relational_message.py) |
| Reliability and cross-relation fusion | [relation_reliability.py](../src/models/relation_reliability.py) |
| Frozen anchor and residual composition | [risk_aware_graph_model.py](../src/models/risk_aware_graph_model.py) |
| Synthetic graph-only step | [synthetic_demo.py](../examples/synthetic_demo.py) |
| Software invariants | [tests](../tests/) |

Existing Python class names and D3/F0 experimental identifiers are retained for compatibility. The thesis uses MDRA and MSAR-HGRN in its narrative.

## Important differences

| Aspect | Formal thesis model | Public synthetic demonstration |
| :--- | :--- | :--- |
| Source inputs | 1 + 32 + 4 + 28 = 65 dimensions | Random 12 / 8 / 4 / 3 dimensional sources |
| Input construction | Fold-specific processing, frozen FinBERT2, cross-fitted risk | No financial preprocessing or text model |
| Anchor preparation | Fitted MDRA anchor, then frozen | Randomly initialized anchor, then frozen |
| Source encoder | Source projection with normalization; history-length deviation feature; fixed formal widths | Simplified projection/MLP; history-availability feature; configurable widths |
| Graph | Ten native channels; audited candidate construction | Three illustrative ring relations |
| Optimization | Formal staged training, selection/refit protocol and audited outputs | One synthetic BCE graph-only step |
| Evaluation | Preset-seed annual metrics and final controls | Shape, gradient and identity smoke checks |

The demo's losses and attention weights are **not research findings**. It cannot regenerate the aggregate numbers in [evidence.json](evidence.json).

## Run and test

```bash
pip install -r requirements.txt
python examples/synthetic_demo.py
python -m unittest discover -s tests -v
```

The tests check deterministic top-half selection (including ties), zero-initialized residual identity, the frozen-anchor gradient boundary and missing-relation behavior. They test this public implementation only; they do not audit or reproduce the thesis experiments.

For real inputs, callers must construct valid, deduplicated peer sets without self-links and enforce their own temporal and information-availability boundaries. This repository does not ship a production ingestion or deployment workflow.

## What is deliberately absent

Raw/processed data, company identifiers and labels, sample-level predictions, checkpoints, private experiment controllers, full artifact histories and thesis drafts are not distributed. Reproducing the thesis requires the official data, exact feature identities, trained assets and research protocol; the showcase is not a substitute for them.
