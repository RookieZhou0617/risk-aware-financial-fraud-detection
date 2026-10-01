# Research & writing status · 研究与写作进展

[Home](../README.md) · [中文首页](../README_CN.md)

Snapshot checked on **2026-10-01** against all four remote branches of the research repository. This page summarizes current scope; it is not a research execution authorization.

## Current state

| Area | Status |
| :--- | :--- |
| Model exploration | Closed; D3 + F0 and final 2022 results are frozen |
| Thesis names | D3 → MDRA; D3 + F0 → MSAR-HGRN |
| Main research question | Heterogeneous relational increment above a strong intrinsic risk anchor |
| External baselines | Six runnable models have completed fixed-configuration 2022 evaluation |
| Source65 same-input control | `BLOCKED_INPUT_UNAVAILABLE`; no 2022 prediction or metric |
| Manuscript | Five-chapter draft and Chinese/English abstracts prepared; draft review integrated |
| Latest visual | Author-refined thesis Figure 3-1, second canvas of the V4 source, exported 2026-10-01 |
| Still distinct from completion | Manuscript revision, acknowledgments and final release; no claim of defense or publication |

论文当前已进入写作与修订阶段，不再开展模型探索。展示重点由实验代号与流程历史转为“企业自身历史偏差—内生风险锚点—异构关系增量”，同时保留 2019 年负迁移、最终测试不确定性和指标取舍。

## Branch roles, not competing latest models

| Research branch | Checked revision | Meaning for this showcase |
| :--- | :--- | :--- |
| `thesis-synthesis` | `0776595` | Current thesis structure, terminology, baseline reporting and Figure 3-1 |
| `strict-temporal` | `9dd9108` | Frozen research history and final experiment closeout |
| `main` | `b56a694` | High-level research closeout summary |
| `research-workflow-v1` | `e4d4b1c` | Older workflow infrastructure branch, not a new scientific result |

Branch entry documents, recent history and relevant differences were reviewed. Old stage notes on infrastructure/history branches must not override the current thesis closeout or be presented as active model development.

## Manuscript structure

1. Introduction: motivation, research context and contributions.
2. Related methods and technical foundations.
3. Multi-source risk anchor and heterogeneous graph residual method.
4. Temporal experiments, controls, baselines and result analysis.
5. Conclusions, limitations and future directions.

Recent revisions explicitly distinguish annual historical-label assumptions from exact disclosure-date availability, preserve the limits of relation-semantic analysis, and remove non-final joint-graph paths from the main model narrative.

## Source65 is an availability blocker

Current checked storage did not contain the exact 2022 Source65 input table or the required frozen FinBERT2 weight snapshot needed for identity-faithful reconstruction. Raw FiGraph records and already-produced predictions do not substitute for the exact source input.

This is **not a claim that recovery is scientifically impossible forever**. Any future recovery would require byte/identity verification and separate authorization; it cannot justify an alternate encoder, missing-text substitute, 2022-driven selection or rewriting frozen results.

## Public release boundary

The showcase contains reviewed aggregate results and a synthetic demonstration. It does not publish the research checkout, full thesis, private artifacts or complete experiment logs. A manuscript draft, frozen experiment and public software demonstration are three different deliverables.
