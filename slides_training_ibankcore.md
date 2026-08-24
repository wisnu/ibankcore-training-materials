layout: title
kicker: Training Core Banking
title: Sistem IBANKCORE
subtitle: |
  Modul Accounting · Funding · Treasury
  dan Interaksi dengan Aplikasi Sekitar
footer: "Ihsan Solusi  |  Overview untuk audiens teknis & bisnis"
===
layout: cards
kicker: Agenda
title: Apa yang Akan Kita Bahas
cards:
  - num: "01"
    heading: Arsitektur IBANKCORE
    text: Modul & sistem sekitar
  - num: "02"
    heading: Modul Accounting
    text: Double-entry ledger
  - num: "03"
    heading: Modul Funding
    text: Produk simpanan nasabah
  - num: "04"
    heading: Treasury / Kas & Vault
    text: CASH_POINT & likuiditas
  - num: "05"
    heading: Integrasi Sistem Sekitar
    text: Kafka, SKN/RTGS/BI-FAST
  - num: "06"
    heading: Contoh Proses Bisnis
    text: Setor Tunai & Pindah Buku
===
layout: cards
kicker: Agenda (Lanjutan)
title: Materi Tambahan
cards:
  - num: "07"
    heading: Produk & Layanan Tambahan
    text: Deposito, Kliring, QRIS, VA, Corporate, dsb.
  - num: "08"
    heading: Batch & Kontinuitas Layanan
    text: EOD/BOD, backup & disaster recovery
  - num: "09"
    heading: Keamanan & Audit Lanjutan
    text: Maker-checker, security, biometrik
===
layout: image
kicker: Bagian 1
title: Arsitektur Modul IBANKCORE
image: diagrams/01_arsitektur_ibankcore.png
===
layout: table-grid
kicker: Bagian 1
title: Delapan Modul Utama
rows:
  - ["Funding", "Produk pendanaan/simpanan (tabungan, giro, deposito)"]
  - ["Financing", "Pembiayaan, termasuk skema syariah (Murabahah, Ijarah, Kafalah)"]
  - ["Accounting", "Pencatatan double-entry & buku besar"]
  - ["Kas & Vault (Teller/ATM)", "Kas fisik: teller, vault, ATM, sundry"]
  - ["Remittance", "Transfer antar bank: SKN, RTGS, BI-FAST"]
  - ["Internal Account", "Rekening internal bank (GL, suspense)"]
  - ["Customer", "Data induk nasabah (CIF)"]
  - ["Enterprise", "Parameter, otorisasi, audit trail lintas modul"]
===
layout: two-column
kicker: Bagian 2
title: Modul Accounting — Prinsip Dasar
left:
  panel: dark
  heading: Double-Entry Bookkeeping
  intro: "Setiap transaksi selalu menghasilkan pasangan mutasi yang seimbang:"
  drcr: ["DR / Debit", "CR / Kredit"]
  items:
    - label: "TRANSACTION_DETAILS"
      text: "tabel inti mutasi, atribut MUTATION_TYPE (DR/CR)"
    - label: "dailybalancerekening"
      text: "saldo harian, direkonsiliasi terhadap mutasi"
    - label: "CTI lintas skema"
      text: "CORE_TRX, FUNDING, CASHMGT, REMIT"
right:
  heading: Mengapa Penting
  bullets:
    - "Menjamin keseimbangan (balance) setiap transaksi secara atomik"
    - "Menjadi dasar rekonsiliasi saldo & deteksi anomali/duplikasi"
    - "Mendukung jejak audit (audit trail) untuk kebutuhan OJK/BI & auditor eksternal"
    - "Menjadi sumber event bagi sistem hilir melalui outbox pattern"
===
layout: image
kicker: Bagian 2
title: Alur Pencatatan Transaksi
image: diagrams/02_alur_double_entry.png
===
layout: numbered-cards
kicker: Bagian 3
title: Modul Funding
intro: "Mengelola produk pendanaan / simpanan nasabah — sumber utama Dana Pihak Ketiga (DPK)."
cards:
  - heading: Pembukaan Rekening
    text: "Tabungan, giro, deposito — termasuk validasi identitas via modul Customer"
  - heading: Bagi Hasil / Bunga
    text: "Perhitungan sesuai jenis produk, konvensional maupun syariah"
  - heading: Mutasi Transaksi
    text: "Setoran, penarikan, pemindahbukuan — tercatat via modul Accounting"
  - heading: Keterkaitan Kas & Vault
    text: "Transaksi tunai berinteraksi dengan CASH_POINT (teller/ATM)"
===
layout: two-column
kicker: Bagian 4
title: Treasury / Kas & Vault (Teller/ATM)
left:
  panel: light
  heading: Abstraksi CASH_POINT
  intro: "Menyeragamkan berbagai titik penyimpanan / perputaran kas dalam satu model:"
  list_cards: ["Laci Teller", "Vault (Khazanah) Cabang", "Mesin ATM", "Rekening Sundry"]
right:
  heading: Fungsi Treasury
  bullets:
    - "Pengelolaan likuiditas harian & posisi kas bank"
    - "Rekonsiliasi kas fisik terhadap catatan sistem"
    - "Interaksi dengan Remittance untuk settlement lintas bank"
  note: "Kas & Vault ⇄ Treasury ⇄ Remittance menjaga likuiditas & settlement bank. Bukan 'Cash Management System' portal korporat — ini kas fisik cabang."
===
layout: image
kicker: Bagian 5
title: Integrasi dengan Sistem Sekitar
image: diagrams/03_integrasi_sistem_sekitar.png
===
layout: two-column
kicker: Bagian 5
title: Kliring, Event Streaming & Pelaporan
left:
  heading: Kliring & Pembayaran Antar Bank
  rows:
    - ["SKN", "Kliring nasional, nilai relatif kecil, proses batch"]
    - ["RTGS", "Transfer bernilai besar, real-time gross settlement"]
    - ["BI-FAST", "Transfer real-time nilai kecil-menengah, tersedia 24/7"]
right:
  panel_top:
    panel: dark
    heading: "Event Streaming — Kafka"
    text: "Pola transactional outbox menjamin event transaksi terpublikasi konsisten ke konsumen hilir (reporting, notifikasi, GL) — loose coupling tanpa akses langsung ke DB inti."
  panel_bottom:
    panel: light
    heading: "Pelaporan Regulator & Audit"
    text: "IBANKCORE mendukung pelaporan berkala ke OJK/BI serta menyediakan jejak data yang tertelusur untuk kebutuhan audit eksternal."
===
layout: image
kicker: Bagian 6
title: Contoh Proses Bisnis — Setor Tunai
image: diagrams/04_proses_setor_tunai.png
===
layout: two-column
kicker: Bagian 6
title: Pindah Buku & Konteks Syariah
left:
  panel: light
  heading: Pindah Buku
  intro: "Transfer antar rekening dalam bank yang sama:"
  bullets:
    - "Mutasi DR pada rekening sumber"
    - "Mutasi CR pada rekening tujuan"
    - "Terjadi secara atomik (bersamaan)"
    - "Tanpa melibatkan modul Kas & Vault (tidak ada kas fisik)"
right:
  panel: dark
  heading: "Konteks Syariah — PSAK 109"
  intro: "Sebagian produk Financing mengikuti prinsip syariah:"
  rows:
    - ["Murabahah", "Jual-beli dengan margin"]
    - ["Ijarah", "Sewa (leasing)"]
    - ["Kafalah", "Penjaminan (guarantee)"]
===
layout: table-grid
kicker: Bagian 7
title: "Produk & Layanan Tambahan (1/2)"
rows:
  - ["Deposito", "Bunga/bagi hasil, pencairan awal, perubahan nisbah"]
  - ["Modul Kliring", "Pencatatan warkat/instruksi kliring nasabah"]
  - ["Teller & Layanan Counter", "Alur transaksi front office via CASH_POINT"]
  - ["QRIS & Virtual Account", "Pembayaran QR & VA, settlement/matching batch"]
  - ["Host-to-Host & REST API", "Integrasi sistem eksternal berbasis JSON"]
  - ["Corporate Banking", "Layanan & otorisasi bertingkat nasabah korporat"]
===
layout: table-grid
kicker: Bagian 7
title: "Produk & Layanan Tambahan (2/2)"
rows:
  - ["Rekening & Manajemen Nasabah", "Siklus hidup CIF, pembukaan-penutupan rekening"]
  - ["Biller & Remittance", "Pembayaran tagihan pihak ketiga & transfer lintas bank/negara"]
  - ["Integrasi SAP/GL Eksternal", "Posting akuntansi batch untuk konsolidasi korporat"]
  - ["Dana Haji", "Produk simpanan/pembiayaan khusus dana haji"]
===
layout: two-column
kicker: Bagian 8
title: Batch Operasional & Kontinuitas Layanan
left:
  panel: dark
  heading: "Batch Process & EOD/BOD"
  intro: "Siklus operasional harian cabang:"
  bullets:
    - "End-of-Day (EOD): tutup hari, rekonsiliasi saldo"
    - "Begin-of-Day (BOD): branch open, persiapan hari kerja baru"
    - "Prasyarat konsistensi data antar hari & pelaporan regulator"
right:
  panel: light
  heading: "Backup & Disaster Recovery"
  intro: "Menjaga kontinuitas layanan (business continuity):"
  bullets:
    - "Backup database berjenjang (penuh & incremental)"
    - "Prosedur disaster recovery"
    - "Bagian dari kepatuhan ketahanan operasional perbankan"
===
layout: numbered-cards
kicker: Bagian 9
title: Keamanan, Otorisasi & Audit Lanjutan
intro: "Lapisan kontrol tambahan di luar hak akses dasar & audit trail (Bagian 6)."
cards:
  - heading: Maker-Checker / Otorisasi
    text: "Transaksi/perubahan data menunggu persetujuan (OtorEntri) sebelum efektif; riwayat otorisasi tersimpan sebagai jejak audit tersendiri"
  - heading: User Security & Access Control
    text: "Validasi keamanan data user, activity log, serta laporan hak akses per user/grup"
  - heading: Session & Block Management
    text: "Kedaluwarsa sesi login & pemblokiran otomatis setelah kondisi tertentu (mis. gagal login berulang)"
  - heading: Verifikasi Biometrik
    text: "Lapisan otentikasi tambahan di luar PIN/password untuk transaksi berisiko tinggi"
===
layout: summary
kicker: Ringkasan
title: Poin-Poin Kunci
points:
  - "IBANKCORE — dua aplikasi (core & enterprise) dengan lapisan data & pola integrasi yang konsisten"
  - "Accounting, Funding, Kas & Vault — pencatatan double-entry & Deposito sebagai contoh produk"
  - "Integrasi sistem sekitar (Kafka, SKN/RTGS/BI-FAST, QRIS, host-to-host/REST) & produk tambahan (Corporate, Biller, Dana Haji)"
  - "Batch EOD/BOD, disaster recovery, maker-checker, user security & biometrik — lapisan operasional dan kontrol keamanan kunci"
discussion_heading: "Bahan Diskusi"
discussion: "Modul mana yang paling relevan untuk didalami lebih lanjut?   •   Bagaimana penerapan maker-checker & EOD/BOD saat ini?"
