# IBANKCORE Training — Materi & Slide (Markdown Source)

Paket ini berisi sumber konten (Markdown) untuk materi training IBANKCORE beserta
script generator yang mengubahnya menjadi `.docx` (dokumen) dan `.pptx` (slide),
dengan desain yang konsisten setiap kali di-generate ulang.

## Struktur Folder

```
ibankcore-training/
├── materi_training_ibankcore.md      # Sumber isi dokumen (Word)
├── slides_training_ibankcore.md      # Sumber isi slide (PowerPoint), YAML per-slide
├── diagrams/                         # 4 diagram PNG dipakai oleh kedua sumber di atas
│   ├── 01_arsitektur_ibankcore.png
│   ├── 02_alur_double_entry.png
│   ├── 03_integrasi_sistem_sekitar.png
│   └── 04_proses_setor_tunai.png
├── scripts/
│   ├── md_to_docx.js                 # Parser markdown → docx (docx-js)
│   ├── md_to_pptx.js                 # Parser YAML-per-slide → pptx (pptxgenjs)
│   └── make_diagrams.py              # Generator 4 diagram PNG di folder diagrams/
├── dist/                             # Hasil generate terakhir (boleh dihapus/di-gitignore)
│   ├── materi_training_ibankcore.docx
│   └── materi_training_ibankcore.pptx
└── package.json
```

## Instalasi

Butuh Node.js ≥ 18.

```bash
cd ibankcore-training
npm install
```

Dependency: `docx`, `pptxgenjs`, `js-yaml`, `image-size` (semua murni npm, tidak butuh binary tambahan untuk proses generate).

## Cara Pakai

### 1. Edit konten
Edit langsung `materi_training_ibankcore.md` (untuk dokumen) atau
`slides_training_ibankcore.md` (untuk slide) dengan text editor apa pun.

### 2. Generate ulang

```bash
npm run build          # generate docx + pptx sekaligus
npm run build:docx     # hanya docx
npm run build:pptx     # hanya pptx
```

Hasil akan ditulis ke `dist/materi_training_ibankcore.docx` dan `dist/materi_training_ibankcore.pptx`.

### 3. (Opsional) QA visual
Kalau di mesin lokal Anda ada LibreOffice (`soffice`) dan `pdftoppm` (Poppler),
Anda bisa render ke gambar untuk cek visual sebelum membagikan:

```bash
soffice --headless --convert-to pdf dist/materi_training_ibankcore.pptx
pdftoppm -jpeg -r 100 materi_training_ibankcore.pdf slide
```

Ini murni opsional — tidak dibutuhkan agar `npm run build` berhasil.

---

## Format Sumber

### `materi_training_ibankcore.md` (dokumen)

Markdown standar dengan sedikit front matter di awal file untuk halaman cover:

```md
---
title: Materi Training
subtitle: Sistem Core Banking IBANKCORE
tagline: Modul Accounting, Funding, Treasury & Interaksi dengan Aplikasi Sekitar
org: Ihsan Solusi
note: Overview / Garis Besar — Audiens Teknis & Bisnis
header: IBANKCORE — Materi Training
---

# 1. Judul Bagian       -> Heading 1 (mulai halaman/section baru secara visual)
## 1.1 Sub-bagian       -> Heading 2
### 1.1.1 Sub-sub       -> Heading 3

Paragraf biasa ditulis sebagai teks polos.

- Bullet list
- Item lain

| Kolom 1 | Kolom 2 |
|---|---|
| Isi | Isi |

![Keterangan gambar](diagrams/nama_file.png)
```

Aturan penting:
- Path gambar relatif terhadap lokasi file `.md` itu sendiri.
- Baris pertama tabel dianggap header.
- Satu paragraf = satu baris (jangan menulis paragraf multi-baris dengan line break manual di tengah kalimat).

### `slides_training_ibankcore.md` (slide)

Bukan markdown biasa — setiap slide adalah blok YAML, dipisahkan baris `===`.
Setiap blok wajib punya `layout:` yang menentukan bagaimana script merender slide tsb.

Layout yang tersedia (didukung oleh `md_to_pptx.js` saat ini):

| Layout | Kegunaan | Field utama |
|---|---|---|
| `title` | Slide judul (cover) | `kicker`, `title`, `subtitle`, `footer` |
| `cards` | Grid 3×2 kartu bernomor (agenda) | `kicker`, `title`, `cards: [{num, heading, text}]` |
| `image` | Slide gambar penuh (diagram) | `kicker`, `title`, `image` (path relatif) |
| `table-grid` | Grid 2 kolom kartu ringkas | `kicker`, `title`, `rows: [[judul, deskripsi], ...]` |
| `numbered-cards` | 4 kartu bernomor sejajar | `kicker`, `title`, `intro`, `cards: [{heading, text}]` |
| `two-column` | Dua panel kiri/kanan (paling fleksibel) | `left`, `right` — lihat sub-field di bawah |
| `summary` | Slide penutup gelap dengan poin bernomor | `kicker`, `title`, `points`, `discussion_heading`, `discussion` |

Sub-field yang didukung di dalam `left:` / `right:` pada layout `two-column`:
- `panel: dark|light` — gaya latar panel (kosongkan untuk transparan/putih)
- `heading`, `intro` — judul & kalimat pembuka panel
- `bullets: [...]` — daftar poin bertitik
- `items: [{label, text}]` — daftar berlabel tebal (mis. nama tabel)
- `rows: [[a, b], ...]` — mini-tabel dua kolom di dalam panel
- `list_cards: [...]` — daftar kartu putih bersusun (mis. daftar CASH_POINT)
- `drcr: ["DR / Debit", "CR / Kredit"]` — dua kotak besar sejajar (khusus slide Accounting)
- `note: "..."` — kotak catatan italic di bagian bawah panel
- `panel_top` / `panel_bottom` — dua panel bertumpuk dalam satu kolom (dipakai di slide Kliring)

Contoh satu slide bertipe `image`:

```yaml
layout: image
kicker: Bagian 1
title: Arsitektur Modul IBANKCORE
image: diagrams/01_arsitektur_ibankcore.png
```

## Menambah Slide / Layout Baru

1. Tambahkan blok baru di `slides_training_ibankcore.md`, dipisah `===` dari blok sebelum/sesudahnya.
2. Kalau memakai layout yang sudah ada, cukup isi field-nya sesuai tabel di atas.
3. Kalau butuh layout baru, tambahkan cabang `else if (sl.layout === "nama-layout") { ... }`
   di `scripts/md_to_pptx.js` (lihat pola cabang yang sudah ada sebagai contoh).

## Palet Warna & Font (untuk konsistensi kalau menambah elemen baru)

| Token | Hex | Dipakai untuk |
|---|---|---|
| Navy Dark | `12233F` | Background gelap, judul |
| Navy | `1E2761` | Aksen panel gelap sekunder |
| Ice | `CADCFC` | Teks di atas latar gelap |
| Gold | `C0862B` | Aksen/kicker/angka |
| Grey Text | `44546A` | Teks body di atas latar terang |
| Card BG | `EAF1F8` | Latar kartu terang |
| Light BG | `F5F8FC` | Latar kartu/panel sangat terang |

Font: judul `Cambria` (serif), body `Calibri` (sans) — keduanya termasuk font "safe" yang
konsisten antara preview LibreOffice dan Microsoft Office asli.

## Diagram

Empat file di `diagrams/` dibuat dengan Python (`matplotlib`) via `scripts/make_diagrams.py`,
bukan hasil screenshot atau gambar generatif — sehingga mudah diubah ulang secara terprogram.

Untuk regenerate (butuh Python 3 + `matplotlib`):

```bash
cd ibankcore-training
python3 scripts/make_diagrams.py
```

Script ini menimpa ulang keempat file di `diagrams/`. Edit langsung isi Python di dalamnya
(posisi kotak, warna, label teks) untuk menyesuaikan diagram, lalu jalankan lagi.
