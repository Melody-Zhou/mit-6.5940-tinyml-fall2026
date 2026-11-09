"""Draw the x86 reference kernel diagram for MIT 6.5940 Lab 5.

Run from the repository root:
    python3 lab5/figures/plot_reference_x86.py
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.offsetbox import AnnotationBbox, HPacker, TextArea, VPacker
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
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
CJK = "Noto Sans CJK SC"


def gradient_block(ax, x, y, w, h, light, dark, zorder=2, n=180):
    c0 = np.array(to_rgb(light))
    c1 = np.array(to_rgb(dark))
    for i in range(n):
        t = i / (n - 1)
        c = tuple((1 - t) * c0 + t * c1)
        ax.add_patch(Rectangle((x + i * w / n, y), w / n + 0.002, h,
                               facecolor=c, edgecolor="none",
                               linewidth=0, zorder=zorder))


def draw_brace(ax, x0, x1, y, height, label, color="#333333", lw=1.2):
    """A shallow horizontal curly brace above a matrix, with a centered label."""
    xm = (x0 + x1) / 2
    w = x1 - x0
    verts = [
        (x0, y),
        (x0, y + 0.55 * height),
        (x0 + 0.15 * w, y + 0.55 * height),
        (x0 + 0.25 * w, y + 0.55 * height),
        (x0 + 0.35 * w, y + 0.55 * height),
        (xm - 0.05 * w, y + 0.55 * height),
        (xm, y + height),
        (xm + 0.05 * w, y + 0.55 * height),
        (x1 - 0.35 * w, y + 0.55 * height),
        (x1 - 0.25 * w, y + 0.55 * height),
        (x1 - 0.15 * w, y + 0.55 * height),
        (x1, y + 0.55 * height),
        (x1, y),
    ]
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(verts) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                           edgecolor=color, linewidth=lw, zorder=8))
    ax.text(xm, y + height + 0.02, label, ha="center", va="bottom",
            fontsize=10.5, color=color, fontfamily=FONT, zorder=8)


def block_matrix(ax, x, y, w, h, rows, title, subtitle, dim_left,
                 hi_row, row_label, row_edge, block_note_blue, block_note_gold):
    """4-row matrix: one blue gradient block for k=0..31 and one gold for k=32..63."""
    half = w / 2
    gradient_block(ax, x, y, half, h, "#eaf3fb", BLUE_DARK)
    gradient_block(ax, x + half, y, half, h, "#fff8df", YELLOW_DARK)

    # Very light row separators; no column grid inside the color blocks.
    for i in range(1, rows):
        yy = y + h - i * h / rows
        ax.plot([x, x + w], [yy, yy], color=GRID_LIGHT, lw=0.8, zorder=4)
    # Thin dashed separator between the two 32-element blocks.
    ax.plot([x + half, x + half], [y, y + h], color=GRID, lw=1.0,
            linestyle=(0, (4, 3)), zorder=5)
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=INK,
                           linewidth=1.5, zorder=5))

    # Highlighted row: bright dashed frame only, no heavy dark band.
    yy = y + h - (hi_row + 1) * h / rows
    ax.add_patch(Rectangle((x, yy), w, h / rows, fill=False,
                           edgecolor=row_edge, linewidth=1.8,
                           linestyle=(0, (5, 3)), zorder=7))

    # Dimension brace above the matrix.
    draw_brace(ax, x, x + w, y + h + 0.06, 0.20, "k = 64")

    ax.text(x, y + h + 0.66, title, va="bottom", ha="left", fontsize=13,
            fontweight="bold", color=INK, fontfamily=FONT, zorder=8)
    ax.text(x, y + h + 0.44, subtitle, va="bottom", ha="left", fontsize=9.5,
            color="#555555", fontfamily=FONT, zorder=8)
    ax.text(x - 0.25, y + h / 2, dim_left, va="center", ha="right",
            fontsize=10.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
    ax.text(x + w + 0.12, yy + h / rows / 2, row_label, va="center",
            ha="left", fontsize=10, fontweight="bold", color=row_edge,
            fontfamily=FONT, zorder=8,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    ax.text(x + w / 4, y - 0.18, block_note_blue, va="top", ha="center",
            fontsize=8.6, color="#1f4e79", fontfamily=FONT, zorder=8)
    ax.text(x + 3 * w / 4, y - 0.18, block_note_gold, va="top", ha="center",
            fontsize=8.6, color="#7f6000", fontfamily=FONT, zorder=8)


def simple_matrix(ax, x, y, w, h, rows, cols, title, subtitle, dim_left,
                  dim_top, hi_cell, cell_label):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=GREEN, edgecolor=INK,
                           linewidth=1.4, zorder=2))
    for i in range(1, rows):
        yy = y + h - i * h / rows
        ax.plot([x, x + w], [yy, yy], color=GRID_LIGHT, lw=0.8, zorder=3)
    for j in range(1, cols):
        xx = x + j * w / cols
        ax.plot([xx, xx], [y, y + h], color=GRID_LIGHT, lw=0.8, zorder=3)

    rr, cc = hi_cell
    cw, ch = w / cols, h / rows
    hx = x + cc * cw
    hy = y + h - (rr + 1) * ch
    # Soft green glow + rounded inner highlight.
    ax.add_patch(FancyBboxPatch((hx + 0.015, hy + 0.015), cw - 0.03, ch - 0.03,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                facecolor="none", edgecolor="#7bc96f",
                                linewidth=5.0, alpha=0.32, zorder=5))
    ax.add_patch(FancyBboxPatch((hx + 0.035, hy + 0.035), cw - 0.07, ch - 0.07,
                                boxstyle="round,pad=0.01,rounding_size=0.08",
                                facecolor=GREEN_DARK, edgecolor="#2f6b2f",
                                linewidth=2.0, alpha=0.95, zorder=6))

    ax.text(x, y + h + 0.42, title, va="bottom", ha="left", fontsize=13,
            fontweight="bold", color=INK, fontfamily=FONT, zorder=8)
    ax.text(x, y + h + 0.16, subtitle, va="bottom", ha="left", fontsize=9.5,
            color="#555555", fontfamily=FONT, zorder=8)
    ax.text(x - 0.25, y + h / 2, dim_left, va="center", ha="right",
            fontsize=10.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
    ax.text(x + w / 2, y + h + 0.02, dim_top, va="bottom", ha="center",
            fontsize=10.5, color=INK, fontfamily=FONT, zorder=8)
    ax.text(x + w + 0.12, hy + 1.15 * ch, cell_label, va="center", ha="left",
            fontsize=10, fontweight="bold", color="#2f6b2f",
            fontfamily=MONO, zorder=8,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.5))


def box(ax, x, y, w, h, text, face="white", edge=INK, fontsize=10,
        fontfamily=FONT, lw=1.2, color=INK, rounding=0.12,
        fontweight="normal", shadow=True):
    if shadow:
        ax.add_patch(FancyBboxPatch((x + 0.05, y - 0.05), w, h,
                                    boxstyle=f"round,pad=0.02,rounding_size={rounding}",
                                    facecolor="#000000", edgecolor="none",
                                    alpha=0.10, zorder=4))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={rounding}",
                                facecolor=face, edgecolor=edge, linewidth=lw,
                                zorder=5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=color, fontfamily=fontfamily,
            fontweight=fontweight, zorder=6)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0), zorder=7)


def dashed_arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=DASH, lw=1.6,
                                linestyle=(0, (6, 3, 1, 3)),
                                shrinkA=0, shrinkB=0), zorder=1)


def code_panel(ax, x, y, w, h):
    """A syntax-highlighted address/scale note with an embedded Chinese caption."""
    ax.add_patch(FancyBboxPatch((x + 0.06, y - 0.06), w, h,
                                boxstyle="round,pad=0.04,rounding_size=0.14",
                                facecolor="#000000", edgecolor="none",
                                alpha=0.08, zorder=4))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.04,rounding_size=0.14",
                                facecolor="#f7f7f7", edgecolor="#9a9a9a",
                                linewidth=1.2, zorder=5))

    header = TextArea(
        "每 2 个 int4 打包进 1 byte，因此地址偏移除以 2",
        textprops=dict(fontfamily=CJK, fontsize=8.8, color="#555555"),
    )

    VAR = "#1f4e79"
    SCALE = "#9c6500"
    ASCALE = "#2f6b2f"
    PTR = "#333333"
    IDX = "#b35c00"
    COMMENT = "#6a737d"
    PLAIN = "#333333"

    lines = [
        [("w_int4", VAR), ("  = ", PLAIN), ("&B->int4_data_ptr", PTR),
         ("[(col*k + ch)", IDX), ("/2]", PLAIN),
         ("   // 2 int4 per byte -> offset /2", COMMENT)],
        [("a_int8", VAR), ("  = ", PLAIN), ("&A->int8_data_ptr", PTR),
         ("[row*k + ch];", IDX)],
        [("s_w", SCALE), ("     = ", PLAIN), ("scales", PTR),
         ("[(col*k+ch)/32];", IDX)],
        [("s_w_2nd", SCALE), (" = ", PLAIN), ("scales", PTR),
         ("[(col*k+ch)/32 + 1];", IDX)],
        [("s_a", ASCALE), ("     = ", PLAIN), ("A_scales", PTR),
         ("[(row*k+ch)/32];", IDX)],
        [("s_a_2nd", ASCALE), (" = ", PLAIN), ("A_scales", PTR),
         ("[(row*k+ch)/32 + 1];", IDX)],
    ]

    code_boxes = []
    for line in lines:
        parts = [TextArea(text, textprops=dict(fontfamily=MONO, fontsize=9.0,
                                                color=color))
                 for text, color in line]
        code_boxes.append(HPacker(children=parts, align="baseline", pad=0, sep=0))

    vp = VPacker(children=[header] + code_boxes, align="left", pad=0, sep=4)
    ab = AnnotationBbox(vp, (x + 0.18, y + h - 0.16), xycoords="data",
                        box_alignment=(0, 1), frameon=False, zorder=8)
    ax.add_artist(ab)


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
        "reference.cc — x86 int4 W4A8 matmul (QM_x86, block_size = 32)",
        fontsize=18, fontweight="bold", fontfamily=MONO, color=INK,
        va="top", ha="left", zorder=10)

# --- Left: exact small matrices --------------------------------------------
# A: m=4, k=64; Block 0 / Block 1 are large gradient bars.  Highlight row 1.
block_matrix(
    ax, 0.9, 7.45, 4.0, 1.55, rows=4,
    title="A  (m × k) = (4 × 64)",
    subtitle="FP32 activation → int8",
    dim_left="m = 4", hi_row=1,
    row_label="row = 1", row_edge="#2f80ed",
    block_note_blue="Block 0 (32 elements)",
    block_note_gold="Block 1 (32 elements)",
)

# B: n=4, k=64.  Highlight row 1.
block_matrix(
    ax, 0.9, 4.60, 4.0, 1.55, rows=4,
    title="B  (n × k) = (4 × 64)",
    subtitle="int4 weights, QM_x86 packed",
    dim_left="n = 4", hi_row=1,
    row_label="col = 1", row_edge="#e69138",
    block_note_blue="Block 0 (32 elements)",
    block_note_gold="Block 1 (32 elements)",
)

# C: m=n=4.  Highlight C[1][1].
simple_matrix(
    ax, 1.4, 1.90, 2.0, 1.55, rows=4, cols=4,
    title="C  (m × n) = (4 × 4)",
    subtitle="FP32 output",
    dim_left="m = 4", dim_top="n = 4",
    hi_cell=(1, 1), cell_label="C[1][1]",
)

# Dashed arrow guides from the highlighted row/column/element to the core.
a_row_y = 7.45 + 1.55 - 1.5 * 1.55 / 4
b_row_y = 4.60 + 1.55 - 1.5 * 1.55 / 4
c_cell_x = 1.4 + 2.0 * 1.5 / 4
c_cell_y = 1.90 + 1.55 - 1.5 * 1.55 / 4
dashed_arrow(ax, 4.9, a_row_y, 6.25, 8.72)
dashed_arrow(ax, 4.9, b_row_y, 6.25, 7.28)
dashed_arrow(ax, 6.25, 2.82, c_cell_x + 0.25, c_cell_y)

# --- Right: core calculation ------------------------------------------------
core = FancyBboxPatch((5.65, 0.65), 12.0, 9.55,
                      boxstyle="round,pad=0.05,rounding_size=0.22",
                      facecolor="#fcfcfc", edgecolor=RED, linewidth=1.6,
                      linestyle=(0, (6, 3)), zorder=0)
ax.add_patch(core)
ax.text(6.0, 9.82,
        "Core calculation: processing 64 elements per iteration (k = 64)",
        fontsize=14, fontweight="bold", color=RED, fontfamily=FONT,
        ha="left", va="top", zorder=10)
ax.text(6.0, 9.48, "ch, ch+1, ..., ch+63   (two 32-weight quantization blocks)",
        fontsize=9.5, color="#555555", fontfamily=FONT, ha="left", va="top",
        zorder=10)

# A int8 chunk: two rows of 32 cells, Block 0 blue and Block 1 gold.
a_x, a_y, a_cw, a_ch = 6.25, 8.55, 0.155, 0.24
for i in range(32):
    ax.add_patch(Rectangle((a_x + i * a_cw, a_y + 0.27), a_cw, a_ch,
                           facecolor=BLUE, edgecolor=INK, linewidth=0.7,
                           zorder=4))
    ax.add_patch(Rectangle((a_x + i * a_cw, a_y), a_cw, a_ch,
                           facecolor=YELLOW, edgecolor=INK, linewidth=0.7,
                           zorder=4))
ax.text(a_x, a_y + 0.27 + a_ch + 0.04,
        "Block 0: a_int8[ch ... ch+31]",
        fontsize=8.8, ha="left", va="bottom", fontfamily=MONO,
        color="#1f4e79", zorder=6)
ax.text(a_x, a_y - 0.05, "Block 1: a_int8[ch+32 ... ch+63]",
        fontsize=8.8, ha="left", va="top", fontfamily=MONO,
        color="#7f6000", zorder=6)
ax.text(a_x + 32 * a_cw + 0.12, a_y + 0.27 + a_ch / 2, "× s_a",
        fontsize=9, ha="left", va="center", color="#1f4e79",
        fontfamily=MONO, zorder=6)
ax.text(a_x + 32 * a_cw + 0.12, a_y + a_ch / 2, "× s_a_2nd",
        fontsize=9, ha="left", va="center", color="#7f6000",
        fontfamily=MONO, zorder=6)

# B packed chunk: 32 bytes, each byte split into high (gold) and low (blue).
b_x, b_y, b_cw, b_ch = 6.25, 7.05, 0.155, 0.42
for i in range(32):
    ax.add_patch(Rectangle((b_x + i * b_cw, b_y), b_cw, b_ch / 2,
                           facecolor=BLUE, edgecolor=INK, linewidth=0.7,
                           zorder=4))
    ax.add_patch(Rectangle((b_x + i * b_cw, b_y + b_ch / 2), b_cw, b_ch / 2,
                           facecolor=YELLOW, edgecolor=INK, linewidth=0.7,
                           zorder=4))
qj = 4
ax.add_patch(Rectangle((b_x + qj * b_cw, b_y), b_cw, b_ch, fill=False,
                       edgecolor=RED, linewidth=1.8, zorder=6))
ax.text(b_x + 16 * b_cw, b_y + b_ch + 0.10,
        "B packed: 32 bytes = 64 int4 weights",
        fontsize=9.2, ha="center", va="bottom", color="#7f6000",
        fontfamily=FONT, zorder=6)
ax.text(b_x, b_y - 0.22,
        "low nibble = Block 0 (blue)      high nibble = Block 1 (gold)",
        fontsize=8.8, ha="left", va="top", color="#333333",
        fontfamily=MONO, zorder=6)

# Expanded byte callout.
cb_x, cb_y, cb_w, cb_h = 12.25, 6.30, 4.25, 1.28
ax.add_patch(FancyBboxPatch((cb_x, cb_y), cb_w, cb_h,
                            boxstyle="round,pad=0.02,rounding_size=0.08",
                            facecolor="white", edgecolor="#8a6a1f",
                            linewidth=1.2, zorder=5))
ax.text(cb_x + cb_w / 2, cb_y + cb_h - 0.15, "byte qj",
        ha="center", va="center", fontsize=10, fontweight="bold",
        color="#7f6000", fontfamily=MONO, zorder=7)
# Gold = Block 1 / high nibble, blue = Block 0 / low nibble.
ax.add_patch(Rectangle((cb_x + 0.22, cb_y + 0.16), 1.55, 0.34,
                       facecolor=YELLOW_DARK, edgecolor=INK, linewidth=1.0,
                       zorder=6))
ax.add_patch(Rectangle((cb_x + 1.93, cb_y + 0.16), 1.55, 0.34,
                       facecolor=BLUE, edgecolor=INK, linewidth=1.0,
                       zorder=6))
ax.text(cb_x + 0.995, cb_y + 0.33, "high", ha="center", va="center",
        fontsize=9, fontfamily=MONO, zorder=7)
ax.text(cb_x + 2.705, cb_y + 0.33, "low", ha="center", va="center",
        fontsize=9, fontfamily=MONO, zorder=7)
ax.text(cb_x + 0.22, cb_y + 0.58, "q_w[ch+32+qj]",
        fontsize=8.4, ha="left", va="bottom", fontfamily=MONO, zorder=7)
ax.text(cb_x + 1.93, cb_y + 0.58, "q_w[ch+qj]",
        fontsize=8.4, ha="left", va="bottom", fontfamily=MONO, zorder=7)
ax.annotate("", xy=(cb_x, cb_y + 0.58),
            xytext=(b_x + qj * b_cw + b_cw, b_y + b_ch / 2),
            arrowprops=dict(arrowstyle="-", color=RED, lw=1.0,
                            linestyle=(0, (3, 2))), zorder=4)

# Two integer dot products.
sum_y = 5.15
box(ax, 6.25, sum_y, 4.35, 0.78,
    "sum0 = Σ_{e=0}^{31} a_int8[ch+e] · (q_w[ch+e] − 8)",
    face="#eef4fb", edge="#2f5f8f", fontsize=9.2, fontfamily=MONO,
    lw=1.8, rounding=0.18, fontweight="bold")
box(ax, 10.85, sum_y, 4.35, 0.78,
    "sum1 = Σ_{e=0}^{31} a_int8[ch+32+e] · (q_w[ch+32+e] − 8)",
    face="#fdf5df", edge="#8a6a1f", fontsize=9.2, fontfamily=MONO,
    lw=1.8, rounding=0.18, fontweight="bold")
ax.text(6.25, sum_y + 0.86, "Block 0  (low nibble)",
        fontsize=8.8, color="#1f4e79", ha="left", va="bottom",
        fontfamily=FONT, zorder=6)
ax.text(10.85, sum_y + 0.86, "Block 1  (high nibble)",
        fontsize=8.8, color="#7f6000", ha="left", va="bottom",
        fontfamily=FONT, zorder=6)

# Dequantization / accumulation.
box(ax, 6.25, 3.78, 9.0, 0.78,
    "acc += sum0 · s_a · s_w  +  sum1 · s_a_2nd · s_w_2nd",
    face="#f4f4f4", edge="#4f4f4f", fontsize=10.2, fontfamily=MONO,
    lw=1.5, rounding=0.14)
arrow(ax, 8.4, sum_y, 8.4, 4.56, color="#555555")
arrow(ax, 13.0, sum_y, 13.0, 4.56, color="#555555")

# Output element.
box(ax, 6.25, 2.55, 3.55, 0.55, "C[row, col]", face=GREEN,
    edge="#4f7a3a", fontsize=11, fontfamily=MONO, lw=1.5, rounding=0.12)
arrow(ax, 8.0, 3.78, 8.0, 3.10, color="#4f7a3a")

# Loop annotation.
ax.annotate("", xy=(6.25, 1.36), xytext=(10.15, 1.36),
            arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.1,
                            connectionstyle="arc3,rad=-0.22"), zorder=6)
ax.text(8.2, 0.92,
        "ch += 64   (loop ends when ch >= k; k is a multiple of 64)",
        fontsize=8.8, ha="center", va="center", color="#555555",
        fontfamily=MONO, zorder=6)

# Syntax-highlighted address/scale note (Chinese caption embedded).
code_panel(ax, 10.55, 1.02, 6.75, 2.0)

# Small formula reminder.
ax.text(5.95, 1.72, "q_w ∈ [0, 15]   ⇒   (q_w − 8) ∈ [−8, 7]",
        fontsize=8.8, ha="left", va="center", fontfamily=MONO,
        color="#7f6000", zorder=6)

fig.tight_layout(pad=0.2)
out = "lab5/figures/reference_x86.png"
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
print("wrote", out)
