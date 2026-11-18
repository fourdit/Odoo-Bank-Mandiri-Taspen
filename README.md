# 🏦 Implementasi Sistem Enterprise — Bank Mandiri Taspen KC Kediri (Odoo 19)

Proyek ini merupakan implementasi dan simulasi sistem enterprise pada **Bank Mandiri Taspen Kantor Cabang (KC) Kediri** menggunakan **Odoo 19 Community Edition** dengan modul kustom Python (`bmt_kediri`).

Sistem ini memodelkan **26 proses bisnis (BPMN As-Is)**, mengelola **30 model data perbankan**, dan telah terintegrasi dengan **47 tabel dataset simulasi** (nasabah pensiunan, UMKM, kredit, deposito, tabungan, transaksi teller, CRM, hingga operasional kepegawaian).

---

## 📑 Daftar Isi
1. [Tentang Proyek](#-tentang-proyek)
2. [Cakupan Proses Bisnis (BPMN)](#-cakupan-proses-bisnis-bpmn)
3. [Dokumentasi Lengkap 34 Modul](#-dokumentasi-lengkap-34-modul)
4. [Struktur Direktori Repository](#-struktur-direktori-repository)
5. [Prasyarat Sistem (Prerequisites)](#-prasyarat-sistem-prerequisites)
6. [Panduan Instalasi & Setup Odoo Lokal](#-panduan-instalasi--setup-odoo-lokal)
7. [Pemasangan Modul Custom `bmt_kediri`](#-pemasangan-modul-custom-bmt_kediri)
8. [Import Otomatis Dataset Dummy (47 Tabel)](#-import-otomatis-dataset-dummy-47-tabel)
9. [Panduan Troubleshooting & Solusi Error Lengkap](#-panduan-troubleshooting--solusi-error-lengkap)
10. [Skenario Demo untuk Presentasi Dosen](#-skenario-demo-untuk-presentasi-dosen)
11. [Tim Pengembang](#-tim-pengembang)

---

## 📚 Dokumentasi Lengkap 34 Modul
Seluruh perancangan, fungsionalitas, evaluasi skor, dan panduan navigasi langkah-demi-langkah tersedia di folder `docs/`:
* 📘 **[Panduan Implementasi & Navigasi 34 Modul Odoo](docs/Panduan_Implementasi_dan_Navigasi_Modul_Odoo_BMT_Kediri.md)**: Panduan detail menu path, URL langsung, dan cara mengoperasikan 20 modul bawaan + 14 modul kustom studio + Executive Dashboard.
* 📊 **[Laporan Evaluasi & Audit 34 Modul Odoo](docs/Laporan_Evaluasi_Modul_Odoo_BMT_Kediri.md)**: Audit real-time database, nilai fungsionalitas (A/A+), integrasi 47 sheet dataset simulasi, pembersihan 100% data demo bawaan, dan pemetaan Enterprise Bridge.

---

## 🏢 Tentang Proyek
* **Nama Instansi**: Bank Mandiri Taspen Kantor Cabang Kediri
* **Alamat**: Jl. Brawijaya No. 29-29A, Kota Kediri
* **Fokus Segmen**: Layanan Keuangan Pensiunan (ASN/TNI/Polri) dan Pemberdayaan Pelaku Usaha Mikro, Kecil, dan Menengah (UMKM).
* **Mata Kuliah**: Sistem Enterprise — Program Studi Sistem Informasi, Fakultas Ilmu Komputer, Universitas Brawijaya.

---

## 🔄 Cakupan Proses Bisnis (BPMN)
Modul kustom `bmt_kediri` mencakup seluruh alur bisnis kantor cabang:
1. **Core Banking & Simpanan**:
   - Pembukaan Rekening Tabungan & Giro (BPMN 2.2)
   - Transaksi Setoran, Penarikan, dan Transfer Dana di Loket (BPMN 2.3)
   - Transaksi Mandiri ATM Bersama (BPMN 2.16)
   - Aktivasi Layanan Mobile & Internet Banking (BPMN 2.17 & 2.18)
   - Layanan Kas Mobil Keliling (BPMN 2.19)
   - Penempatan Deposito Berjangka & Bilyet (BPMN 2.22)
   - Penutupan Rekening Nasabah (BPMN 2.26)
2. **Kredit & Pembiayaan**:
   - Pengajuan Pinjaman Pensiun, Mikro, & Retail (BPMN 2.4)
   - Pemeriksaan Kelayakan Kredit / SLIK & Blacklist
   - Otorisasi Pinjaman oleh Kepala Cabang & Kalkulasi Angsuran Otomatis
3. **Pemasaran, CRM & Kemitraan**:
   - Sosialisasi Produk ke Instansi Pemerintah, BUMN, & Sekolah (BPMN 2.6)
   - Program Loyalitas Doorprize Tahunan Nasabah Prioritas (BPMN 2.5)
   - Promo Suku Bunga Kompetitif (BPMN 2.20)
   - Manajemen Suara Nasabah: Keluhan & Saran (BPMN 2.7)
   - Keagenan Investasi Reksa Dana APERD & Profil Risiko (BPMN 2.23)
4. **Human Capital Management & Logistik Cabang**:
   - Penggajian & Slip Kompensasi Karyawan (BPMN 2.9)
   - Evaluasi & Penilaian Kinerja Karyawan (BPMN 2.10)
   - Penanganan Pelanggaran Disiplin Pegawai (BPMN 2.24)
   - Offboarding & Pemutusan Hubungan Kerja (PHK / Resign) (BPMN 2.24 & 2.25)
   - Pengaduan & Pemeliharaan IT Internal (BPMN 2.13 & 2.14)
   - Pengadaan, Distribusi, & Rekonsiliasi Buku Tabungan/ATK (BPMN 2.1 & 2.15)

---

## 📂 Struktur Direktori Repository
```text
.
├── addons/
│   └── bmt_kediri/                  # Modul Custom Odoo 19
│       ├── __init__.py
│       ├── __manifest__.py          # Metadata modul & dependensi
│       ├── models/                  # 30 Model Data Python
│       │   ├── banking_master.py    # Suku Bunga & Riwayat Perbankan SLIK
│       │   ├── crm_operations.py    # Sosialisasi, Doorprize, Promo, Keluhan/Saran
│       │   ├── deposito.py          # Deposito Berjangka
│       │   ├── employee.py          # Relasi Karyawan Cabang
│       │   ├── hcm_operations.py    # Kompensasi Gaji, Penilaian, PHK, IT
│       │   ├── logistik.py          # Stok Buku Tabungan, Permintaan, Terima/Pakai
│       │   ├── partner.py           # Relasi Nasabah & Instansi Mitra
│       │   ├── pinjaman.py          # Pinjaman / Loan Management
│       │   ├── rekening.py          # Rekening Simpanan, Kartu ATM, Layanan Digital
│       │   ├── reksa_dana.py        # Katalog & Transaksi Reksa Dana APERD
│       │   └── teller.py            # Transaksi Setoran, Tarik, Transfer, Kas Teller
│       ├── security/
│       │   └── ir.model.access.csv  # Hak Akses Model (CRUD)
│       └── views/                   # Tampilan XML Odoo (Form, List, Menu)
│           ├── crm_views.xml
│           ├── dashboard_views.xml  # Tampilan Dashboard KPI Cabang
│           ├── deposito_views.xml
│           ├── hcm_views.xml
│           ├── logistik_views.xml
│           ├── menu_views.xml
│           ├── partner_views.xml
│           ├── pinjaman_views.xml
│           ├── rekening_views.xml
│           ├── reksa_dana_views.xml
│           └── teller_views.xml
├── docs/
│   ├── Panduan_Implementasi_dan_Navigasi_Modul_Odoo_BMT_Kediri.md # Panduan akses & URL modul
│   └── Laporan_Evaluasi_Modul_Odoo_BMT_Kediri.md                  # Laporan evaluasi 34 modul
├── data/
│   ├── data_simulasi_bmt_kediri.xlsx # Dataset 47 sheet data simulasi
│   ├── import_all_data.py           # Auto-populate 14 modul kustom
│   ├── import_standard_modules.py   # Auto-populate 20 modul bawaan community
│   ├── setup_surveys.py             # Setup survey profil risiko & seleksi HR
│   ├── setup_leaves_discuss.py      # Setup cuti tahunan & channel koordinasi
│   └── execute_company_fix.py       # Pengunci entitas tunggal Bank Mandiri Taspen
├── .gitignore                       # Filter file sensitif & cache
└── README.md                        # Dokumentasi utama proyek
```

---

## ⚙️ Prasyarat Sistem (Prerequisites)
* **Sistem Operasi**: Windows 10 / 11 (atau Linux Ubuntu 22.04+)
* **Odoo**: Odoo 19.0 Community Edition
* **Database**: PostgreSQL 14+ (bawaan instalasi Odoo Windows)
* **Python**: Python 3.10+ (bawaan direktori `C:\Program Files\Odoo 19.0... \python`)
* **Library Python**: `openpyxl`, `psycopg2`

---

## 🚀 Panduan Instalasi & Setup Odoo Lokal

### 1. Instalasi Odoo 19 di Windows
1. Download installer resmi Odoo 19 Community untuk Windows (`odoo_19.0.latest.exe`).
2. Jalankan instalasi sebagai **Administrator**. Installer akan otomatis menginstal server Odoo dan PostgreSQL di:
   ```text
   C:\Program Files\Odoo 19.0.xxxxxxxx\
   ```
3. Pastikan service `odoo-server-19.0` dan `postgresql-x64-xx` berjalan di Windows Services (`services.msc`).

### 2. Konfigurasi `odoo.conf` & Password PostgreSQL
Sebelum membuat database, pastikan kredensial pada file konfigurasi sudah benar:
* Lokasi file: `C:\Program Files\Odoo 19.0.xxxxxxxx\server\odoo.conf`
* Buka **Notepad (Run as Administrator)** dan pastikan parameter berikut:
  ```ini
  [options]
  admin_passwd = admin
  db_host = localhost
  db_port = 5432
  db_user = odoo
  db_password = odoo
  ```

### 3. Pembuatan Database di Web Browser
1. Buka browser dan akses: `http://localhost:8069/web/database/manager` (atau `http://localhost:8069`).
2. Masukkan rincian form **Create Database**:
   - **Master Password**: `admin` *(sesuai dengan `admin_passwd` di `odoo.conf`)*
   - **Database Name**: `odoo_db`
   - **Email**: `admin@example.com`
   - **Password**: `admin`
   - **Language**: `Indonesian (ID)`
   - **Country**: `Indonesia`
   - **Demo Data**: ❌ *Jangan dicentang*
3. Klik **Create Database** dan tunggu proses inisialisasi awal selesai (2–4 menit).

---

## 🧩 Pemasangan Modul Custom `bmt_kediri`

1. **Copy folder modul ke direktori Addons Odoo**:
   Buka **PowerShell (Administrator)**, lalu jalankan:
   ```powershell
   Copy-Item -Path "addons\bmt_kediri" -Destination "C:\Program Files\Odoo 19.0.xxxxxxxx\server\odoo\addons\bmt_kediri" -Recurse -Force
   Restart-Service odoo-server-19.0
   ```

2. **Aktifkan Modul di Odoo**:
   - Buka browser di `http://localhost:8069`.
   - Masuk ke menu **Settings (Pengaturan)** → scroll ke paling bawah → klik **Activate the developer mode**.
   - Buka menu **Apps (Aplikasi)**.
   - Di bilah menu atas, klik **Update Apps List** → klik **Update**.
   - Pada kolom pencarian, hapus filter bawaan *"Apps"*, lalu cari: `bmt_kediri` atau `Bank Mandiri Taspen`.
   - Klik tombol **Activate**.
   - Menu utama **"Bank Mandiri Taspen"** akan langsung muncul pada navbar Odoo!

---

## 📥 Import Otomatis Dataset Dummy (47 Tabel)

Untuk mengisi seluruh data nasabah, rekening, transaksi, pinjaman, dan rekonsiliasi tanpa perlu input manual satu per satu:

1. Pastikan modul `bmt_kediri` sudah terpasang dan aktif di Odoo.
2. Buka **PowerShell (Administrator)** dan navigasikan ke folder `data/`:
   ```powershell
   & "C:\Program Files\Odoo 19.0.xxxxxxxx\python\python.exe" "data\import_all_data.py"
   ```
3. Script akan otomatis membaca `data_simulasi_bmt_kediri.xlsx` dan memasukkan seluruh rekaman data ke database `odoo_db`.
4. Refresh browser Anda, seluruh data simulasi akan langsung tampil di menu Odoo!

---

## 🛠️ Panduan Troubleshooting & Solusi Error Lengkap

Berikut adalah rangkuman masalah nyata yang sering terjadi saat instalasi Odoo di Windows beserta solusinya:

### 1. Error: `Database creation error: Access Denied`
* **Penyebab**: Nilai `admin_passwd` di `odoo.conf` berupa hash string `$pbkdf2-sha512$...` yang di-generate otomatis oleh installer, sehingga saat memasukkan password di browser ditolak oleh validasi `check_super(passwd)`.
* **Solusi**:
  1. Buka PowerShell Administrator.
  2. Ganti nilai hash menjadi password plaintext yang Anda ketahui:
     ```powershell
     (Get-Content "C:\Program Files\Odoo 19.0.xxxx\server\odoo.conf" -Raw) -replace 'admin_passwd = \$pbkdf2-sha512\$[^\r\n]+', 'admin_passwd = admin' | Set-Content "C:\Program Files\Odoo 19.0.xxxx\server\odoo.conf" -NoNewline
     ```
  3. Restart service Odoo: `Restart-Service odoo-server-19.0`.
  4. Gunakan `admin` sebagai Master Password saat membuat database di browser.

### 2. Error: `fe_sendauth: no password supplied` / Autentikasi PostgreSQL Gagal
* **Penyebab**: User database `odoo` di PostgreSQL belum di-set passwordnya atau berbeda dengan parameter `db_password` di `odoo.conf`.
* **Solusi**:
  1. Buka file `C:\Program Files\Odoo 19.0.xxxx\PostgreSQL\data\pg_hba.conf`.
  2. Ubah sementara metode autentikasi dari `scram-sha-256` atau `md5` menjadi `trust`.
  3. Restart PostgreSQL: `Restart-Service postgresql*`.
  4. Masuk ke PostgreSQL tanpa password dan set password user `odoo`:
     ```powershell
     & "C:\Program Files\Odoo 19.0.xxxx\PostgreSQL\bin\psql.exe" -U odoo -d template1 -c "ALTER USER odoo WITH PASSWORD 'odoo';"
     ```
  5. Kembalikan `pg_hba.conf` ke `scram-sha-256`, lalu isi `db_password = odoo` di `odoo.conf`.
  6. Restart PostgreSQL dan Odoo.

### 3. Error: `FATAL: role "postgres" does not exist`
* **Penyebab**: Installer Odoo Windows tidak membuat superuser dengan nama `postgres`, melainkan menggunakan user `odoo` atau nama user Windows lokal.
* **Solusi**: Selalu gunakan parameter `-U odoo` dan target database `-d template1` saat menjalankan perintah CLI PostgreSQL.

### 4. Error: `Invalid Operation: Odoo is currently processing a scheduled action`
* **Penyebab**: Odoo mengunci operasi modul saat background cron job (Scheduled Action) sedang aktif mengeksekusi tugas latar belakang.
* **Solusi**:
  1. Tunggu 30–60 detik hingga proses cron latar belakang selesai.
  2. Jika masih terkunci, restart service Odoo via PowerShell Admin:
     ```powershell
     Restart-Service odoo-server-19.0
     ```
  3. Refresh browser (F5) dan klik **Activate** kembali.

### 5. Error: `Access is denied` saat manipulasi file di `Program Files`
* **Penyebab**: Proteksi UAC Windows melarang user standar menulis langsung ke dalam direktori `C:\Program Files\`.
* **Solusi**:
  Jalankan perintah izin ACL di PowerShell Administrator:
  ```powershell
  icacls "C:\Program Files\Odoo 19.0.xxxx\server\odoo\addons" /grant "Users:(OI)(CI)F" /T
  ```

### 6. Masalah Modul Bawaan Terlihat Kosong (Multi-Company Context & Cuti Pribadi)
* **Penyebab**: Saat database baru diinisialisasi, Odoo membuat perusahaan demo bawaan (`ID Company` atau `My Company Chicago`). Jika sesi browser Anda aktif di dalam `ID Company`, Odoo menerapkan filter multi-company `WHERE company_id = 2`. Karena seluruh 47 dataset di-input ke perusahaan resmi **`Bank Mandiri Taspen KC Kediri`** (`company_id = 1`), modul bawaan (CRM, Employees, Purchase, Time Off, Accounting) akan menampilkan 0 data. Selain itu, pada modul **Time Off**, halaman default adalah `My Time` (cuti pribadi akun login), bukan cuti seluruh cabang.
* **Solusi**:
  1. Jalankan script pengunci entitas tunggal:
     ```powershell
     & "C:\Program Files\Odoo 19.0.xxxx\python\python.exe" data/execute_company_fix.py
     ```
  2. Tekan `Ctrl + F5` di browser.
  3. Pada modul **Time Off**, klik tab menu atas **Overview** atau **Management → Time Off** untuk melihat seluruh pengajuan cuti staf cabang.

---

## 🎤 Skenario Demo untuk Presentasi Dosen

| Skenario | Menu Odoo | Alur yang Ditampilkan |
|---|---|---|
| **1. Pembukaan Rekening Pensiunan** | `Core Banking → Data Nasabah` & `Rekening Simpanan` | Tunjukkan profil nasabah pensiunan (NIK, No Pensiun), pengecekan SLIK (bersih/kolektibilitas 1), dan otorisasi rekening aktif oleh Operation Manager. |
| **2. Pengajuan Pinjaman Kredit** | `Core Banking → Kredit & Pinjaman` | Tunjukkan plafon pinjaman, tenor, suku bunga, dan **perhitungan angsuran per bulan otomatis** via ORM logic, serta status persetujuan Kepala Cabang. |
| **3. Transaksi Teller & Kas Harian** | `Teller & Kas → Setoran, Tarik, Transfer` & `Rekonsiliasi Kas` | Tunjukkan pencatatan mutasi transaksi loket dan rekonsiliasi saldo fisik vs saldo sistem teller di akhir hari (selisih Rp 0). |
| **4. CRM & Pemasaran Segmen Khusus** | `Pemasaran & CRM → Sosialisasi & Doorprize` | Tunjukkan rencana sosialisasi triwulan ke instansi target, penawaran promo bunga kompetitif, dan program hadiah doorprize nasabah prioritas. |
| **5. Manajemen SDM & Kedisiplinan** | `HCM & Disiplin → Kompensasi & PHK/Resign` | Tunjukkan rincian slip kompensasi gaji (tunjangan, BPJS, PPh 21), riwayat audit pelanggaran pegawai, dan clearance aset saat proses offboarding. |

---

## 👥 Tim Pengembang
* **Rifky Aditya Harun** (245150400111002)
* **Muhammad Faiz Rahman** (245150400111003)
* **Luhung Arkananta Rohmat** (245150407111011)
* **Abdul Hakim** (245150407111019)

*Program Studi Sistem Informasi — Fakultas Ilmu Komputer, Universitas Brawijaya (2026)*
