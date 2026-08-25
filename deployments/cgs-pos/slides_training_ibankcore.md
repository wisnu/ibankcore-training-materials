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
    text: Feeder SAP & pelaporan regulator
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
    text: Deposito, QRIS, VA, Corporate, dsb.
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
title: Enam Modul Utama
rows:
  - ["Enterprise", "Struktur organisasi, user & hak akses, otorisasi, audit trail"]
  - ["Funding", "Produk pendanaan/simpanan (tabungan, giro, deposito)"]
  - ["Accounting", "Pencatatan double-entry & buku besar"]
  - ["Kas & Vault (Teller/ATM)", "Kas fisik: teller, vault, ATM, sundry"]
  - ["Internal Account", "Rekening internal bank (GL, suspense)"]
  - ["Customer", "Data induk nasabah (CIF)"]
===
layout: two-column
kicker: Bagian 1
title: "Tiga Aplikasi: Core, Enterprise & Switching-CGS"
left:
  panel: dark
  heading: "Core & Enterprise"
  intro: "Python, akses DB lewat lapisan aplikasi sendiri:"
  bullets:
    - "Enterprise — platform/administratif (user, cabang, otorisasi)"
    - "Core — mesin transaksi & produk perbankan"
right:
  panel: light
  heading: "Switching-CGS (Go)"
  intro: "Modernisasi switching dari Python legacy:"
  bullets:
    - "Microservice: core, jalin/QRIS, bca, topup, dll — BL2 (TCP) & gRPC"
    - "Redis untuk job-queue/idempotency, deploy Docker/Kubernetes"
    - "Akses langsung ke Oracle — skema sama persis dengan core/enterprise"
===
layout: two-column
kicker: Bagian 1
title: "3rd Party Service & Internal Support Layer"
left:
  panel: dark
  heading: "3rd Party Service"
  intro: "Terhubung ke IBANKCORE via satu jalur dua arah:"
  bullets:
    - "PGC (Bansos) — instansi pemerintah/himbara penyalur"
    - "Jalin (QRIS) — termasuk rekonsiliasi manual berbasis file"
    - "Bank — mitra transfer/switching antar bank"
right:
  panel: light
  heading: "Internal Support Layer"
  intro: "Layanan pendukung internal, di luar envelope IBANKCORE:"
  bullets:
    - "Feeder SAP — pull data akuntansi ke SAP"
    - "Cut-off & Cleansing Service — selaras dengan EOD/BOD"
    - "DWH — sumber data untuk Dashboard"
    - "Reporting Service — pelaporan ke Regulator OJK/BI"
===
layout: image
kicker: Bagian 1
title: Struktur Organisasi — Wilayah, Cabang & Atribut Kantor
image: diagrams/05_struktur_organisasi.png
===
layout: two-column
kicker: Bagian 1
title: Kaitan Struktur Cabang dengan COA & Neraca
left:
  panel: dark
  heading: "Chart of Accounts (COA)"
  intro: "Bagaimana akun COA menyatu dengan cabang:"
  bullets:
    - "Account (COA master) — daftar akun, tanpa dimensi cabang"
    - "Account Instance — akun COA diinstansiasi per cabang & mata uang"
    - "GL Account (saldo/posting) menempel ke Account Instance, bukan ke Account master"
right:
  panel: light
  heading: "Neraca & Dimensi Cost Center"
  intro: "Penyusunan laporan & dimensi biaya/pendapatan:"
  bullets:
    - "Neraca disusun per cabang maupun konsolidasi (parameter cabang opsional)"
    - "Wilayah bukan dimensi langsung GL — agregasi per wilayah dilakukan via Cabang → Area Cabang"
    - "Dimensi cost center pada jurnal = Kode RC (Project), bukan Departemen"
===
layout: two-column
kicker: Bagian 1
title: Isolasi Akses — Cabang & Departemen
left:
  panel: dark
  heading: "Isolasi Cabang"
  intro: "Gerbang akses aktif per user, 3 mode:"
  bullets:
    - "Semua — akses ke seluruh cabang"
    - "Tunggal — hanya cabang milik user sendiri"
    - "Parsial — hanya cabang yang terdaftar di daftar 'cabang diizinkan' + cabang sendiri"
right:
  panel: light
  heading: "Isolasi Departemen"
  intro: "Konsep serupa, konstruksi berbeda:"
  bullets:
    - "Daftar 'departemen diizinkan' terhubung ke data karyawan, bukan langsung ke user"
    - "Lebih banyak dipakai untuk administrasi/pemilihan departemen (HR), bukan gerbang akses transaksi"
    - "Mode akses meminjam pengaturan mode akses cabang milik user — tidak punya mode tersendiri"
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
    - label: "JOURNAL / JOURNALITEM"
      text: "tabel inti ledger, baris mutasi DR/CR"
    - label: "dailybalancerekening"
      text: "saldo harian, direkonsiliasi terhadap mutasi"
right:
  heading: Mengapa Penting
  bullets:
    - "Menjamin keseimbangan (balance) setiap transaksi secara atomik"
    - "Menjadi dasar rekonsiliasi saldo & deteksi anomali/duplikasi"
    - "Mendukung jejak audit (audit trail) untuk kebutuhan OJK/BI & auditor eksternal"
    - "Menjadi sumber data bagi Feeder SAP untuk konsolidasi keuangan"
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
  note: "Kas & Vault ⇄ Treasury menjaga likuiditas bank. Bukan 'Cash Management System' portal korporat — ini kas fisik cabang."
===
layout: image
kicker: Bagian 5
title: Integrasi dengan Sistem Sekitar
image: diagrams/03_integrasi_sistem_sekitar.png
===
layout: two-column
kicker: Bagian 5
title: Feeder SAP & Pelaporan
left:
  panel: dark
  heading: "Feeder SAP"
  intro: "Integrasi akuntansi eksternal secara batch:"
  bullets:
    - "Feeder SAP mengambil (pull) data langsung dari DB Core secara berkala"
    - "Bukan push/event-driven — Core tidak mengirim data secara aktif"
    - "Melengkapi pencatatan GL internal pada modul Accounting"
right:
  panel: light
  heading: "Pelaporan Regulator & Audit"
  intro: "Kebutuhan kepatuhan & audit eksternal:"
  bullets:
    - "Pelaporan berkala ke OJK/BI (laporan keuangan, transaksi, kepatuhan)"
    - "Jejak data yang tertelusur untuk kebutuhan audit eksternal"
===
layout: two-column
kicker: Bagian 5
title: Payment Switching — Akses Langsung DB
left:
  panel: dark
  heading: "Payment Switching"
  intro: "Berbeda dari kanal lain (QRIS, host-to-host, REST API):"
  bullets:
    - "Akses langsung ke basis data Core, bukan lewat lapisan aplikasi/API"
    - "Konfigurasi di level infrastruktur/database (mis. database link)"
    - "Terkonfirmasi: skema DB switching sama persis dengan skema core/enterprise"
right:
  panel: light
  heading: "Implikasi Tata Kelola"
  intro: "Perlu perhatian ekstra dibanding integrasi berbasis API:"
  bullets:
    - "Melewati lapisan validasi aplikasi Core"
    - "Perubahan skema database berpotensi berdampak langsung ke switching"
    - "Tidak terikat kontrak API yang terversi seperti kanal lain"
===
layout: image
kicker: Bagian 5
title: "Sistem Sekitar Khusus PT Pos: PGC & CMS"
image: diagrams/06_pgc_cms.png
===
layout: two-column
kicker: Bagian 5
title: "PGC & CMS (Khusus PT Pos)"
left:
  panel: dark
  heading: "CMS (Cash Management System)"
  intro: "Kanal digital untuk institusi/korporat:"
  bullets:
    - "Instansi pemerintah/himbara kirim instruksi penyaluran massal (bulk disbursement)"
    - "Berbeda dari modul internal 'Kas & Vault' — CMS murni kanal eksternal, bukan kas fisik"
right:
  panel: light
  heading: "PGC (Pos Giro Cash)"
  intro: "PT Pos sebagai agen penyalur ke penerima manfaat:"
  bullets:
    - "Loket/Counter (tunai), QRIS (non-tunai), atau kredit rekening tabungan"
    - "Metode pencairan tergantung program PGC terkait"
  note: "Berdasarkan konfirmasi bisnis — PGC & CMS tidak ditemukan pada eksplorasi source code core/enterprise."
===
layout: two-column
kicker: Bagian 5
title: "Verifikasi Identitas & OTP"
left:
  panel: dark
  heading: "API KTP"
  intro: "Verifikasi identitas nasabah:"
  bullets:
    - "Validasi data kependudukan"
    - "Dipanggil aplikasi switching saat diperlukan"
right:
  panel: light
  heading: "SMS API"
  intro: "Otentikasi transaksi tambahan:"
  bullets:
    - "Pengiriman OTP (One-Time Password)"
    - "Melengkapi verifikasi di luar PIN"
===
layout: image
kicker: Bagian 6
title: Contoh Proses Bisnis — Setor Tunai
image: diagrams/04_proses_setor_tunai.png
===
layout: two-column
kicker: Bagian 6
title: Pindah Buku
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
  heading: "Dibanding Setor Tunai"
  intro: "Perbedaan utama dengan proses Setor Tunai:"
  bullets:
    - "Tidak melibatkan CASH_POINT (teller/vault/ATM)"
    - "Kedua mutasi (DR & CR) terjadi dalam satu bank yang sama"
    - "Tidak ada pertukaran kas fisik dengan nasabah"
===
layout: table-grid
kicker: Bagian 7
title: "Produk & Layanan Tambahan (1/2)"
rows:
  - ["Deposito", "Bunga/bagi hasil, pencairan awal, perubahan nisbah"]
  - ["Teller & Layanan Counter", "Alur transaksi front office via CASH_POINT"]
  - ["QRIS & Virtual Account", "Pembayaran QR & VA, settlement/matching batch"]
  - ["Host-to-Host & REST API", "Integrasi sistem eksternal berbasis JSON"]
  - ["Corporate Banking", "Layanan & otorisasi bertingkat nasabah korporat"]
  - ["Rekening & Manajemen Nasabah", "Siklus hidup CIF, pembukaan-penutupan rekening"]
===
layout: table-grid
kicker: Bagian 7
title: "Produk & Layanan Tambahan (2/2)"
rows:
  - ["Biller", "Pembayaran tagihan pihak ketiga (listrik, telekomunikasi, dsb.)"]
  - ["Feeder SAP / GL Eksternal", "Posting akuntansi batch untuk konsolidasi korporat"]
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
  - "Integrasi sistem sekitar (Feeder SAP, QRIS, host-to-host/REST) & produk tambahan (Corporate Banking, Biller)"
  - "Batch EOD/BOD, disaster recovery, maker-checker, user security & biometrik — lapisan operasional dan kontrol keamanan kunci"
discussion_heading: "Bahan Diskusi"
discussion: "Modul mana yang paling relevan untuk didalami lebih lanjut?   •   Bagaimana penerapan maker-checker & EOD/BOD saat ini?"
