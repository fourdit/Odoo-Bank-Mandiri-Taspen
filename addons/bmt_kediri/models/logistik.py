# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTPersediaanBukuATM(models.Model):
    _name = 'bmt.persediaan.buku.atm'
    _description = 'Persediaan Buku Tabungan dan Kartu ATM'
    _rec_name = 'name'

    name = fields.Char('ID Persediaan', required=True)
    jenis_item = fields.Selection([
        ('Buku Tabungan', 'Buku Tabungan'),
        ('Kartu ATM', 'Kartu ATM')
    ], string='Jenis Item', default='Buku Tabungan')
    jumlah_stok = fields.Integer('Jumlah Stok')
    stok_minimum = fields.Integer('Stok Minimum', default=20)
    jumlah_terpakai = fields.Integer('Jumlah Terpakai')
    lokasi_penyimpanan = fields.Char('Lokasi Penyimpanan')
    tanggal_pembaruan = fields.Date('Tanggal Pembaruan')
    id_pengelola = fields.Many2one('hr.employee', string='Pengelola (GA)')


class BMTPermintaanBahan(models.Model):
    _name = 'bmt.permintaan.bahan'
    _description = 'Permintaan Bahan dan Inventaris'
    _rec_name = 'name'

    name = fields.Char('ID Permintaan', required=True)
    id_pemohon = fields.Many2one('hr.employee', string='Pemohon')
    id_operation_manager = fields.Many2one('hr.employee', string='Operation Manager')
    kode_barang = fields.Char('Kode Barang / Item')
    divisi_pemohon = fields.Char('Divisi Pemohon', default='Pelayanan')
    tanggal_permintaan = fields.Date('Tanggal Permintaan')
    jumlah_diminta = fields.Integer('Jumlah Diminta')
    jumlah_tersedia = fields.Integer('Jumlah Tersedia')
    alasan_kebutuhan = fields.Text('Alasan Kebutuhan')
    hasil_pengecekan = fields.Selection([
        ('Tersedia', 'Tersedia'),
        ('Tidak Tersedia', 'Tidak Tersedia')
    ], string='Hasil Pengecekan', default='Tidak Tersedia')
    status_permintaan = fields.Selection([
        ('Draft', 'Draft'),
        ('Disetujui', 'Disetujui'),
        ('Dipenuhi dari Stok', 'Dipenuhi dari Stok')
    ], string='Status', default='Disetujui')


class BMTPenerimaanBuku(models.Model):
    _name = 'bmt.penerimaan.buku'
    _description = 'Penerimaan Buku Tabungan dari Pusat'
    _rec_name = 'name'

    name = fields.Char('ID Penerimaan', required=True)
    no_surat_jalan = fields.Char('No Surat Jalan', required=True)
    tanggal_terima = fields.Date('Tanggal Terima')
    asal_pengiriman = fields.Char('Asal Pengiriman', default='Kantor Pusat Bank Mandiri Taspen')
    jumlah_dikirim = fields.Integer('Jumlah Dikirim')
    jumlah_diterima = fields.Integer('Jumlah Diterima')
    selisih = fields.Integer('Selisih', default=0)
    status_kesesuaian = fields.Selection([
        ('Sesuai', 'Sesuai'),
        ('Tidak Sesuai', 'Tidak Sesuai')
    ], string='Status Kesesuaian', default='Sesuai')
    no_berita_acara_selisih = fields.Char('No Berita Acara Selisih')
    status_retur = fields.Selection([
        ('Tidak Diperlukan', 'Tidak Diperlukan'),
        ('Retur', 'Retur ke Pusat')
    ], string='Status Retur', default='Tidak Diperlukan')
    id_penerima = fields.Many2one('hr.employee', string='Penerima (GA)')
    id_penyetuju = fields.Many2one('hr.employee', string='Penyetuju (Operation Manager)')
    tanggal_persetujuan = fields.Date('Tanggal Persetujuan')


class BMTPemakaianBuku(models.Model):
    _name = 'bmt.pemakaian.buku'
    _description = 'Alokasi dan Pemakaian Buku Tabungan'
    _rec_name = 'name'

    name = fields.Char('ID Pemakaian', required=True)
    id_penerimaan = fields.Many2one('bmt.penerimaan.buku', string='Batch Penerimaan')
    id_cs = fields.Many2one('hr.employee', string='CS Pengguna')
    id_pengarsip = fields.Many2one('hr.employee', string='Pengarsip (GA)')
    tanggal_alokasi = fields.Date('Tanggal Alokasi')
    jumlah_dialokasikan = fields.Integer('Jumlah Dialokasikan')
    jumlah_terpakai = fields.Integer('Jumlah Terpakai')
    jumlah_rusak = fields.Integer('Jumlah Rusak', default=1)
    sisa_stok = fields.Integer('Sisa Stok')
    status_rekonsiliasi = fields.Selection([
        ('Proses', 'Proses'),
        ('Selesai', 'Selesai')
    ], string='Status Rekonsiliasi', default='Selesai')
    tanggal_rekonsiliasi = fields.Date('Tanggal Rekonsiliasi')
