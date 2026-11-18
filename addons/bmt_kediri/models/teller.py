# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTTransaksiSetoran(models.Model):
    _name = 'bmt.transaksi.setoran'
    _description = 'Transaksi Setoran Kas'
    _rec_name = 'name'

    name = fields.Char('ID Setoran', required=True)
    no_rekening = fields.Many2one('bmt.rekening', string='No Rekening', required=True)
    id_teller = fields.Many2one('hr.employee', string='Teller')
    tanggal_waktu = fields.Datetime('Tanggal & Waktu', default=fields.Datetime.now)
    nominal = fields.Float('Nominal (Rp)', required=True)
    nama_penyetor = fields.Char('Nama Penyetor')
    saluran = fields.Selection([
        ('Loket', 'Loket'),
        ('Mobil Keliling', 'Mobil Keliling')
    ], string='Saluran', default='Loket')
    no_bukti = fields.Char('No Bukti')
    keterangan = fields.Text('Keterangan')


class BMTTransaksiPenarikan(models.Model):
    _name = 'bmt.transaksi.penarikan'
    _description = 'Transaksi Penarikan Kas'
    _rec_name = 'name'

    name = fields.Char('ID Penarikan', required=True)
    no_rekening = fields.Many2one('bmt.rekening', string='No Rekening', required=True)
    no_kartu = fields.Many2one('bmt.kartu.atm', string='Kartu ATM')
    id_teller = fields.Many2one('hr.employee', string='Teller')
    tanggal_waktu = fields.Datetime('Tanggal & Waktu', default=fields.Datetime.now)
    nominal = fields.Float('Nominal (Rp)', required=True)
    saluran = fields.Selection([
        ('Loket', 'Loket'),
        ('ATM', 'ATM'),
        ('Mobil Keliling', 'Mobil Keliling')
    ], string='Saluran', default='Loket')
    no_bukti = fields.Char('No Bukti')
    saldo_setelah_transaksi = fields.Float('Saldo Setelah Transaksi (Rp)')


class BMTTransaksiTransfer(models.Model):
    _name = 'bmt.transaksi.transfer'
    _description = 'Transaksi Transfer Dana'
    _rec_name = 'name'

    name = fields.Char('ID Transfer', required=True)
    no_rekening_asal = fields.Many2one('bmt.rekening', string='Rekening Asal', required=True)
    id_teller = fields.Many2one('hr.employee', string='Teller')
    bank_tujuan = fields.Char('Bank Tujuan', default='Bank Mandiri Taspen')
    no_rekening_tujuan = fields.Char('No Rekening Tujuan', required=True)
    nama_penerima = fields.Char('Nama Penerima', required=True)
    jenis_transfer = fields.Selection([
        ('Sesama Bank', 'Sesama Bank'),
        ('Antar Bank', 'Antar Bank')
    ], string='Jenis Transfer', default='Sesama Bank')
    nominal = fields.Float('Nominal (Rp)', required=True)
    biaya_transfer = fields.Float('Biaya Transfer (Rp)', default=0.0)
    tanggal_waktu = fields.Datetime('Tanggal & Waktu', default=fields.Datetime.now)
    berita = fields.Text('Berita / Berita Acara')
    no_bukti = fields.Char('No Bukti')
    status_transfer = fields.Selection([
        ('Berhasil', 'Berhasil'),
        ('Gagal', 'Gagal')
    ], string='Status Transfer', default='Berhasil')


class BMTPersediaanKas(models.Model):
    _name = 'bmt.persediaan.kas'
    _description = 'Persediaan Kas Teller'
    _rec_name = 'name'

    name = fields.Char('ID Persediaan Kas', required=True)
    id_teller = fields.Many2one('hr.employee', string='Teller', required=True)
    tanggal = fields.Date('Tanggal', default=fields.Date.context_today)
    saldo_awal_kas = fields.Float('Saldo Awal Kas (Rp)')
    total_setoran = fields.Float('Total Setoran (Rp)')
    total_penarikan = fields.Float('Total Penarikan (Rp)')
    saldo_akhir_sistem = fields.Float('Saldo Akhir Sistem (Rp)')
    saldo_fisik = fields.Float('Saldo Fisik (Rp)')
    selisih = fields.Float('Selisih (Rp)', default=0.0)
    keterangan_selisih = fields.Text('Keterangan Selisih')
