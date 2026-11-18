# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_nasabah = fields.Char('ID Nasabah', index=True)
    id_instansi = fields.Char('ID Instansi', index=True)
    id_supplier_bmt = fields.Char('ID Supplier BMT', index=True)
    
    nik = fields.Char('NIK', size=20)
    tempat_lahir = fields.Char('Tempat Lahir')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    jenis_kelamin = fields.Selection([
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan')
    ], string='Jenis Kelamin')
    
    pekerjaan = fields.Char('Pekerjaan')
    nama_ibu_kandung = fields.Char('Nama Ibu Kandung')
    jenis_nasabah = fields.Selection([
        ('Pensiunan', 'Pensiunan'),
        ('UMKM', 'UMKM'),
        ('Umum', 'Umum')
    ], string='Jenis Nasabah', default='Umum')
    no_pensiun = fields.Char('No Pensiun')
    status_prioritas = fields.Selection([
        ('Reguler', 'Reguler'),
        ('Prioritas', 'Prioritas')
    ], string='Status Prioritas', default='Reguler')
    tanggal_registrasi = fields.Date('Tanggal Registrasi', default=fields.Date.context_today)
    status_nasabah = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif')
    ], string='Status Nasabah', default='Aktif')
    
    is_nasabah = fields.Boolean('Is Nasabah', default=False)
    is_instansi = fields.Boolean('Is Instansi', default=False)
    
    jenis_instansi = fields.Selection([
        ('Pemerintah', 'Pemerintah'),
        ('BUMN', 'BUMN'),
        ('Swasta', 'Swasta'),
        ('Sekolah', 'Sekolah')
    ], string='Jenis Instansi')
    nama_penanggung_jawab = fields.Char('Penanggung Jawab')
    jumlah_pegawai = fields.Integer('Jumlah Pegawai')
    
    kategori_barang = fields.Char('Kategori Barang')
    nama_kontak = fields.Char('Nama Kontak')
    status_supplier = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif')
    ], string='Status Supplier', default='Aktif')
