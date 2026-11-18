# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTProfilRisiko(models.Model):
    _name = 'bmt.profil.risiko'
    _description = 'Profil Risiko Investasi Nasabah'
    _rec_name = 'name'

    name = fields.Char('ID Profil Risiko', required=True)
    id_nasabah = fields.Many2one('res.partner', string='Nasabah', required=True)
    tanggal_asesmen = fields.Date('Tanggal Asesmen')
    tujuan_investasi = fields.Char('Tujuan Investasi', default='Menjaga likuiditas')
    jangka_waktu_investasi = fields.Char('Jangka Waktu', default='< 1 Tahun')
    skor_risiko = fields.Integer('Skor Risiko', default=20)
    kategori_profil = fields.Selection([
        ('Konservatif', 'Konservatif'),
        ('Moderat', 'Moderat'),
        ('Agresif', 'Agresif')
    ], string='Kategori Profil', default='Konservatif')
    masa_berlaku = fields.Date('Masa Berlaku')
    id_tenaga_pemasar = fields.Many2one('hr.employee', string='Tenaga Pemasar')


class BMTProdukRD(models.Model):
    _name = 'bmt.produk.rd'
    _description = 'Katalog Produk Reksa Dana'
    _rec_name = 'nama_produk'

    name = fields.Char('ID Produk', required=True)
    nama_produk = fields.Char('Nama Produk', required=True)
    jenis_reksa_dana = fields.Selection([
        ('Pasar Uang', 'Pasar Uang'),
        ('Pendapatan Tetap', 'Pendapatan Tetap'),
        ('Campuran', 'Campuran'),
        ('Saham', 'Saham')
    ], string='Jenis Reksa Dana', default='Pasar Uang')
    nama_manajer_investasi = fields.Char('Manajer Investasi')
    tingkat_risiko = fields.Selection([
        ('Rendah', 'Rendah'),
        ('Sedang', 'Sedang'),
        ('Tinggi', 'Tinggi')
    ], string='Tingkat Risiko', default='Rendah')
    minimal_pembelian = fields.Float('Minimal Pembelian (Rp)', default=100000.0)
    biaya_subscription_persen = fields.Float('Biaya Subscription (%)', default=0.5)
    nab_per_up = fields.Float('NAB / UP (Rp)', default=1000.0)
    tanggal_nab = fields.Date('Tanggal NAB')
    status_produk = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif')
    ], string='Status Produk', default='Aktif')


class BMTTransaksiRD(models.Model):
    _name = 'bmt.transaksi.rd'
    _description = 'Transaksi Reksa Dana APERD'
    _rec_name = 'name'

    name = fields.Char('ID Transaksi RD', required=True)
    id_nasabah = fields.Many2one('res.partner', string='Nasabah', required=True)
    no_rekening = fields.Many2one('bmt.rekening', string='Rekening Sumber')
    id_produk_rd = fields.Many2one('bmt.produk.rd', string='Produk Reksa Dana', required=True)
    id_tenaga_pemasar = fields.Many2one('hr.employee', string='Tenaga Pemasar')
    no_formulir_subscription = fields.Char('No Formulir Subscription')
    tanggal_pemesanan = fields.Date('Tanggal Pemesanan')
    nominal_pembelian = fields.Float('Nominal Pembelian (Rp)', required=True)
    biaya_subscription = fields.Float('Biaya Subscription (Rp)')
    nab_per_up = fields.Float('NAB / UP (Rp)')
    jumlah_unit_penyertaan = fields.Float('Jumlah Unit Penyertaan', digits=(16, 4))
    tanggal_setelmen = fields.Date('Tanggal Setelmen')
    no_konfirmasi_kepemilikan = fields.Char('No Konfirmasi Kepemilikan (KSEI)')
    status_transaksi = fields.Selection([
        ('Pemesanan', 'Pemesanan'),
        ('Setelmen', 'Setelmen'),
        ('Selesai', 'Selesai')
    ], string='Status Transaksi', default='Selesai')
