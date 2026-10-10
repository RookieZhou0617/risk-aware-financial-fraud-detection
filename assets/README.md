# Visual assets

The presentation uses a restrained navy / teal palette; orange marks a negative development-year increment. All images are checked in, with no third-party rendering service required.

| Asset | Purpose / source |
| :--- | :--- |
| [research-cover.svg](research-cover.svg) | Original vector cover; network is decorative, not measured data |
| [model-framework.png](model-framework.png) | Latest thesis Figure 3-1, rendered unchanged at 3000 × 2187 |
| [evidence-overview.svg](evidence-overview.svg) | Data-backed vector figure from reviewed aggregate results |
| [evidence-overview.png](evidence-overview.png) | Raster version of the same result chart |

## Thesis Figure 3-1

The author explicitly selected thesis Figure 3-1 for reuse. The public PNG was refreshed on **2026-10-11** from the approved `chapter3_model_framework_v4.pdf` in thesis revision `4ca0c78`. That PDF is the 2026-10-06 export of the author-refined V4 second canvas. The public conversion changes resolution only, not wording, layout or arrows. The older 2026-10-01 PNG still present in the research checkout was not used.

The update includes the thesis's wording “交叉拟合风险分数”, “企业自身风险锚点” and “空关系通道”. Legacy relation-channel labels in the figure are explained separately in [the methodology](../docs/methodology.md). Only the final PNG is distributed, not other draft canvases, embedded editable XML or the full thesis source.

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

The script deliberately does not redraw or overwrite the thesis model figure. To update that figure, review and copy the new approved export, then update its recorded checksum here.
