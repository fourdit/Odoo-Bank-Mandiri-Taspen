# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTKompensasi(models.Model):
    _name = 'bmt.kompensasi'
    _description = 'Kompensasi dan Gaji Pegawai'
    _rec_name = 'name'

    name = fields.Char('ID Kompensasi', required=True)
    id_karyawan = fields.Many2one('hr.employee', string='Karyawan', required=True)
    id_pengelola = fields.Many2one('hr.employee', string='Pengelola (GA)')
    periode_bulan = fields.Integer('Periode Bulan', default=9)
    periode_tahun = fields.Integer('Periode Tahun', default=2026)
    gaji_pokok = fields.Float('Gaji Pokok (Rp)')
    tunjangan_jabatan = fields.Float('Tunjangan Jabatan (Rp)')
    tunjangan_lain = fields.Float('Tunjangan Lain (Rp)')
    upah_lembur = fields.Float('Upah Lembur (Rp)')
    potongan_ketidakhadiran = fields.Float('Potongan Kehadiran (Rp)')
    potongan_bpjs = fields.Float('Potongan BPJS (Rp)')
    pph21 = fields.Float('PPh 21 (Rp)')
    gaji_bersih = fields.Float('Gaji Bersih / Take Home Pay (Rp)')
    tanggal_pembayaran = fields.Date('Tanggal Pembayaran')
    status_pembayaran = fields.Selection([
        ('Draft', 'Draft'),
        ('Disetujui', 'Disetujui'),
        ('Sukses', 'Sukses')
    ], string='Status', default='Sukses')


class BMTPenilaianKinerja(models.Model):
    _name = 'bmt.penilaian.kinerja'
    _description = 'Penilaian Kinerja Pegawai'
    _rec_name = 'name'

    name = fields.Char('ID Penilaian', required=True)
    id_karyawan = fields.Many2one('hr.employee', string='Karyawan', required=True)
    id_penilai = fields.Many2one('hr.employee', string='Penilai (Kepala Cabang)')
    periode_penilaian = fields.Char('Periode Penilaian', default='September 2026')
    nilai_kehadiran = fields.Float('Nilai Kehadiran')
    nilai_pencapaian_target = fields.Float('Nilai Pencapaian Target')
    nilai_kualitas_pelayanan = fields.Float('Nilai Kualitas Pelayanan')
    nilai_sikap_kerja = fields.Float('Nilai Sikap Kerja')
    nilai_akhir = fields.Float('Nilai Akhir')
    predikat = fields.Selection([
        ('Sangat Baik', 'Sangat Baik'),
        ('Baik', 'Baik'),
        ('Cukup', 'Cukup'),
        ('Kurang', 'Kurang')
    ], string='Predikat', default='Baik')
    catatan_penilai = fields.Text('Catatan Penilai')
    tanggal_penilaian = fields.Date('Tanggal Penilaian')


class BMTPelanggaran(models.Model):
    _name = 'bmt.pelanggaran'
    _description = 'Laporan Pelanggaran Pegawai'
    _rec_name = 'name'

    name = fields.Char('ID Pelanggaran', required=True)
    id_karyawan = fields.Many2one('hr.employee', string='Karyawan Terlapor', required=True)
    id_pelapor = fields.Many2one('hr.employee', string='Pelapor')
    id_pemeriksa = fields.Many2one('hr.employee', string='Pemeriksa (GA Supervisor)')
    no_laporan_kejadian = fields.Char('No Laporan Kejadian (LKP)')
    tanggal_kejadian = fields.Date('Tanggal Kejadian')
    jenis_pelanggaran = fields.Char('Jenis Pelanggaran')
    uraian_pelanggaran = fields.Text('Uraian Pelanggaran')
    hasil_audit_internal = fields.Text('Hasil Audit Internal')
    memenuhi_syarat_phk = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak', 'Tidak')
    ], string='Memenuhi Syarat PHK', default='Tidak')
    jenis_sanksi = fields.Selection([
        ('SP 1', 'SP 1'),
        ('SP 2', 'SP 2'),
        ('SP 3', 'SP 3'),
        ('PHK', 'PHK')
    ], string='Jenis Sanksi')
    no_surat_peringatan = fields.Char('No Surat Sanksi / SP')
    tanggal_sanksi = fields.Date('Tanggal Sanksi')


class BMTPemutusanKerja(models.Model):
    _name = 'bmt.pemutusan.kerja'
    _description = 'Pemutusan Hubungan Kerja (PHK & Resign)'
    _rec_name = 'name'

    name = fields.Char('ID Pemutusan', required=True)
    id_karyawan = fields.Many2one('hr.employee', string='Karyawan', required=True)
    id_pelanggaran = fields.Many2one('bmt.pelanggaran', string='Kasus Pelanggaran')
    id_otorisator = fields.Many2one('hr.employee', string='Otorisator (Kepala Cabang)')
    jenis_pemutusan = fields.Selection([
        ('PHK', 'Pemutusan Hubungan Kerja (PHK)'),
        ('Pengunduran Diri', 'Pengunduran Diri (Resign)')
    ], string='Jenis Pemutusan', required=True)
    tanggal_pengajuan = fields.Date('Tanggal Pengajuan')
    alasan = fields.Text('Alasan')
    hasil_wawancara_retention = fields.Text('Hasil Wawancara Retention / Bipartit')
    status_persetujuan = fields.Selection([
        ('Menunggu Persetujuan', 'Menunggu Persetujuan'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
        ('Dibatalkan', 'Dibatalkan')
    ], string='Status Persetujuan', default='Disetujui')
    no_sk = fields.Char('No SK')
    tanggal_sk = fields.Date('Tanggal SK')
    tanggal_efektif = fields.Date('Tanggal Efektif')
    tanggal_deaktivasi_akses = fields.Date('Tanggal Deaktivasi Akses')
    status_clearance_aset = fields.Selection([
        ('Belum Dimulai', 'Belum Dimulai'),
        ('Selesai', 'Selesai')
    ], string='Clearance Aset', default='Selesai')
    nilai_hak_keuangan = fields.Float('Nilai Hak Keuangan / Pesangon (Rp)')
    tanggal_pembayaran = fields.Date('Tanggal Pembayaran')
    no_laporan_disnaker = fields.Char('No Laporan Disnaker')
    tanggal_lapor_disnaker = fields.Date('Tanggal Lapor Disnaker')
    status_proses = fields.Selection([
        ('Verifikasi Administrasi', 'Verifikasi Administrasi'),
        ('Selesai', 'Selesai'),
        ('Ditolak', 'Ditolak'),
        ('Dibatalkan', 'Dibatalkan')
    ], string='Status Proses', default='Selesai')


class BMTPengaduanIT(models.Model):
    _name = 'bmt.pengaduan.it'
    _description = 'Pengaduan & Pemeliharaan IT Internal'
    _rec_name = 'name'

    name = fields.Char('ID Tiket IT', required=True)
    id_karyawan_pelapor = fields.Many2one('hr.employee', string='Karyawan Pelapor', required=True)
    id_penangan = fields.Many2one('hr.employee', string='Staf IT')
    divisi_pelapor = fields.Char('Divisi Pelapor')
    tanggal_pengaduan = fields.Date('Tanggal Pengaduan')
    nama_aplikasi = fields.Char('Nama Aplikasi')
    jenis_pengaduan = fields.Selection([
        ('Gangguan', 'Gangguan'),
        ('Pengembangan', 'Pengembangan')
    ], string='Jenis Pengaduan', default='Gangguan')
    uraian_pengaduan = fields.Text('Uraian Masalah')
    tingkat_prioritas = fields.Selection([
        ('Rendah', 'Rendah'),
        ('Sedang', 'Sedang'),
        ('Tinggi', 'Tinggi')
    ], string='Prioritas', default='Tinggi')
    status_penanganan = fields.Selection([
        ('Diterima', 'Diterima'),
        ('Diproses', 'Diproses'),
        ('Selesai', 'Selesai')
    ], string='Status Penanganan', default='Selesai')
    hasil_analisis_atau_perbaikan = fields.Text('Hasil Perbaikan / Solusi')
    tanggal_selesai = fields.Date('Tanggal Selesai')
