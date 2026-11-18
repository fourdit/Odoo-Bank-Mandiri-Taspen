# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTSukuBunga(models.Model):
    _name = 'bmt.suku.bunga'
    _description = 'Master Suku Bunga Bank'
    _rec_name = 'nama_produk'

    name = fields.Char('Kode Bunga', required=True)
    jenis_produk = fields.Selection([
        ('Deposito', 'Deposito'),
        ('Tabungan', 'Tabungan'),
        ('Giro', 'Giro'),
        ('Pinjaman Pensiun', 'Pinjaman Pensiun'),
        ('Pinjaman Mikro', 'Pinjaman Mikro'),
        ('Pinjaman Retail', 'Pinjaman Retail')
    ], string='Jenis Produk', required=True)
    nama_produk = fields.Char('Nama Produk', required=True)
    suku_bunga_persen_pa = fields.Float('Suku Bunga (% p.a.)', digits=(5, 2))
    tenor_minimum = fields.Integer('Tenor Minimum (Bulan)')
    tenor_maksimum = fields.Integer('Tenor Maksimum (Bulan)')
    plafon_minimum = fields.Float('Plafon Minimum (Rp)')
    plafon_maksimum = fields.Float('Plafon Maksimum (Rp)')
    tanggal_berlaku = fields.Date('Tanggal Berlaku')
    tanggal_berakhir = fields.Date('Tanggal Berakhir')
    status_bunga = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif')
    ], string='Status Bunga', default='Aktif')


class BMTRiwayatPerbankan(models.Model):
    _name = 'bmt.riwayat.perbankan'
    _description = 'Pemeriksaan Riwayat Perbankan / SLIK'

    name = fields.Char('ID Riwayat', required=True)
    nasabah_id = fields.Many2one('res.partner', string='Nasabah', required=True)
    verifikator_id = fields.Many2one('hr.employee', string='Verifikator')
    tanggal_pengecekan = fields.Date('Tanggal Pengecekan', default=fields.Date.context_today)
    kolektibilitas = fields.Selection([
        ('1', '1 - Lancar'),
        ('2', '2 - Dalam Perhatian Khusus'),
        ('3', '3 - Kurang Lancar'),
        ('4', '4 - Diragukan'),
        ('5', '5 - Macet')
    ], string='Kolektibilitas', default='1')
    jumlah_fasilitas_aktif = fields.Integer('Jumlah Fasilitas Aktif', default=0)
    total_kewajiban = fields.Float('Total Kewajiban (Rp)', default=0.0)
    status_daftar_hitam = fields.Selection([
        ('Tidak', 'Tidak'),
        ('Ya', 'Ya')
    ], string='Daftar Hitam (Blacklist)', default='Tidak')
    hasil_pengecekan = fields.Selection([
        ('Bersih', 'Bersih (Layak)'),
        ('Tidak Bersih', 'Tidak Bersih (Ditolak)')
    ], string='Hasil Pengecekan', default='Bersih')
    keterangan = fields.Text('Keterangan')
