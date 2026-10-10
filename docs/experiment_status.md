# Experiment status · 实验状态

[Home](../README.md) · [中文首页](../README_CN.md)

Evidence checked on **2026-10-11** against accepted result files. This page records completed evaluations and their reporting boundaries; it is not an authorization to run new experiments.

## Current state

| Area | Status |
| :--- | :--- |
| Model exploration | Closed; D3 + F0 and final 2022 results are frozen |
| Models | D3 → MDRA; D3 + F0 → MSAR-HGRN |
| Main research question | Heterogeneous relational increment above a strong intrinsic risk anchor |
| External baselines | Six runnable models have completed fixed-configuration 2022 evaluation |
| Source65 same-input control | `BLOCKED_INPUT_UNAVAILABLE`; no 2022 prediction or metric |
| Development evaluation | 2018–2021 annual rolling folds; history controls and relation-module variants |
| Final evaluation | Fixed-protocol 2022 OOT; 5,132 companies and 123 positive cases |
| Public implementation | Compact model components and a synthetic software demonstration; not a full reproduction pipeline |

本仓库展示已完成的财务造假检测实验，围绕企业自身历史比较、风险锚点与异构关系增量呈现方法和结果。开发期与最终测试分开报告，保留2019年负增量、固定阈值F1的取舍及既有补充不确定性证据，不据最终测试继续调参或选模。

## How to read the evidence

- **Primary results:** five-seed arithmetic means; ensemble metrics are supplementary and separately labeled.
- **History controls:** the current-state-reference control retains historical information in base inputs and history availability; only the reference inside the deviation branch changes.
- **Input families:** the 65-dimensional development LightGBM and 901-dimensional final tabular LightGBM are different references.
- **Literature reports:** original-paper results are separate from locally evaluated models, with their source and protocol differences retained.
- **Scope:** the results concern risk ranking and budget-limited screening on FiGraph, not causal attribution, guaranteed future-year gains or production deployment.

See [experimental evidence](experiments.md), [the temporal protocol](strict_temporal_protocol.md) and [reviewed aggregates](evidence.json) for details and run identifiers.

## Source65 is an availability blocker

Current checked storage did not contain the exact 2022 Source65 input table or the required frozen FinBERT2 weight snapshot needed for identity-faithful reconstruction. Raw FiGraph records and already-produced predictions do not substitute for the exact source input.

This is **not a claim that recovery is scientifically impossible forever**. Any future recovery would require byte/identity verification and separate authorization; it cannot justify an alternate encoder, missing-text substitute, 2022-driven selection or rewriting frozen results.

## Public release boundary

The showcase contains reviewed aggregate results and a synthetic demonstration. It does not publish company-level records, labels, predictions, checkpoints, private artifacts or complete experiment logs. The demonstration illustrates software behavior; its outputs are not empirical detection results.
