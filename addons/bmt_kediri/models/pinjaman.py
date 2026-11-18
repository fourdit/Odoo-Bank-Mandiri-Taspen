# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BMTPinjaman(models.Model):
    _name = 'bmt.pinjaman'
    _description = 'Fasilitas Pinjaman / Kredit'
    _rec_name = 'name'

    name = fields.Char('No Pinjaman', required=True)
    nasabah_id = fields.Many2one('res.partner', string='Nasabah', required=True)
    id_suku_bunga = fields.Many2one('bmt.suku.bunga', string='Suku Bunga Acuan')
    jenis_pinjaman = fields.Selection([
        ('Pensiun', 'Kredit Pensiun'),
        ('Mikro', 'Kredit Mikro'),
        ('Retail', 'Kredit Retail')
    ], string='Jenis Pinjaman', default='Pensiun', required=True)
    tanggal_pengajuan = fields.Date('Tanggal Pengajuan', default=fields.Date.context_today)
    tujuan_pinjaman = fields.Text('Tujuan Pinjaman')
    status_kelengkapan_berkas = fields.Selection([
        ('Lengkap', 'Lengkap'),
        ('Belum Lengkap', 'Belum Lengkap')
    ], string='Kelengkapan Berkas', default='Lengkap')
    plafon_diajukan = fields.Float('Plafon Diajukan (Rp)')
    plafon_disetujui = fields.Float('Plafon Disetujui (Rp)')
    tenor_bulan = fields.Integer('Tenor (Bulan)', default=36)
    suku_bunga_persen = fields.Float('Suku Bunga (% p.a.)', default=8.5)
    angsuran_per_bulan = fields.Float('Angsuran per Bulan (Rp)', compute='_compute_angsuran', store=True)
    status_pinjaman = fields.Selection([
        ('Diajukan', 'Diajukan'),
        ('Ditolak', 'Ditolak'),
        ('Disetujui', 'Disetujui (KC)'),
        ('Aktif', 'Aktif / Dicairkan'),
        ('Lunas', 'Lunas')
    ], string='Status Pinjaman', default='Diajukan')
    alasan_penolakan = fields.Text('Alasan Penolakan')
    no_surat_perjanjian = fields.Char('No SPK / Perjanjian')
    tanggal_perjanjian = fields.Date('Tanggal Perjanjian')
    tanggal_pencairan = fields.Date('Tanggal Pencairan')
    id_cs_pemeriksa = fields.Many2one('hr.employee', string='CS Pemeriksa')
    id_verifikator = fields.Many2one('hr.employee', string='Verifikator')
    id_penyetuju = fields.Many2one('hr.employee', string='Penyetuju (Kepala Cabang)')

    @api.depends('plafon_disetujui', 'plafon_diajukan', 'tenor_bulan', 'suku_bunga_persen')
    def _compute_angsuran(self):
        for rec in self:
            plafon = rec.plafon_disetujui or rec.plafon_diajukan
            if plafon and rec.tenor_bulan:
                pokok = plafon / rec.tenor_bulan
                bunga_bulan = (plafon * (rec.suku_bunga_persen / 100.0)) / 12.0
                rec.angsuran_per_bulan = round(pokok + bunga_bulan, 2)
            else:
                rec.angsuran_per_bulan = 0.0

    def action_approve(self):
        self.status_pinjaman = 'Disetujui'

    def action_disburse(self):
        self.status_pinjaman = 'Aktif'
