# -*- coding: utf-8 -*-
from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    id_karyawan_bmt = fields.Char('ID Karyawan BMT', index=True)
    nik = fields.Char('NIK', size=20)
    tempat_lahir = fields.Char('Tempat Lahir')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    jenis_kelamin = fields.Selection([
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan')
    ], string='Jenis Kelamin')
    pendidikan_terakhir = fields.Selection([
        ('SMA', 'SMA'),
        ('D3', 'D3'),
        ('S1', 'S1'),
        ('S2', 'S2')
    ], string='Pendidikan Terakhir')
    tanggal_masuk = fields.Date('Tanggal Masuk')
    status_kepegawaian = fields.Selection([
        ('Tetap', 'Tetap'),
        ('Kontrak', 'Kontrak')
    ], string='Status Kepegawaian', default='Tetap')
    status_karyawan_bmt = fields.Selection([
        ('Aktif', 'Aktif'),
        ('Resign', 'Resign'),
        ('PHK', 'PHK'),
        ('Nonaktif', 'Nonaktif')
    ], string='Status Karyawan', default='Aktif')
    no_rekening_gaji = fields.Char('No Rekening Gaji')
    npwp = fields.Char('NPWP')
    no_bpjs_kesehatan = fields.Char('No BPJS Kesehatan')
    no_bpjs_ketenagakerjaan = fields.Char('No BPJS Ketenagakerjaan')
