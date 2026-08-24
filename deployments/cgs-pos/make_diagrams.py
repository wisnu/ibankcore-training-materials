"""Generator diagram untuk deployment CGS di PT Pos (tanpa Financing & Remittance,
tanpa Kafka/event-streaming — diganti Feeder SAP berbasis pull, dan tanpa klaim
PostgreSQL/CTI yang tidak berbasis kode).

Men-generate ulang Diagram 1 (arsitektur modul), Diagram 2 (alur double-entry),
dan Diagram 3 (integrasi sistem sekitar) — tiga diagram yang kontennya berbeda
dari versi master (lihat training-materials/scripts/make_diagrams.py). Diagram 4
tidak berubah — cukup dicopy apa adanya dari diagrams/ master.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Rectangle

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


def db_cylinder(ax, x, y, w, h, text, fc=NAVY, ec=NAVY, tc=WHITE, fs=10.5):
    """Simbol database fisik: silinder horizontal (rectangle + tutup elips kiri/kanan)."""
    cap_w = h * 0.55
    body = Rectangle((x + cap_w / 2, y), w - cap_w, h, linewidth=0, edgecolor=ec, facecolor=fc, zorder=1)
    ax.add_patch(body)
    for cx in (x + cap_w / 2, x + w - cap_w / 2):
        cap = Ellipse((cx, y + h / 2), cap_w, h, linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=2)
        ax.add_patch(cap)
    ax.plot([x + cap_w / 2, x + w - cap_w / 2], [y, y], color=ec, linewidth=1.4, zorder=3)
    ax.plot([x + cap_w / 2, x + w - cap_w / 2], [y + h, y + h], color=ec, linewidth=1.4, zorder=3)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fs, color=tc, fontweight="bold", zorder=4)


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
    "Enterprise", "Funding", "Accounting",
    "Kas & Vault\n(Teller/ATM)", "Internal\nAccount", "Customer"
]
mw, mh = 1.42, 1.15
gap = 0.14
row_w = len(modules) * mw + (len(modules) - 1) * gap
start_x = envelope_x + (envelope_w - row_w) / 2
y_mod = 4.15
for i, m in enumerate(modules):
    box(ax, start_x + i * (mw + gap), y_mod, mw, mh, m, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9)

db_cylinder(ax, 0.75, 2.65, 11.85, 0.85, "Shared Data Layer  —  Oracle", fc=NAVY, ec=NAVY, tc=WHITE, fs=10.5)

for i in range(len(modules)):
    xc = start_x + i * (mw + gap) + mw / 2
    arrow(ax, (xc, y_mod), (xc, 3.5), color=STEEL, lw=1.3)

box(ax, 10.9, 1.1, 2.1, 0.85, "Feeder SAP\n(Pull dari DB)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (11.95, 1.95), (10.9, 2.9), color=ACCENT, connectionstyle="arc3,rad=0.2", ls="--")

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
# DIAGRAM 2 — Alur Double-Entry Ledger (Modul Accounting)
# =====================================================================
fig, ax = new_fig(13, 6.8)
ax.text(6.5, 6.35, "Alur Pencatatan Transaksi — Modul Accounting", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 5.9, "Double-Entry Ledger & Propagasi Saldo Harian", ha="center", fontsize=10.5, color=GREY)

steps = [
    ("1. Transaksi\nMasuk", "Setor Tunai,\nPindah Buku, dll"),
    ("2. JOURNAL /\nJOURNALITEM", "Baris mutasi\nDR / CR"),
    ("3. Update Saldo\nRekening", "dailybalance-\nrekening"),
    ("4. Feeder SAP", "Pull berkala\ndari DB"),
    ("5. Downstream", "SAP, Reporting,\nRekonsiliasi"),
]
n = len(steps)
w, h = 2.15, 1.55
gap = (13 - n * w) / (n + 1)
y = 3.4
xs = []
for i, (title, sub) in enumerate(steps):
    x = gap + i * (w + gap)
    xs.append(x)
    fc = BG_CARD if i not in (1, 3) else "#FCEFDA" if i == 3 else "#E7F3EC"
    ec = BLUE_LIGHT if i not in (3,) else ACCENT
    box(ax, x, y, w, h, title, fc=fc, ec=ec, tc=NAVY, fs=10)
    ax.text(x + w / 2, y - 0.35, sub, ha="center", va="center", fontsize=8.6, color=GREY)

for i in range(n - 1):
    x1 = xs[i] + w
    x2 = xs[i + 1]
    arrow(ax, (x1, y + h / 2), (x2, y + h / 2), color=STEEL, lw=2.0)

fig.savefig(os.path.join(OUT_DIR, "02_alur_double_entry.png"), dpi=200, bbox_inches="tight", facecolor="white")
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

box(ax, 4.9, 1.15, 3.2, 0.95, "Feeder SAP\n(Pull dari DB Core)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (6.5, 2.1), (6.5, 3.55), color=ACCENT, ls="--")

box(ax, 0.6, 1.15, 3.4, 0.95, "Pelaporan Regulator\n(OJK / BI)", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=9.5)
arrow(ax, (4.9, 1.6), (4.0, 1.6), color=GREEN)

box(ax, 8.9, 1.15, 3.6, 0.95, "Rekonsiliasi &\nDailybalancerekening", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=9.5)
arrow(ax, (8.1, 1.6), (8.9, 1.6), color=GREEN)

fig.savefig(os.path.join(OUT_DIR, "03_integrasi_sistem_sekitar.png"), dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

# =====================================================================
# DIAGRAM 5 — Struktur Organisasi: Wilayah, Cabang & Atribut Kantor
# =====================================================================
fig, ax = new_fig(13, 8)
ax.text(6.5, 7.55, "Struktur Organisasi: Wilayah, Cabang & Atribut Kantor", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 7.12, "Ilustrasi hierarki Area Cabang → Cabang, relasi Cabang Induk-Anak, dan atribut Kantor", ha="center", fontsize=10, color=GREY)

# Wilayah (top)
box(ax, 4.85, 6.0, 3.3, 0.9, "Wilayah\n(Area Cabang)", fc=NAVY, ec=NAVY, tc=WHITE, fs=11)
box(ax, 8.75, 5.95, 3.35, 1.0, "Istilah bisnis di PT Pos:\n\"Regional\"", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.2, bold=False)
arrow(ax, (8.75, 6.45), (8.15, 6.45), color=ACCENT, connectionstyle="arc3,rad=0.0")

# Cabang A & B (children of wilayah)
box(ax, 1.3, 4.15, 3.9, 1.15, "Cabang A\nTipe: Cabang Utama (CU)", fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=10)
box(ax, 7.8, 4.15, 3.9, 1.15, "Cabang B\nTipe: Cabang Utama (CU)", fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=10)
arrow(ax, (5.6, 6.0), (3.25, 5.3), color=STEEL, connectionstyle="arc3,rad=-0.1")
arrow(ax, (7.35, 6.0), (9.75, 5.3), color=STEEL, connectionstyle="arc3,rad=0.1")
ax.text(6.5, 5.55, "1 wilayah menaungi\nbanyak cabang", ha="center", va="center", fontsize=8.3, color=GREY, style="italic")

# Cabang A1 — cabang anak dari Cabang A (relasi induk-anak, garis putus-putus, TERPISAH dari wilayah)
box(ax, 1.3, 2.15, 3.9, 1.15, "Cabang A1\nTipe: Cabang Pembantu (CP)", fc="#F5F8FC", ec=STEEL, tc=NAVY, fs=10)
arrow(ax, (3.25, 3.3), (3.25, 4.15), color=ACCENT, ls="--", connectionstyle="arc3,rad=0.0")
ax.text(5.35, 2.9, "kode_cabang_induk\n= Cabang A", ha="left", va="center", fontsize=8.0, color=ACCENT, style="italic")

# Kantor Kas — juga anak dari Cabang A, contoh tipe unit lain
box(ax, 7.8, 2.15, 3.9, 1.15, "Cabang C\nTipe: Kantor Kas (KS)", fc="#F5F8FC", ec=STEEL, tc=NAVY, fs=10)
arrow(ax, (9.75, 3.3), (9.75, 4.15), color=ACCENT, ls="--", connectionstyle="arc3,rad=0.0")
ax.text(7.65, 2.55, "kode_cabang_induk\n= Cabang B", ha="right", va="center", fontsize=8.0, color=ACCENT, style="italic")

# Legend
box(ax, 0.6, 0.35, 5.5, 1.35,
    "", fc=WHITE, ec=GREY, lw=1.0, fs=9)
ax.plot([0.9, 1.7], [1.35, 1.35], color=STEEL, linewidth=1.8)
ax.text(1.85, 1.35, "Pengelompokan wilayah (1 wilayah → banyak cabang)", ha="left", va="center", fontsize=8.5, color=NAVY)
ax.plot([0.9, 1.7], [0.75, 0.75], color=ACCENT, linewidth=1.8, linestyle="--")
ax.text(1.85, 0.75, "Relasi cabang induk-anak (kode_cabang_induk)", ha="left", va="center", fontsize=8.5, color=NAVY)

box(ax, 6.5, 0.35, 6.0, 1.35,
    "\"Kantor\" = atribut tipe/status & alamat-kontak yang\nmenempel pada Cabang — bukan level hierarki tersendiri\n(nilai: CU, CP, KS, PO, NO, GM, dst.)",
    fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=8.8, bold=False)

fig.savefig(os.path.join(OUT_DIR, "05_struktur_organisasi.png"), dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

print("done:", OUT_DIR)
