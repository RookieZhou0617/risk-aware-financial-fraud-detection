# Experimental evidence · 实验证据

[Home](../README.md) · [Temporal protocol](strict_temporal_protocol.md) · [Aggregate JSON](evidence.json)

All figures below were checked against accepted summary/metric files, not copied from an earlier conversational summary. No inference, training or metric recomputation from private predictions was performed for this refresh. The public JSON stores only reviewed aggregates and source identifiers.

## Reading the numbers

- **Primary metric:** AUC-PR, implemented as average precision.
- **Primary aggregation:** arithmetic mean over seeds 42, 52, 62, 72 and 82. Deterministic logistic regression is a single result.
- **Same final population:** 5,132 companies, 123 positive cases in 2022.
- **Budget recall:** fraction of positives captured in the top 5% / 10% of the ranked population.
- **F1:** fixed probability threshold 0.5, not a test-selected optimal threshold.
- Five-seed metric means and metrics of five-seed averaged probabilities are different quantities.

## 1 · Rolling development: an uneven relational increment

| Year | MDRA AUC-PR | MSAR-HGRN AUC-PR | Difference |
| ---: | ---: | ---: | ---: |
| 2018 | 0.597773 | 0.597915 | +0.000142 |
| 2019 | 0.636014 | 0.623425 | -0.012589 |
| 2020 | 0.506731 | 0.509296 | +0.002565 |
| 2021 | 0.579532 | 0.593541 | +0.014009 |

The four-year mean increment is **+0.001032**. The 2019 decline is part of the conclusion, not an outlier removed from reporting. Annual variation is considerably larger than the mean gain.

![Development increments and final comparison](../assets/evidence-overview.svg)

## 2 · Final fixed-protocol anchor / relation comparison

| Arm | Five-seed mean AUC-PR |
| :--- | ---: |
| MDRA (T0_D3) | 0.489256 |
| MSAR-HGRN, real relations (T1_F0_REAL) | 0.507052 |
| Matched shuffled relations (T2_F0_SHUFFLE) | 0.489639 |

- Real minus anchor: **+0.017797**, positive in 5/5 paired seeds.
- Real minus matched shuffle: **+0.017414**, positive in 5/5 paired seeds.

### Bootstrap uncertainty is a separate estimand

The paired bootstrap first averages the five seed probabilities for each company and arm, then resamples companies within positive/negative strata. It uses 10,000 replicates. These intervals are **not across-seed confidence intervals around the table's mean metrics**.

| Paired comparison | Bootstrap mean difference | Percentile 95% interval |
| :--- | ---: | :--- |
| Real − MDRA | +0.017781 | [−0.017470, +0.056282] |
| Real − matched shuffle | +0.017348 | [−0.017450, +0.055039] |

Both intervals cross zero. Neither 5/5 positive seeds nor the bootstrap mean establishes statistical significance.

### Metric trade-offs depend on aggregation

| Reporting mode | MDRA | Real graph residual | Reading |
| :--- | ---: | ---: | :--- |
| Five-seed mean F1 @ 0.5 | 0.585282 | 0.576771 | Decreases |
| Five-seed mean Recall @ 5% | 0.809756 | 0.814634 | Increases |
| Five-seed mean Recall @ 10% | 0.866667 | 0.871545 | Increases |
| Ensemble AUC-PR | 0.492451 | 0.507894 | Increases |
| Ensemble Recall @ 5% | 0.821138 | 0.813008 | Decreases |
| Ensemble Recall @ 10% | 0.878049 | 0.878049 | Unchanged |

The homepage consistently uses seed means. The ensemble Recall@5% decrease must not be described as a decrease in the primary five-seed mean Recall@5%.

## 3 · Six external baselines and the thesis models

| Model | AUC-PR ↑ | AUC-ROC ↑ | LogLoss ↓ | F1 @ 0.5 ↑ | R@5% ↑ | R@10% ↑ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic regression¹ | 0.025249 | 0.500220 | 0.704830 | 0.039627 | 0.048780 | 0.105691 |
| LightGBM | 0.407467 | 0.925975 | 0.072930 | 0.316580 | 0.622764 | 0.764228 |
| XGBoost | 0.336483 | 0.921669 | 0.079920 | 0.330464 | 0.575610 | 0.747967 |
| RGCN | 0.024694 | 0.504132 | 2.191274 | 0.021701 | 0.055285 | 0.107317 |
| HGT | 0.024858 | 0.509413 | 1.860234 | 0.036326 | 0.073171 | 0.115447 |
| FFD-DHG-inspired² | 0.148570 | 0.859742 | 0.187617 | 0.268376 | 0.409756 | 0.611382 |
| MDRA | 0.489256 | 0.945054 | 0.056671 | 0.585282 | 0.809756 | 0.866667 |
| MSAR-HGRN | 0.507052 | 0.947675 | 0.054272 | 0.576771 | 0.814634 | 0.871545 |

¹ Deterministic single run. All other rows are five-seed arithmetic means.

² FFD-DHG-inspired is an adapted implementation informed by the method, not an official exact reproduction.

### Comparison boundary

These models share the audited final evaluation population, but **their input families and modeling pipelines differ**. LightGBM's 0.407467 and MSAR-HGRN's 0.507052 can be compared descriptively; the difference does not isolate architecture under matched source inputs. Poor RGCN/HGT results here do not establish that these architectures are generally ineffective.

The supplementary **LightGBM-Source65** same-input comparison has status `BLOCKED_INPUT_UNAVAILABLE` for 2022. No test prediction or metric exists for that row. Do not substitute the ordinary LightGBM result or another text encoder; see [the availability explanation](research_status.md#source65-is-an-availability-blocker).

## 4 · What the evidence supports

In this dataset and protocol, current–history deviations help construct an intrinsic anchor, and real heterogeneous relations provide directionally positive incremental evidence in the final test. The graph contribution remains year-dependent and uncertain.

The results do **not** establish causal fraud transmission, uniformly positive transfer, statistical significance, broad state-of-the-art superiority, or production deployment validity. No test-driven repair or successor model is introduced by this showcase.

## Provenance

The aggregate snapshot was checked against research revision `0776595279d9a483bb8e66b5d33dd48e51f1a28e`.

| Evidence | Accepted source |
| :--- | :--- |
| Development rows | `s24_2_anchor_selective_native_gnn/formal/20260905T014639704710Z/seed_metrics.csv` |
| Final arms and bootstrap | `final_2022_oot/20260918T132623475938Z/`: seed metrics, ensemble metrics, OOT summary, bootstrap |
| External baseline means | `baseline_benchmark/final_2022/`: each model's summary |

These are source identifiers for traceability, not promises that the private artifact paths are downloadable from this public repository.
