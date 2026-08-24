"""Generator diagram untuk deployment CGS di PT Pos (tanpa Financing & Remittance).

Hanya men-generate ulang Diagram 1 (arsitektur modul) dan Diagram 3 (integrasi
sistem sekitar), karena keduanya satu-satunya diagram yang menyebut modul
Financing/Remittance di versi master (lihat training-materials/scripts/make_diagrams.py).
Diagram 2 dan 4 tidak berubah — cukup dicopy apa adanya dari diagrams/ master.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")

# ---- palette (samakan dengan scripts/make_diagrams.py) ----
NAVY = "#12233F"
BLUE = "#1F4E79"
BLUE_LIGHT = "#2E75B6"
STEEL = "#5B7FA6"
BG_CARD = "#EAF1F8"
ACCENT = "#C0862B"
GREEN = "#2E7D5B"
GREY = "#6B7280"
WHITE = "#FFFFFF"
TEXT_DARK = "#12233F"

plt.rcParams["font.family"] = "DejaVu Sans"


def box(ax, x, y, w, h, text, fc=BG_CARD, ec=BLUE, tc=TEXT_DARK, fs=10.5, bold=True, radius=0.02, lw=1.4):
    b = FancyBboxPatch((x, y), w, h,
                        boxstyle=f"round,pad=0.01,rounding_size={radius}",
                        linewidth=lw, edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fs, color=tc, fontweight="bold" if bold else "normal", wrap=True)
    return b


def arrow(ax, p1, p2, color=STEEL, lw=1.8, style="-|>", connectionstyle="arc3,rad=0.0", ls="-"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                         linewidth=lw, color=color, connectionstyle=connectionstyle, linestyle=ls, zorder=5)
    ax.add_patch(a)


def new_fig(w=13, h=8):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


# =====================================================================
# DIAGRAM 1 — Arsitektur Modul IBANKCORE (tanpa Financing & Remittance)
# =====================================================================
fig, ax = new_fig(13.5, 8.5)

ax.text(6.75, 8.15, "Arsitektur Modul IBANKCORE", ha="center", fontsize=17, fontweight="bold", color=NAVY)
ax.text(6.75, 7.72, "Core Banking Multi-Modul & Sistem di Sekitarnya", ha="center", fontsize=10.5, color=GREY)

channels = ["Teller /\nBranch", "ATM / EDC", "Mobile &\nInternet Banking", "E-Channel /\nAPI Gateway"]
cx = 0.6
cw = 3.0
for i, c in enumerate(channels):
    box(ax, cx + i * (cw + 0.15), 6.75, cw, 0.75, c, fc=WHITE, ec=STEEL, tc=NAVY, fs=9.5)

arrow(ax, (6.75, 6.75), (6.75, 6.35), color=STEEL)

envelope_x, envelope_w = 0.5, 12.5
box(ax, envelope_x, 2.35, envelope_w, 4.0, "", fc="#F5F8FC", ec=BLUE, lw=1.6, radius=0.03)
ax.text(0.85, 6.05, "IBANKCORE  (Core Banking System)", fontsize=12, fontweight="bold", color=BLUE)

modules = [
    "Funding", "Accounting", "Kas & Vault\n(Teller/ATM)",
    "Internal\nAccount", "Customer", "Enterprise"
]
mw, mh = 1.42, 1.15
gap = 0.14
row_w = len(modules) * mw + (len(modules) - 1) * gap
start_x = envelope_x + (envelope_w - row_w) / 2
y_mod = 4.15
for i, m in enumerate(modules):
    box(ax, start_x + i * (mw + gap), y_mod, mw, mh, m, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9)

box(ax, 0.75, 2.65, 11.85, 0.85, "Shared Ledger & Data Layer  —  Oracle  /  PostgreSQL", fc=NAVY, ec=NAVY, tc=WHITE, fs=10.5)

for i in range(len(modules)):
    xc = start_x + i * (mw + gap) + mw / 2
    arrow(ax, (xc, y_mod), (xc, 3.5), color=STEEL, lw=1.3)

box(ax, 10.9, 1.1, 2.1, 0.85, "Kafka\n(Outbox Events)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (10.9, 2.9), (11.95, 1.95), color=ACCENT, connectionstyle="arc3,rad=-0.2")

surround_items = [
    "Payment Switching /\nSwitching Gateway",
    "Regulator\nOJK / BI Reporting",
    "Kantor Akuntan /\nExternal Audit",
]
surround_w = 2.5
surround_gap = 0.15
surround_row_w = len(surround_items) * surround_w + (len(surround_items) - 1) * surround_gap
surround_start_x = envelope_x + (envelope_w - surround_row_w) / 2
surround = [(label, surround_start_x + i * (surround_w + surround_gap)) for i, label in enumerate(surround_items)]
for label, x in surround:
    box(ax, x, 0.35, 2.5, 0.9, label, fc=WHITE, ec=GREY, tc=NAVY, fs=9.2)
    xc = x + 1.25
    arrow(ax, (xc, 2.35), (xc, 1.25), color=GREY, connectionstyle="arc3,rad=0.0")

fig.savefig(os.path.join(OUT_DIR, "01_arsitektur_ibankcore.png"), dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

# =====================================================================
# DIAGRAM 3 — Integrasi dengan Sistem Sekitar (Treasury / Kas & Vault)
# =====================================================================
fig, ax = new_fig(13, 8)
ax.text(6.5, 7.55, "Integrasi IBANKCORE dengan Sistem Sekitar", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 7.12, "Kas & Vault & Treasury", ha="center", fontsize=10.5, color=GREY)

box(ax, 5.15, 3.55, 2.7, 1.3, "IBANKCORE\n(Kas & Vault /\nTreasury)", fc=NAVY, ec=NAVY, tc=WHITE, fs=9.8)

left_items = [
    ("Teller / Vault /\nATM (CASH_POINT)", 4.3),
]
for label, yy in left_items:
    box(ax, 0.6, yy, 2.9, 1.0, label, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9.5)
    arrow(ax, (3.5, yy + 0.5), (5.15, 4.2), color=STEEL, connectionstyle="arc3,rad=0.15")

right_items = [
    ("Internal Account\n(Sundry, GL)", 4.3),
]
for label, yy in right_items:
    box(ax, 9.6, yy, 2.9, 1.0, label, fc="#F5F8FC", ec=STEEL, tc=NAVY, fs=9.5)
    arrow(ax, (7.85, 4.2), (9.6, yy + 0.5), color=STEEL, connectionstyle="arc3,rad=-0.15")

box(ax, 4.9, 1.15, 3.2, 0.95, "Kafka Outbox\n(Transactional Events)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (6.5, 3.55), (6.5, 2.1), color=ACCENT)

box(ax, 0.6, 1.15, 3.4, 0.95, "Pelaporan Regulator\n(OJK / BI)", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=9.5)
arrow(ax, (4.9, 1.6), (4.0, 1.6), color=GREEN)

box(ax, 8.9, 1.15, 3.6, 0.95, "Rekonsiliasi &\nDailybalancerekening", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=9.5)
arrow(ax, (8.1, 1.6), (8.9, 1.6), color=GREEN)

fig.savefig(os.path.join(OUT_DIR, "03_integrasi_sistem_sekitar.png"), dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

print("done:", OUT_DIR)
