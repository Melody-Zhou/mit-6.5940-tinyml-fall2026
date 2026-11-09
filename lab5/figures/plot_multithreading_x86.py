"""Draw the multithreading x86 kernel diagram for MIT 6.5940 Lab 5.

Run from the repository root:
    python3 lab5/figures/plot_multithreading_x86.py
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path


BG = "white"
INK = "#222222"
GRID_LIGHT = "#cfcfcf"
RED = "#cc4125"

BLUE = "#cfe2f3"
BLUE_DARK = "#8fb9e3"
YELLOW = "#fff2cc"
YELLOW_DARK = "#e6c470"
GREEN = "#d9ead3"

FONT = "DejaVu Sans"
MONO = "DejaVu Sans Mono"


def pick_code_font():
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Consolas", "Courier New", "DejaVu Sans Mono"):
        if name in installed:
            return name
    return "monospace"


CODE_FONT = pick_code_font()

THREADS = [
    ("#dbe9f7", "#9fc5e8", "#2f80ed"),
    ("#e2f0d9", "#a9d18e", "#5a8f3c"),
    ("#e8e0f4", "#b4a7d6", "#7a63b5"),
    ("#fdf2d0", "#f1c232", "#b07d18"),
]


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
            fontsize=9.5, color=color, fontfamily=FONT, zorder=8)


def box(ax, x, y, w, h, text, face="white", edge=INK, fontsize=8.5,
        lw=1.3, rounding=0.12, color=INK, weight="normal", shadow=True):
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
            fontsize=fontsize, color=color, fontfamily=MONO,
            fontweight=weight, zorder=6)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0), zorder=7)


def dashed_arrow(ax, x1, y1, x2, y2, color, lw=1.3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=(0, (4, 3)),
                                shrinkA=0, shrinkB=0), zorder=3)


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
        "multithreading.cc — x86: four pthreads on disjoint output columns",
        fontsize=18, fontweight="bold", fontfamily=MONO, color=INK,
        va="top", ha="left", zorder=10)

# --- Left: work decomposition ----------------------------------------------
ax.text(0.65, 10.12, "Work decomposition", fontsize=12.5,
        fontweight="bold", color="#444444", fontfamily=FONT,
        va="top", ha="left", zorder=9)

# A: one row, shared by all four workers.
a_x, a_y, a_w, a_h = 1.0, 8.62, 4.0, 0.46
half = a_w / 2
gradient_block(ax, a_x, a_y, half, a_h, "#eaf3fb", BLUE_DARK)
gradient_block(ax, a_x + half, a_y, half, a_h, "#fff8df", YELLOW_DARK)
ax.plot([a_x + half, a_x + half], [a_y, a_y + a_h], color="#666666",
        lw=1.0, linestyle=(0, (4, 3)), zorder=5)
ax.add_patch(Rectangle((a_x, a_y), a_w, a_h, fill=False, edgecolor=INK,
                       linewidth=1.4, zorder=5))
ax.text(a_x, a_y + a_h + 0.52, "A  (m × k) = (1 × 4096)", va="bottom",
        ha="left", fontsize=12, fontweight="bold", color=INK,
        fontfamily=FONT, zorder=8)
ax.text(a_x, a_y + a_h + 0.30, "FP32 activation → int8, k = 4096, quantized once",
        va="bottom", ha="left", fontsize=8.8, color="#555555",
        fontfamily=FONT, zorder=8)
ax.text(a_x - 0.22, a_y + a_h / 2, "m = 1", va="center", ha="right",
        fontsize=9.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
ax.text(a_x + a_w + 0.15, a_y - 0.02, "row = 0",
        va="center", ha="left", fontsize=8.6, color="#1f4e79",
        fontfamily=MONO, zorder=8)

# B: 32000 rows (output columns), split into four contiguous bands.
b_x, b_y, b_w, b_h = 1.0, 5.50, 4.0, 2.46
for i, (light, dark, edge) in enumerate(THREADS):
    by = b_y + b_h - (i + 1) * b_h / 4
    bh = b_h / 4
    gradient_block(ax, b_x, by, b_w, bh, light, dark)
    ax.add_patch(Rectangle((b_x, by), b_w, bh, fill=False, edgecolor=edge,
                           linewidth=1.2, zorder=5))
    start = i * 8000
    end = (i + 1) * 8000 - 1
    ax.text(b_x + b_w + 0.15, by + bh / 2,
            f"T{i}: rows {start}..{end} (output cols)", va="center", ha="left",
            fontsize=7.8, fontweight="bold", color=edge,
            fontfamily=MONO, zorder=8,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4))

ax.add_patch(Rectangle((b_x, b_y), b_w, b_h, fill=False, edgecolor=INK,
                       linewidth=1.5, zorder=6))
for i in range(1, 4):
    yy = b_y + b_h - i * b_h / 4
    ax.plot([b_x, b_x + b_w], [yy, yy], color="white", lw=1.8,
            linestyle=(0, (4, 3)), zorder=6)
ax.text(b_x, b_y + b_h + 0.36, "B  (n × k) = (32000 × 4096)", va="bottom",
        ha="left", fontsize=12, fontweight="bold", color=INK,
        fontfamily=FONT, zorder=8)
ax.text(b_x, b_y + b_h + 0.16, "int4 weights, QM_x86 packed; each band = 8000 rows (output cols)",
        va="bottom", ha="left", fontsize=8.8, color="#555555",
        fontfamily=FONT, zorder=8)
ax.text(b_x - 0.22, b_y + b_h / 2, "n = 32000 rows", va="center", ha="right",
        fontsize=9.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
ax.text(b_x, b_y - 0.18, "B rows are output columns (n = 32000); B cols are k = 4096",
        va="top", ha="left", fontsize=8.2, color="#555555",
        fontfamily=FONT, zorder=8)

# C: output row, split into the same four ranges.
c_x, c_y, c_w, c_h = 1.0, 2.78, 4.0, 0.52
seg_w = c_w / 4
for i, (light, dark, edge) in enumerate(THREADS):
    sx = c_x + i * seg_w
    ax.add_patch(Rectangle((sx, c_y), seg_w, c_h, facecolor=light,
                           edgecolor=edge, linewidth=1.4, zorder=3))
    ax.text(sx + seg_w / 2, c_y + c_h / 2, f"T{i}", ha="center",
            va="center", fontsize=9.0, fontweight="bold", color=edge,
            fontfamily=MONO, zorder=6)
ax.add_patch(Rectangle((c_x, c_y), c_w, c_h, fill=False, edgecolor=INK,
                       linewidth=1.5, zorder=5))
ax.text(c_x, c_y + c_h + 0.48, "C  (m × n) = (1 × 32000)", va="bottom",
        ha="left", fontsize=12, fontweight="bold", color=INK,
        fontfamily=FONT, zorder=8)
ax.text(c_x, c_y + c_h + 0.28, "FP32 output; each worker writes only its own segment",
        va="bottom", ha="left", fontsize=8.8, color="#555555",
        fontfamily=FONT, zorder=8)
ax.text(c_x - 0.22, c_y + c_h / 2, "m = 1", va="center", ha="right",
        fontsize=9.5, color=INK, fontfamily=FONT, rotation=90, zorder=8)
ax.text(c_x, c_y - 0.18, "Disjoint C columns → no locks, no atomic updates",
        va="top", ha="left", fontsize=8.6, color="#2f6b2f",
        fontfamily=FONT, zorder=8)

# --- Right: concurrent execution -------------------------------------------
ax.text(6.0, 10.12, "Concurrent execution", fontsize=12.5,
        fontweight="bold", color="#444444", fontfamily=FONT,
        va="top", ha="left", zorder=9)

main_y, main_h = 9.22, 0.50
box(ax, 6.35, main_y, 2.15, main_h, "quantize A", face="white",
    edge="#555555", fontsize=8.8, lw=1.4)
box(ax, 9.00, main_y, 2.15, main_h, "pthread_create ×4", face="white",
    edge="#555555", fontsize=8.8, lw=1.4)
box(ax, 14.05, main_y, 1.95, main_h, "pthread_join", face="white",
    edge="#555555", fontsize=8.8, lw=1.4)
arrow(ax, 8.50, main_y + main_h / 2, 9.00, main_y + main_h / 2,
      color="#555555")
arrow(ax, 11.15, main_y + main_h / 2, 11.42, main_y + main_h / 2,
      color="#555555")
arrow(ax, 13.90, main_y + main_h / 2, 14.05, main_y + main_h / 2,
      color="#555555")
ax.text(6.35, main_y + main_h + 0.10, "main thread", fontsize=8.5,
        color="#555555", fontfamily=MONO, va="bottom", zorder=8)

# Parallel region and four worker lanes.
region_x0, region_x1 = 11.45, 13.90
ax.add_patch(FancyBboxPatch((region_x0, 6.38), region_x1 - region_x0, 2.42,
                            boxstyle="round,pad=0.03,rounding_size=0.10",
                            facecolor="#fafafa", edgecolor="#9a9a9a",
                            linewidth=0.9, linestyle=(0, (3, 3)),
                            zorder=1))
ax.plot([region_x0, region_x0], [6.38, 9.18], color="#777777", lw=1.1,
        linestyle=(0, (3, 3)), zorder=2)
ax.plot([region_x1, region_x1], [6.38, 9.18], color="#777777", lw=1.1,
        linestyle=(0, (3, 3)), zorder=2)
ax.text((region_x0 + region_x1) / 2, 8.92, "parallel region",
        ha="center", va="bottom", fontsize=8.2, color="#555555",
        fontfamily=FONT, zorder=8)

lane_y = [8.40, 7.72, 7.04, 6.36]
for i, (light, dark, edge) in enumerate(THREADS):
    y = lane_y[i]
    ax.add_patch(FancyBboxPatch((region_x0 + 0.05, y), region_x1 - region_x0 - 0.10,
                                0.46, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=light, edgecolor=edge, linewidth=1.2,
                                zorder=4))
    ax.text(region_x0 + 0.22, y + 0.23, f"T{i}", ha="left", va="center",
            fontsize=8.4, fontweight="bold", color=edge, fontfamily=MONO,
            zorder=6)
    ax.text(region_x0 + 0.72, y + 0.23, f"cols {i * 8000}..{(i + 1) * 8000 - 1}",
            ha="left", va="center", fontsize=7.8, color="#333333",
            fontfamily=MONO, zorder=6)

ax.text(region_x0 - 0.08, 9.17, "fork", ha="right", va="center",
        fontsize=8.0, color="#555555", fontfamily=FONT, zorder=8)
ax.text(region_x1 + 0.08, 9.17, "join", ha="left", va="center",
        fontsize=8.0, color="#555555", fontfamily=FONT, zorder=8)

# A is read by every worker: one dashed bus fans out to all four lanes.
a_bus_x = 7.55
a_row_center = a_y + a_h / 2
ax.plot([a_x + a_w, a_bus_x], [a_row_center, a_row_center],
        color="#2f80ed", lw=1.5, linestyle=(0, (5, 3)), zorder=3)
ax.plot([a_bus_x, a_bus_x], [a_row_center, lane_y[-1] + 0.23],
        color="#2f80ed", lw=1.5, linestyle=(0, (5, 3)), zorder=3)
for y in lane_y:
    ax.plot([a_bus_x, region_x0], [y + 0.23, y + 0.23],
            color="#2f80ed", lw=1.2, linestyle=(0, (4, 3)), zorder=3)
    ax.add_patch(plt.Circle((a_bus_x, y + 0.23), 0.045,
                            facecolor="#2f80ed", edgecolor="none", zorder=6))
    dashed_arrow(ax, a_bus_x, y + 0.23, region_x0 + 0.03, y + 0.23,
                 color="#2f80ed", lw=1.3)
ax.text(a_bus_x + 0.10, 8.35, "A: shared read-only",
        va="center", ha="left", fontsize=8.2, color="#1f4e79",
        fontfamily=FONT, zorder=8,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.5))

# Worker kernel summary.
panel_x, panel_w = 6.15, 11.25
ax.add_patch(FancyBboxPatch((panel_x, 4.28), panel_w, 1.48,
                            boxstyle="round,pad=0.04,rounding_size=0.12",
                            facecolor="#f7f7f7", edgecolor="#9a9a9a",
                            linewidth=1.0, zorder=4))
ax.text(panel_x + 0.18, 5.55, "multithreading_worker_func  (one call per thread)",
        fontsize=8.8, fontweight="bold", fontfamily=CODE_FONT, color="#333333",
        ha="left", va="top", zorder=6)
worker_lines = [
    "for (row = 0; row < m; row++)",
    "    for (col = start; col < end; col++)",
    "        acc = same x86 64-weight block dot product;",
    "        C[row, col] = acc;",
]
ax.text(panel_x + 0.18, 5.28, "\n".join(worker_lines), fontsize=8.4,
        ha="left", va="top", fontfamily=CODE_FONT, color="#333333",
        linespacing=1.35, zorder=6)
ax.plot([panel_x + 6.95, panel_x + 6.95], [4.42, 5.62],
        color="#d0d0d0", lw=0.8, zorder=5)
ax.text(panel_x + 7.12, 5.55,
        "shared, read-only:\nA, B, params\nA_int8, A_scales",
        fontsize=7.6, ha="left", va="top", fontfamily=CODE_FONT,
        color="#1f4e79", linespacing=1.30, zorder=6)
ax.text(panel_x + 7.12, 4.98,
        "private:\nacc, args\nC[row, col]",
        fontsize=7.6, ha="left", va="top", fontfamily=CODE_FONT,
        color="#a61c00", linespacing=1.30, zorder=6)

# Thread creation / join code.
code_x, code_y, code_w, code_h = 6.15, 2.12, 11.25, 1.98
ax.add_patch(FancyBboxPatch((code_x, code_y), code_w, code_h,
                            boxstyle="round,pad=0.04,rounding_size=0.12",
                            facecolor="#f2f2f2", edgecolor="#a0a0a0",
                            linewidth=1.0, zorder=4))
code_lines = [
    "const int num_thread = 4;",
    "const int cols_per_thread = n / num_thread;",
    "for (int i = 0; i < num_thread; i++) {",
    "    threads_args[i].start = i * cols_per_thread;",
    "    threads_args[i].end = (i == num_thread - 1) ? n",
    "                          : (i + 1) * cols_per_thread;",
    "    threads_args[i].params = params;",
    "    pthread_create(&thread_pool[i], NULL,",
    "                   multithreading_worker_func, &threads_args[i]);",
    "}",
    "for (int i = 0; i < num_thread; i++)",
    "    pthread_join(thread_pool[i], NULL);",
]
ax.text(code_x + 0.18, code_y + code_h - 0.16, "\n".join(code_lines),
        fontsize=7.9, ha="left", va="top", fontfamily=CODE_FONT,
        color="#242424", linespacing=1.28, zorder=6)

# Bottom takeaway badge.
ax.text(6.15, 1.42,
        "4 threads × 8000 columns = 32000 outputs\n"
        "Speedup ≈ 4× (measured 3.70×);  main-thread serial cost = quantize + fork/join",
        fontsize=8.5, fontweight="bold", color="#a61c00", ha="left",
        va="center", fontfamily=FONT, zorder=8, linespacing=1.30,
        bbox=dict(boxstyle="round,pad=0.32", facecolor="#fdecea",
                  edgecolor="#cc4125", linewidth=1.1))

fig.tight_layout(pad=0.2)
out = "lab5/figures/multithreading_x86.png"
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
print("wrote", out)
