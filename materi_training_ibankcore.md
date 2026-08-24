---
title: Materi Training
subtitle: Sistem Core Banking IBANKCORE
tagline: Modul Accounting, Funding, Treasury & Interaksi dengan Aplikasi Sekitar
org: Ihsan Solusi
note: Overview / Garis Besar — Audiens Teknis & Bisnis
header: IBANKCORE — Materi Training
---

# 1. Pendahuluan

## 1.1 Tujuan Training

Sesi ini bertujuan memberikan pemahaman menyeluruh (overview) mengenai sistem core banking IBANKCORE, khususnya modul Accounting, Funding, dan Treasury (Cash Management), serta bagaimana ketiga modul tersebut berinteraksi satu sama lain maupun dengan aplikasi/sistem di sekitarnya (channel, sistem kliring, regulator, dan platform integrasi).

Materi disusun untuk audiens campuran — baik yang berlatar belakang teknis (developer, DBA) maupun bisnis (business analyst, product owner, auditor) — sehingga penjelasan konsep akan diberikan pada level arsitektur dan proses bisnis, sebelum masuk ke detail data model bila diperlukan.

## 1.2 Ruang Lingkup

- Arsitektur modul IBANKCORE secara keseluruhan (Funding, Financing, Accounting, Cash Management, Remittance, Internal Account, Customer, Enterprise).
- Prinsip pencatatan transaksi (double-entry ledger) pada modul Accounting.
- Konsep dasar modul Funding (produk pendanaan/simpanan).
- Konsep Treasury / Cash Management, termasuk abstraksi CASH_POINT (teller, vault, ATM, sundry).
- Struktur organisasi cabang & departemen, serta manajemen user dan hak akses (role, limit otorisasi).
- Interaksi dengan sistem sekitar: event streaming (Kafka), kliring & pembayaran (SKN, RTGS, BI-FAST), serta pelaporan regulator (OJK/BI).
- Contoh proses bisnis end-to-end: Setor Tunai dan Pindah Buku.
- Konteks regulasi & syariah (PSAK 109) yang relevan dengan sebagian produk pembiayaan.

## 1.3 Konteks Lingkungan

IBANKCORE beroperasi pada lingkungan perbankan yang diatur (regulated), tunduk pada ketentuan OJK/BI serta audit eksternal. Sistem berjalan di atas basis data Oracle dan PostgreSQL, dengan kode sumber dikelola pada instance GitLab internal (self-hosted).

# 2. Arsitektur Modul IBANKCORE

IBANKCORE adalah sistem core banking multi-modul. Setiap modul menangani domain bisnis tertentu namun berbagi lapisan data (shared ledger) dan pola integrasi yang konsisten. Diagram berikut menggambarkan posisi setiap modul beserta kanal dan sistem sekitarnya.

![Gambar 2.1 — Arsitektur Modul IBANKCORE](diagrams/01_arsitektur_ibankcore.png)

## 2.1 Modul-Modul Utama

| Modul | Fungsi Utama |
|---|---|
| Funding | Produk pendanaan/simpanan nasabah (tabungan, giro, deposito). |
| Financing | Produk pembiayaan, termasuk skema syariah (Murabahah, Ijarah, Kafalah). |
| Accounting | Pencatatan transaksi double-entry, buku besar (GL), saldo harian. |
| Cash Management | Pengelolaan kas fisik: teller, vault, ATM, sundry (CASH_POINT). |
| Remittance | Transfer dana antar bank: SKN, RTGS, BI-FAST. |
| Internal Account | Rekening internal bank (GL internal, suspense, sundry account). |
| Customer | Data induk nasabah (CIF), identitas, profil risiko. |
| Enterprise | Fungsi lintas modul: parameter, otorisasi, audit trail. |

## 2.2 Lapisan Data

Seluruh modul berbagi lapisan data pada Oracle dan/atau PostgreSQL. Pemisahan skema dilakukan dengan pola Class Table Inheritance (CTI) lintas skema — misalnya CORE_TRX, FUNDING, CASHMGT, REMIT — agar setiap modul dapat memiliki atribut spesifik tanpa mengorbankan konsistensi struktur transaksi inti.

## 2.3 Kanal & Sistem Sekitar

Transaksi dapat masuk melalui berbagai kanal (teller/cabang, ATM/EDC, mobile & internet banking, maupun API gateway). Di sisi hilir, IBANKCORE terhubung dengan sistem kliring/pembayaran (SKN/RTGS/BI-FAST), kebutuhan pelaporan regulator (OJK/BI), serta kebutuhan audit eksternal.

# 3. Modul Accounting

Modul Accounting adalah jantung pencatatan finansial IBANKCORE. Prinsip utamanya adalah double-entry bookkeeping — setiap transaksi selalu menghasilkan pasangan mutasi debit (DR) dan kredit (CR) yang seimbang.

## 3.1 Struktur Pencatatan

- TRANSACTION_DETAILS — tabel inti yang menyimpan detail setiap mutasi, dengan atribut MUTATION_TYPE bernilai DR (debit) atau CR (kredit).
- dailybalancerekening — saldo harian per rekening, yang direkonsiliasi terhadap akumulasi mutasi debit/kredit dari tabel transaksi historis dan berjalan.
- Setiap transaksi bisnis (Setor Tunai, Pindah Buku, dsb.) pada akhirnya diterjemahkan menjadi satu atau lebih pasangan entri DR/CR yang tersimpan secara atomik.

## 3.2 Alur Pencatatan Transaksi

![Gambar 3.1 — Alur pencatatan transaksi pada modul Accounting](diagrams/02_alur_double_entry.png)

## 3.3 Event & Outbox

Setelah mutasi tercatat, sistem mempublikasikan event melalui pola transactional outbox ke Kafka. Pola ini menjaga konsistensi antara perubahan data di database dan event yang dikirim ke konsumen hilir (reporting, notifikasi, modul GL lain), tanpa risiko event hilang atau terkirim ganda.

## 3.4 Audit & Rekonsiliasi

Karena berada dalam lingkungan yang diaudit, modul Accounting perlu mendukung: jejak audit (audit trail) yang lengkap, kemampuan rekonsiliasi saldo (membandingkan saldo tersimpan vs. hasil rekonstruksi dari mutasi), dan deteksi anomali seperti duplikasi transaksi.

# 4. Modul Funding

Modul Funding mengelola produk-produk pendanaan/simpanan nasabah — misalnya tabungan, giro, dan deposito. Modul ini menjadi sumber utama dana pihak ketiga (DPK) bank.

## 4.1 Cakupan Fungsional

- Pembukaan dan pemeliharaan rekening simpanan.
- Perhitungan bagi hasil/bunga sesuai jenis produk (konvensional maupun syariah).
- Integrasi dengan modul Accounting untuk pencatatan mutasi rekening (setoran, penarikan, pemindahbukuan).
- Integrasi dengan modul Customer untuk validasi identitas dan profil nasabah.

## 4.2 Keterkaitan dengan Modul Lain

Setiap transaksi pada rekening Funding (misalnya Setor Tunai) akan memicu pencatatan pada modul Accounting (DR/CR) dan, bila melibatkan kas fisik, berinteraksi dengan modul Cash Management melalui abstraksi CASH_POINT.

# 5. Modul Treasury / Cash Management

Modul Cash Management mengelola pergerakan kas fisik dan likuiditas bank, termasuk kas teller, vault (khazanah), ATM, dan rekening sundry.

## 5.1 Abstraksi CASH_POINT

CASH_POINT adalah abstraksi yang menyeragamkan berbagai titik penyimpanan/perputaran kas — baik itu laci teller, vault cabang, mesin ATM, maupun rekening sundry — sehingga logika pengelolaan saldo kas dapat digeneralisasi lintas titik tersebut.

## 5.2 Fungsi Treasury

- Pengelolaan likuiditas harian dan posisi kas bank.
- Rekonsiliasi kas fisik terhadap catatan sistem.
- Interaksi dengan Remittance untuk kebutuhan settlement lintas bank (SKN, RTGS, BI-FAST).

![Gambar 5.1 — Integrasi Cash Management, Treasury & Remittance dengan sistem sekitar](diagrams/03_integrasi_sistem_sekitar.png)

# 6. Manajemen Cabang, Departemen & User

Selain modul-modul fungsional (Funding, Accounting, Treasury, dsb.), IBANKCORE juga memiliki lapisan struktur organisasi — cabang, departemen, dan user — yang menjadi atribut wajib pada hampir setiap transaksi maupun aktivitas sistem. Lapisan ini dikelola terutama melalui modul Enterprise dan Customer.

## 6.1 Struktur Organisasi: Cabang & Departemen

- **Cabang (Branch)** — unit operasional yang melayani nasabah secara langsung (tatap muka maupun melalui kanal cabang). Setiap cabang memiliki kode unik (kode cabang) yang menjadi atribut wajib pada transaksi yang terjadi di cabang tersebut.
- **Departemen** — unit di kantor pusat (head office) yang umumnya bersifat back office/non-transaksional, misalnya Departemen Treasury, Departemen Accounting, Departemen Kepatuhan, atau Departemen IT. Departemen lebih banyak berfungsi sebagai cost center/unit organisasi untuk keperluan GL dan pelaporan manajerial dibandingkan sebagai titik transaksi nasabah.
- **Hierarki Wilayah** — cabang dapat dikelompokkan ke dalam area/wilayah/regional untuk keperluan agregasi laporan manajerial (mis. kinerja cabang per wilayah).

## 6.2 Kode Cabang sebagai Atribut Transaksi

- Setiap transaksi (Setor Tunai, Pindah Buku, dsb.) membawa kode cabang tempat transaksi dilakukan atau diinisiasi.
- TRANSACTION_DETAILS dan dailybalancerekening turut menyimpan kode cabang, sehingga saldo dan mutasi dapat direkonsiliasi maupun dilaporkan per cabang.
- Setiap CASH_POINT (laci teller, vault, ATM) selalu terasosiasi ke satu kode cabang tertentu, sehingga posisi kas fisik dapat dipantau per cabang.

## 6.3 Manajemen User & Hak Akses

- User sistem — mulai dari teller, customer service, supervisor cabang, branch manager, hingga user di kantor pusat/departemen — dikelola melalui modul Enterprise.
- Setiap user umumnya terikat ke satu kode cabang atau departemen tertentu, yang menentukan lingkup data dan transaksi yang dapat dilihat maupun diproses oleh user tersebut.
- Role-Based Access Control (RBAC) — peran (role) menentukan menu, jenis transaksi, dan limit otorisasi yang dapat diakses oleh user, misalnya perbedaan hak akses antara teller, supervisor, dan branch manager.
- Limit otorisasi berjenjang (approval limit) — transaksi dengan nilai di atas limit tertentu memerlukan persetujuan (approval) dari user dengan peran/level lebih tinggi, sesuai prinsip maker-checker atau dual control.

## 6.4 Segregasi & Pelaporan Berdasarkan Cabang/Departemen

- Modul Internal Account menggunakan kode departemen sebagai cost center untuk pencatatan biaya/pendapatan non-operasional pada buku besar (GL).
- Laporan manajerial (mis. volume transaksi per cabang, kinerja cabang) direkonstruksi dari agregasi TRANSACTION_DETAILS berdasarkan kode cabang.
- Audit trail pada modul Enterprise mencatat user, kode cabang/departemen, serta waktu setiap aksi — mendukung kebutuhan investigasi maupun kepatuhan (OJK/BI, audit eksternal).

# 7. Interaksi dengan Aplikasi & Sistem Sekitar

## 7.1 Event Streaming — Kafka

IBANKCORE menggunakan pola transactional outbox untuk mempublikasikan event transaksi ke Kafka. Pendekatan ini memungkinkan sistem-sistem hilir (reporting, notifikasi, modul lain) berlangganan event tanpa perlu mengakses langsung basis data inti, sekaligus menjaga loose coupling antar sistem.

## 7.2 Kliring & Pembayaran Antar Bank

| Sistem | Karakteristik |
|---|---|
| SKN | Kliring nasional untuk transaksi bernilai relatif kecil; proses batch. |
| RTGS | Transfer bernilai besar, real-time gross settlement. |
| BI-FAST | Transfer real-time antar bank untuk nilai kecil-menengah, tersedia 24/7. |

## 7.3 Pelaporan Regulator & Audit Eksternal

Sebagai entitas yang diawasi OJK dan BI, IBANKCORE perlu mendukung pelaporan berkala (mis. laporan keuangan, laporan transaksi, laporan kepatuhan) serta menyediakan jejak data yang dapat ditelusuri untuk kebutuhan audit eksternal.

# 8. Contoh Proses Bisnis

## 8.1 Setor Tunai

Proses Setor Tunai melibatkan nasabah, teller, modul core (validasi & pencatatan), hingga modul Accounting/Ledger untuk pembaruan saldo. Diagram berikut menggambarkan alur lintas fungsi secara sederhana.

![Gambar 8.1 — Alur proses Setor Tunai (simplified swimlane)](diagrams/04_proses_setor_tunai.png)

## 8.2 Pindah Buku

Pindah Buku (transfer antar rekening dalam bank yang sama) mengikuti pola serupa dengan Setor Tunai, namun tanpa melibatkan kas fisik — mutasi DR terjadi pada rekening sumber dan mutasi CR pada rekening tujuan secara bersamaan (atomik), tanpa keterlibatan modul Cash Management.

# 9. Konteks Regulasi & Produk Syariah

Sebagian produk pada modul Financing mengikuti prinsip syariah dan mengacu pada PSAK 109, mencakup skema seperti Murabahah (jual-beli dengan margin), Ijarah (sewa), dan Kafalah (penjaminan). Perlakuan akuntansi untuk skema-skema ini memiliki kekhususan dibandingkan produk konvensional, dan tetap harus konsisten dengan prinsip double-entry pada modul Accounting.

# 10. Ringkasan

- IBANKCORE adalah sistem core banking multi-modul yang berbagi lapisan data dan pola integrasi yang konsisten.
- Modul Accounting menjadi pusat pencatatan double-entry yang menopang seluruh modul lain.
- Modul Funding dan Cash Management/Treasury saling terkait erat dalam setiap transaksi yang melibatkan dana maupun kas fisik.
- Struktur cabang, departemen, dan user/hak akses menjadi lapisan pengendalian yang melekat pada hampir seluruh transaksi dan aktivitas sistem.
- Interaksi dengan sistem sekitar (Kafka, SKN/RTGS/BI-FAST, regulator) menjadi bagian penting dari arsitektur end-to-end.
- Diskusi lanjutan dapat difokuskan ke salah satu area untuk pendalaman lebih lanjut, misalnya detail data model, pola integrasi, atau studi kasus incident/rekonsiliasi.

## Bahan Diskusi

- Modul mana yang paling relevan untuk didalami lebih lanjut oleh masing-masing peserta?
- Apakah ada isu integrasi atau kepatuhan yang ingin dibahas lebih jauh?
- Bagaimana pengelolaan hak akses/limit otorisasi saat ini dijalankan di masing-masing cabang/departemen?
