"""Draw the loop-unrolling x86 kernel diagram for MIT 6.5940 Lab 5.

Run from the repository root:
    python3 lab5/figures/plot_loop_unrolling_x86.py
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path


BG = "white"
INK = "#222222"
GRID = "#666666"
GRID_LIGHT = "#cfcfcf"
DASH = "#6f6f6f"
RED = "#cc4125"

BLUE = "#cfe2f3"
BLUE_DARK = "#8fb9e3"
YELLOW = "#fff2cc"
YELLOW_DARK = "#e6c470"
GREEN = "#d9ead3"
GREEN_DARK = "#93c47d"

FONT = "DejaVu Sans"
MONO = "DejaVu Sans Mono"


def gradient_block(ax, x, y, w, h, light, dark, zorder=2, n=180):
    c0 = np.array(to_rgb(light))
    c1 = np.array(to_rgb(dark))
    for i in range(n):
        t = i / (n - 1)
        c = tuple((1 - t) * c0 + t * c1)
        ax.add_patch(Rectangle((x + i * w / n, y), w / n + 0.002, h,
                               facecolor=c, edgecolor="none", linewidth=0,
                               zorder=zorder))


def draw_brace(ax, x0, x1, y, height, label, color="#333333", lw=1.2):
    xm = (x0 + x1) / 2
    w = x1 - x0
    verts = [
        (x0, y),
        (x0, y + 0.55 * height), (x0 + 0.15 * w, y + 0.55 * height),
        (x0 + 0.25 * w, y + 0.55 * height),
        (x0 + 0.35 * w, y + 0.55 * height), (xm - 0.05 * w, y + 0.55 * height),
        (xm, y + height),
        (xm + 0.05 * w, y + 0.55 * height), (x1 - 0.35 * w, y + 0.55 * height),
        (x1 - 0.25 * w, y + 0.55 * height),
        (x1 - 0.15 * w, y + 0.55 * height), (x1, y + 0.55 * height),
        (x1, y),
    ]
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(verts) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                           edgecolor=color, linewidth=lw, zorder=8))
    ax.text(xm, y + height + 0.02, label, ha="center", va="bottom",
            fontsize=10.5, color=color, fontfamily=FONT, zorder=8)


def block_matrix(ax, x, y, w, h, rows, title, subtitle, dim_left, hi_rows,
                 row_label, row_edge, block_note_blue, block_note_gold,
                 row_label_y=None):
    half = w / 2
    gradient_block(ax, x, y, half, h, "#eaf3fb", BLUE_DARK)
    gradient_block(ax, x + half, y, half, h, "#fff8df", YELLOW_DARK)
    for i in range(1, rows):
        yy = y + h - i * h / rows
        ax.plot([x, x + w], [yy, yy], color=GRID_LIGHT, lw=0.8, zorder=4)
    ax.plot([x + half, x + half], [y, y + h], color=GRID, lw=1.0,
            linestyle=(0, (4, 3)), zorder=5)
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=INK,
                           linewidth=1.5, zorder=5))

    lo, hi = min(hi_rows), max(hi_rows)
    y0 = y + h - (hi + 1) * h / rows
    y1 = y + h - lo * h / rows
    ax.add_patch(Rectangle((x, y0), w, y1 - y0, fill=False,
                           edgecolor=row_edge, linewidth=1.8,
                           linestyle=(0, (5, 3)), zorder=7))

    draw_brace(ax, x, x + w, y + h + 0.06, 0.20, "k = 64")

    ax.text(x, y + h + 0.66, title, va="bottom", ha="left", fontsize=13,
            fontweight="bold", color=INK, fontfamily=FONT, zorder=8)
    ax.text(x, y + h + 0.44, subtitle, va="bottom", ha="left", fontsize=9.5,
            color="#555555", fontfamily=FONT, zorder=8)
    ax.text(x - 0.25, y + h / 2, dim_left, va="center", ha="right",
            fontsize=10.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
    label_y = row_label_y if row_label_y is not None else (y0 + y1) / 2
    ax.text(x + w + 0.12, label_y, row_label, va="center", ha="left",
            fontsize=10, fontweight="bold", color=row_edge,
            fontfamily=FONT, zorder=8,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    ax.text(x + w / 4, y - 0.18, block_note_blue, va="top", ha="center",
            fontsize=8.6, color="#1f4e79", fontfamily=FONT, zorder=8)
    ax.text(x + 3 * w / 4, y - 0.18, block_note_gold, va="top", ha="center",
            fontsize=8.6, color="#7f6000", fontfamily=FONT, zorder=8)


def simple_matrix(ax, x, y, w, h, rows, cols, title, subtitle, dim_left,
                  dim_top, hi_row, band_label):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=GREEN, edgecolor=INK,
                           linewidth=1.4, zorder=2))
    for i in range(1, rows):
        yy = y + h - i * h / rows
        ax.plot([x, x + w], [yy, yy], color=GRID_LIGHT, lw=0.8, zorder=3)
    for j in range(1, cols):
        xx = x + j * w / cols
        ax.plot([xx, xx], [y, y + h], color=GRID_LIGHT, lw=0.8, zorder=3)

    cw, ch = w / cols, h / rows
    hy = y + h - (hi_row + 1) * ch
    ax.add_patch(FancyBboxPatch((x + 0.02, hy + 0.02), w - 0.04, ch - 0.04,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                facecolor="none", edgecolor="#7bc96f",
                                linewidth=5.0, alpha=0.32, zorder=5))
    ax.add_patch(FancyBboxPatch((x + 0.04, hy + 0.04), w - 0.08, ch - 0.08,
                                boxstyle="round,pad=0.01,rounding_size=0.08",
                                facecolor=GREEN_DARK, edgecolor="#2f6b2f",
                                linewidth=2.0, alpha=0.80, zorder=6))

    ax.text(x, y + h + 0.42, title, va="bottom", ha="left", fontsize=13,
            fontweight="bold", color=INK, fontfamily=FONT, zorder=8)
    ax.text(x, y + h + 0.16, subtitle, va="bottom", ha="left", fontsize=9.5,
            color="#555555", fontfamily=FONT, zorder=8)
    ax.text(x - 0.25, y + h / 2, dim_left, va="center", ha="right",
            fontsize=10.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
    ax.text(x + w / 2, y + h + 0.02, dim_top, va="bottom", ha="center",
            fontsize=10.5, color=INK, fontfamily=FONT, zorder=8)
    ax.text(x + w + 0.12, hy - 0.10, band_label, va="center", ha="left",
            fontsize=9.5, fontweight="bold", color="#2f6b2f",
            fontfamily=MONO, zorder=8,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.5))


def box(ax, x, y, w, h, text, face="white", edge=INK, fontsize=8.0,
        lw=1.3, rounding=0.12, shadow=True, color=INK):
    if shadow:
        ax.add_patch(FancyBboxPatch((x + 0.04, y - 0.04), w, h,
                                    boxstyle=f"round,pad=0.02,rounding_size={rounding}",
                                    facecolor="#000000", edgecolor="none",
                                    alpha=0.08, zorder=4))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={rounding}",
                                facecolor=face, edgecolor=edge, linewidth=lw,
                                zorder=5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=color, fontfamily=MONO, zorder=6)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.1):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0), zorder=7)


def dashed_arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=DASH, lw=1.6,
                                linestyle=(0, (6, 3, 1, 3)),
                                shrinkA=0, shrinkB=0), zorder=1)


def colored_dashed_arrow(ax, x1, y1, x2, y2, color):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3,
                                linestyle=(0, (4, 3)),
                                shrinkA=0, shrinkB=0), zorder=2)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(18, 11), dpi=160)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis("off")

ax.text(0.35, 10.55,
        "loop_unrolling.cc — x86: four output columns per iteration",
        fontsize=18, fontweight="bold", fontfamily=MONO, color=INK,
        va="top", ha="left", zorder=10)

# --- Left: matrix-level view ------------------------------------------------
block_matrix(
    ax, 0.9, 7.45, 4.0, 1.55, rows=4,
    title="A  (m × k) = (4 × 64)",
    subtitle="FP32 activation → int8",
    dim_left="m = 4", hi_rows=[1],
    row_label="row = 1", row_edge="#2f80ed",
    block_note_blue="Block 0 (32 elements)",
    block_note_gold="Block 1 (32 elements)",
)

block_matrix(
    ax, 0.9, 4.60, 4.0, 1.55, rows=4,
    title="B  (n × k) = (4 × 64)",
    subtitle="int4 weights, QM_x86 packed",
    dim_left="n = 4", hi_rows=[0, 1, 2, 3],
    row_label="col..col+3", row_edge="#e69138",
    block_note_blue="Block 0 (32 elements)",
    block_note_gold="Block 1 (32 elements)",
    row_label_y=4.52,
)

simple_matrix(
    ax, 1.4, 1.90, 2.0, 1.55, rows=4, cols=4,
    title="C  (m × n) = (4 × 4)",
    subtitle="FP32 output",
    dim_left="m = 4", dim_top="n = 4",
    hi_row=1, band_label="C[row, 0..3]",
)

a_row_y = 7.45 + 1.55 - 1.5 * 1.55 / 4
b_row_ys = [4.60 + 1.55 - (i + 0.5) * 1.55 / 4 for i in range(4)]
c_row_y = 1.90 + 1.55 - 1.5 * 1.55 / 4
c_cell_xs = [1.4 + (j + 0.5) * 0.5 for j in range(4)]
card_xs = [6.25, 9.0, 11.75, 14.5]
card_w = 2.55
card_top = 7.45
b_colors = ["#5b8db8", "#6aa84f", "#8e7cc3", "#d6a84b"]

# A row -> shared A (thick light-blue line).
arrow(ax, 4.9, a_row_y, 6.25, 8.28, color="#6fa8dc", lw=2.4)

# B group -> each unrolled B block (four distinct dashed arrows).
for i, (yy, color) in enumerate(zip(b_row_ys, b_colors)):
    colored_dashed_arrow(ax, 4.9, yy, card_xs[i] + card_w / 2, card_top, color)

# C row -> one fan-out node -> four outputs.
c_colors = ["#4f7a3a", "#6aa84f", "#7bc96f", "#93c47d"]
node_x, node_y = 5.15, 3.25
ax.plot([3.4, node_x], [c_row_y, node_y], color="#4f7a3a", lw=1.4,
        zorder=3)
ax.add_patch(plt.Circle((node_x, node_y), 0.08, facecolor="#4f7a3a",
                        edgecolor="none", zorder=6))
for j, color in enumerate(c_colors):
    colored_dashed_arrow(ax, node_x, node_y,
                         card_xs[j] + 0.25, 3.93, color)

# --- Right: four unrolled columns ------------------------------------------
core = FancyBboxPatch((5.65, 0.65), 12.0, 9.55,
                      boxstyle="round,pad=0.05,rounding_size=0.22",
                      facecolor="#fcfcfc", edgecolor=RED, linewidth=1.6,
                      linestyle=(0, (6, 3)), zorder=0)
ax.add_patch(core)
ax.text(6.0, 9.82,
        "Core calculation: four output columns per iteration",
        fontsize=14, fontweight="bold", color=RED, fontfamily=FONT,
        ha="left", va="top", zorder=10)
ax.text(6.0, 9.48,
        "one shared A int8 chunk + four B rows, each with its own scales",
        fontsize=9.5, color="#555555", fontfamily=FONT, ha="left", va="top",
        zorder=10)

# A int8 chunk: shared by all four columns.
a_x, a_y, a_cw, a_ch = 6.25, 8.65, 0.155, 0.20
for i in range(32):
    ax.add_patch(Rectangle((a_x + i * a_cw, a_y + 0.24), a_cw, a_ch,
                           facecolor=BLUE, edgecolor=INK, linewidth=0.7,
                           zorder=4))
    ax.add_patch(Rectangle((a_x + i * a_cw, a_y), a_cw, a_ch,
                           facecolor=YELLOW, edgecolor=INK, linewidth=0.7,
                           zorder=4))
ax.text(a_x, a_y + 0.24 + a_ch + 0.03,
        "Block 0: a_int8[ch ... ch+31]",
        fontsize=8.3, ha="left", va="bottom", fontfamily=MONO,
        color="#1f4e79", zorder=6)
ax.text(a_x, a_y - 0.04, "Block 1: a_int8[ch+32 ... ch+63]",
        fontsize=8.3, ha="left", va="top", fontfamily=MONO,
        color="#7f6000", zorder=6)
ax.text(a_x + 32 * a_cw + 0.12, a_y + 0.24 + a_ch / 2, "× s_a",
        fontsize=8.3, ha="left", va="center", color="#1f4e79",
        fontfamily=MONO, zorder=6)
ax.text(a_x + 32 * a_cw + 0.12, a_y + a_ch / 2, "× s_a_2nd",
        fontsize=8.3, ha="left", va="center", color="#7f6000",
        fontfamily=MONO, zorder=6)

# Shared A labels and distribution buses.
ax.text(6.25, 8.28, "shared A: a_lo / a_hi", fontsize=9.0,
        fontweight="bold", color="#1f4e79", fontfamily=FONT,
        zorder=7)
bus_lo_y, bus_hi_y = 7.95, 7.62
ax.text(6.25, 8.05, "a_lo = a_int8[qj]", fontsize=8.2,
        color="#1f4e79", fontfamily=MONO, zorder=7)
ax.text(6.25, 7.72, "a_hi = a_int8[qj+32]", fontsize=8.2,
        color="#7f6000", fontfamily=MONO, zorder=7)
ax.plot([6.90, 16.90], [bus_lo_y, bus_lo_y], color=BLUE_DARK, lw=1.8,
        zorder=3)
ax.plot([6.90, 16.90], [bus_hi_y, bus_hi_y], color=YELLOW_DARK, lw=1.8,
        zorder=3)
for cx in card_xs:
    x_lo = cx + card_w / 2 - 0.55
    x_hi = cx + card_w / 2 + 0.55
    arrow(ax, x_lo, bus_lo_y, x_lo, 7.19, color=BLUE_DARK, lw=1.4)
    arrow(ax, x_hi, bus_hi_y, x_hi, 7.19, color=YELLOW_DARK, lw=1.4)

# Four column cards.
card_y, card_h = 4.75, 2.70
card_styles = [
    ("#6fa8dc", "#f2f8fd"),
    ("#6aa84f", "#f2f8ed"),
    ("#8e7cc3", "#f7f4fc"),
    ("#d6a84b", "#fdf8ec"),
]
for i, cx in enumerate(card_xs):
    edge, face = card_styles[i]
    box(ax, cx, card_y, card_w, card_h, "", face=face, edge=edge,
        lw=1.5, rounding=0.16)

    # lo and hi are placed side by side so the shared-A arrows land cleanly.
    bar_y, bar_h = 6.95, 0.24
    bar_w = (card_w - 0.24) / 2
    ax.add_patch(Rectangle((cx + 0.08, bar_y), bar_w, bar_h,
                           facecolor=BLUE, edgecolor="#5b8db8", linewidth=0.8,
                           zorder=6))
    ax.add_patch(Rectangle((cx + 0.16 + bar_w, bar_y), bar_w, bar_h,
                           facecolor=YELLOW, edgecolor="#b08a2e", linewidth=0.8,
                           zorder=6))
    ax.text(cx + 0.08 + bar_w / 2, bar_y + bar_h / 2, "lo",
            ha="center", va="center", fontsize=7.4, fontfamily=MONO,
            color="#1f4e79", zorder=7)
    ax.text(cx + 0.16 + bar_w + bar_w / 2, bar_y + bar_h / 2, "hi",
            ha="center", va="center", fontsize=7.4, fontfamily=MONO,
            color="#7f6000", zorder=7)

    ax.text(cx + card_w / 2, 6.35, f"B[col+{i}]", ha="center", va="center",
            fontsize=9.4, fontweight="bold", color="#333333",
            fontfamily=MONO, zorder=7)

    ax.text(cx + card_w / 2, 5.88,
            f"sum{i} = Σ a_lo·w{i}_lo\n"
            f"sum{i}_2nd = Σ a_hi·w{i}_hi",
            ha="center", va="center", fontsize=7.8, fontfamily=MONO,
            fontweight="bold", color="#222222", linespacing=1.35, zorder=7)
    ax.text(cx + card_w / 2, 5.10,
            f"acc{i} += sum{i}·s_a·s_w{i}\n"
            f"       + sum{i}_2nd·s_a_2nd·s_w{i}_2nd",
            ha="center", va="center", fontsize=7.0, fontfamily=MONO,
            color="#333333", linespacing=1.35, zorder=7)

    # C output for this column.
    out_y = 3.72
    box(ax, cx + 0.25, out_y, card_w - 0.50, 0.42,
        f"C[row, {i}]", face=GREEN, edge="#4f7a3a", fontsize=8.5,
        lw=1.2, rounding=0.10)
    arrow(ax, cx + card_w / 2, card_y, cx + card_w / 2, out_y + 0.42,
          color="#4f7a3a")

# Emphasize the eight independent MACs.
ax.text(11.65, 3.22, "8 independent MACs per qj",
        fontsize=9.4, fontweight="bold", color="#a61c00", ha="center",
        va="center", fontfamily=FONT, zorder=8,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fdecea",
                  edgecolor="#cc4125", linewidth=1.2))

# Source-like inner-loop pseudocode.
ax.add_patch(FancyBboxPatch((6.25, 0.95), 10.8, 1.75,
                            boxstyle="round,pad=0.04,rounding_size=0.12",
                            facecolor="#f7f7f7", edgecolor="#9a9a9a",
                            linewidth=1.1, zorder=4))
code_lines = [
    "for (col = 0; col < n; col += 4)",
    "    for (qj = 0; qj < 32; qj++) {",
    "        a_lo = a_int8[qj];",
    "        a_hi = a_int8[qj + 32];",
    "        // ... 8 MACs using a_lo and a_hi ...",
    "    }",
]
ax.text(6.45, 2.45, "\n".join(code_lines), fontsize=8.8, ha="left",
        va="top", fontfamily=MONO, color="#333333", linespacing=1.35,
        zorder=6)

fig.tight_layout(pad=0.2)
out = "lab5/figures/loop_unrolling_x86.png"
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
print("wrote", out)
