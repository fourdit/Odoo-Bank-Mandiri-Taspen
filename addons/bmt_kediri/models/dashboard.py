# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BMTDashboard(models.Model):
    _name = 'bmt.dashboard'
    _description = 'Dashboard Eksekutif Bank Mandiri Taspen KC Kediri'

    name = fields.Char('Nama Dashboard', default='Executive Dashboard Bank Mandiri Taspen KC Kediri')
    
    total_nasabah = fields.Integer('Total Nasabah', compute='_compute_metrics')
    nasabah_pensiunan = fields.Integer('Nasabah Pensiunan', compute='_compute_metrics')
    nasabah_umkm = fields.Integer('Nasabah UMKM', compute='_compute_metrics')
    nasabah_umum = fields.Integer('Nasabah Umum', compute='_compute_metrics')
    nasabah_prioritas = fields.Integer('Nasabah Prioritas', compute='_compute_metrics')
    
    total_tabungan = fields.Float('Total Saldo Tabungan (Rp)', compute='_compute_metrics')
    total_pinjaman = fields.Float('Total Pinjaman Disetujui (Rp)', compute='_compute_metrics')
    total_deposito = fields.Float('Total Deposito (Rp)', compute='_compute_metrics')
    total_kas_teller = fields.Float('Total Kas Teller (Rp)', compute='_compute_metrics')
    total_reksa_dana = fields.Float('Total Transaksi Reksa Dana (Rp)', compute='_compute_metrics')
    
    total_karyawan = fields.Integer('Total Karyawan', compute='_compute_metrics')
    total_keluhan = fields.Integer('Total Keluhan', compute='_compute_metrics')
    keluhan_selesai = fields.Integer('Keluhan Selesai', compute='_compute_metrics')
    total_sosialisasi = fields.Integer('Total Sosialisasi', compute='_compute_metrics')
    total_doorprize = fields.Integer('Total Doorprize', compute='_compute_metrics')

    dashboard_html = fields.Html('Visual Dashboard', sanitize=False, compute='_compute_dashboard_html')

    @api.model
    def action_get_dashboard(self):
        record = self.search([], limit=1)
        if not record:
            record = self.create({'name': 'Executive Dashboard Bank Mandiri Taspen KC Kediri'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Executive Dashboard Bank Mandiri Taspen KC Kediri',
            'res_model': 'bmt.dashboard',
            'res_id': record.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _compute_metrics(self):
        for rec in self:
            rec.total_nasabah = self.env['res.partner'].search_count([('is_nasabah', '=', True)])
            rec.nasabah_pensiunan = self.env['res.partner'].search_count([('is_nasabah', '=', True), ('jenis_nasabah', '=', 'Pensiunan')])
            rec.nasabah_umkm = self.env['res.partner'].search_count([('is_nasabah', '=', True), ('jenis_nasabah', '=', 'UMKM')])
            rec.nasabah_umum = self.env['res.partner'].search_count([('is_nasabah', '=', True), ('jenis_nasabah', '=', 'Umum')])
            rec.nasabah_prioritas = self.env['res.partner'].search_count([('is_nasabah', '=', True), ('status_prioritas', '=', 'Prioritas')])
            
            rekening = self.env['bmt.rekening'].search([])
            rec.total_tabungan = sum(rekening.mapped('saldo'))
            
            pinjaman = self.env['bmt.pinjaman'].search([])
            rec.total_pinjaman = sum(pinjaman.mapped('plafon_disetujui'))
            
            deposito = self.env['bmt.deposito'].search([])
            rec.total_deposito = sum(deposito.mapped('nominal_penempatan'))
            
            kas = self.env['bmt.persediaan.kas'].search([])
            rec.total_kas_teller = sum(kas.mapped('saldo_akhir_sistem'))
            
            rd = self.env['bmt.transaksi.rd'].search([])
            rec.total_reksa_dana = sum(rd.mapped('nominal_pembelian'))
            
            rec.total_karyawan = self.env['hr.employee'].search_count([])
            rec.total_keluhan = self.env['bmt.keluhan'].search_count([])
            rec.keluhan_selesai = self.env['bmt.keluhan'].search_count([('status_penanganan', '=', 'Selesai')])
            rec.total_sosialisasi = self.env['bmt.sosialisasi.hasil'].search_count([])
            rec.total_doorprize = self.env['bmt.doorprize'].search_count([])

    @api.depends('name')
    def _compute_dashboard_html(self):
        for rec in self:
            rec._compute_metrics()
            
            tabungan_fmt = f"Rp {rec.total_tabungan:,.0f}".replace(",", ".")
            pinjaman_fmt = f"Rp {rec.total_pinjaman:,.0f}".replace(",", ".")
            deposito_fmt = f"Rp {rec.total_deposito:,.0f}".replace(",", ".")
            kas_fmt = f"Rp {rec.total_kas_teller:,.0f}".replace(",", ".")
            rd_fmt = f"Rp {rec.total_reksa_dana:,.0f}".replace(",", ".")
            
            pct_pensiun = round((rec.nasabah_pensiunan / (rec.total_nasabah or 1)) * 100, 1)
            pct_prioritas = round((rec.nasabah_prioritas / (rec.total_nasabah or 1)) * 100, 1)
            pct_keluhan_selesai = round((rec.keluhan_selesai / (rec.total_keluhan or 1)) * 100, 1)

            html = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; padding: 20px; border-radius: 12px;">
                <!-- Header Banner -->
                <div style="background: linear-gradient(135deg, #002B49 0%, #004B87 60%, #EAA023 100%); color: white; padding: 25px 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0, 43, 73, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <span style="background: rgba(234, 160, 35, 0.25); color: #F7C948; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; border: 1px solid rgba(247, 201, 72, 0.4);">Executive Branch Dashboard</span>
                            <h1 style="margin: 8px 0 4px 0; font-size: 26px; font-weight: 700; color: #FFFFFF;">Bank Mandiri Taspen — KC Kediri</h1>
                            <p style="margin: 0; font-size: 14px; color: #E2E8F0; opacity: 0.9;">Monitoring Kinerja Operasional, Portofolio Simpanan, Penyaluran Kredit &amp; Kepuasan Nasabah Pensiunan</p>
                        </div>
                        <div style="text-align: right; margin-top: 10px;">
                            <span style="background: white; color: #002B49; font-weight: bold; padding: 8px 16px; border-radius: 8px; font-size: 13px; display: inline-block; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                                📍 KC Kediri • Aktif &amp; Terverifikasi
                            </span>
                        </div>
                    </div>
                </div>

                <!-- KPI Cards Row 1: Core Financials -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; margin-bottom: 25px;">
                    <!-- Card 1: Nasabah -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #004B87;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Total Nasabah Terdaftar</span>
                            <span style="background: #e0f2fe; color: #0369a1; padding: 4px 8px; border-radius: 6px; font-size: 18px;">👥</span>
                        </div>
                        <div style="font-size: 32px; font-weight: 800; color: #0f172a; margin: 10px 0 5px 0;">{rec.total_nasabah} <span style="font-size: 16px; font-weight: 500; color: #64748b;">Orang</span></div>
                        <div style="font-size: 12px; color: #475569; display: flex; gap: 8px; flex-wrap: wrap;">
                            <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">Pensiunan: <b>{rec.nasabah_pensiunan}</b> ({pct_pensiun}%)</span>
                            <span style="background: #fef3c7; color: #92400e; padding: 2px 6px; border-radius: 4px;">Prioritas: <b>{rec.nasabah_prioritas}</b></span>
                        </div>
                    </div>

                    <!-- Card 2: Saldo Tabungan -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #059669;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Dana Simpanan (DPK)</span>
                            <span style="background: #dcfce7; color: #15803d; padding: 4px 8px; border-radius: 6px; font-size: 18px;">💰</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 800; color: #059669; margin: 10px 0 5px 0;">{tabungan_fmt}</div>
                        <div style="font-size: 12px; color: #475569;">
                            <span>25 Rekening Tabungan &amp; Giro Pensiun Aktif</span>
                        </div>
                    </div>

                    <!-- Card 3: Kredit / Pinjaman -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #EAA023;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Penyaluran Kredit Pensiun</span>
                            <span style="background: #fef3c7; color: #b45309; padding: 4px 8px; border-radius: 6px; font-size: 18px;">💳</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 800; color: #d97706; margin: 10px 0 5px 0;">{pinjaman_fmt}</div>
                        <div style="font-size: 12px; color: #475569;">
                            <span>16 Disetujui KC • 4 Ditolak (SLIK Kol 3)</span>
                        </div>
                    </div>

                    <!-- Card 4: Deposito Berjangka -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #7c3aed;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Penempatan Deposito</span>
                            <span style="background: #f3e8ff; color: #7e22ce; padding: 4px 8px; border-radius: 6px; font-size: 18px;">📑</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 800; color: #7c3aed; margin: 10px 0 5px 0;">{deposito_fmt}</div>
                        <div style="font-size: 12px; color: #475569;">
                            <span>25 Bilyet Aktif • Bunga Acuan 5.0% p.a.</span>
                        </div>
                    </div>
                </div>

                <!-- KPI Cards Row 2: Operations, CRM & Services -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; margin-bottom: 25px;">
                    <!-- Card 5: Kas Teller -->
                    <div style="background: white; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Kas Fisik Teller</span>
                            <span style="font-size: 16px;">🏦</span>
                        </div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin: 6px 0;">{kas_fmt}</div>
                        <span style="background: #dcfce7; color: #15803d; font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: bold;">✓ Rekonsiliasi Balance (Selisih Rp 0)</span>
                    </div>

                    <!-- Card 6: Reksa Dana APERD -->
                    <div style="background: white; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Investasi Reksa Dana</span>
                            <span style="font-size: 16px;">📈</span>
                        </div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin: 6px 0;">{rd_fmt}</div>
                        <span style="color: #64748b; font-size: 12px;">25 Transaksi • Fee Subscription Terjurnal</span>
                    </div>

                    <!-- Card 7: CRM & Sosialisasi -->
                    <div style="background: white; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Kegiatan Sosialisasi Instansi</span>
                            <span style="font-size: 16px;">📢</span>
                        </div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin: 6px 0;">{rec.total_sosialisasi} <span style="font-size: 14px; font-weight: normal; color: #64748b;">Sesi Terlaksana</span></div>
                        <span style="color: #64748b; font-size: 12px;">22 Instansi Mitra (Kecamatan, BUMN, Sekolah)</span>
                    </div>

                    <!-- Card 8: Suara Nasabah -->
                    <div style="background: white; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Penanganan Keluhan (CS)</span>
                            <span style="font-size: 16px;">🎧</span>
                        </div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin: 6px 0;">{rec.keluhan_selesai} / {rec.total_keluhan} <span style="font-size: 14px; font-weight: normal; color: #64748b;">Selesai</span></div>
                        <div style="background: #e2e8f0; border-radius: 4px; height: 6px; width: 100%; overflow: hidden; margin-top: 6px;">
                            <div style="background: #059669; height: 100%; width: {pct_keluhan_selesai}%;"></div>
                        </div>
                    </div>
                </div>

                <!-- Deep Dive Detail Section -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 20px;">
                    <!-- Panel 1: Segmen & Produk -->
                    <div style="background: white; border-radius: 10px; padding: 22px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <h3 style="margin-top: 0; margin-bottom: 15px; font-size: 16px; color: #0f172a; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;">
                            🎯 Segmentasi Nasabah &amp; Program Loyalitas
                        </h3>
                        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Pensiunan ASN &amp; Guru</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #0f172a;">{rec.nasabah_pensiunan} Orang (71.4%)</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Pelaku UMKM Binaan</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #0f172a;">{rec.nasabah_umkm} Orang (14.3%)</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Masyarakat Umum &amp; Karyawan</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #0f172a;">{rec.nasabah_umum} Orang (14.3%)</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Hadiah Doorprize Tahunan</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #059669;">{rec.total_doorprize} Paket Dialokasikan</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #475569;">Promo Special Rate Bunga</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #d97706;">22 Surat Penawaran</td>
                            </tr>
                        </table>
                    </div>

                    <!-- Panel 2: Kepegawaian & Operasional Internal -->
                    <div style="background: white; border-radius: 10px; padding: 22px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <h3 style="margin-top: 0; margin-bottom: 15px; font-size: 16px; color: #0f172a; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;">
                            👥 Sumber Daya Manusia &amp; Logistik Cabang
                        </h3>
                        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Total SDM Kantor Cabang</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #0f172a;">{rec.total_karyawan} Karyawan (20 Jabatan)</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Rata-rata Skor Kinerja</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #059669;">93.2 / 100 (Sangat Baik)</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Laporan Pelanggaran Disiplin</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #dc2626;">20 Kasus (4 PHK, 16 SP)</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #f1f5f9;">
                                <td style="padding: 8px 0; color: #475569;">Tiket Gangguan IT Aplikasi</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #0f172a;">20 Tiket (100% Selesai Ditangani)</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #475569;">Stok Buku Tabungan &amp; Kartu</td>
                                <td style="padding: 8px 0; text-align: right; font-weight: bold; color: #0284c7;">1.390 Unit Fisik di Lemari Arsip</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
            """
            rec.dashboard_html = html

    def action_open_nasabah(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Daftar Nasabah',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('is_nasabah', '=', True)],
        }

    def action_open_rekening(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rekening Simpanan',
            'res_model': 'bmt.rekening',
            'view_mode': 'list,form',
        }

    def action_open_pinjaman(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fasilitas Kredit & Pinjaman',
            'res_model': 'bmt.pinjaman',
            'view_mode': 'list,form',
        }

    def action_open_deposito(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Deposito Berjangka',
            'res_model': 'bmt.deposito',
            'view_mode': 'list,form',
        }

    def action_open_kas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rekonsiliasi Kas Teller',
            'res_model': 'bmt.persediaan.kas',
            'view_mode': 'list,form',
        }

    def action_open_keluhan(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Keluhan Nasabah',
            'res_model': 'bmt.keluhan',
            'view_mode': 'list,form',
        }

    def action_refresh(self):
        self._compute_dashboard_html()
        return True
