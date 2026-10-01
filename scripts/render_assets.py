"""Render public presentation assets from reviewed aggregates, never predictions.

Run: python scripts/render_assets.py (requires matplotlib).
The author's thesis Figure 3-1 is intentionally NOT regenerated here.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY, TEAL, ORANGE = "#142C46", "#087F8C", "#C4683B"
MUTED, LINE = "#52667B", "#DDE6EC"


def render_cover() -> None:
    # Decorative network, not a data-derived topology or an additional model diagram.
    nodes = [(915, 72), (1095, 81), (1190, 180), (1130, 290), (934, 305), (851, 183)]
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 4), (1, 3)]
    edges = "".join(
        f'<path d="M {nodes[a][0]} {nodes[a][1]} L {nodes[b][0]} {nodes[b][1]}"/>'
        for a, b in links
    )
    spokes = "".join(f'<path d="M 1020 184 L {x} {y}"/>' for x, y in nodes)
    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{11 if i % 2 else 15}" '
        f'fill="{TEAL if i % 2 else "#7F9DB9"}" stroke="#A4CDD0" stroke-width="2"/>'
        for i, (x, y) in enumerate(nodes)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="400" viewBox="0 0 1280 400" role="img" aria-labelledby="title desc">
<title id="title">MSAR-HGRN: Financial fraud detection</title>
<desc id="desc">A multi-source intrinsic risk anchor with selective heterogeneous relational evidence. Frozen research model; strict temporal evaluation; synthetic public demo. Decorative network on the right.</desc>
<defs><linearGradient id="bg" x2="1" y2="0.5"><stop stop-color="#10273F"/><stop offset="1" stop-color="#183C4D"/></linearGradient></defs>
<rect width="1280" height="400" rx="20" fill="url(#bg)"/>
<path d="M 56 54 H 94" stroke="#6AD3C9" stroke-width="4"/>
<g font-family="Arial,Helvetica,sans-serif">
<text x="110" y="60" font-size="15" letter-spacing="3" fill="#A9C9D6">MASTER'S THESIS · RESEARCH SHOWCASE</text>
<text x="54" y="146" font-size="67" font-weight="700" letter-spacing="-2" fill="#FFFFFF">MSAR-HGRN</text>
<text x="57" y="196" font-size="27" fill="#EDF5F8">Financial fraud detection</text>
<text x="57" y="240" font-size="21" fill="#BBD1DD">An intrinsic risk anchor.</text>
<text x="57" y="272" font-size="21" fill="#BBD1DD">Selective relational evidence.</text>
<g font-size="14" fill="#D6E9ED">
<rect x="57" y="324" width="157" height="33" rx="16" fill="#234557"/><text x="76" y="346">Multi-source inputs</text>
<rect x="227" y="324" width="165" height="33" rx="16" fill="#234557"/><text x="246" y="346">Temporal evaluation</text>
<rect x="405" y="324" width="153" height="33" rx="16" fill="#234557"/><text x="424" y="346">Frozen risk anchor</text>
</g></g>
<g stroke="#52788B" stroke-width="1.5" opacity="0.65" fill="none">{edges}</g>
<g stroke="#53B8B5" stroke-width="2" opacity="0.7" fill="none">{spokes}</g>
<circle cx="1020" cy="184" r="71" fill="none" stroke="#609B9E" opacity="0.25"/>
<circle cx="1020" cy="184" r="48" fill="#183E51" stroke="#82D8CD" stroke-width="2.5"/>
<text x="1020" y="192" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="22" font-weight="700" fill="#D9FFF8">ANCHOR</text>
{circles}
<text x="1020" y="357" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="13" letter-spacing="2" fill="#91B8C4">COMPANY + CONTEXT</text>
</svg>'''
    (ASSETS / "research-cover.svg").write_text(svg + "\n", encoding="utf-8")


def render_evidence() -> None:
    data = json.loads((ROOT / "docs/evidence.json").read_text(encoding="utf-8"))
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "text.color": NAVY, "axes.labelcolor": MUTED,
                         "xtick.color": MUTED, "ytick.color": MUTED,
                         "svg.fonttype": "path", "svg.hashsalt": "msar-hgrn-evidence-v1"})
    fig = plt.figure(figsize=(13, 5.4), facecolor="#F7FAFC")
    left = fig.add_axes([0.07, 0.25, 0.40, 0.48], facecolor="#F7FAFC")
    right = fig.add_axes([0.67, 0.25, 0.27, 0.48], facecolor="#F7FAFC")
    fig.text(0.045, 0.925, "Relational gains, with their limits", fontsize=23, weight="bold")
    fig.text(0.045, 0.865, "Preset five-seed arithmetic means · AUC-PR = average precision", color=MUTED, fontsize=11)
    fig.text(0.07, 0.78, "01  ROLLING DEVELOPMENT", fontsize=12, weight="bold")
    fig.text(0.58, 0.78, "02  FIXED-PROTOCOL 2022 OOT", fontsize=12, weight="bold")
    values = [row["delta"] for row in data["development"]]
    left.bar(range(4), values, width=0.5, color=[TEAL if x >= 0 else ORANGE for x in values], zorder=3)
    left.set_xticks(range(4), [str(row["year"]) for row in data["development"]])
    left.set_ylim(-0.020, 0.025)
    left.set_yticks([-0.02, -0.01, 0, 0.01, 0.02])
    left.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:+.2f}" if x else "0"))
    left.set_ylabel("MSAR-HGRN − MDRA", fontsize=10)
    left.axhline(0, color="#9DAFBC", lw=1)
    left.grid(axis="y", color=LINE, linewidth=0.8, zorder=0)
    for i, value in enumerate(values):
        left.text(i, value + (0.0016 if value >= 0 else -0.002), f"{value:+.4f}",
                  ha="center", va="bottom" if value >= 0 else "top", fontsize=11, weight="bold",
                  color=TEAL if value >= 0 else ORANGE)
    names = ["MDRA", "Matched shuffle", "MSAR-HGRN"]
    scores = [data["models"][name]["auc_pr"] for name in names]
    right.barh(range(3), scores, height=0.46, color=["#718DA6", "#B6C5D0", TEAL], zorder=3)
    right.set_yticks(range(3), names)
    right.invert_yaxis()
    right.set_xlim(0, 0.62)
    right.set_xticks([0, 0.2, 0.4, 0.6])
    right.set_xlabel("Mean AUC-PR", fontsize=10)
    right.grid(axis="x", color=LINE, linewidth=0.8, zorder=0)
    for i, value in enumerate(scores):
        right.text(value + 0.012, i, f"{value:.4f}", va="center", fontsize=11, weight="bold")
    for ax in (left, right):
        ax.tick_params(length=0, pad=8)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.text(0.07, 0.13, "2019: negative transfer remains visible.", color=ORANGE, fontsize=11, weight="bold")
    fig.text(0.58, 0.13, "Both paired bootstrap 95% intervals cross zero.", color=MUTED, fontsize=10)
    fig.text(0.045, 0.04, "Development and final testing are separate; no pooled five-year score.  Source: docs/evidence.json", color=MUTED, fontsize=9)
    fig.savefig(ASSETS / "evidence-overview.svg", metadata={"Date": None, "Creator": "MSAR-HGRN public showcase"})
    svg_path = ASSETS / "evidence-overview.svg"
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    fig.savefig(ASSETS / "evidence-overview.png", dpi=180, metadata={"Software": "MSAR-HGRN public showcase"})
    plt.close(fig)


if __name__ == "__main__":
    render_cover()
    render_evidence()
    print("Rendered research-cover.svg and evidence-overview.svg/png")
