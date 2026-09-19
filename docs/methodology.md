# Methodology

## 1. Problem definition

For company $i$ at year $t$, the task is to estimate financial-statement-fraud risk using information available at or before $t$. Inputs include company-level financial variables, an MD&A text representation, self-history, point-in-time risk signals, and heterogeneous relations to peers or background entities.

The central question is whether relational information can add useful evidence without damaging an already strong company-level risk representation.

## 2. D3 multi-source intrinsic risk anchor

Each source is projected independently into a common hidden space and fused into a current state. Keeping source projections separate makes the representation auditable and limits domination by source dimensionality.

Only strictly historical observations of the same company are summarized. For current token $c_{i,t}^{(s)}$ and historical token $r_{i,<t}^{(s)}$, the deviation encoder uses

$$
[c-r,\ |c-r|,\ c\odot r,\ \cos(c,r),\ m],
$$

where $m$ indicates whether history is available. Missing history is represented explicitly rather than imputed from future observations. The fused current and deviation states produce the frozen D3 representation $h_i^0$, logit $z_i^0$, and probability $p_i^0$.

## 3. Stable peer selection

Within each available relation, peers are ranked by cosine similarity in the frozen D3 hidden space. F0 keeps the top $\lceil n/2 \rceil$ peers for each target and relation. Ranking is label-free and non-differentiable; ties are resolved deterministically by ascending canonical peer index.

This selection is conservative: it reduces noisy propagation without changing the intrinsic anchor or using target labels.

## 4. Risk-aware relational messages

For a selected peer $j$ connected to target $i$ through relation $r$, the message function consumes

$$
[h_j^0,\ h_j^0-h_i^0,\ |h_j^0-h_i^0|,\ p_j^0-p_i^0,\ e_r].
$$

The relation context is the mean selected-peer message. The implementation uses native PyTorch operations and does not require PyTorch Geometric or DGL.

## 5. Relation reliability and NULL-aware fusion

Relation utility is not assumed to be uniform. A low-capacity gate estimates reliability from label-free statistics:

- selected-peer count;
- selected-peer similarity mean and standard deviation;
- mean absolute intrinsic-risk gap;
- peer-risk dispersion;
- relation-context norm.

The gate has a conservative prior, and unavailable relations receive zero reliability. Target-conditioned attention then combines the gated relation contexts. An explicit NULL relation is always available, allowing the model to abstain when no observed relation is useful.

## 6. Anchor-preserving graph residual

The final representation is

$$
h_i^{\mathrm{final}} = h_i^0 + \Delta h_i^{\mathrm{graph}},
\qquad
\Delta h_i^{\mathrm{graph}}=W_{\mathrm{graph}}c_i^{\mathrm{graph}}.
$$

$W_{\mathrm{graph}}$ is initialized to zero. Before graph-branch training, the full model therefore exactly reproduces D3. During F0 fitting, the D3 encoder and classifier remain frozen and only graph-branch parameters are optimized.

## 7. Why this design was retained

The research compared unrestricted joint graph training, alternative residual fusion positions, temporal/state modulation, inference-time selection, relation aggregation changes, ranking-aligned objectives, and robust optimization. None provided sufficient stable evidence under its frozen acceptance rules to replace F0.

The final choice is therefore deliberately conservative: protect the strongest intrinsic anchor, use real relations only as an incremental residual, and preserve the option to abstain. Retention does not imply that F0 wins in every year; the development evidence contains a material negative 2019 fold.

## 8. Public implementation boundary

This repository provides a compact reimplementation of the frozen design and a synthetic demonstration. It does not include the private feature pipeline, formal experiment controller, training artifacts, or data needed to reproduce the thesis evidence package.
