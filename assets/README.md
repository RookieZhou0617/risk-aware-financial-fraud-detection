# Visual assets

The presentation uses a restrained navy / teal palette; orange marks a negative development-year increment. All images are checked in, with no third-party rendering service required.

| Asset | Purpose / source |
| :--- | :--- |
| [research-cover.svg](research-cover.svg) | Original vector cover; network is decorative, not measured data |
| [model-framework.png](model-framework.png) | Model architecture, rendered at 3000 × 2187 |
| [evidence-overview.svg](evidence-overview.svg) | Data-backed vector figure from reviewed aggregate results |
| [evidence-overview.png](evidence-overview.png) | Raster version of the same result chart |

## Model architecture

The author-approved model architecture was refreshed on **2026-10-11** at 3000 × 2187 pixels. The export preserves its wording, layout and arrows. It describes the model used in the reported experiments, not the simplified synthetic demonstration.

Legacy relation-channel labels in the figure are explained separately in [the methodology](../docs/methodology.md). Only the final PNG is distributed, without embedded editable XML or private source files.

Public PNG SHA-256:

```text
0b39235e1b23b74642cf6a54c8fdf45fd2360415e394d86633f6e162bd29b1e6
```

Clicking the figure in either README opens the full-resolution image. The old simplified D3/F0 SVG was retired; Git history retains it.

## Regenerate the cover and evidence chart

```bash
pip install matplotlib
python scripts/render_assets.py
```

The renderer reads only [docs/evidence.json](../docs/evidence.json); it never loads private data or predictions. Matplotlib is an optional presentation dependency, not a model-runtime dependency. The result chart keeps development and final testing separate, uses a zero-based final-score axis, preserves the 2019 negative increment and labels LightGBM as a descriptive, different-input reference. Archived Bootstrap evidence remains in the [experiment supplement](../docs/experiments.md#supplementary-evidence), rather than the headline graphic.

The script deliberately does not redraw or overwrite the model architecture. To update that figure, review and copy the new approved export, then update its recorded checksum here.
