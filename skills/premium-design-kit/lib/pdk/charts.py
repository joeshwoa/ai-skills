"""Themed, publication-quality charts as images (PNG/SVG) for documents and PDFs.

Slides and spreadsheets use NATIVE editable charts (python-pptx / openpyxl); this module is for
places where a picture is the right thing: Word/PDF reports, handouts, HTML pages.

chart spec: {"type": "bar|hbar|stacked|line|area|pie|donut|scatter",
             "categories": [...], "series": [{"name": "2025", "values": [...]}],
             "title": "...", "unit": "%", "prefix": "$", "highlight": 2, "source": "...",
             "y_min": 0, "labels": true}
"""
from __future__ import annotations

from pathlib import Path

from .text import has_arabic, shape
from .themes import mix

_FONT_CACHE: dict = {}


def _font(names: list[str]) -> str | None:
    from matplotlib import font_manager as fm
    key = tuple(names)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    avail = {f.name for f in fm.fontManager.ttflist}
    pick = next((n for n in names if n in avail), None)
    _FONT_CACHE[key] = pick
    return pick


def palette(tk: dict, n: int) -> list[str]:
    base = [tk["accent"], tk["accent_2"], mix(tk["accent"], tk["ink"], 0.45), mix(tk["accent"], tk["paper"], 0.45),
            mix(tk["accent_2"], tk["paper"], 0.4), tk["muted"]]
    while len(base) < n:
        base.append(mix(base[len(base) % 6], tk["paper"], 0.3))
    return ["#" + c for c in base[:n]]


def render_chart(spec: dict, tk: dict, out: str | Path, *, width_in: float = 7.0, height_in: float = 3.6,
                 dpi: int = 220, transparent: bool = False) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    arabic = any(has_arabic(x) for x in [spec.get("title", "")] + list(map(str, spec.get("categories", []))) +
                 [s.get("name", "") for s in spec.get("series", [])])
    fam = _font(([tk["body_font"]] if not arabic else []) + (
        ["Cairo", "Tajawal", "IBM Plex Sans Arabic", "Noto Naskh Arabic", "Geeza Pro", "Arial"] if arabic else
        [tk.get("body_font_latin", ""), "Helvetica Neue", "Helvetica", "Inter", "Arial", "DejaVu Sans"]))
    rc = {"font.size": 10, "axes.edgecolor": "#" + tk["line"], "axes.labelcolor": "#" + tk["ink_soft"],
          "xtick.color": "#" + tk["muted"], "ytick.color": "#" + tk["muted"], "text.color": "#" + tk["ink"]}
    if fam:
        rc["font.family"] = fam
    S = shape if arabic else (lambda x: x)
    kind = spec.get("type", "bar")
    cats = [S(str(c)) for c in spec.get("categories", [])]
    series = spec.get("series") or [{"name": "", "values": spec.get("values", [])}]
    unit, prefix = spec.get("unit", ""), spec.get("prefix", "")
    colors = palette(tk, max(len(series), len(cats) if kind in ("pie", "donut") else 1))
    hl = spec.get("highlight")

    def fmt(v):
        v = float(v)
        s = f"{v:,.0f}" if abs(v) >= 100 or v == int(v) else f"{v:,.1f}"
        return f"{prefix}{s}{unit}"

    with plt.rc_context(rc):
        fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=dpi)
        fig.patch.set_alpha(0 if transparent else 1)
        fig.patch.set_facecolor("#" + tk["paper"])
        ax.set_facecolor("#" + tk["paper"])
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(length=0)
        if kind in ("pie", "donut"):
            vals = series[0]["values"]
            cols = [colors[i] if (hl is None or i == hl) else "#" + mix(tk["line"], tk["paper"], 0.2)
                    for i in range(len(vals))] if hl is not None else colors[:len(vals)]
            wedges, *_ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                                wedgeprops={"width": 0.38 if kind == "donut" else 1, "edgecolor": "#" + tk["paper"], "linewidth": 2})
            ax.legend(wedges, [f"{c}  {fmt(v)}" for c, v in zip(cats, vals)], loc="center left",
                      bbox_to_anchor=(1.0, 0.5), frameon=False)
            if kind == "donut" and spec.get("center"):
                ctext = S(str(spec["center"]))
                ax.text(0, 0, ctext, ha="center", va="center", fontsize=max(9, min(18, 150 / max(len(ctext), 1))), fontweight="bold",
                        color="#" + tk["ink"])
            ax.set_aspect("equal")
        elif kind == "scatter":
            for i, s in enumerate(series):
                ax.scatter(s.get("x", []), s["values"], s=36, color=colors[i], alpha=.85, label=S(s.get("name", "")))
            ax.grid(color="#" + tk["line"], linewidth=.6)
        else:
            import numpy as np
            x = np.arange(len(cats))
            n = len(series)
            if kind in ("bar", "stacked", "hbar"):
                w = 0.68 / (1 if kind == "stacked" else n)
                bottom = np.zeros(len(cats))
                for i, s in enumerate(series):
                    vals = np.array([float(v) for v in s["values"]])
                    col = [colors[i]] * len(vals)
                    if hl is not None and n == 1:
                        col = [colors[0] if j == hl else "#" + mix(tk["line"], tk["paper"], 0.1) for j in range(len(vals))]
                    pos = x if kind == "stacked" else x - 0.34 + w * (i + 0.5)
                    if kind == "hbar":
                        bars = ax.barh(pos, vals, height=w, color=col, label=S(s.get("name", "")))
                    else:
                        bars = ax.bar(pos, vals, width=w, bottom=bottom if kind == "stacked" else None, color=col,
                                      label=S(s.get("name", "")))
                    if spec.get("labels", True) and kind != "stacked":
                        for b, v in zip(bars, vals):
                            if kind == "hbar":
                                ax.text(b.get_width(), b.get_y() + b.get_height() / 2, " " + fmt(v), va="center",
                                        fontsize=9, color="#" + tk["ink_soft"])
                            else:
                                ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt(v), ha="center",
                                        va="bottom", fontsize=9, color="#" + tk["ink_soft"])
                    if kind == "stacked":
                        bottom = bottom + vals
                if kind == "hbar":
                    ax.set_yticks(x, cats)
                    ax.invert_yaxis()
                    ax.xaxis.set_visible(False)
                    ax.spines["bottom"].set_visible(False)
                else:
                    ax.set_xticks(x, cats)
                    ax.grid(axis="y", color="#" + tk["line"], linewidth=.6)
                    ax.set_axisbelow(True)
            else:  # line / area
                for i, s in enumerate(series):
                    vals = [float(v) for v in s["values"]]
                    ax.plot(x, vals, color=colors[i], linewidth=2.4, marker="o", markersize=4, label=S(s.get("name", "")))
                    if kind == "area":
                        ax.fill_between(x, vals, alpha=.14, color=colors[i])
                    if spec.get("labels", True) and n == 1:
                        ax.annotate(fmt(vals[-1]), (x[-1], vals[-1]), textcoords="offset points", xytext=(6, 4),
                                    fontsize=9, fontweight="bold", color=colors[i])
                ax.set_xticks(x, cats)
                ax.grid(axis="y", color="#" + tk["line"], linewidth=.6)
            if "y_min" in spec:
                ax.set_ylim(bottom=spec["y_min"])
            if kind != "hbar":
                ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: fmt(v)))
            if n > 1:
                ax.legend(frameon=False, loc="upper left", ncols=min(n, 4), bbox_to_anchor=(0, 1.12))
        if arabic and kind not in ("pie", "donut", "hbar", "scatter"):
            ax.invert_xaxis()           # Arabic readers scan right → left: first category on the right
            ax.yaxis.tick_right()
        if spec.get("title"):
            fig.suptitle(S(spec["title"]), x=0.98 if arabic else 0.02, ha="right" if arabic else "left",
                         fontsize=13, fontweight="bold", color="#" + tk["ink"])
        if spec.get("source"):
            fig.text(0.98 if arabic else 0.02, 0.01, S(spec["source"]), ha="right" if arabic else "left",
                     fontsize=7.5, color="#" + tk["muted"])
        fig.tight_layout(rect=(0, 0.03 if spec.get("source") else 0, 1, 0.95 if spec.get("title") else 1))
        fig.savefig(out, dpi=dpi, transparent=transparent, facecolor=fig.get_facecolor())
        plt.close(fig)
    return str(out)
