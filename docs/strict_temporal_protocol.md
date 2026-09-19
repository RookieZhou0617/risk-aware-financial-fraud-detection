# Strict temporal evaluation protocol

## Why random splitting is unsafe

Random train/test splits mix companies and market regimes from different calendar years. In financial fraud detection, this can leak future preprocessing statistics, labels, risk estimates, text representations, or graph structure into model development. It also differs from deployment, where future years do not yet exist.

## Rolling development evaluation

The thesis used expanding, point-in-time folds:

| Training years | Validation year | Future development fold |
|---|---:|---:|
| 2014–2016 | 2017 | 2018 |
| 2014–2017 | 2018 | 2019 |
| 2014–2018 | 2019 | 2020 |
| 2014–2019 | 2020 | 2021 |

The validation year selects checkpoints or frozen protocol choices. The future fold is accessed only after selection for that fold.

## Cross-fitting and historical risk banks

Any learned risk value used as a feature must be out-of-fold for the row that receives it. Historical cross-fitting trains only on earlier years, predicts a later held-out historical year, and stores predictions with explicit year provenance. A target-year model may consume only bank entries whose availability predates that target.

## Final fixed-protocol 2022 OOT

Model development was closed before final D3/F0 2022 outcome access. The frozen terminal protocol used:

| Phase | Years |
|---|---|
| Selection training | 2016–2020 |
| Validation | 2021 |
| Final refit | 2016–2021 |
| Terminal OOT evaluation | 2022 |

Only three frozen arms were evaluated: D3, F0 with real relations, and F0 with matched shuffled relations. The result cannot authorize rescue, retuning, a successor model, or a second model-selection run.

The project does not describe 2022 as a pristine holdout for its entire history because an older candidate had previously been evaluated on that year. The precise claim is narrower: later D3/F0 development, structural selection, and freezing did not use the D3/F0 2022 outcome; the reported result is the final fixed-protocol OOT evaluation of that frozen framework.

## Point-in-time rules

- Split raw rows by year before fitting preprocessing.
- Fit scalers, imputers, text transforms, and learned representations inside each training boundary.
- Use only same-company observations from earlier years for history.
- Never use target-year labels to construct graph features, gates, peer rankings, or historical risks.
- Select checkpoints on the validation year, not the future evaluation year.
- Build graph inputs only from information available for the relevant snapshot.
- Record the maximum accessible year and fail closed on unexpected future inputs.
- Freeze protocols, model identities, source identities, and artifact hashes before outcome access.

The utilities in `src/data/temporal_split.py` encode ordering constraints, but a full application must enforce point-in-time availability in every upstream feature builder.
