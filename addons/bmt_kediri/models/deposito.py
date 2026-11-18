# -*- coding: utf-8 -*-
from odoo import models, fields

class BMTDeposito(models.Model):
    _name = 'bmt.deposito'
    _description = 'Deposito Berjangka'
    _rec_name = 'name'

    name = fields.Char('No Bilyet Deposito', required=True)
    no_rekening_sumber = fields.Many2one('bmt.rekening', string='Rekening Sumber', required=True)
    nasabah_id = fields.Many2one('res.partner', string='Nasabah', related='no_rekening_sumber.nasabah_id', store=True)
    id_suku_bunga = fields.Many2one('bmt.suku.bunga', string='Suku Bunga Acuan')
    id_cs = fields.Many2one('hr.employee', string='Customer Service')
    nominal_penempatan = fields.Float('Nominal Penempatan (Rp)', required=True)
    tenor_bulan = fields.Integer('Tenor (Bulan)', default=12)
    suku_bunga_persen = fields.Float('Suku Bunga (% p.a.)', default=5.0)
    tanggal_mulai = fields.Date('Tanggal Mulai', default=fields.Date.context_today)
    tanggal_jatuh_tempo = fields.Date('Tanggal Jatuh Tempo')
    opsi_perpanjangan = fields.Selection([
        ('ARO', 'ARO (Automatic Roll Over)'),
        ('Non-ARO', 'Non-ARO')
    ], string='Opsi Perpanjangan', default='Non-ARO')
    status_deposito = fields.Selection([
        ('Draft', 'Draft'),
        ('Aktif', 'Aktif'),
        ('Cair', 'Cair / Ditutup')
    ], string='Status Deposito', default='Aktif')
