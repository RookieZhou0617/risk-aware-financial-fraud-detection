# Methodology

## 1. Problem definition

For company \(i\) at year \(t\), the task is to estimate the probability of financial statement fraud using information available at or before \(t\). Inputs include company-level financial variables, an MD&A text representation, self-history, risk signals, and heterogeneous relations to peers or background entities.

The public code focuses on a central question: can relational information provide stable incremental evidence without damaging an already useful company-level risk representation?

## 2. Multi-source intrinsic risk

Each source \(s\) is independently projected into a common hidden space. Source attention combines the current tokens into a current state. Keeping source projections separate makes the fusion auditable and prevents one high-dimensional source from dominating only because of scale.

## 3. Current-history deviation

Only strictly historical observations of the same company are summarized. For current token \(c_{i,t}^{(s)}\) and historical token \(r_{i,<t}^{(s)}\), the deviation encoder uses

\[
[c-r,\ |c-r|,\ c\odot r,\ \cos(c,r),\ m],
\]

where \(m\) indicates whether history is available. Missing history is represented explicitly rather than imputed from future observations. The fused current and deviation states produce the intrinsic hidden representation \(h_i^0\) and risk probability \(p_i^0\).

## 4. Risk-aware relational messages

For a peer \(j\) connected to target \(i\) through relation \(r\), the message function consumes

\[
[h_j^0,\ h_j^0-h_i^0,\ |h_j^0-h_i^0|,\ p_j^0-p_i^0,\ e_r].
\]

This gives the graph branch both peer state and target-relative risk evidence. The implementation aggregates messages with native PyTorch operations and does not require PyTorch Geometric or DGL.

## 5. Relation reliability

Relation utility is not assumed to be uniform. A low-capacity gate estimates \(g_{ir}\in(0,1)\) from label-free context statistics:

- peer count;
- mean and standard deviation of intrinsic similarity;
- mean absolute risk gap;
- peer-risk dispersion;
- relation-context norm.

The gate has a conservative prior, and unavailable relations receive zero reliability.

## 6. Cross-relation fusion

Attention combines the gated relation contexts. An explicit NULL relation is always available, allowing the model to abstain from graph correction when none of the observed relation contexts is useful.

## 7. Graph residual learning

The final representation is

\[
h_i^{\mathrm{final}} = h_i^0 + \Delta h_i^{\mathrm{graph}},
\qquad
\Delta h_i^{\mathrm{graph}}=W_{\mathrm{graph}}c_i^{\mathrm{graph}}.
\]

\(W_{\mathrm{graph}}\) is initialized to zero. Therefore, before graph-branch training, the model exactly preserves the intrinsic representation. In the thesis development protocol, the intrinsic encoder can be frozen so that graph learning is restricted to incremental relational correction.

This repository is a compact showcase implementation. It does not include the private feature pipeline, formal experiment runner, or data needed to reproduce the full thesis evidence package.
