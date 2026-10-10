<div align="center">

![MSAR-HGRN — Financial fraud detection with an intrinsic risk anchor and relational evidence](assets/research-cover.svg)

# MSAR-HGRN

Multi-Source Anchor-Guided Risk-Aware Heterogeneous Graph Residual Network

**[English](README.md) · [中文](README_CN.md)**

[Method](#method) · [Evidence](#evidence) · [Run the demo](#run-the-demo) · [Experiment status](docs/experiment_status.md)

</div>

Experimental results and model components for financial-statement-fraud detection on FiGraph. Maintained by [周文杰 · RookieZhou0617](https://github.com/RookieZhou0617).

> **The research question:** Once a company-level risk model is already strong, what useful evidence can heterogeneous relations still add?

This project builds a multi-source, current–history risk anchor (**MDRA**), then learns a selective graph residual on top of that frozen anchor (**MSAR-HGRN**). It studies financial-statement-fraud risk ranking on FiGraph under annual temporal evaluation—not causal fraud attribution or a production decision system.

| Inputs | Evaluation | Experiment status |
| :--- | :--- | :--- |
| Financial features + MD&A + self-history + cross-fitted risk | 2018–2021 rolling development; fixed-protocol 2022 OOT | Frozen models and reviewed aggregate results |

## Method

**Build the anchor → select relational evidence → learn a residual.**

1. **MDRA · Understand the company.** Compare each source's current state with the same company's available prior two years. Fuse current information, per-source deviations, and history availability.
2. **Graph residual · Add context selectively.** Select the top half of peers by frozen-anchor similarity, construct risk-relative messages, and combine relation-wise means through reliability gates and NULL-aware attention.
3. **Frozen prediction path · Preserve the starting point.** Add a zero-initialized hidden-state residual and reuse the frozen anchor classifier. Only the graph branch is trained in stage two.

[![Model architecture: multi-source risk anchor and heterogeneous graph residual framework](assets/model-framework.png)](assets/model-framework.png)

*Model architecture. Click for full resolution. [Detailed method](docs/methodology.md) · [Public implementation boundary](docs/implementation.md)*

The residual is exactly zero **at initialization**. Frozen parameters do not guarantee better future-year performance; the NULL channel can reduce reliance on relations but does not guarantee a zero learned residual.

## Evidence

The evidence follows the two-stage design:

- **Company history first.** MDRA outperforms the no-deviation, current-state-reference and shuffled-history controls in all four development years.
- **Relations as a supplement.** MSAR-HGRN improves on MDRA in three of four development years and in the frozen 2022 comparison; 2019 remains negative.
- **Risk ranking for targeted screening.** In 2022, the top 5% and 10% of companies capture 81.46% and 87.15% of positive cases, respectively, on average over the preset seeds.

![Development-year graph increments and fixed-protocol 2022 comparisons](assets/evidence-overview.svg)

### Fixed-protocol 2022 OOT

Same 5,132-company population, 123 positive cases. Primary results below are **arithmetic means over five preset seeds**, not metrics of averaged predictions. AUC-PR is computed as average precision.

| Model | AUC-PR ↑ | AUC-ROC ↑ | F1 @ 0.5 ↑ | Recall @ 5% ↑ | Recall @ 10% ↑ |
| :--- | ---: | ---: | ---: | ---: | ---: |
| LightGBM · tabular reference | 0.407467 | 0.925975 | 0.316580 | 0.622764 | 0.764228 |
| MDRA · company-level anchor | 0.489256 | 0.945054 | **0.585282** | 0.809756 | 0.866667 |
| MSAR-HGRN · real relations | **0.507052** | **0.947675** | 0.576771 | **0.814634** | **0.871545** |

Real relations improve mean AUC-PR by **+0.017797** over MDRA and **+0.017414** over the matched shuffled-relation control (AUC-PR 0.489639). Both paired comparisons are positive in 5/5 seeds.

Compared with the 901-dimensional tabular LightGBM reference, MSAR-HGRN has **+0.099586 AUC-PR** and **+19.19 / +10.73 percentage points** in Recall@5% / Recall@10%. This comparison is descriptive: the input families differ, so it does not isolate architecture under matched inputs.

The primary benefit is ranking and budget-limited screening, not improvement in every metric: F1 at 0.5 is lower than MDRA, and relational gains vary by year. Statistical significance and uniform temporal robustness are not established; [archived uncertainty and ensemble results](docs/experiments.md#supplementary-evidence) remain available.

The experiment page separates locally evaluated baselines from FiGraph literature reports, including FSFDLLM. The Source65 same-input reference is available for development only, not for 2022.

[Controls, variants, baselines & literature →](docs/experiments.md) · [Temporal protocol →](docs/strict_temporal_protocol.md) · [Reviewed aggregate numbers →](docs/evidence.json)

## Run the demo

```bash
git clone https://github.com/RookieZhou0617/risk-aware-financial-fraud-detection.git
cd risk-aware-financial-fraud-detection
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python examples/synthetic_demo.py
python -m unittest discover -s tests -v
```

No dataset download, GPU, or graph-framework dependency is needed. The demo uses **entirely synthetic inputs and labels** to exercise zero-initialized residuals and one graph-only optimization step.

This is a compact educational implementation, **not a one-command reproduction of the reported experiments**. The synthetic anchor is randomly initialized and frozen; its loss is a software smoke check, not experimental evidence.

## Explore the repository

| Start here | What you will find |
| :--- | :--- |
| [Methodology](docs/methodology.md) | Source representations, history deviations, graph residual and training boundary |
| [Evaluation](docs/experiments.md) | History controls, module variants, final screening results, baselines and literature |
| [Temporal protocol](docs/strict_temporal_protocol.md) | Selection / refit windows and historical-label availability assumptions |
| [Implementation guide](docs/implementation.md) | Model-to-code map and explicit differences from the research implementation |
| [Experiment status](docs/experiment_status.md) | Completed evaluations, frozen configuration and input-availability limits |
| [Model components](src/models/) · [Synthetic example](examples/) | Readable PyTorch components and executable demonstration |
| [Visual assets](assets/) | Model architecture, cover, result chart and rendering instructions |

## Data, scope & attribution

The study uses [FiGraph](https://github.com/XiaoguangWang23/FiGraph); see the [dataset paper](https://doi.org/10.1145/3701716.3715301). Data is not redistributed. Obtain it from the official source and follow the authors' license and usage terms.

This repository publishes reviewed aggregate results, methodology, compact code and synthetic examples. It excludes company-level data, labels, predictions, checkpoints, full experiment artifacts and private logs. No post-OOT retuning is performed.

**License status:** no open-source license has been granted for this repository yet. No ownership is claimed over FiGraph or other third-party resources.

---

<sub>Evidence snapshot: 2026-10-11 · Frozen results unchanged. Experiment IDs D3 / F0 remain unchanged.</sub>
