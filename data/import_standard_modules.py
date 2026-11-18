import sys, os, datetime
sys.path.insert(0, r"C:\Program Files\Odoo 19.0.20261118\server")

import openpyxl
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

# Script: import_standard_modules.py
# Membersihkan seluruh data demo bawaan Odoo dan mempopulasikan modul-modul standar
# (CRM, Purchase, Inventory, Maintenance, HR Attendance, Recruitment, Calendar, eLearning, Accounting)
# dengan data simulasi Bank Mandiri Taspen KC Kediri.

script_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(script_dir, "data_simulasi_bmt_kediri.xlsx")
if not os.path.exists(xlsx_path):
    xlsx_path = r'C:/Users/Harun/.gemini/antigravity/brain/dd8d7e7b-535e-4ca1-8603-3183723e8ef9/.user_uploaded/media_1795000267890_c6740cde.xlsx'

wb = openpyxl.load_workbook(xlsx_path, data_only=True)

def get_sheet_data(sheet_name):
    for name in wb.sheetnames:
        if sheet_name.lower() in name.lower():
            sh = wb[name]
            rows = list(sh.iter_rows(values_only=True))
            if not rows: return []
            headers = [str(h).strip() if h else '' for h in rows[0]]
            data = []
            for r in rows[1:]:
                if not any(r): continue
                row_dict = {}
                for i, h in enumerate(headers):
                    if h:
                        val = r[i] if i < len(r) else None
                        if isinstance(val, datetime.datetime):
                            val = val.date()
                        row_dict[h] = val
                data.append(row_dict)
            return data
    return []

data_dir = r"C:\Users\Harun\.gemini\antigravity\brain\dd8d7e7b-535e-4ca1-8603-3183723e8ef9\scratch\odoo_data"
os.makedirs(data_dir, exist_ok=True)
odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20261118\server\odoo.conf', '-d', 'odoo_db', f'--data-dir={data_dir}'])
odoo.tools.config['data_dir'] = data_dir

registry = Registry('odoo_db')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    print("==================================================")
    print("STEP 1: PEMBERSIHAN DATA DEMO BAWAAN ODOO")
    print("==================================================")

    if 'maintenance.request' in env:
        reqs = env['maintenance.request'].search([])
        print(f"Menghapus {len(reqs)} Maintenance Requests...")
        reqs.unlink()

    if 'maintenance.equipment' in env:
        eqs = env['maintenance.equipment'].search([])
        print(f"Menghapus {len(eqs)} Maintenance Equipments...")
        eqs.unlink()

    if 'crm.lead' in env:
        leads = env['crm.lead'].search([])
        print(f"Menghapus {len(leads)} demo CRM leads...")
        leads.unlink()

    if 'purchase.order' in env:
        pos = env['purchase.order'].search([])
        print(f"Menghapus {len(pos)} demo Purchase Orders...")
        for po in pos:
            try:
                po.button_cancel()
                po.unlink()
            except Exception: pass

    if 'hr.applicant' in env:
        apps = env['hr.applicant'].search([])
        print(f"Menghapus {len(apps)} demo HR Applicants...")
        apps.unlink()

    if 'hr.attendance' in env:
        atts = env['hr.attendance'].search([])
        print(f"Menghapus {len(atts)} demo Attendances...")
        atts.unlink()

    if 'calendar.event' in env:
        events = env['calendar.event'].search([])
        print(f"Menghapus {len(events)} demo Calendar Events...")
        events.unlink()

    if 'slide.slide' in env:
        slides = env['slide.slide'].search([])
        print(f"Menghapus {len(slides)} demo Slides...")
        slides.unlink()
    if 'slide.channel' in env:
        channels = env['slide.channel'].search([])
        print(f"Menghapus {len(channels)} demo eLearning Channels...")
        channels.unlink()

    if 'account.move' in env:
        moves = env['account.move'].search([])
        print(f"Mereset & Menghapus {len(moves)} demo Account Moves...")
        for m in moves:
            try:
                m.button_draft()
                m.unlink()
            except Exception: pass

    # Clean/Archive Products non-BMT
    bmt_prods = env['product.template'].search([('default_code', '!=', False)])
    if bmt_prods:
        bmt_prods.unlink()
    demo_prods = env['product.template'].search([('active', '=', True)])
    print(f"Mengarsipkan {len(demo_prods)} demo products bawaan...")
    demo_prods.write({'active': False})

    # Archive Demo Users & Demo Partners
    demo_users = env['res.users'].search([('login', 'in', ['demo', 'portal'])])
    if demo_users:
        demo_users.write({'active': False})

    demo_partners = env['res.partner'].search([
        ('is_nasabah', '=', False),
        ('is_instansi', '=', False),
        ('id_supplier_bmt', '=', False),
        ('user_ids', '=', False),
        ('name', 'not in', ['OdooBot', 'Administrator', 'My Company', 'Bank Mandiri Taspen'])
    ])
    print(f"Mengarsipkan {len(demo_partners)} demo Partners kontak bawaan...")
    demo_partners.write({'active': False})

    cr.commit()
    print(">>> Data demo bawaan Odoo berhasil dibersihkan!\n")

    print("==================================================")
    print("STEP 2: POPULASI DATA SIMULASI BANK MANDIRI TASPEN")
    print("==================================================")

    emp_map = {e.id_karyawan_bmt: e.id for e in env['hr.employee'].search([('id_karyawan_bmt', '!=', False)])}
    instansi_map = {p.id_instansi: p.id for p in env['res.partner'].search([('is_instansi', '=', True)])}
    supplier_map = {p.id_supplier_bmt: p.id for p in env['res.partner'].search([('id_supplier_bmt', '!=', False)])}
    admin_user = env.ref('base.user_admin').id

    # 1. CRM
    calon_data = get_sheet_data('Calon_Nasabah')
    stage_qual = env['crm.stage'].search([('name', '=', 'Qualified')], limit=1).id or 2
    stage_prop = env['crm.stage'].search([('name', '=', 'Proposition')], limit=1).id or 3
    stage_won = env['crm.stage'].search([('name', '=', 'Won')], limit=1).id or 4

    for d in calon_data:
        code = d.get('id_calon_nasabah')
        name = d.get('nama_lengkap')
        produk = d.get('produk_diminati')
        status = d.get('status_tindak_lanjut')
        stg = stage_won if status == 'Menjadi Nasabah' else (stage_prop if status == 'Dalam Proses' else stage_qual)
        probability = 100.0 if status == 'Menjadi Nasabah' else (70.0 if status == 'Dalam Proses' else 30.0)
        rev = 75000000.0 if 'Kredit' in str(produk) or 'Pinjaman' in str(produk) else 25000000.0

        env['crm.lead'].create({
            'name': f"Prospek {produk} - {name} [{code}]",
            'partner_name': name,
            'contact_name': name,
            'phone': str(d.get('no_telepon') or ''),
            'street': d.get('alamat'),
            'type': 'opportunity',
            'stage_id': stg,
            'probability': probability,
            'expected_revenue': rev,
            'user_id': admin_user,
            'description': f"CALON NASABAH BANK MANDIRI TASPEN KC KEDIRI\nID: {code}\nNIK: {d.get('nik')}\nProduk: {produk}\nStatus: {status}",
        })
    print(f"-> CRM: Memasukkan {len(calon_data)} Calon Nasabah ke CRM Pipeline.")

    # 2. Inventory / Products
    inv_data = get_sheet_data('Inventaris')
    buku_data = get_sheet_data('Persediaan_Buku_ATM')
    prod_map = {}
    for d in inv_data:
        code = d.get('kode_barang')
        name = d.get('nama_barang')
        merek = d.get('merek')
        harga = float(d.get('nilai_perolehan') or 0.0)
        p = env['product.template'].create({
            'name': f"{name} - {merek}",
            'default_code': code,
            'list_price': harga,
            'standard_price': harga,
            'type': 'consu',
            'active': True,
            'description': f"Aset KC Kediri: {d.get('kategori')} | Lokasi: {d.get('lokasi_penempatan')}",
        })
        prod_map[code] = p.product_variant_id.id

    for d in buku_data:
        code = d.get('id_persediaan')
        jns = d.get('jenis_persediaan')
        p = env['product.template'].create({
            'name': f"Warkat: {jns} [{code}]",
            'default_code': code,
            'list_price': 15000.0,
            'standard_price': 10000.0,
            'type': 'consu',
            'active': True,
            'description': f"Jenis Persediaan BMT: {jns}",
        })
        prod_map[code] = p.product_variant_id.id
    print(f"-> Inventory: Memasukkan {len(inv_data) + len(buku_data)} Katalog Aset & Warkat.")

    # 3. Maintenance Equipment & Requests
    equip_map = {}
    for d in inv_data:
        code = d.get('kode_barang')
        name = d.get('nama_barang')
        merek = d.get('merek')
        eq = env['maintenance.equipment'].create({
            'name': f"{name} ({merek})",
            'serial_no': code,
            'model': merek,
            'cost': float(d.get('nilai_perolehan') or 0.0),
            'assign_date': d.get('tanggal_perolehan'),
            'note': f"<p>Aset: {d.get('kategori')}<br/>Lokasi: {d.get('lokasi_penempatan')}<br/>Kondisi: {d.get('kondisi')}</p>",
        })
        equip_map[code] = eq.id

    it_data = get_sheet_data('Pengaduan_Aplikasi')
    m_stage_new = env['maintenance.stage'].search([('name', 'ilike', 'New')], limit=1).id or 1
    m_stage_done = env['maintenance.stage'].search([('name', 'ilike', 'Repaired')], limit=1).id or 3
    for idx, d in enumerate(it_data):
        code = d.get('id_pengaduan')
        judul = d.get('judul_masalah') or d.get('jenis_aplikasi') or 'Gangguan Sistem'
        stg = m_stage_done if d.get('status_penanganan') == 'Selesai' else m_stage_new
        eq_id = list(equip_map.values())[idx % len(equip_map)] if equip_map else False
        env['maintenance.request'].create({
            'name': f"[{code}] {judul} ({d.get('jenis_aplikasi')})",
            'equipment_id': eq_id,
            'request_date': d.get('tanggal_pengaduan'),
            'stage_id': stg,
            'description': f"ID Pengaduan: {code}\nUser: {d.get('id_karyawan')}\nAplikasi: {d.get('jenis_aplikasi')}\nSolusi: {d.get('tindakan_perbaikan')}",
        })
    print(f"-> Maintenance: Memasukkan {len(equip_map)} Peralatan & {len(it_data)} Tiket Pemeliharaan.")

    # 4. Purchase
    po_data = get_sheet_data('Pengadaan')
    for d in po_data:
        code = d.get('id_pengadaan')
        supp_id = supplier_map.get(d.get('id_supplier')) or list(supplier_map.values())[0] if supplier_map else env.user.partner_id.id
        prod_var_id = prod_map.get(d.get('kode_barang')) or list(prod_map.values())[0]
        dt_plan = d.get('tanggal_persetujuan') or d.get('tanggal_pengajuan') or datetime.date.today()
        if isinstance(dt_plan, datetime.date) and not isinstance(dt_plan, datetime.datetime):
            dt_plan = datetime.datetime.combine(dt_plan, datetime.time(9, 0))
        order_line = [(0, 0, {
            'product_id': prod_var_id,
            'name': f"Pengadaan Barang {d.get('kode_barang')}",
            'product_qty': float(d.get('jumlah') or 1.0),
            'price_unit': float(d.get('harga_satuan') or 0.0),
            'date_planned': dt_plan,
        })]
        po = env['purchase.order'].create({
            'partner_id': supp_id,
            'origin': f"BMT-{code} / Permintaan {d.get('id_permintaan')}",
            'date_order': d.get('tanggal_pengajuan'),
            'order_line': order_line,
        })
        if d.get('status_persetujuan') == 'Disetujui':
            try: po.button_confirm()
            except: pass
    print(f"-> Purchase: Memasukkan {len(po_data)} Pesanan Pengadaan Supplier.")

    # 5. Attendances
    pres_data = get_sheet_data('Presensi')
    att_count = 0
    for d in pres_data:
        emp_id = emp_map.get(d.get('id_karyawan'))
        tgl = d.get('tanggal')
        if emp_id and tgl and d.get('status_kehadiran') == 'Hadir':
            jam_m = d.get('jam_masuk') or '08:00:00'
            jam_p = d.get('jam_pulang') or '17:00:00'
            try:
                h_in, m_in = int(str(jam_m).split(':')[0]), int(str(jam_m).split(':')[1])
                h_out, m_out = int(str(jam_p).split(':')[0]), int(str(jam_p).split(':')[1])
                dt_in = datetime.datetime.combine(tgl, datetime.time(max(0, h_in - 7), m_in))
                dt_out = datetime.datetime.combine(tgl, datetime.time(max(0, h_out - 7), m_out))
                env['hr.attendance'].create({'employee_id': emp_id, 'check_in': dt_in, 'check_out': dt_out})
                att_count += 1
            except: pass
    print(f"-> Attendance: Memasukkan {att_count} Rekaman Presensi Karyawan.")

    # 6. Calendar Events
    jadwal_data = get_sheet_data('Jadwal_Sosialisasi')
    for d in jadwal_data:
        code = d.get('id_jadwal_sosialisasi')
        tgl = d.get('tanggal_pelaksanaan')
        if tgl:
            dt_start = datetime.datetime.combine(tgl, datetime.time(2, 0))
            dt_stop = datetime.datetime.combine(tgl, datetime.time(5, 0))
            inst_partner_id = instansi_map.get(d.get('id_instansi'))
            partner_ids = [env.user.partner_id.id]
            if inst_partner_id: partner_ids.append(inst_partner_id)
            env['calendar.event'].create({
                'name': f"Sosialisasi Taspen: {d.get('materi')} [{code}]",
                'start': dt_start,
                'stop': dt_stop,
                'location': d.get('lokasi'),
                'partner_ids': [(6, 0, partner_ids)],
                'description': f"Instansi Mitra: {d.get('id_instansi')}\nMateri: {d.get('materi')}",
            })
    print(f"-> Calendar: Memasukkan {len(jadwal_data)} Jadwal Sosialisasi.")

    # 7. Recruitment Applicants
    pelamar_data = get_sheet_data('Calon_Karyawan')
    job_default = env['hr.job'].search([], limit=1).id
    stage_signed = env['hr.recruitment.stage'].search([('name', 'ilike', 'Signed')], limit=1).id or 6
    stage_init = env['hr.recruitment.stage'].search([('name', 'ilike', 'Initial')], limit=1).id or 1
    for d in pelamar_data:
        code = d.get('id_pelamar')
        name = d.get('nama_lengkap')
        stg = stage_signed if d.get('status_akhir') == 'Diterima' else stage_init
        env['hr.applicant'].create({
            'partner_name': f"{name} ({code})",
            'email_from': d.get('email'),
            'partner_phone': str(d.get('no_telepon') or ''),
            'job_id': job_default,
            'stage_id': stg,
            'applicant_notes': f"<p>ID: {code}<br/>NIK: {d.get('nik')}<br/>Pendidikan: {d.get('pendidikan_terakhir')}<br/>Status: {d.get('status_akhir')}</p>",
        })
    print(f"-> Recruitment: Memasukkan {len(pelamar_data)} Calon Pegawai.")

    # 8. eLearning Channels
    if 'slide.channel' in env:
        prog_data = get_sheet_data('Program_Pelatihan')
        for d in prog_data:
            code = d.get('id_program')
            name = d.get('nama_program')
            env['slide.channel'].create({
                'name': f"BMT Academy: {name} [{code}]",
                'description': f"Program Pengembangan SDM KC Kediri\nTrainer: {d.get('nama_trainer')}\nBiaya: Rp {float(d.get('biaya_pelatihan') or 0):,.0f}",
                'channel_type': 'training',
            })
        print(f"-> eLearning: Memasukkan {len(prog_data)} Program Pelatihan.")

    # 9. Accounting General Ledger
    bmt_coa = [
        ('1.101', 'Kas Operasional Cabang & Teller', 'asset_cash'),
        ('1.102', 'Penempatan BI & Giro Bank Lain', 'asset_current'),
        ('1.201', 'Portofolio Kredit Mantap Pensiun', 'asset_current'),
        ('2.101', 'Simpanan Tabungan SiMantap', 'liability_current'),
        ('2.102', 'Deposito Berjangka Nasabah', 'liability_current'),
        ('4.101', 'Pendapatan Bunga Kredit Pensiun', 'income'),
        ('4.102', 'Pendapatan Fee & Administrasi', 'income_other'),
        ('5.101', 'Beban Pengadaan & Inventaris Cabang', 'expense'),
        ('5.201', 'Beban Gaji & Tunjangan Pegawai', 'expense'),
        ('5.301', 'Beban Pelatihan & Operasional Kantor', 'expense'),
    ]
    coa_map = {}
    for code, name, atype in bmt_coa:
        acc = env['account.account'].search([('code', '=', code)], limit=1)
        if not acc:
            acc = env['account.account'].create({'code': code, 'name': name, 'account_type': atype})
        coa_map[code] = acc.id
        coa_map[code.replace('.', '-')] = acc.id
        coa_map[code.replace('.', '')] = acc.id

    fallback_acc = list(coa_map.values())[0]
    misc_journal = env['account.journal'].search([('type', '=', 'general')], limit=1)
    jrn_data = get_sheet_data('Jurnal_Keuangan')
    jrn_by_bukti = {}
    for d in jrn_data:
        bukti = d.get('no_bukti') or 'MISC'
        if bukti not in jrn_by_bukti:
            jrn_by_bukti[bukti] = []
        jrn_by_bukti[bukti].append(d)

    posted_moves = 0
    for bukti, lines in list(jrn_by_bukti.items())[:60]:
        tgl = lines[0].get('tanggal_jurnal') or datetime.date(2026, 9, 30)
        move_lines = []
        for line in lines:
            c_code = str(line.get('kode_akun') or '')
            acc_id = coa_map.get(c_code) or fallback_acc
            deb = float(line.get('debit') or 0.0)
            crd = float(line.get('kredit') or line.get('credit') or 0.0)
            move_lines.append((0, 0, {
                'name': line.get('keterangan') or f"Transaksi {bukti}",
                'account_id': acc_id,
                'debit': deb,
                'credit': crd,
            }))
        tot_deb = round(sum(l[2]['debit'] for l in move_lines), 2)
        tot_crd = round(sum(l[2]['credit'] for l in move_lines), 2)
        if tot_deb == tot_crd and tot_deb > 0:
            try:
                move = env['account.move'].create({
                    'ref': f"BMT/{bukti}",
                    'date': tgl,
                    'journal_id': misc_journal.id,
                    'line_ids': move_lines,
                })
                move.action_post()
                posted_moves += 1
            except: pass
    print(f"-> Accounting: Memposting {posted_moves} Entri Buku Besar (General Ledger).")

    cr.commit()
    print("==================================================")
    print(">>> SELURUH MODUL STANDAR SUDAH TERPOPULASI! <<<")
    print("==================================================")
