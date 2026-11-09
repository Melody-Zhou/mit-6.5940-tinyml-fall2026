"""Draw the x86 AVX2 SIMD kernel diagram for MIT 6.5940 Lab 5.

Run from the repository root:
    python3 lab5/figures/plot_simd_x86.py
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle


BG = "white"
INK = "#222222"
RED = "#cc4125"

BLUE = "#dbe9f7"
BLUE_EDGE = "#2f80ed"
GOLD = "#fdf2d0"
GOLD_EDGE = "#b07d18"
TEAL = "#d9edf7"
TEAL_EDGE = "#1f6f8b"
PURPLE = "#e8e0f4"
PURPLE_EDGE = "#7a63b5"
GREEN = "#d9ead3"
GREEN_EDGE = "#4f7a3a"

FONT = "DejaVu Sans"
MONO = "DejaVu Sans Mono"


def pick_code_font():
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Consolas", "Courier New", "DejaVu Sans Mono"):
        if name in installed:
            return name
    return "monospace"


CODE_FONT = pick_code_font()


def box(ax, x, y, w, h, text, face="white", edge=INK, fontsize=7.5,
        lw=1.1, rounding=0.08, color=INK, weight="normal", family=MONO,
        linespacing=1.25):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={rounding}",
                                facecolor=face, edgecolor=edge, linewidth=lw,
                                zorder=5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=color, fontfamily=family,
            fontweight=weight, linespacing=linespacing, zorder=6)


def lane_bar(ax, x, y, w, h, n, face, edge, lw=0.7, zorder=4):
    cw = w / n
    for i in range(n):
        ax.add_patch(Rectangle((x + i * cw, y), cw, h, facecolor=face,
                               edgecolor=edge, linewidth=lw, zorder=zorder))
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=INK,
                           linewidth=1.0, zorder=zorder + 1))


def arrow(ax, x1, y1, x2, y2, color="#555555", lw=1.1):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
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
        "simd_programming.cc — x86 AVX2: 64 int4 weights + 64 int8 activations",
        fontsize=18, fontweight="bold", fontfamily=MONO, color=INK,
        va="top", ha="left", zorder=10)

# --- Left: packed data and 256-bit vector views ----------------------------
ax.text(0.65, 10.05, "Data layout", fontsize=12.5, fontweight="bold",
        color="#444444", fontfamily=FONT, va="top", ha="left", zorder=9)

# raw_w: 32 packed bytes.
raw_x, raw_y, raw_w, raw_h = 0.9, 8.85, 4.8, 0.58
cell_w = raw_w / 32
for i in range(32):
    x = raw_x + i * cell_w
    ax.add_patch(Rectangle((x, raw_y), cell_w, raw_h / 2,
                           facecolor=BLUE, edgecolor=BLUE_EDGE,
                           linewidth=0.55, zorder=4))
    ax.add_patch(Rectangle((x, raw_y + raw_h / 2), cell_w, raw_h / 2,
                           facecolor=GOLD, edgecolor=GOLD_EDGE,
                           linewidth=0.55, zorder=4))
ax.add_patch(Rectangle((raw_x, raw_y), raw_w, raw_h, fill=False,
                       edgecolor=INK, linewidth=1.2, zorder=5))
ax.text(raw_x, raw_y + raw_h + 0.18,
        "raw_w = loadu_si256(w_start)", fontsize=8.8, fontweight="bold",
        family=MONO, color="#333333", ha="left", va="bottom", zorder=8)
ax.text(raw_x, raw_y - 0.16,
        "32 bytes = 256 bits; low nibble (blue) = Block 0, high nibble (gold) = Block 1",
        fontsize=7.9, color="#555555", family=FONT, ha="left", va="top",
        zorder=8)

# Unpacked low/high halves.
w0_y, w128_y, bar_h = 7.45, 6.55, 0.33
lane_bar(ax, raw_x, w0_y, raw_w, bar_h, 32, BLUE, BLUE_EDGE)
lane_bar(ax, raw_x, w128_y, raw_w, bar_h, 32, GOLD, GOLD_EDGE)
ax.text(raw_x, w0_y + bar_h + 0.12,
        "w_0 = (raw_w & 0x0F) - 8       32 × int8 (Block 0)",
        fontsize=8.2, color="#1f4e79", family=MONO, ha="left", va="bottom",
        zorder=8)
ax.text(raw_x, w128_y + bar_h + 0.12,
        "w_128 = ((raw_w >> 4) & 0x0F) - 8       32 × int8 (Block 1)",
        fontsize=8.2, color="#7f6000", family=MONO, ha="left", va="bottom",
        zorder=8)

# A: 64 int8 activations loaded as two 256-bit chunks.
a0_y, a1_y = 5.28, 4.48
lane_bar(ax, raw_x, a0_y, raw_w, bar_h, 32, TEAL, TEAL_EDGE)
lane_bar(ax, raw_x, a1_y, raw_w, bar_h, 32, TEAL, TEAL_EDGE)
ax.text(raw_x, a0_y + bar_h + 0.12,
        "A: 64 int8 activations = two 256-bit loads",
        fontsize=8.6, fontweight="bold", color="#1f6f8b", family=FONT,
        ha="left", va="bottom", zorder=8)
ax.text(raw_x + raw_w + 0.10, a0_y + bar_h / 2, "a0 = a_start[0]",
        fontsize=7.6, color="#1f6f8b", family=MONO, ha="left", va="center",
        zorder=8)
ax.text(raw_x + raw_w + 0.10, a1_y + bar_h / 2, "a1 = a_start[1]",
        fontsize=7.6, color="#1f6f8b", family=MONO, ha="left", va="center",
        zorder=8)

# Sign trick callout.
ax.add_patch(FancyBboxPatch((0.9, 2.55), 5.7, 1.25,
                            boxstyle="round,pad=0.04,rounding_size=0.10",
                            facecolor="#f7f7f7", edgecolor="#9a9a9a",
                            linewidth=1.0, zorder=4))
ax.text(1.08, 3.55, "Why the sign trick?", fontsize=8.8, fontweight="bold",
        color="#333333", family=FONT, ha="left", va="top", zorder=6)
ax.text(1.08, 3.27,
        "maddubs needs unsigned × signed:\n"
        "abs_w = |w| ∈ [0, 8],  signed_a = sign(a, w)\n"
        "⇒ abs_w · signed_a = a · w",
        fontsize=8.0, color="#333333", family=CODE_FONT, ha="left", va="top",
        linespacing=1.35, zorder=6)
ax.text(1.08, 2.34,
        "Each q iteration consumes 64 weights and 64 activations.",
        fontsize=8.0, color="#555555", family=FONT, ha="left", va="top",
        zorder=6)

# --- Right: AVX2 pipeline, Block 0 and Block 1 side by side -----------------
ax.text(7.8, 10.05, "AVX2 pipeline (per q iteration)", fontsize=12.5,
        fontweight="bold", color="#444444", fontfamily=FONT, va="top",
        ha="left", zorder=9)

col_x = [8.2, 12.9]
col_w = 4.0
col_color = [(BLUE, BLUE_EDGE, "#1f4e79", "Block 0  (low nibble)"),
             (GOLD, GOLD_EDGE, "#7f6000", "Block 1  (high nibble)")]

for i, (x, (face, edge, text_color, title)) in enumerate(zip(col_x, col_color)):
    w_name = "w_0" if i == 0 else "w_128"
    abs_name = "abs_w0" if i == 0 else "abs_w128"
    signed_name = "signed_a0" if i == 0 else "signed_a128"
    activation_name = "activation" if i == 0 else "activation2"
    tail = "" if i == 0 else "2"
    v_name = "v_s" if i == 0 else "v_s2"
    inter_name = "intermediate" if i == 0 else "intermediate2"

    ax.text(x, 9.72, title, fontsize=9.0, fontweight="bold",
            color=text_color, family=FONT, ha="left", va="bottom", zorder=8)

    # Activation load: the code stores a_start[0] / a_start[1] in
    # `activation` / `activation2`.
    box(ax, x, 9.28, col_w, 0.34,
        f"{activation_name} = load 256-bit(a_start[{i}])",
        face=TEAL, edge=TEAL_EDGE, fontsize=7.0, lw=1.0)
    arrow(ax, x + 2.70, 9.28, x + 2.70, 9.22, color=TEAL_EDGE, lw=0.9)

    # abs(w) and signed activation.
    box(ax, x, 8.82, 1.35, 0.38,
        f"{abs_name} = abs({w_name})",
        face="white", edge=edge, fontsize=6.5, lw=1.0)
    box(ax, x + 1.45, 8.82, 2.55, 0.38,
        f"{signed_name} = sign({activation_name}, {w_name})",
        face="white", edge=TEAL_EDGE, fontsize=6.0, lw=1.0)
    arrow(ax, x + 0.675, 8.82, x + 0.675, 8.75, color=edge, lw=0.9)
    arrow(ax, x + 2.725, 8.82, x + 2.725, 8.75, color=TEAL_EDGE, lw=0.9)

    # maddubs.
    box(ax, x, 8.30, col_w, 0.42,
        f"dot{tail} = maddubs({abs_name}, {signed_name})",
        face=face, edge=edge, fontsize=6.9, lw=1.0)
    arrow(ax, x + col_w / 2, 8.30, x + col_w / 2, 7.97, color=edge)

    # 16 int16 pair sums.
    lane_bar(ax, x, 7.64, col_w, 0.30, 16, PURPLE, PURPLE_EDGE)
    ax.text(x, 7.98, "16 × int16 pair sums", fontsize=7.2,
            color=PURPLE_EDGE, family=MONO, ha="left", va="bottom", zorder=8)
    arrow(ax, x + col_w / 2, 7.64, x + col_w / 2, 7.36, color=edge)

    # madd + 8 int32 quads.  The `ones` chip makes the int16 -> int32
    # pair reduction visible.
    box(ax, x, 6.93, col_w, 0.37,
        f"madd(ones, dot{tail})", face="white", edge=edge,
        fontsize=7.4, lw=1.0)
    ones_x = x + 2.40
    ax.add_patch(Rectangle((ones_x, 7.38), 1.42, 0.16,
                           facecolor=PURPLE, edgecolor=PURPLE_EDGE,
                           linewidth=0.7, zorder=5))
    ax.text(ones_x + 0.71, 7.46, "1 1 1 ...", fontsize=6.2,
            color=PURPLE_EDGE, family=MONO, ha="center", va="center",
            zorder=6)
    arrow(ax, ones_x + 0.71, 7.38, ones_x + 0.71, 7.30,
          color=PURPLE_EDGE, lw=0.8)
    arrow(ax, x + col_w / 2, 6.93, x + col_w / 2, 6.67, color=edge)
    lane_bar(ax, x, 6.32, col_w, 0.29, 8, PURPLE, PURPLE_EDGE)
    ax.text(x, 6.65, "8 × int32", fontsize=7.2, color=PURPLE_EDGE,
            family=MONO, ha="left", va="bottom", zorder=8)
    arrow(ax, x + col_w / 2, 6.32, x + col_w / 2, 6.05, color=edge)

    # Convert to float.
    box(ax, x, 5.63, col_w, 0.36, "cvtepi32_ps", face="white", edge=edge,
        fontsize=7.4, lw=1.0)
    arrow(ax, x + col_w / 2, 5.63, x + col_w / 2, 5.37, color=edge)
    lane_bar(ax, x, 5.02, col_w, 0.29, 8, GREEN, GREEN_EDGE)
    ax.text(x, 5.35, "8 × float", fontsize=7.2, color=GREEN_EDGE,
            family=MONO, ha="left", va="bottom", zorder=8)
    arrow(ax, x + col_w / 2, 5.02, x + col_w / 2, 4.76, color=edge)

    # FMA with per-block scale.
    scale = "v_s = set1(s_a * s_w)" if i == 0 else "v_s2 = set1(s_a_2nd * s_w_2nd)"
    box(ax, x, 4.18, col_w, 0.56,
        f"acc0 = fmadd({inter_name}, {v_name}, acc0)\n{scale}",
        face="#f4f4f4", edge="#555555", fontsize=7.0, lw=1.0)
    arrow(ax, x + col_w / 2, 4.18, x + col_w / 2, 3.91, color=edge)

# One shared acc0 vector, updated by both blocks.
acc_x, acc_y, acc_w, acc_h = 10.2, 3.58, 4.7, 0.33
lane_bar(ax, acc_x, acc_y, acc_w, acc_h, 8, GREEN, GREEN_EDGE)
ax.text(12.55, 3.98, "acc0 = acc0 + ...   (retained across q iterations)",
        fontsize=7.1, fontweight="bold", color=GREEN_EDGE, family=MONO,
        ha="center", va="bottom", zorder=8)
arrow(ax, acc_x + acc_w / 2, acc_y, acc_x + acc_w / 2, 3.25,
      color="#4f7a3a", lw=1.2)

box(ax, 10.45, 2.87, 4.15, 0.38,
    "C[row, col] = ptr[0] + ... + ptr[7]",
    face=GREEN, edge=GREEN_EDGE, fontsize=7.6, lw=1.2)
arrow(ax, 12.52, 2.87, 12.52, 2.62, color="#4f7a3a", lw=1.2)
box(ax, 11.45, 2.22, 2.15, 0.36, "C[row, col]", face=GREEN,
    edge=GREEN_EDGE, fontsize=8.4, lw=1.3)

# Loop bookkeeping.
box(ax, 8.20, 1.30, 8.60, 0.66,
    "q += 2;  w_start += 1  (= 32 bytes / 256 bits)\n"
    "a_start += 2  (= 64 bytes / 512 bits);  s_ptr += 2;  sa_ptr += 2",
    face="#f2f2f2", edge="#a0a0a0", fontsize=7.4, lw=1.0)
ax.text(8.20, 1.10,
        "two quantization blocks per iteration; horizontal reduction only once per output element",
        fontsize=7.8, color="#555555", family=FONT, ha="left", va="top",
        zorder=8)

fig.tight_layout(pad=0.2)
out = "lab5/figures/simd_x86.png"
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
print("wrote", out)
