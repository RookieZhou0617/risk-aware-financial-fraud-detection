# Temporal evaluation · 严格时序评价

[Home](../README.md) · [Results](experiments.md)

## Annual expanding windows

Selection training, validation and refitting are different operations. The supervised model-training rows start in **2016**, not 2014. The 2014–2015 snapshots provide historical / preprocessing context where allowed.

| Future evaluation year | Selection training | Validation | Refit window | Role |
| ---: | :--- | ---: | :--- | :--- |
| 2018 | 2016 | 2017 | 2016–2017 | Rolling development |
| 2019 | 2016–2017 | 2018 | 2016–2018 | Rolling development |
| 2020 | 2016–2018 | 2019 | 2016–2019 | Rolling development |
| 2021 | 2016–2019 | 2020 | 2016–2020 | Rolling development |
| 2022 | 2016–2020 | 2021 | 2016–2021 | Final fixed-protocol OOT |

Four development folds are not pooled with the final test into a five-year model-selection score.

## Information boundary

- Fit normalization, imputation, PCA and trainable feature components within each fold's permitted history.
- Build historical company summaries only from earlier available years; do not backfill from future observations.
- Generate cross-fitted risk signals without using a row's own target label in its fitted risk model.
- Keep model selection on the training/validation side of the boundary.
- Use annual relation snapshots without future-year edges or future outcomes.
- Freeze configurations and preset seeds before the final test for the corresponding evaluation protocol.
- Keep fitted transformations, probabilities and evaluation identities auditable in the research repository.

### Historical-label availability is an assumption

FiGraph's annual label organization does not itself establish exact real-world disclosure dates. The thesis treats prior annual labels as available according to its annual protocol. This is a study assumption; it must not be advertised as fully verified, disclosure-date-level point-in-time deployment.

### The 2022 boundary is protocol-specific

A historical candidate was evaluated on 2022 earlier in the research project. Therefore, 2022 was **not untouched throughout the entire project's history**. The current result is the terminal evaluation of the frozen MDRA / graph-residual protocol, not a claim of a pristine never-accessed holdout across all past experiments.

The final anchor/real/shuffle comparison and the subsequently frozen external-baseline benchmark have their own recorded protocols. Their fixed configurations are retained; no final outcomes are used here for retuning, model rescue or successor selection.

## What the public helpers do

`src/data/` contains small temporal-split and cross-fitting helpers. They illustrate the boundary but do not reproduce the full causal feature pipeline, native graph construction or formal artifact audit. The synthetic demo has no claim of temporal generalization.

## Reporting rule

Report five-seed arithmetic means separately from metrics computed on averaged probabilities. Label development, final OOT and post-hoc interpretation clearly. Never replace preset-seed summaries with the best seed or best year.
