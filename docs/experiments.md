# Development-study summary

The private thesis pipeline explored how to add heterogeneous graph evidence to a strong no-graph risk model. This public page reports only aggregated development conclusions; it contains no sample-level predictions, checkpoints, or full experiment history.

| Design | Development finding |
|---|---|
| No-graph current-history model | Established the stable intrinsic risk anchor used by later graph studies. |
| Unrestricted joint graph model | Unstable across years; graph integration could degrade the intrinsic representation. |
| Frozen risk anchor | Structurally protected the intrinsic encoder and isolated graph correction. |
| Selective relation gate | Best current graph mechanism; mean AUC-PR change of +0.006005 versus the no-graph anchor across 2018–2021 development folds. |
| Temporal extension | Exploratory and not supported as a final extension. |

The selective graph model improved AUC-PR in three of four development years, but it did **not** pass all preregistered acceptance gates because the worst-year change and cross-seed stability were insufficient. Accordingly, this repository does not claim statistical significance, state-of-the-art performance, or a finalized thesis model.

The main mechanism-level findings are:

1. Strong intrinsic risk representations should be protected from unrestricted graph message passing.
2. Real relational structure can carry incremental fraud-risk information.
3. Relational utility varies by company, relation, and time.
4. Selective correction was more reliable than unrestricted integration in the current development study, while still falling short of the full stability criteria.

All figures above are development evidence from previously inspected 2018–2021 folds. They are not an independent final OOT claim.
