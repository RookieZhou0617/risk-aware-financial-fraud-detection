# Visual assets

The presentation uses a restrained navy / teal palette; orange marks a negative development-year increment. All images are checked in, with no third-party rendering service required.

| Asset | Purpose / source |
| :--- | :--- |
| [research-cover.svg](research-cover.svg) | Original vector cover; network is decorative, not measured data |
| [model-framework.png](model-framework.png) | Current thesis Figure 3-1, reused unchanged at 2400 × 1749 |
| [evidence-overview.svg](evidence-overview.svg) | Data-backed vector figure from reviewed aggregate results |
| [evidence-overview.png](evidence-overview.png) | Raster version of the same result chart |

## Thesis Figure 3-1

The author explicitly selected the current thesis figure for reuse. It is the 2026-10-01 export of the author-refined second canvas in `chapter3_model_framework_v4.drawio`. Only the final PNG is distributed here, not other draft canvases or the full thesis source.

Original/public PNG SHA-256:

```text
828b42799238d0eab040ecd960d7362a6c97a5ba2b720f1e3080a2acb6a6ff55
```

Clicking the figure in either README opens the full-resolution image. The old simplified D3/F0 SVG was retired; Git history retains it.

## Regenerate the cover and evidence chart

```bash
pip install matplotlib
python scripts/render_assets.py
```

The renderer reads only [docs/evidence.json](../docs/evidence.json); it never loads private data or predictions. Matplotlib is an optional presentation dependency, not a model-runtime dependency. The result chart keeps development and final testing separate, uses a zero-based final-score axis, and explicitly notes bootstrap uncertainty.

The script deliberately does not redraw or overwrite the thesis model figure. To update that figure, review and copy the new approved export, then update its recorded checksum here.
