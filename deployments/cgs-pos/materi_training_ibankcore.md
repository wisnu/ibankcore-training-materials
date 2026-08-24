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

Sesi ini bertujuan memberikan pemahaman menyeluruh (overview) mengenai sistem core banking IBANKCORE, khususnya modul Accounting, Funding, dan Treasury (Kas & Vault), serta bagaimana ketiga modul tersebut berinteraksi satu sama lain maupun dengan aplikasi/sistem di sekitarnya (channel, regulator, dan platform integrasi).

Materi disusun untuk audiens campuran — baik yang berlatar belakang teknis (developer, DBA) maupun bisnis (business analyst, product owner, auditor) — sehingga penjelasan konsep akan diberikan pada level arsitektur dan proses bisnis, sebelum masuk ke detail data model bila diperlukan.

## 1.2 Ruang Lingkup

- Arsitektur modul IBANKCORE yang diimplementasikan pada sistem ini (Enterprise, Funding, Accounting, Kas & Vault, Internal Account, Customer).
- Struktur organisasi cabang & departemen, serta manajemen user dan hak akses (role, limit otorisasi) — dikelola melalui modul Enterprise.
- Prinsip pencatatan transaksi (double-entry ledger) pada modul Accounting.
- Konsep dasar modul Funding (produk pendanaan/simpanan).
- Konsep Treasury / Kas & Vault (Teller/ATM), termasuk abstraksi CASH_POINT (teller, vault, ATM, sundry).
- Interaksi dengan sistem sekitar: integrasi Feeder SAP serta pelaporan regulator (OJK/BI).
- Contoh proses bisnis end-to-end: Setor Tunai dan Pindah Buku.
- Produk & layanan tambahan: Deposito, Teller & Layanan Counter, QRIS & Virtual Account, Host-to-Host & REST API, Corporate Banking, Manajemen Rekening & Nasabah (CIF), Biller, dan integrasi SAP/GL eksternal.
- Operasional batch & kontinuitas layanan: End-of-Day/Begin-of-Day (EOD/BOD) cabang, serta backup & disaster recovery.
- Keamanan, otorisasi, dan audit lanjutan: mekanisme maker-checker (OtorEntri), user security & access control, session/block management, dan verifikasi biometrik.

## 1.3 Konteks Lingkungan

IBANKCORE beroperasi pada lingkungan perbankan yang diatur (regulated), tunduk pada ketentuan OJK/BI serta audit eksternal. Sistem berjalan di atas basis data Oracle, dengan kode sumber dikelola pada instance GitLab internal (self-hosted).

# 2. Arsitektur Modul IBANKCORE

IBANKCORE adalah sistem core banking multi-modul. Setiap modul menangani domain bisnis tertentu namun berbagi lapisan data (shared ledger) dan pola integrasi yang konsisten. Diagram berikut menggambarkan posisi setiap modul beserta kanal dan sistem sekitarnya.

![Gambar 2.1 — Arsitektur Modul IBANKCORE](diagrams/01_arsitektur_ibankcore.png)

## 2.1 Modul-Modul Utama

| Modul | Fungsi Utama |
|---|---|
| Enterprise | Fungsi lintas modul: struktur organisasi, user & hak akses, parameter, otorisasi, audit trail. |
| Funding | Produk pendanaan/simpanan nasabah (tabungan, giro, deposito). |
| Accounting | Pencatatan transaksi double-entry, buku besar (GL), saldo harian. |
| Kas & Vault (Teller/ATM) | Pengelolaan kas fisik: teller, vault, ATM, sundry (CASH_POINT). |
| Internal Account | Rekening internal bank (GL internal, suspense, sundry account). |
| Customer | Data induk nasabah (CIF), identitas, profil risiko. |

## 2.2 Lapisan Data

Seluruh modul berbagi satu basis data Oracle yang sama — bukan database terpisah per modul — sehingga transaksi lintas modul (mis. Setor Tunai yang melibatkan Funding, Accounting, dan Kas & Vault sekaligus) dapat tercatat secara konsisten dalam satu lapisan data.

## 2.3 Kanal & Sistem Sekitar

Transaksi dapat masuk melalui berbagai kanal (teller/cabang, ATM/EDC, mobile & internet banking, maupun API gateway). Di sisi hilir, IBANKCORE terhubung dengan kebutuhan pelaporan regulator (OJK/BI) serta kebutuhan audit eksternal.

## 2.4 Aplikasi Core vs Enterprise

Secara implementasi, IBANKCORE terdiri dari dua aplikasi terpisah namun saling terkait: **core** dan **enterprise**.

- **Aplikasi Enterprise** — modul platform/administratif di atas core: manajemen user & cabang, keamanan & hak akses, mekanisme otorisasi (maker-checker), proses batch operasional (EOD/BOD), backup/disaster recovery, serta monitoring sesi user.
- **Aplikasi Core** — mesin transaksi & produk perbankan itu sendiri: logika akun, transaksi, jurnal, serta produk (Deposito, Tabungan, Teller, Corporate) dan integrasi kanal (QRIS, host-to-host, REST API). Aplikasi ini dideploy per-instansi/bank, ditandai dengan konfigurasi lingkungan terpisah seperti training, UAT, dan production.
- Kedua aplikasi berbagi prinsip dan pola arsitektur yang sama (lapisan data, struktur transaksi), namun **enterprise** berfokus pada domain administrasi, keamanan, dan operasional platform, sedangkan **core** berfokus pada domain bisnis/produk.

# 3. Manajemen Cabang, Departemen & User

Selain modul-modul fungsional (Funding, Accounting, Treasury, dsb.), IBANKCORE juga memiliki lapisan struktur organisasi — cabang, departemen, dan user — yang menjadi atribut wajib pada hampir setiap transaksi maupun aktivitas sistem. Lapisan ini dikelola terutama melalui modul Enterprise dan Customer.

## 3.1 Struktur Organisasi: Cabang, Wilayah & Departemen

- **Cabang (Branch)** — unit operasional yang melayani nasabah secara langsung (tatap muka maupun melalui kanal cabang). Setiap cabang memiliki kode unik (kode cabang) yang menjadi atribut wajib pada transaksi yang terjadi di cabang tersebut.
- **Wilayah (Area Cabang)** — cabang dikelompokkan ke dalam wilayah melalui entity Area Cabang (dengan kode wilayah tersendiri); setiap cabang menyimpan kode wilayahnya sebagai atribut, sehingga laporan manajerial dapat diagregasi per wilayah (satu wilayah menaungi banyak cabang). Pada implementasi di PT Pos, entity ini dikenal dengan istilah bisnis **"Regional"**.
- **Cabang Induk & Cabang Anak** — selain pengelompokan per wilayah, setiap cabang juga dapat mereferensikan satu cabang induk secara langsung, membentuk hierarki induk-anak antar cabang — umum dipakai untuk struktur kantor cabang pembantu/kantor kas di bawah kantor cabang utamanya.
- **Jenis/Tipe Unit ("Kantor")** — istilah "Kantor" pada sistem ini bukan level organisasi tersendiri di atas/di bawah cabang, melainkan atribut tipe & status dari cabang itu sendiri (mis. Kantor Pusat, Cabang Utama, Cabang Pembantu, Kantor Kas, Kantor Fungsional, Pusat Operasional/Non-Operasional, Gerai), beserta data alamat & kontak resmi yang melekat pada cabang tersebut.
- **Departemen** — unit di kantor pusat (head office) yang umumnya bersifat back office/non-transaksional, misalnya Departemen Treasury, Departemen Accounting, Departemen Kepatuhan, atau Departemen IT. Sebagai entity organisasi, Departemen terhubung ke data kepegawaian (employee/HR); kode departemen juga ikut terekam pada header transaksi/jurnal (lihat 3.2), namun bukan sebagai dimensi cost center yang formal pada Chart of Accounts (lihat 3.5).

![Gambar 3.1 — Struktur Organisasi: Wilayah, Cabang & Atribut Kantor](diagrams/05_struktur_organisasi.png)

## 3.2 Kode Cabang & Kantor sebagai Atribut Transaksi

- Setiap transaksi (Setor Tunai, Pindah Buku, dsb.) membawa kode cabang tempat transaksi dilakukan atau diinisiasi.
- Header JOURNAL (bukan baris JOURNALITEM-nya) menyimpan tiga kode organisasi sekaligus pada setiap transaksi: **kode cabang**, **kode kantor**, dan **kode departemen** — sebagai kolom data biasa (tanpa foreign key formal ke entity Cabang/Kantor/Departemen).
  - **Kode kantor** diisi dari kode kantor transaksi bila tersedia, dan otomatis jatuh kembali (fallback) ke kode cabang apabila kode kantor tidak diisi — sehingga nilainya bisa sama dengan kode cabang pada banyak kasus, namun kolomnya tetap terpisah secara fisik.
  - **Kode departemen** diisi dari departemen user yang memposting transaksi, atau dari data transaksi eksternal (untuk transaksi masuk via interface/API) — bukan dari struktur Departemen sebagai unit organisasi (3.1).
  - Baris JOURNALITEM (detail mutasi) sendiri hanya menyimpan kode cabang, tidak menyimpan kode kantor/departemen — kedua kode itu hanya ada di level header transaksi.
- dailybalancerekening turut menyimpan kode cabang, sehingga saldo dapat direkonsiliasi maupun dilaporkan per cabang.
- Setiap CASH_POINT (laci teller, vault, ATM) selalu terasosiasi ke satu kode cabang tertentu, sehingga posisi kas fisik dapat dipantau per cabang.

## 3.3 Manajemen User & Hak Akses

- User sistem — mulai dari teller, customer service, supervisor cabang, branch manager, hingga user di kantor pusat/departemen — dikelola melalui modul Enterprise.
- Role-Based Access Control (RBAC) — peran (role) menentukan menu, jenis transaksi, dan limit otorisasi yang dapat diakses oleh user, misalnya perbedaan hak akses antara teller, supervisor, dan branch manager.
- Limit otorisasi (approval limit) — dicek per-user (bukan per-jenjang hierarki cabang/role): setiap user punya nilai limit transaksinya sendiri, dan transaksi yang melebihi limit tersebut memerlukan persetujuan (approval) dari user lain yang punya limit mencukupi, sesuai prinsip maker-checker atau dual control.

**Isolasi akses berdasarkan cabang & departemen** — akses user terhadap data/transaksi dibatasi lewat dua mekanisme yang berbeda konstruksinya:

- **Isolasi cabang** — diatur oleh atribut tipe akses cabang pada masing-masing user, dengan tiga mode: **Semua** (akses ke seluruh cabang), **Tunggal** (hanya cabang milik user sendiri), atau **Parsial** (hanya cabang yang eksplisit terdaftar sebagai "cabang diizinkan" untuk user tersebut, ditambah cabang miliknya sendiri). Ini gerbang akses aktif yang dicek setiap kali sistem perlu memvalidasi apakah seorang user boleh mengakses data suatu cabang.
- **Isolasi departemen** — konsepnya mirip (ada daftar "departemen diizinkan"), tapi konstruksinya berbeda: daftar ini terhubung ke data **karyawan**, bukan langsung ke akun user, dan lebih banyak dipakai dalam konteks pemilihan/administrasi departemen (mis. saat menetapkan departemen seorang karyawan) daripada sebagai gerbang akses transaksi/data yang independen. Mode "Semua/Tunggal/Parsial" untuk departemen juga meminjam pengaturan mode akses cabang milik user, bukan pengaturan tersendiri untuk departemen.

## 3.4 Segregasi & Pelaporan Berdasarkan Cabang/Wilayah

- Laporan manajerial (mis. volume transaksi per cabang, kinerja cabang) direkonstruksi dari agregasi JOURNAL/JOURNALITEM berdasarkan kode cabang, dan dapat diagregasi lebih lanjut per wilayah melalui relasi cabang ke Area Cabang.
- Audit trail pada modul Enterprise mencatat user, kode cabang/departemen, serta waktu setiap aksi — mendukung kebutuhan investigasi maupun kepatuhan (OJK/BI, audit eksternal).

## 3.5 Kaitan dengan Chart of Accounts (COA) & Neraca

Struktur cabang/wilayah di atas menyatu langsung dengan cara Chart of Accounts (COA) dan laporan Neraca disusun pada sistem ini.

- **Account (COA master)** — daftar akun standar bank (kode akun, nama akun, tipe akun), tanpa dimensi cabang.
- **Account Instance** — setiap akun COA "diinstansiasi" per cabang dan mata uang (dibuat melalui proses generate instance per cabang); saldo & posting GL (GL Account) menempel ke Account Instance ini, bukan ke Account master secara langsung. Artinya **setiap cabang punya salinan instance akunnya sendiri** untuk setiap akun COA yang relevan.
- **Neraca (Balance Sheet)** — dihasilkan dari laporan yang menggabungkan Account Instance dengan data Cabang (join berdasarkan kode cabang), dengan parameter cabang yang bersifat opsional — sehingga Neraca dapat ditampilkan **per cabang** maupun **konsolidasi seluruh bank**.
- **Wilayah bukan dimensi langsung pada GL** — tidak ada kolom kode wilayah pada tabel Account Instance/GL Account/posting jurnal. Agregasi Neraca per wilayah harus dilakukan secara tidak langsung: menjumlahkan Account Instance dari seluruh cabang yang berada di wilayah tersebut (via relasi Cabang → Area Cabang).
- **Dimensi cost center pada posting jurnal** — setiap baris jurnal (JOURNALITEM) membawa "Kode RC" (Revenue-Cost Center, entity Project) sebagai dimensi biaya/pendapatan non-operasional, terpisah dari kode cabang. Kode RC inilah dimensi cost center yang formal pada COA/GL — berbeda dari kode departemen yang tersimpan di header JOURNAL (3.2), yang sifatnya administratif/audit (mencatat departemen user pemosting atau data transaksi eksternal) dan tidak terhubung ke struktur Account/Account Instance.

# 4. Modul Accounting

Modul Accounting adalah jantung pencatatan finansial IBANKCORE. Prinsip utamanya adalah double-entry bookkeeping — setiap transaksi selalu menghasilkan pasangan mutasi debit (DR) dan kredit (CR) yang seimbang.

## 4.1 Struktur Pencatatan

- JOURNAL/JOURNALITEM — tabel inti buku besar (ledger) yang menyimpan baris mutasi (jurnal) untuk setiap transaksi, dengan pembedaan debit (DR) dan kredit (CR).
- dailybalancerekening — saldo harian per rekening, yang direkonsiliasi terhadap akumulasi mutasi debit/kredit dari tabel transaksi historis dan berjalan.
- Setiap transaksi bisnis (Setor Tunai, Pindah Buku, dsb.) pada akhirnya diterjemahkan menjadi satu atau lebih pasangan entri DR/CR yang tersimpan secara atomik.

## 4.2 Alur Pencatatan Transaksi

![Gambar 4.1 — Alur pencatatan transaksi pada modul Accounting](diagrams/02_alur_double_entry.png)

## 4.3 Feeder SAP

Data akuntansi yang sudah tercatat pada modul Accounting diambil (pull) secara berkala oleh mekanisme Feeder SAP langsung dari basis data Core — bukan dikirim/dipublikasikan secara aktif oleh sistem Core — untuk kebutuhan konsolidasi keuangan pada level korporasi/holding (lihat Bagian 7.4 untuk detail integrasi).

## 4.4 Audit & Rekonsiliasi

Karena berada dalam lingkungan yang diaudit, modul Accounting perlu mendukung: jejak audit (audit trail) yang lengkap, kemampuan rekonsiliasi saldo (membandingkan saldo tersimpan vs. hasil rekonstruksi dari mutasi), dan deteksi anomali seperti duplikasi transaksi.

# 5. Modul Funding

Modul Funding mengelola produk-produk pendanaan/simpanan nasabah — misalnya tabungan, giro, dan deposito. Modul ini menjadi sumber utama dana pihak ketiga (DPK) bank.

## 5.1 Cakupan Fungsional

- Pembukaan dan pemeliharaan rekening simpanan.
- Perhitungan bagi hasil/bunga sesuai jenis produk (konvensional maupun syariah).
- Integrasi dengan modul Accounting untuk pencatatan mutasi rekening (setoran, penarikan, pemindahbukuan).
- Integrasi dengan modul Customer untuk validasi identitas dan profil nasabah.

## 5.2 Keterkaitan dengan Modul Lain

Setiap transaksi pada rekening Funding (misalnya Setor Tunai) akan memicu pencatatan pada modul Accounting (DR/CR) dan, bila melibatkan kas fisik, berinteraksi dengan modul Kas & Vault melalui abstraksi CASH_POINT.

## 5.3 Produk Deposito

Deposito adalah salah satu produk Funding dengan karakteristik jangka waktu dan perhitungan bagi hasil/bunga tersendiri, mencakup beberapa proses khusus.

- **Perhitungan bunga/bagi hasil** — dihitung berdasarkan nominal, jangka waktu, dan nisbah/suku bunga yang berlaku pada saat pembukaan atau perpanjangan deposito.
- **Pencairan awal (premature withdrawal)** — pencairan sebelum jatuh tempo, umumnya dikenakan penalti atau penyesuaian bagi hasil sesuai kebijakan bank.
- **Perubahan nisbah** — penyesuaian porsi bagi hasil (untuk produk syariah) yang dapat berlaku pada perpanjangan otomatis (roll-over) deposito.

# 6. Modul Treasury / Kas & Vault (Teller/ATM)

Modul Kas & Vault mengelola pergerakan kas fisik dan likuiditas bank, termasuk kas teller, vault (khazanah), ATM, dan rekening sundry.

> **Catatan istilah**: modul ini berbeda dengan istilah industri "Cash Management System (CMS)", yang umumnya merujuk pada portal/aplikasi web bagi nasabah korporat (CIF) untuk kebutuhan pembayaran massal, koleksi, dan monitoring likuiditas multi-rekening. Modul yang dibahas di sini secara spesifik menangani manajemen kas fisik internal cabang (laci teller, vault, ATM, sundry), bukan kanal digital nasabah korporat.

## 6.1 Abstraksi CASH_POINT

CASH_POINT adalah abstraksi yang menyeragamkan berbagai titik penyimpanan/perputaran kas — baik itu laci teller, vault cabang, mesin ATM, maupun rekening sundry — sehingga logika pengelolaan saldo kas dapat digeneralisasi lintas titik tersebut.

## 6.2 Fungsi Treasury

- Pengelolaan likuiditas harian dan posisi kas bank.
- Rekonsiliasi kas fisik terhadap catatan sistem.

![Gambar 6.1 — Integrasi Kas & Vault & Treasury dengan sistem sekitar](diagrams/03_integrasi_sistem_sekitar.png)

## 6.3 Modul Teller & Layanan Counter

Modul Teller/Layanan Counter merepresentasikan alur transaksi front office di cabang — titik interaksi langsung antara nasabah dan sistem melalui CASH_POINT laci teller.

- Mendukung ragam transaksi counter (setor, tarik, pemindahbukuan, layanan lain) dalam satu alur kerja teller yang konsisten.
- Setiap transaksi teller tervalidasi terhadap saldo kas fisik pada CASH_POINT terkait sebelum dicatat ke modul Accounting.
- Menjadi titik awal (entry point) paling umum bagi sebagian besar contoh proses bisnis (lihat Bagian 8).

# 7. Interaksi dengan Aplikasi & Sistem Sekitar

## 7.1 Pelaporan Regulator & Audit Eksternal

Sebagai entitas yang diawasi OJK dan BI, IBANKCORE perlu mendukung pelaporan berkala (mis. laporan keuangan, laporan transaksi, laporan kepatuhan) serta menyediakan jejak data yang dapat ditelusuri untuk kebutuhan audit eksternal.

## 7.2 QRIS & Virtual Account

- **QRIS** — kanal pembayaran berbasis kode QR standar nasional; transaksi QRIS masuk melalui integrasi channel pihak ketiga dan diselesaikan (settlement) ke rekening tujuan melalui proses tersendiri.
- **Virtual Account (VA)** — nomor rekening virtual yang dipetakan ke rekening nasabah/tujuan sebenarnya, umumnya dipakai untuk penagihan (billing) atau penerimaan pembayaran; pencocokan (matching) pembayaran VA dilakukan secara terjadwal (batch).

## 7.3 Host-to-Host & REST API

Selain kanal konvensional, IBANKCORE menyediakan integrasi host-to-host serta REST API bagi sistem eksternal (mis. aplikasi mitra, agregator pembayaran) untuk memicu transaksi maupun menarik data secara terprogram, mengikuti kontrak/format pesan yang telah disepakati (request/response berbasis JSON).

## 7.4 Feeder SAP (Integrasi Akuntansi Eksternal)

Untuk kebutuhan konsolidasi keuangan pada level korporasi/holding, posting akuntansi diambil (pull) secara batch oleh mekanisme Feeder SAP langsung dari basis data Core, sebagai pelengkap pencatatan GL internal pada modul Accounting. Pendekatan ini berbeda dari pola push/event-driven — sistem Core tidak secara aktif mengirim data, melainkan Feeder SAP yang menjalankan proses ekstraksi terjadwal terhadap database.

# 8. Contoh Proses Bisnis

## 8.1 Setor Tunai

Proses Setor Tunai melibatkan nasabah, teller, modul core (validasi & pencatatan), hingga modul Accounting/Ledger untuk pembaruan saldo. Diagram berikut menggambarkan alur lintas fungsi secara sederhana.

![Gambar 8.1 — Alur proses Setor Tunai (simplified swimlane)](diagrams/04_proses_setor_tunai.png)

## 8.2 Pindah Buku

Pindah Buku (transfer antar rekening dalam bank yang sama) mengikuti pola serupa dengan Setor Tunai, namun tanpa melibatkan kas fisik — mutasi DR terjadi pada rekening sumber dan mutasi CR pada rekening tujuan secara bersamaan (atomik), tanpa keterlibatan modul Kas & Vault.

# 9. Produk & Layanan Tambahan

Selain modul-modul inti (Bagian 3-8), IBANKCORE mendukung sejumlah produk dan layanan tambahan yang memperluas cakupan bisnis bank.

## 9.1 Corporate Banking

Layanan khusus untuk nasabah korporat — mencakup parameter dan fitur yang berbeda dari nasabah ritel, seperti otorisasi transaksi bertingkat sesuai struktur kewenangan perusahaan nasabah.

## 9.2 Manajemen Rekening & Nasabah (CIF)

Modul ini menangani siklus hidup data nasabah dan rekening — mulai dari pembukaan Customer Information File (CIF), pembukaan rekening, pemeliharaan data, hingga penutupan rekening — dan menjadi rujukan identitas/profil yang divalidasi oleh modul Funding saat transaksi terjadi.

## 9.3 Biller

Integrasi pembayaran tagihan pihak ketiga (listrik, telekomunikasi, dan sejenisnya) melalui antarmuka biller tersendiri.

# 10. Operasional Batch & Kontinuitas Layanan

## 10.1 Batch Process & EOD/BOD

Operasional cabang mengikuti siklus harian yang dikelola melalui proses batch:

- **End-of-Day (EOD)** — rangkaian proses tutup hari yang memastikan seluruh transaksi hari tersebut telah tercatat, saldo direkonsiliasi, dan cabang dapat ditutup secara sistem.
- **Begin-of-Day (BOD)** — proses pembukaan hari kerja baru, termasuk persiapan cabang (branch open) sebelum transaksi hari itu dapat dimulai.
- Proses ini memastikan konsistensi data antar hari operasional dan menjadi prasyarat sebelum laporan harian maupun pelaporan regulator dapat disusun.

## 10.2 Backup & Disaster Recovery

Untuk menjaga kontinuitas layanan, IBANKCORE mendukung mekanisme backup database secara berjenjang (mis. backup penuh maupun incremental) serta prosedur disaster recovery, sebagai bagian dari kepatuhan terhadap kebutuhan ketahanan operasional (business continuity) perbankan.

# 11. Keamanan, Otorisasi & Audit Lanjutan

Selain hak akses dasar dan audit trail yang telah dibahas pada Bagian 3, IBANKCORE menerapkan beberapa mekanisme keamanan dan kontrol tambahan yang penting untuk dipahami.

## 11.1 Maker-Checker / Otorisasi

Prinsip maker-checker (dual control) diimplementasikan melalui mekanisme otorisasi entri (OtorEntri) — transaksi atau perubahan data tertentu dicatat dalam status "menunggu otorisasi" dan baru berlaku efektif setelah disetujui oleh user lain dengan kewenangan yang sesuai. Riwayat otorisasi (termasuk siapa yang mengajukan dan siapa yang menyetujui/menolak) tersimpan sebagai jejak audit tersendiri, terpisah dari data transaksi utama.

## 11.2 User Security & Access Control

Selain Role-Based Access Control dasar (lihat 3.3), sistem menyediakan validasi keamanan data user, pencatatan aktivitas user (activity log), serta laporan hak akses (daftar menu/hak akses per user maupun per grup) yang mendukung kebutuhan audit periodik terhadap kesesuaian hak akses dengan peran pekerjaan.

## 11.3 Session & Block Management

Sistem memantau dan mengelola sesi login user, termasuk kedaluwarsa sesi (session expiry) dan pemblokiran otomatis user setelah kondisi tertentu (mis. percobaan login gagal berulang), sebagai kontrol keamanan tambahan terhadap akses tidak sah.

## 11.4 Verifikasi Biometrik

Untuk transaksi atau proses yang memerlukan tingkat keyakinan identitas lebih tinggi, IBANKCORE mendukung verifikasi biometrik nasabah sebagai lapisan otentikasi tambahan di luar PIN/password konvensional.

# 12. Ringkasan

- IBANKCORE adalah sistem core banking multi-modul yang berbagi lapisan data dan pola integrasi yang konsisten, terdiri dari dua aplikasi utama: enterprise (platform, keamanan, operasional) dan core (mesin transaksi/produk).
- Modul Enterprise menjadi fondasi struktur organisasi, user, dan hak akses yang melekat pada hampir seluruh transaksi dan aktivitas sistem.
- Modul Accounting menjadi pusat pencatatan double-entry yang menopang seluruh modul lain.
- Modul Funding dan Kas & Vault/Treasury saling terkait erat dalam setiap transaksi yang melibatkan dana maupun kas fisik, termasuk produk khusus seperti Deposito.
- Interaksi dengan sistem sekitar (Feeder SAP, QRIS, host-to-host/REST API, regulator) menjadi bagian penting dari arsitektur end-to-end.
- Produk & layanan tambahan (Corporate Banking, Biller, dsb.) memperluas cakupan bisnis di luar produk simpanan dasar.
- Operasional batch (EOD/BOD) dan backup/disaster recovery menjaga konsistensi data dan kontinuitas layanan dari hari ke hari.
- Mekanisme maker-checker (otorisasi), user security, session/block management, dan verifikasi biometrik menjadi lapisan kontrol keamanan yang penting dipahami baik oleh audiens teknis maupun bisnis/audit.
- Diskusi lanjutan dapat difokuskan ke salah satu area untuk pendalaman lebih lanjut, misalnya detail data model, pola integrasi, atau studi kasus incident/rekonsiliasi.

## Bahan Diskusi

- Modul mana yang paling relevan untuk didalami lebih lanjut oleh masing-masing peserta?
- Apakah ada isu integrasi atau kepatuhan yang ingin dibahas lebih jauh?
- Bagaimana pengelolaan hak akses/limit otorisasi saat ini dijalankan di masing-masing cabang/departemen?
- Bagaimana mekanisme maker-checker (otorisasi) saat ini diterapkan untuk transaksi bernilai besar atau berisiko tinggi?
- Seberapa sering proses EOD/BOD dan backup/disaster recovery diuji atau mengalami kendala di lapangan?
