# Research & writing status · 研究与写作进展

[Home](../README.md) · [中文首页](../README_CN.md)

Snapshot updated on **2026-10-11** against the current `thesis-synthesis` checkout (`4ca0c78`), manuscript and accepted result files. The four-branch review below was performed on 2026-10-01; only the thesis branch is newly checked in this refresh. This page summarizes scope, not research execution authorization.

## Current state

| Area | Status |
| :--- | :--- |
| Model exploration | Closed; D3 + F0 and final 2022 results are frozen |
| Thesis names | D3 → MDRA; D3 + F0 → MSAR-HGRN |
| Main research question | Heterogeneous relational increment above a strong intrinsic risk anchor |
| External baselines | Six runnable models have completed fixed-configuration 2022 evaluation |
| Source65 same-input control | `BLOCKED_INPUT_UNAVAILABLE`; no 2022 prediction or metric |
| Manuscript | Chinese/English abstracts and Chapters 1–5 have completed multiple rounds of revision |
| Latest visual | Figure 3-1 from the approved V4 second-canvas PDF, exported to the public PNG on 2026-10-11; layout preserved |
| Still distinct from completion | Manuscript revision, acknowledgments and final release; no claim of defense or publication |

论文当前已进入写作与修订阶段，不再开展模型探索。展示重点为“企业自身历史比较—风险锚点—异构关系补充—重点筛查”，同时保留2019年负增量与固定阈值F1的取舍。最新论文将Bootstrap与独立排序诊断章节移出正文；公开仓库仍保留既有补充证据，不改变冻结结果或宣称显著性。

## Branch roles, not competing latest models

| Research branch | Checked revision | Meaning for this showcase |
| :--- | :--- | :--- |
| `thesis-synthesis` | `4ca0c78` · checked 2026-10-11 | Revised abstracts/chapters, control terminology, literature grouping, FiGraph categories and current Figure 3-1 |
| `strict-temporal` | `9dd9108` | Frozen research history and final experiment closeout |
| `main` | `b56a694` | High-level research closeout summary |
| `research-workflow-v1` | `e4d4b1c` | Older workflow infrastructure branch, not a new scientific result |

The other three revisions record the 2026-10-01 branch review, not a new assertion about their current remote heads. Old stage notes on infrastructure/history branches must not override the current thesis closeout or be presented as active model development.

## Manuscript structure

1. Introduction: motivation, research context and contributions.
2. Related methods and technical foundations.
3. Multi-source risk anchor and heterogeneous graph residual method.
4. Experimental settings; multi-source anchor prediction; heterogeneous-relation prediction; 2022 results.
5. Conclusions, limitations and future directions.

Recent manuscript revisions:

- Use **current-state-reference control / 当前状态参照对照** consistently. Historical information in base inputs and history availability remain present; only the reference inside the deviation branch changes.
- Separate the **65-dimensional development LightGBM** from the **901-dimensional final tabular LightGBM**.
- Add FiGraph literature reports alongside local results, with explicit source and protocol distinctions; interpret the result in terms of ranking and budget-limited screening.
- Clarify FiGraph background node categories versus legacy graph-channel labels.
- Retain the 2019 negative increment, distinguish development from final testing, and keep the accepted model and scientific artifacts frozen.

The current handoff records a successful five-step thesis build and 59-page PDF. No new thesis build, experiment or prediction was run for this showcase refresh. A revised manuscript is not a claim of defense, publication or a new model release.

## Source65 is an availability blocker

Current checked storage did not contain the exact 2022 Source65 input table or the required frozen FinBERT2 weight snapshot needed for identity-faithful reconstruction. Raw FiGraph records and already-produced predictions do not substitute for the exact source input.

This is **not a claim that recovery is scientifically impossible forever**. Any future recovery would require byte/identity verification and separate authorization; it cannot justify an alternate encoder, missing-text substitute, 2022-driven selection or rewriting frozen results.

## Public release boundary

The showcase contains reviewed aggregate results and a synthetic demonstration. It does not publish the research checkout, full thesis, private artifacts or complete experiment logs. A manuscript draft, frozen experiment and public software demonstration are three different deliverables.
