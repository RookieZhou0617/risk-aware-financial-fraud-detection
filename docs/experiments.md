# Evidence summary

This page reports only aggregate conclusions from the private thesis evidence package. The public repository contains no sample-level predictions, checkpoints, raw data, or complete experiment history.

## Model-selection outcome

Model development is closed. The frozen framework is:

- **D3** — multi-source current-history deviation intrinsic risk anchor;
- **F0** — frozen-anchor, conservative relational hidden-state residual.

F0 uses stable top-half peer selection, target-relative risk-aware messages, a low-capacity relation reliability gate, NULL-aware cross-relation fusion, and a zero-initialized hidden residual. D3 remains frozen during graph-branch fitting.

More complex aggregation, gating, temporal repair, selector, fusion, ranking-objective, and robust-optimization candidates were evaluated under preregistered rules but did not provide sufficient stable evidence to replace F0. These negative and mixed results are part of the scientific conclusion: complexity was not promoted merely because it was available.

## Development evidence: 2018–2021

| Future fold | F0 minus D3 AUC-PR |
|---:|---:|
| 2018 | +0.000142 |
| 2019 | -0.012589 |
| 2020 | +0.002565 |
| 2021 | +0.014009 |
| Equal-year mean | +0.001032 |

F0 was positive in three of four years, but the 2019 negative transfer is material. The model was retained as a conservative relational extension with an explicit temporal-heterogeneity caveat—not as a uniformly superior replacement for D3.

## Final fixed-protocol 2022 OOT

Model exploration was closed and the D3 + F0 framework was frozen before outcome access. The terminal comparison used D3, F0 with real relations, and F0 with matched shuffled relations.

### Five-seed primary metric

| Arm | Mean AUC-PR | Difference |
|---|---:|---:|
| D3 | 0.489255663 | — |
| F0 real relations | 0.507052423 | +0.017796761 vs D3 |
| F0 matched shuffle | 0.489638571 | +0.017413852 real vs shuffle |

The two F0 comparisons were positive for all five matched seeds.

### Uncertainty

| Comparison | Paired bootstrap 95% interval |
|---|---:|
| F0 real minus D3 | [-0.017470368, 0.056282279] |
| F0 real minus matched shuffle | [-0.017450167, 0.055038887] |

Both intervals cross zero. The appropriate interpretation is directionally consistent positive OOT evidence with substantial estimation uncertainty. The result does not establish statistical significance or prove temporal robustness.

### Ensemble metrics

| Arm | AUC-PR | AUC-ROC | LogLoss | Recall@5% | Recall@10% |
|---|---:|---:|---:|---:|---:|
| D3 | 0.492451 | 0.948642 | 0.055589 | 0.821138 | 0.878049 |
| F0 real relations | 0.507894 | 0.951169 | 0.053383 | 0.813008 | 0.878049 |
| F0 matched shuffle | 0.492832 | 0.947592 | 0.055908 | 0.813008 | 0.878049 |

F0 improved ensemble AUC-PR, AUC-ROC, and LogLoss over D3, while Recall@5% was lower and Recall@10% was unchanged. No across-the-board metric improvement is claimed.

## Interpretation boundary

The final result is a fixed-protocol OOT evaluation of the frozen D3 + F0 framework. It is not a new model-selection fold, and it cannot be used to rescue, retune, or redesign the model. Earlier work had used 2022 for an older candidate, so 2022 is not described as a never-touched pristine holdout for the entire project; the later D3/F0 development and freeze did not use the D3/F0 2022 outcome.

No post-OOT model modification, additional model-selection run, or claim of state-of-the-art performance is made.
