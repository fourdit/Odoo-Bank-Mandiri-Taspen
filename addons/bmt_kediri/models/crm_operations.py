# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTSosialisasiRencana(models.Model):
    _name = 'bmt.sosialisasi.rencana'
    _description = 'Rencana Sosialisasi Tahunan'
    _rec_name = 'judul_rencana'

    name = fields.Char('ID Rencana', required=True)
    tahun_anggaran = fields.Integer('Tahun Anggaran', default=2025)
    judul_rencana = fields.Char('Judul Rencana', required=True)
    tujuan = fields.Text('Tujuan Kegiatan')
    target_peserta = fields.Integer('Target Peserta')
    anggaran = fields.Float('Anggaran (Rp)')
    tanggal_penyusunan = fields.Date('Tanggal Penyusunan')
    status_persetujuan = fields.Selection([
        ('Draft', 'Draft'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak')
    ], string='Status Persetujuan', default='Disetujui')
    tanggal_persetujuan = fields.Date('Tanggal Persetujuan')
    id_penyusun = fields.Many2one('hr.employee', string='Penyusun (GA)')
    id_penyetuju = fields.Many2one('hr.employee', string='Penyetuju (Kepala Cabang)')


class BMTSosialisasiJadwal(models.Model):
    _name = 'bmt.sosialisasi.jadwal'
    _description = 'Jadwal Sosialisasi'
    _rec_name = 'name'

    name = fields.Char('ID Jadwal', required=True)
    id_rencana_sosialisasi = fields.Many2one('bmt.sosialisasi.rencana', string='Rencana Sosialisasi')
    id_instansi = fields.Many2one('res.partner', string='Instansi Target')
    no_surat_pengajuan = fields.Char('No Surat Pengajuan')
    tanggal_surat = fields.Date('Tanggal Surat')
    tanggal_pelaksanaan = fields.Date('Tanggal Pelaksanaan')
    waktu_mulai = fields.Char('Waktu Mulai')
    waktu_selesai = fields.Char('Waktu Selesai')
    lokasi = fields.Char('Lokasi')
    materi = fields.Char('Materi')
    status_pelaksanaan = fields.Selection([
        ('Terjadwal', 'Terjadwal'),
        ('Selesai', 'Selesai'),
        ('Dibatalkan', 'Dibatalkan')
    ], string='Status Pelaksanaan', default='Selesai')
    id_penanggung_jawab = fields.Many2one('hr.employee', string='Penanggung Jawab')


class BMTSosialisasiHasil(models.Model):
    _name = 'bmt.sosialisasi.hasil'
    _description = 'Hasil Sosialisasi'
    _rec_name = 'name'

    name = fields.Char('ID Hasil', required=True)
    id_jadwal_sosialisasi = fields.Many2one('bmt.sosialisasi.jadwal', string='Jadwal Sosialisasi')
    tanggal_realisasi = fields.Date('Tanggal Realisasi')
    jumlah_peserta = fields.Integer('Jumlah Peserta')
    jumlah_calon_nasabah = fields.Integer('Jumlah Calon Nasabah')
    ringkasan_hasil = fields.Text('Ringkasan Hasil')
    kendala = fields.Text('Kendala')
    tanggal_rekap = fields.Date('Tanggal Rekap')
    id_penyusun = fields.Many2one('hr.employee', string='Penyusun Rekap')


class BMTDoorprize(models.Model):
    _name = 'bmt.doorprize'
    _description = 'Program Pembagian Doorprize'
    _rec_name = 'name'

    name = fields.Char('ID Doorprize', required=True)
    id_nasabah = fields.Many2one('res.partner', string='Nasabah', required=True)
    tahun_program = fields.Integer('Tahun Program', default=2025)
    jenis_hadiah = fields.Char('Jenis Hadiah', required=True)
    nilai_hadiah = fields.Float('Nilai Hadiah (Rp)')
    status_persetujuan_daftar = fields.Selection([
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui')
    ], string='Persetujuan Daftar', default='Disetujui')
    status_persetujuan_pelaksanaan = fields.Selection([
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui')
    ], string='Persetujuan Pelaksanaan', default='Disetujui')
    tanggal_pembagian = fields.Date('Tanggal Pembagian')
    status_penerimaan = fields.Selection([
        ('Belum Diterima', 'Belum Diterima'),
        ('Sudah Diterima', 'Sudah Diterima'),
        ('Diwakilkan', 'Diwakilkan')
    ], string='Status Penerimaan', default='Sudah Diterima')
    id_penyeleksi = fields.Many2one('hr.employee', string='Penyeleksi (Operation Manager)')
    id_pengelola = fields.Many2one('hr.employee', string='Pengelola (GA)')
    id_penyetuju = fields.Many2one('hr.employee', string='Penyetuju (Kepala Cabang)')


class BMTPromoBunga(models.Model):
    _name = 'bmt.promo.bunga'
    _description = 'Promo Bunga Kompetitif'
    _rec_name = 'name'

    name = fields.Char('ID Promo', required=True)
    id_nasabah = fields.Many2one('res.partner', string='Nasabah', required=True)
    id_suku_bunga = fields.Many2one('bmt.suku.bunga', string='Suku Bunga Acuan')
    no_surat_promo = fields.Char('No Surat Promo')
    tanggal_surat = fields.Date('Tanggal Surat')
    jenis_produk = fields.Selection([
        ('Deposito', 'Deposito'),
        ('Tabungan', 'Tabungan')
    ], string='Jenis Produk', default='Deposito')
    suku_bunga_promo = fields.Float('Suku Bunga Promo (% p.a.)')
    syarat_dana_minimum = fields.Float('Syarat Dana Minimum (Rp)')
    periode_mulai = fields.Date('Periode Mulai')
    periode_selesai = fields.Date('Periode Selesai')
    status_persetujuan_nasabah = fields.Selection([
        ('Menunggu', 'Menunggu'),
        ('Setuju', 'Setuju'),
        ('Menolak', 'Menolak')
    ], string='Persetujuan Nasabah', default='Setuju')
    tanggal_tanda_tangan_kontrak = fields.Date('Tgl Tanda Tangan')
    id_penyusun = fields.Many2one('hr.employee', string='Penyusun (GA)')
    id_penyetuju = fields.Many2one('hr.employee', string='Penyetuju (Operation Manager)')


class BMTKeluhan(models.Model):
    _name = 'bmt.keluhan'
    _description = 'Keluhan Nasabah'
    _rec_name = 'name'

    name = fields.Char('ID Keluhan', required=True)
    id_nasabah = fields.Many2one('res.partner', string='Nasabah', required=True)
    tanggal_keluhan = fields.Date('Tanggal Keluhan')
    kategori_keluhan = fields.Selection([
        ('Pelayanan', 'Pelayanan'),
        ('Produk', 'Produk'),
        ('Transaksi', 'Transaksi')
    ], string='Kategori')
    media_penyampaian = fields.Selection([
        ('WhatsApp', 'WhatsApp'),
        ('Telepon', 'Telepon'),
        ('Email', 'Email'),
        ('Datang Langsung', 'Datang Langsung'),
        ('Kotak Saran', 'Kotak Saran')
    ], string='Kanal')
    uraian_keluhan = fields.Text('Uraian')
    status_penanganan = fields.Selection([
        ('Diterima', 'Diterima'),
        ('Diproses', 'Diproses'),
        ('Selesai', 'Selesai')
    ], string='Status', default='Selesai')
    id_cs = fields.Many2one('hr.employee', string='Customer Service')
    hasil_evaluasi = fields.Text('Solusi / Evaluasi')
    tanggal_penyelesaian = fields.Date('Tanggal Penyelesaian')


class BMTSaran(models.Model):
    _name = 'bmt.saran'
    _description = 'Saran Nasabah'
    _rec_name = 'name'

    name = fields.Char('ID Saran', required=True)
    id_nasabah = fields.Many2one('res.partner', string='Nasabah', required=True)
    tanggal_saran = fields.Date('Tanggal Saran')
    kategori_saran = fields.Selection([
        ('Produk', 'Produk'),
        ('Layanan', 'Layanan'),
        ('Fasilitas', 'Fasilitas'),
        ('Digital', 'Digital')
    ], string='Kategori')
    uraian_saran = fields.Text('Uraian Saran')
    status_evaluasi = fields.Selection([
        ('Belum Dievaluasi', 'Belum Dievaluasi'),
        ('Sedang Dievaluasi', 'Sedang Dievaluasi'),
        ('Selesai Dievaluasi', 'Selesai Dievaluasi')
    ], string='Status Evaluasi', default='Selesai Dievaluasi')
    id_cs = fields.Many2one('hr.employee', string='Customer Service')
    hasil_evaluasi = fields.Text('Hasil Evaluasi')
    tanggal_evaluasi = fields.Date('Tanggal Evaluasi')
