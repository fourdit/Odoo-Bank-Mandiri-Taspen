# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BMTRekening(models.Model):
    _name = 'bmt.rekening'
    _description = 'Rekening Simpanan Nasabah'
    _rec_name = 'name'

    name = fields.Char('No Rekening', required=True, copy=False)
    nasabah_id = fields.Many2one('res.partner', string='Nasabah', required=True)
    jenis_rekening = fields.Selection([
        ('Tabungan', 'Tabungan'),
        ('Giro', 'Giro')
    ], string='Jenis Rekening', default='Tabungan', required=True)
    nama_produk = fields.Char('Nama Produk', default='Tabungan Pensiun (Simulasi)')
    tanggal_pembukaan = fields.Date('Tanggal Pembukaan', default=fields.Date.context_today)
    setoran_awal = fields.Float('Setoran Awal (Rp)', default=0.0)
    saldo = fields.Float('Saldo Saat Ini (Rp)', default=0.0)
    saldo_minimum = fields.Float('Saldo Minimum (Rp)', default=50000.0)
    status_rekening = fields.Selection([
        ('Draft', 'Draft (Verifikasi)'),
        ('Aktif', 'Aktif'),
        ('Dormant', 'Dormant'),
        ('Blokir', 'Blokir'),
        ('Closed', 'Closed (Ditutup)')
    ], string='Status Rekening', default='Aktif')
    
    id_cs_pembuka = fields.Many2one('hr.employee', string='CS Pembuka')
    id_penyetuju = fields.Many2one('hr.employee', string='Penyetuju (Operation Manager)')
    tanggal_penutupan = fields.Date('Tanggal Penutupan')
    biaya_penutupan = fields.Float('Biaya Penutupan (Rp)', default=0.0)
    alasan_penutupan = fields.Text('Alasan Penutupan')

    def action_approve(self):
        self.status_rekening = 'Aktif'

    def action_close(self):
        self.status_rekening = 'Closed'


class BMTKartuATM(models.Model):
    _name = 'bmt.kartu.atm'
    _description = 'Kartu ATM Nasabah'
    _rec_name = 'name'

    name = fields.Char('No Kartu ATM', required=True)
    rekening_id = fields.Many2one('bmt.rekening', string='No Rekening', required=True)
    nasabah_id = fields.Many2one('res.partner', string='Nasabah', related='rekening_id.nasabah_id', store=True)
    jenis_kartu = fields.Selection([
        ('Debit Silver', 'Debit Silver'),
        ('Debit Gold', 'Debit Gold')
    ], string='Jenis Kartu', default='Debit Silver')
    tanggal_terbit = fields.Date('Tanggal Terbit', default=fields.Date.context_today)
    masa_berlaku = fields.Date('Masa Berlaku')
    pin_terenkripsi = fields.Char('PIN Terenkripsi')
    batas_tarik_harian = fields.Float('Batas Tarik Harian (Rp)', default=5000000.0)
    status_kartu = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Blokir', 'Blokir'),
        ('Kedaluwarsa', 'Kedaluwarsa')
    ], string='Status Kartu', default='Aktif')
    id_cs = fields.Many2one('hr.employee', string='Customer Service')


class BMTLayananDigital(models.Model):
    _name = 'bmt.layanan.digital'
    _description = 'Layanan Digital Banking'
    _rec_name = 'name'

    name = fields.Char('ID Layanan', required=True)
    nasabah_id = fields.Many2one('res.partner', string='Nasabah', required=True)
    rekening_id = fields.Many2one('bmt.rekening', string='Rekening')
    jenis_layanan = fields.Selection([
        ('Mobile Banking', 'Mobile Banking'),
        ('Internet Banking', 'Internet Banking')
    ], string='Jenis Layanan', required=True)
    user_id = fields.Char('User ID Layanan')
    no_hp_terdaftar = fields.Char('No HP Terdaftar')
    email_terdaftar = fields.Char('Email Terdaftar')
    tanggal_pengajuan = fields.Date('Tanggal Pengajuan')
    hasil_verifikasi_identitas = fields.Selection([
        ('Lolos', 'Lolos'),
        ('Tidak Lolos', 'Tidak Lolos')
    ], string='Verifikasi Identitas', default='Lolos')
    tanggal_aktivasi = fields.Date('Tanggal Aktivasi')
    status_layanan = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif')
    ], string='Status Layanan', default='Aktif')
    id_cs = fields.Many2one('hr.employee', string='Customer Service')
    id_pengaktivasi = fields.Many2one('hr.employee', string='Otorisator (Operation Manager)')
