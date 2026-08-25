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
fig, ax = new_fig(16.7, 8.5)

ax.text(8.35, 8.15, "Arsitektur Modul IBANKCORE", ha="center", fontsize=17, fontweight="bold", color=NAVY)
ax.text(8.35, 7.72, "Core Banking Multi-Modul & Sistem di Sekitarnya", ha="center", fontsize=10.5, color=GREY)

box(ax, 0.45, 6.6, 12.8, 1.1, "", fc="#F5F8FC", ec=BLUE, lw=1.6, radius=0.03)
ax.text(0.75, 7.65, "Channel Layer", fontsize=9.5, fontweight="bold", color=BLUE, va="top")

channels = ["BDS /\nAppClient", "ATM / EDC", "Mobile &\nInternet Banking", "E-Channel /\nAPI Gateway"]
cx = 0.6
cw = 3.0
for i, c in enumerate(channels):
    box(ax, cx + i * (cw + 0.15), 6.65, cw, 0.75, c, fc=WHITE, ec=STEEL, tc=NAVY, fs=9.5)

arrow(ax, (6.75, 6.55), (6.75, 5.9), color=STEEL, style="<|-|>")

envelope_x, envelope_w = 0.5, 12.5
box(ax, envelope_x, 2.35, envelope_w, 3.5, "", fc="#F5F8FC", ec=BLUE, lw=1.6, radius=0.03)
ax.text(0.85, 5.82, "IBANKCORE  (Core Banking System)", fontsize=12, fontweight="bold", color=BLUE, va="top")

modules = [
    "Enterprise", "Funding", "Accounting",
    "Kas & Vault\n(Teller/ATM)", "Internal\nAccount", "Customer"
]
switching_label = "Switching-CGS\n(Akses DB)"
mw, mh = 1.42, 1.15
gap = 0.14
row_w = (len(modules) + 1) * mw + len(modules) * gap
start_x = envelope_x + (envelope_w - row_w) / 2
y_mod = 4.15
for i, m in enumerate(modules):
    box(ax, start_x + i * (mw + gap), y_mod, mw, mh, m, fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9)

# Switching-CGS digambar sebagai bagian dari IBANKCORE (aplikasi ketiga, lihat Bagian 2.5),
# bukan sistem sekitar eksternal — tapi tetap ditandai beda (gold + garis putus-putus)
# karena aksesnya langsung ke DB, bukan lewat lapisan aplikasi seperti modul lain.
x_switch = start_x + len(modules) * (mw + gap)
box(ax, x_switch, y_mod, mw, mh, switching_label, fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=8.5)

db_cylinder(ax, 0.75, 2.65, 11.85, 0.85, "Shared Data Layer  —  Oracle", fc=NAVY, ec=NAVY, tc=WHITE, fs=10.5)

for i in range(len(modules)):
    xc = start_x + i * (mw + gap) + mw / 2
    arrow(ax, (xc, y_mod), (xc, 3.5), color=STEEL, lw=1.3)

xc_switch = x_switch + mw / 2
arrow(ax, (xc_switch, y_mod), (xc_switch, 3.5), color=ACCENT, lw=1.3, ls="--")

# 3rd Party Service — di sisi kanan IBANKCORE, satu garis koneksi saja ke IBANKCORE
tp_x, tp_w = envelope_x + envelope_w + 0.7, 3.0
tp_bottom, tp_height = 2.35, 3.7
box(ax, tp_x, tp_bottom, tp_w, tp_height, "", fc="#EAF5EF", ec=GREEN, lw=1.6, radius=0.03)
ax.text(tp_x + 0.3, tp_bottom + tp_height - 0.15, "3rd Party Service", fontsize=9.5, fontweight="bold", color=GREEN, va="top")

tp_items = ["PGC", "QRIS Provider", "Bank"]
tp_item_w, tp_item_h = 2.4, 0.95
tp_item_gap = 0.15
tp_item_x = tp_x + (tp_w - tp_item_w) / 2
tp_item_top = tp_bottom + tp_height - 0.5
for i, label in enumerate(tp_items):
    y = tp_item_top - (i + 1) * tp_item_h - i * tp_item_gap
    box(ax, tp_item_x, y, tp_item_w, tp_item_h, label, fc=WHITE, ec=GREEN, tc=NAVY, fs=9.5)

arrow(ax, (tp_x, tp_bottom + tp_height / 2), (envelope_x + envelope_w, tp_bottom + tp_height / 2), color=GREEN, style="<|-|>")

# External Systems Layer (selebar IBANKCORE): Feeder SAP (pull dari DB), Cut-off/Cleansing,
# DWH, Reporting Service — kotak independen tanpa garis relasi antar-sesama.
# Feeder SAP -> SAP (sistem tujuan feed) digambar terpisah di baris paling bawah.
# Laporan ke Regulator berasal dari kotak External Systems Layer (bukan dari sub-servicenya),
# sedangkan Dashboard tetap disuplai dari DWH.
ext_x, ext_w = envelope_x, envelope_w
ext_bottom, ext_height = 1.05, 1.1
box(ax, ext_x, ext_bottom, ext_w, ext_height, "", fc="#FCEFDA", ec=ACCENT, lw=1.4, radius=0.03)
ax.text(0.75, 2.08, "External Systems Layer", fontsize=9.5, fontweight="bold", color=ACCENT, va="top")

ext_items = [
    "Feeder SAP\n(Pull dari DB)",
    "Cut-off &\nCleansing Service",
    "DWH\n(Data Warehouse)",
    "Reporting Service",
]
eb_w, eb_h = 2.7, 0.55
eb_gap = 0.3
eb_row_w = len(ext_items) * eb_w + (len(ext_items) - 1) * eb_gap
eb_start_x = ext_x + (ext_w - eb_row_w) / 2
eb_y = 1.25
eb_xs = []
for i, label in enumerate(ext_items):
    x = eb_start_x + i * (eb_w + eb_gap)
    eb_xs.append(x)
    box(ax, x, eb_y, eb_w, eb_h, label, fc=WHITE, ec=ACCENT, tc=NAVY, fs=9)

arrow(ax, (6.75, ext_bottom + ext_height), (6.75, 2.65), color=ACCENT, ls="--")

feeder_center_x = eb_xs[0] + eb_w / 2

sap_w, sap_h = 2.6, 0.6
sap_x, sap_y = feeder_center_x - sap_w / 2, 0.15
box(ax, sap_x, sap_y, sap_w, sap_h, "SAP", fc=WHITE, ec=ACCENT, tc=NAVY, fs=9.5)
arrow(ax, (feeder_center_x, eb_y), (feeder_center_x, sap_y + sap_h), color=ACCENT)

report_items = [
    "Regulator\nOJK / BI Reporting",
    "Dashboard",
]
rb_w, rb_h = 4.3, 0.6
rb_gap = 0.3
rb_start_x = sap_x + sap_w + 0.4
rb_y = 0.15
for i, label in enumerate(report_items):
    x = rb_start_x + i * (rb_w + rb_gap)
    box(ax, x, rb_y, rb_w, rb_h, label, fc=WHITE, ec=GREY, tc=NAVY, fs=9.2)
    xc = x + rb_w / 2
    arrow(ax, (xc, ext_bottom), (xc, rb_y + rb_h), color=GREY)

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

# =====================================================================
# DIAGRAM 6 — Sistem Sekitar Khusus PT Pos: PGC & CMS
# (berdasarkan konfirmasi bisnis, bukan hasil verifikasi kode)
# =====================================================================
fig, ax = new_fig(13, 7.2)
ax.text(6.5, 6.75, "Sistem Sekitar Khusus PT Pos: PGC & CMS", ha="center", fontsize=16, fontweight="bold", color=NAVY)
ax.text(6.5, 6.32, "Penyaluran PGC (Pos Giro Cash) melalui CMS Korporat & Kanal PT Pos", ha="center", fontsize=10, color=GREY)

ax.text(6.5, 5.85, "Catatan: berdasarkan konfirmasi bisnis — PGC & CMS tidak ditemukan pada eksplorasi source code core/enterprise", ha="center", va="center", fontsize=7.5, color=ACCENT, style="italic")

box(ax, 0.5, 4.35, 2.9, 1.1, "Instansi Pemerintah /\nHimbara (Penyalur PGC)", fc=BG_CARD, ec=BLUE_LIGHT, tc=NAVY, fs=9.3)
box(ax, 4.15, 4.35, 2.9, 1.1, "CMS\n(Cash Management System)", fc="#FCEFDA", ec=ACCENT, tc=NAVY, fs=10)
arrow(ax, (3.4, 4.9), (4.15, 4.9), color=STEEL, lw=1.8)
ax.text(3.775, 5.65, "instruksi\npenyaluran", ha="center", va="center", fontsize=7.6, color=GREY, style="italic")

box(ax, 7.8, 4.35, 4.2, 1.1, "IBANKCORE (PT Pos)\nProses Penyaluran PGC", fc=NAVY, ec=NAVY, tc=WHITE, fs=10)
arrow(ax, (7.05, 4.9), (7.8, 4.9), color=STEEL, lw=1.8)

channels = [
    ("Loket / Counter\n(Tunai)", 0.7),
    ("QRIS\n(Non-Tunai)", 4.85),
    ("Kredit Rekening\n(Tabungan)", 9.0),
]
for label, x in channels:
    box(ax, x, 2.1, 3.0, 1.0, label, fc="#F5F8FC", ec=STEEL, tc=NAVY, fs=9.5)
    xc_top = x + 1.5
    arrow(ax, (9.9, 4.35), (xc_top, 3.1), color=STEEL, lw=1.4)

box(ax, 3.6, 0.35, 5.8, 1.0, "Penerima Manfaat PGC", fc=BG_CARD, ec=GREEN, tc=NAVY, fs=10)
for label, x in channels:
    xc = x + 1.5
    arrow(ax, (xc, 2.1), (6.5, 1.35), color=GREEN, lw=1.4)

fig.savefig(os.path.join(OUT_DIR, "06_pgc_cms.png"), dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

print("done:", OUT_DIR)
