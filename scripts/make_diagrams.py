import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.path import Path
import matplotlib.patches as mpatches

# ---- palette ----
NAVY = "#12233F"
BLUE = "#1F4E79"
BLUE_LIGHT = "#2E75B6"
STEEL = "#5B7FA6"
BG_CARD = "#EAF1F8"
ACCENT = "#C0862B"   # gold accent for Islamic finance / regulatory
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
# DIAGRAM 1 — Arsitektur Modul IBANKCORE
# =====================================================================
fig, ax = new_fig(13.5, 8.5)

ax.text(6.75, 8.15, "Arsitektur Modul IBANKCORE", ha="center", fontsize=17, fontweight="bold", color=NAVY)
ax.text(6.75, 7.72, "Core Banking Multi-Modul & Sistem di Sekitarnya", ha="center", fontsize=10.5, color=GREY)

# Channels row (top)
box(ax, 0.45, 6.7, 12.8, 1.0, "", fc="#F5F8FC", ec=BLUE, lw=1.6, radius=0.03)
ax.text(0.75, 7.65, "Channel Layer", fontsize=9.5, fontweight="bold", color=BLUE, va="top")
channels = ["Teller /\nBranch", "ATM / EDC", "Mobile &\nInternet Banking", "E-Channel /\nAPI Gateway"]
cx = 0.6
cw = 3.0
for i, c in enumerate(channels):
    box(ax, cx + i * (cw + 0.15), 6.75, cw, 0.75, c, fc=WHITE, ec=STEEL, tc=NAVY, fs=9.5)

arrow(ax, (6.75, 6.7), (6.75, 6.35), color=STEEL)

# Core banking envelope
box(ax, 0.5, 2.35, 12.5, 4.0, "", fc="#F5F8FC", ec=BLUE, lw=1.6, radius=0.03)
ax.text(0.85, 6.05, "IBANKCORE  (Core Banking System)", fontsize=12, fontweight="bold", color=BLUE)

modules = [
    "Funding", "Financing", "Accounting", "Kas & Vault\n(Teller/ATM)",
    "Remittance", "Internal\nAccount", "Customer", "Enterprise"
]
mw, mh = 1.42, 1.15
gap = 0.14
start_x = 0.75
y_mod = 4.15
for i, m in enumerate(modules):
    box(ax, start_x + i * (mw + gap), y_mod, mw, mh, m, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9)

# ledger / db bar
box(ax, 0.75, 2.65, 11.85, 0.85, "Shared Ledger & Data Layer  —  Oracle  /  PostgreSQL", fc=NAVY, ec=NAVY, tc=WHITE, fs=10.5)

for i in range(len(modules)):
    xc = start_x + i * (mw + gap) + mw / 2
    arrow(ax, (xc, y_mod), (xc, 3.5), color=STEEL, lw=1.3)

# Kafka outbox
box(ax, 10.9, 1.1, 2.1, 0.85, "Kafka\n(Outbox Events)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (10.9, 2.9), (11.95, 1.95), color=ACCENT, connectionstyle="arc3,rad=-0.2")

# Surrounding systems (bottom row)
surround = [
    ("SKN / RTGS /\nBI-FAST", 0.5),
    ("Payment Switching /\nSwitching Gateway", 3.15),
    ("Regulator\nOJK / BI Reporting", 5.85),
    ("Kantor Akuntan /\nExternal Audit", 8.55),
]
for label, x in surround:
    box(ax, x, 0.35, 2.5, 0.9, label, fc=WHITE, ec=GREY, tc=NAVY, fs=9.2)
    xc = x + 1.25
    arrow(ax, (xc, 2.35), (xc, 1.25), color=GREY, connectionstyle="arc3,rad=0.0")

fig.savefig("diagrams/01_arsitektur_ibankcore.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

# =====================================================================
# DIAGRAM 2 — Alur Double-Entry Ledger (Modul Accounting)
# =====================================================================
fig, ax = new_fig(13, 6.8)
ax.text(6.5, 6.35, "Alur Pencatatan Transaksi — Modul Accounting", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 5.9, "Double-Entry Ledger & Propagasi Saldo Harian", ha="center", fontsize=10.5, color=GREY)

steps = [
    ("1. Transaksi\nMasuk", "Setor Tunai,\nPindah Buku, dll"),
    ("2. TRANSACTION_\nDETAILS", "MUTATION_TYPE\nDR / CR"),
    ("3. Update Saldo\nRekening", "dailybalance-\nrekening"),
    ("4. Outbox Event", "Publish ke\nKafka"),
    ("5. Downstream", "Reporting,\nNotifikasi, GL"),
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

# CTI cross-schema note under step 2-3
box(ax, xs[1] - 0.1, 1.15, xs[2] + w - xs[1] + 0.2, 0.75,
    "Class Table Inheritance (CTI) — skema terpisah:\nCORE_TRX · FUNDING · CASHMGT · REMIT",
    fc="white", ec=STEEL, tc=NAVY, fs=8.6)
arrow(ax, (xs[1] + 0.3, 1.9), (xs[1] + 0.3, y), color=STEEL, ls="--", lw=1.2)

fig.savefig("diagrams/02_alur_double_entry.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

# =====================================================================
# DIAGRAM 3 — Integrasi dengan Sistem Sekitar (Treasury / Kas & Vault / Remittance)
# =====================================================================
fig, ax = new_fig(13, 8)
ax.text(6.5, 7.55, "Integrasi IBANKCORE dengan Sistem Sekitar", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 7.12, "Kas & Vault, Treasury & Remittance", ha="center", fontsize=10.5, color=GREY)

# center core
box(ax, 5.15, 3.55, 2.7, 1.3, "IBANKCORE\n(Kas & Vault /\nTreasury / Remittance)", fc=NAVY, ec=NAVY, tc=WHITE, fs=9.8)

left_items = [
    ("Teller / Vault /\nATM (CASH_POINT)", 5.9),
    ("Internal Account\n(Sundry, GL)", 4.3),
]
for i, (label, yy) in enumerate(left_items):
    box(ax, 0.6, yy, 2.9, 1.0, label, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9.5)
    arrow(ax, (3.5, yy + 0.5), (5.15, 4.2), color=STEEL, connectionstyle="arc3,rad=0.15")

right_items = [
    ("SKN — Kliring\nAntar Bank", 5.9),
    ("RTGS — Transfer\nBernilai Besar", 4.3),
    ("BI-FAST — Transfer\nRealtime", 2.7),
]
for label, yy in right_items:
    box(ax, 9.6, yy, 2.9, 1.0, label, fc="#F5F8FC", ec=STEEL, tc=NAVY, fs=9.5)
    arrow(ax, (7.85, 4.2), (9.6, yy + 0.5), color=STEEL, connectionstyle="arc3,rad=-0.15")

# bottom: Kafka + reporting
box(ax, 4.9, 1.15, 3.2, 0.95, "Kafka Outbox\n(Transactional Events)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (6.5, 3.55), (6.5, 2.1), color=ACCENT)

box(ax, 0.6, 1.15, 3.4, 0.95, "Pelaporan Regulator\n(OJK / BI)", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=9.5)
arrow(ax, (4.9, 1.6), (4.0, 1.6), color=GREEN)

box(ax, 8.9, 1.15, 3.6, 0.95, "Rekonsiliasi &\nDailybalancerekening", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=9.5)
arrow(ax, (8.1, 1.6), (8.9, 1.6), color=GREEN)

fig.savefig("diagrams/03_integrasi_sistem_sekitar.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

# =====================================================================
# DIAGRAM 4 — Contoh Proses Bisnis: Setor Tunai (swimlane sederhana)
# =====================================================================
fig, ax = new_fig(13, 7.5)
ax.text(6.5, 7.1, "Contoh Proses Bisnis — Setor Tunai", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 6.68, "Alur Lintas Fungsi (Simplified Swimlane)", ha="center", fontsize=10.5, color=GREY)

lanes = ["Nasabah", "Teller", "IBANKCORE\n(Core)", "Accounting /\nLedger"]
lane_h = 1.35
lane_y0 = 1.0
for i, lane in enumerate(lanes):
    y = lane_y0 + (len(lanes) - 1 - i) * lane_h
    ax.add_patch(Rectangle((0.4, y), 12.2, lane_h, fill=False, edgecolor=GREY, linewidth=1.0))
    ax.text(0.15, y + lane_h / 2, lane, ha="right", va="center", fontsize=9.5, fontweight="bold", color=NAVY)

steps4 = [
    (0, 1.3, "Datang &\nserahkan dana"),
    (1, 3.4, "Input transaksi\nSetor Tunai"),
    (2, 5.6, "Validasi rekening\n& saldo"),
    (2, 7.8, "Catat mutasi\nCR (kredit)"),
    (3, 10.0, "Update ledger &\ndailybalance"),
    (1, 12.0, "Cetak bukti /\nnotifikasi"),
]
positions = {}
for lane_idx, x, label in steps4:
    y = lane_y0 + (len(lanes) - 1 - lane_idx) * lane_h + lane_h / 2
    box(ax, x - 0.85, y - 0.42, 1.7, 0.84, label, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=8.3, radius=0.06)
    positions[x] = (x, y)

order = [1.3, 3.4, 5.6, 7.8, 10.0, 12.0]
lane_map = [0, 1, 2, 2, 3, 1]
for i in range(len(order) - 1):
    x1, y1 = positions[order[i]]
    x2, y2 = positions[order[i + 1]]
    arrow(ax, (x1 + 0.85, y1), (x2 - 0.85, y2), color=STEEL, connectionstyle="arc3,rad=0.0" if lane_map[i]==lane_map[i+1] else "arc3,rad=0.25")

fig.savefig("diagrams/04_proses_setor_tunai.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

print("done")
