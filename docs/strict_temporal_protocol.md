# Strict temporal evaluation protocol

## Why random splitting is unsafe

Random train/test splits mix companies and market regimes from different calendar years. In financial fraud detection, this can leak future preprocessing statistics, labels, risk estimates, text representations, or graph structure into the model-development period. It also produces an evaluation that is unlike deployment, where future years do not yet exist.

## Rolling evaluation

The thesis development study uses expanding, point-in-time folds. For the public summary, the verified evaluation pattern is:

| Training years | Validation year | Future development fold |
|---|---:|---:|
| 2014–2016 | 2017 | 2018 |
| 2014–2017 | 2018 | 2019 |
| 2014–2018 | 2019 | 2020 |
| 2014–2019 | 2020 | 2021 |

The validation year selects checkpoints or hyperparameters. The future fold is used only after that selection. The 2022 snapshot is not part of the public development result reported here.

## Cross-fitting and historical risk banks

Any learned risk value used as a feature must be out-of-fold for the row that receives it. Historical cross-fitting trains only on earlier years, produces predictions for a later held-out historical year, and stores those predictions with explicit year provenance. A target-year model may consume only bank entries whose availability predates that target.

## Point-in-time rules

- Split raw rows by year before fitting preprocessing.
- Fit scalers, imputers, text transforms, and learned representations inside each training boundary.
- Use only same-company observations from earlier years for history.
- Never use target-year labels to construct graph features, gates, or historical risks.
- Select checkpoints on the inner validation year, not the future evaluation year.
- Record the maximum accessible year and fail closed on unexpected future inputs.

The utilities in `src/data/temporal_split.py` encode the ordering constraints, but a full application must also enforce point-in-time availability in every upstream feature builder.
