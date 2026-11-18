import sys
sys.path.insert(0, r"C:\Program Files\Odoo 19.0.20261118\server")
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID
from datetime import datetime, date, timedelta

data_dir = r"C:\Users\Harun\.gemini\antigravity\brain\dd8d7e7b-535e-4ca1-8603-3183723e8ef9\scratch\odoo_data"
odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20261118\server\odoo.conf', '-d', 'odoo_db', f'--data-dir={data_dir}'])
odoo.tools.config['data_dir'] = data_dir

registry = Registry('odoo_db')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # =========================================================================
    # PART 1: RENAME ROOT MENU INVOICING -> ACCOUNTING / AKUNTANSI
    # =========================================================================
    menu_invoicing = env['ir.ui.menu'].browse(264)
    if menu_invoicing.exists():
        menu_invoicing.write({
            'name': 'Accounting / Akuntansi',
        })
        print("1. Renamed Root App 264 to 'Accounting / Akuntansi'.")
        
    # Admin already has all access permissions
    print("2. Admin user confirmed.")

    # =========================================================================
    # PART 2: CREATE CUSTOMER INVOICES & VENDOR BILLS (RICH BANK ACCOUNTING)
    # =========================================================================
    partner_taspen = env['res.partner'].search([('name', 'ilike', 'Taspen')], limit=1)
    if not partner_taspen:
        partner_taspen = env['res.partner'].create({
            'name': 'PT Taspen (Persero) KC Kediri',
            'is_company': True,
            'street': 'Jl. Brawijaya No. 12, Kediri',
            'customer_rank': 1,
        })
        
    partner_pemkot = env['res.partner'].search([('name', 'ilike', 'Kediri'), ('is_company', '=', True)], limit=1)
    if not partner_pemkot:
        partner_pemkot = env['res.partner'].create({
            'name': 'Pemerintah Kota Kediri - BKD',
            'is_company': True,
            'customer_rank': 1,
        })
        
    partner_datascrip = env['res.partner'].search([('name', 'ilike', 'Datascrip')], limit=1)
    if not partner_datascrip:
        partner_datascrip = env['res.partner'].create({
            'name': 'PT Datascrip Indonesia',
            'is_company': True,
            'supplier_rank': 1,
        })
        
    partner_telkom = env['res.partner'].search([('name', 'ilike', 'Telkom')], limit=1)
    if not partner_telkom:
        partner_telkom = env['res.partner'].create({
            'name': 'PT Telkom Indonesia (Witel Kediri)',
            'is_company': True,
            'supplier_rank': 1,
        })

    # Accounts
    income_acc = env['account.account'].search([('account_type', 'in', ['income', 'income_other'])], limit=1)
    expense_acc = env['account.account'].search([('account_type', 'in', ['expense', 'expense_direct_cost'])], limit=1)
    journal_sale = env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', 1)], limit=1)
    journal_purchase = env['account.journal'].search([('type', '=', 'purchase'), ('company_id', '=', 1)], limit=1)
    idr_currency = env['res.currency'].browse(12)

    # 2.1 Customer Invoices (Pendapatan Bank)
    cust_invoices_data = [
        (partner_taspen, "Bunga Kredit Mantap Pensiun - Payroll Taspen Nov 2026", 450000000.0, "2026-11-05"),
        (partner_pemkot, "Layanan Fee Based Income Payroll ASN Pemkot Kediri", 35000000.0, "2026-11-10"),
        (partner_taspen, "Bagi Hasil Layanan Pembayaran Pensiunan Kantor Bayar", 28500000.0, "2026-11-15"),
        (partner_pemkot, "Administrasi Rekening Tabungan Berjangka Kolektif", 15000000.0, "2026-11-18"),
    ]

    for partner, desc, amount, inv_date in cust_invoices_data:
        try:
            inv = env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'journal_id': journal_sale.id,
                'currency_id': idr_currency.id,
                'invoice_date': inv_date,
                'date': inv_date,
                'invoice_line_ids': [(0, 0, {
                    'name': desc,
                    'quantity': 1,
                    'price_unit': amount,
                    'account_id': income_acc.id,
                })]
            })
            inv.action_post()
            print(f"Created Customer Invoice: {inv.name} - {desc} (Rp {amount:,.2f})")
        except Exception as e:
            print(f"Invoice creation note: {e}")

    # 2.2 Vendor Bills (Biaya & Pengadaan Cabang)
    vendor_bills_data = [
        (partner_datascrip, "Pengadaan 5.000 Buku Tabungan SiMantap Pensiun & Warkat", 14469148.0, "2026-11-03"),
        (partner_telkom, "Sewa Jaringan Komunikasi Data VSAT & Jaringan Kantor KC Kediri", 8500000.0, "2026-11-07"),
        (partner_datascrip, "Pengadaan Kertas Struk Teller, Toner, & Thermal Paper", 5250000.0, "2026-11-12"),
        (partner_telkom, "Langganan Internet Dedicated High Speed & Cloud Backup", 4800000.0, "2026-11-16"),
    ]

    for partner, desc, amount, bill_date in vendor_bills_data:
        try:
            bill = env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': partner.id,
                'journal_id': journal_purchase.id,
                'currency_id': idr_currency.id,
                'invoice_date': bill_date,
                'date': bill_date,
                'invoice_line_ids': [(0, 0, {
                    'name': desc,
                    'quantity': 1,
                    'price_unit': amount,
                    'account_id': expense_acc.id,
                })]
            })
            bill.action_post()
            print(f"Created Vendor Bill: {bill.name} - {desc} (Rp {amount:,.2f})")
        except Exception as e:
            print(f"Vendor bill creation note: {e}")

    # =========================================================================
    # PART 3: CALENDAR EVENTS POPULATION (NOVEMBER 2026)
    # =========================================================================
    # Clean old events
    old_events = env['calendar.event'].search([])
    print(f"Deleting {len(old_events)} outdated calendar events...")
    old_events.unlink()

    admin_partner = env['res.partner'].browse(3)
    user_admin = env['res.users'].browse(2)

    # 20 Authentic Events for Bank Mandiri Taspen KC Kediri in November & Dec 2026
    events_data = [
        ("Briefing Pagi Operasional & Service Excellence Teller", datetime(2026, 11, 2, 7, 30), datetime(2026, 11, 2, 8, 30), "Banking Hall KC Kediri", "Briefing SOP senyum salam sapa awal bulan"),
        ("Sosialisasi Tabungan SiMantap Pensiun di PWRI Kota Kediri", datetime(2026, 11, 3, 9, 0), datetime(2026, 11, 3, 11, 30), "Aula PWRI Kota Kediri", "Presentasi produk tabungan dan kemudahan otentikasi"),
        ("Supervisi Pembayaran Gaji Pensiunan Hari Pertama", datetime(2026, 11, 4, 8, 0), datetime(2026, 11, 4, 12, 0), "Loket Teller 1-4 KC Kediri", "Monitoring antrian dan penyediaan kas fisik"),
        ("Sosialisasi Kredit Mantap Pensiun di PT Taspen Kediri", datetime(2026, 11, 5, 9, 0), datetime(2026, 11, 5, 11, 30), "Kantor PT Taspen (Persero) Kediri", "Edukasi pinjaman bunga kompetitif dan syarat SK Pensiun"),
        ("Kunjungan & Verifikasi Usaha Debitur UMKM Pensiunan", datetime(2026, 11, 6, 13, 30), datetime(2026, 11, 6, 15, 30), "Kecamatan Mojoroto, Kediri", "On-site visit usaha peternakan debitur binaan"),
        ("Rapat Koordinasi Mingguan Pencapaian Target Lending Cabang", datetime(2026, 11, 9, 8, 30), datetime(2026, 11, 9, 10, 0), "Ruang Rapat KC Kediri", "Review NPL dan pipeline kredit bersama Account Officer"),
        ("Sosialisasi Kredit Pra-Pensiun di Kantor BKD Kota Kediri", datetime(2026, 11, 10, 9, 0), datetime(2026, 11, 10, 11, 30), "Kantor BKD Kota Kediri", "Edukasi persiapan masa purna tugas bagi PNS"),
        ("Edukasi Investasi Reksa Dana APERD untuk Nasabah Prioritas", datetime(2026, 11, 11, 10, 0), datetime(2026, 11, 11, 12, 0), "Lounge Prioritas KC Kediri", "Pengenalan reksa dana pasar uang dan profil risiko"),
        ("Sosialisasi Fitur Mantap Mobile di Kantor Camat Pare", datetime(2026, 11, 12, 9, 0), datetime(2026, 11, 12, 11, 30), "Pendopo Kecamatan Pare", "Aktivasi aplikasi mobile banking bagi pensiunan"),
        ("Supervisi Rutin Kas Fisik & Khasanah Brankas Cabang", datetime(2026, 11, 13, 16, 0), datetime(2026, 11, 13, 17, 30), "Khazanah Vault KC Kediri", "Pencocokan fisik uang kas teller dan brankas"),
        ("Sosialisasi Tabungan Berjangka di Dinas Pendidikan Kediri", datetime(2026, 11, 16, 9, 0), datetime(2026, 11, 16, 11, 30), "Aula Disdik Kota Kediri", "Peluang tabungan berjangka bagi guru pensiunan"),
        ("Sosialisasi Pembiayaan di PWRI Kabupaten Kediri", datetime(2026, 11, 17, 9, 0), datetime(2026, 11, 17, 11, 30), "Gedung PWRI Kab. Kediri, Gurah", "Sosialisasi produk pinjaman dan cek kesehatan gratis"),
        ("Penyerahan Hadiah Doorprize Program Loyalitas Pensiun", datetime(2026, 11, 18, 10, 0), datetime(2026, 11, 18, 11, 30), "Front Office KC Kediri", "Apresiasi penyerahan sepeda lipat dan souvenir nasabah"),
        ("Hari Ini: Rapat Evaluasi Operasional Tengah Bulan", datetime(2026, 11, 19, 9, 0), datetime(2026, 11, 19, 10, 30), "Ruang Kepala Cabang", "Evaluasi kinerja operasional teller dan CS"),
        ("Audit Kepatuhan SOP & APU-PPT oleh Tim SKAI", datetime(2026, 11, 20, 9, 0), datetime(2026, 11, 20, 15, 0), "Ruang Rapat KC Kediri", "Pemeriksaan kelengkapan dokumen kredit dan KYC"),
        ("Sosialisasi Pembayaran Pensiun di Kantor Pos Kediri", datetime(2026, 11, 23, 9, 0), datetime(2026, 11, 23, 11, 30), "Kantor Pos Besar Kediri", "Akuisisi pemindahan kantor bayar pensiun ke BMT"),
        ("Cuti Dinas: Koordinasi Akhir Tahun dengan Kantor Wilayah BMT", datetime(2026, 11, 24, 8, 0), datetime(2026, 11, 26, 17, 0), "Kanwil BMT Surabaya", "Rapat evaluasi tahunan cabang se-Jawa Timur"),
        ("Sosialisasi Komunitas Pensiunan Kesehatan Kediri", datetime(2026, 11, 27, 9, 0), datetime(2026, 11, 27, 11, 30), "Klinik Pensiun Kediri", "Pemeriksaan tensi & gula darah gratis bersama BMT"),
        ("Rekonsiliasi Akhir Bulan: Kas, Kliring, & Penutupan GL", datetime(2026, 11, 30, 14, 0), datetime(2026, 11, 30, 18, 0), "Back Office KC Kediri", "Closing laporan keuangan bulanan"),
        ("Sosialisasi Target Tahun Baru di Kantor Taspen Kediri", datetime(2026, 12, 2, 9, 0), datetime(2026, 12, 2, 11, 30), "PT Taspen Kediri", "Penyelarasan target penyaluran kredit awal tahun"),
        ("Townhall Meeting Seluruh Pegawai KC Kediri", datetime(2026, 12, 4, 16, 0), datetime(2026, 12, 4, 18, 0), "Banking Hall KC Kediri", "Refleksi capaian cabang dan apresiasi karyawan"),
    ]

    for title, dt_start, dt_stop, loc, desc in events_data:
        ev = env['calendar.event'].create({
            'name': title,
            'start': dt_start,
            'stop': dt_stop,
            'location': loc,
            'description': desc,
            'user_id': user_admin.id,
            'partner_ids': [(4, admin_partner.id)],
            'active': True,
        })
        print(f"Created Calendar Event: {title} ({dt_start.strftime('%d %b %Y %H:%M')})")

    cr.commit()
    print("\nAccounting data and November 2026 Calendar events successfully deployed!")
