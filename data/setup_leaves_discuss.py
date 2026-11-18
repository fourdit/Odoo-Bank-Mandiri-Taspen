import sys
sys.path.insert(0, r"C:\Program Files\Odoo 19.0.20261118\server")
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID
from datetime import date, timedelta

data_dir = r"C:\Users\Harun\.gemini\antigravity\brain\dd8d7e7b-535e-4ca1-8603-3183723e8ef9\scratch\odoo_data"
odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20261118\server\odoo.conf', '-d', 'odoo_db', f'--data-dir={data_dir}'])
odoo.tools.config['data_dir'] = data_dir

registry = Registry('odoo_db')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Clean demo leaves & allocations via SQL
    cr.execute("DELETE FROM hr_leave;")
    cr.execute("DELETE FROM hr_leave_allocation;")
    cr.commit()
    print("Purged old demo leaves and allocations.")
    
    # 2. Get BMT Employees
    bmt_employees = env['hr.employee'].search([('active', '=', True)], order="id asc")
    print(f"Found {len(bmt_employees)} active BMT employees.")
    
    # Find Leave Type: ID Annual Leaves or Paid Time Off
    paid_leave_type = env['hr.leave.type'].search([('name', 'ilike', 'Paid Time Off')], limit=1)
    if not paid_leave_type:
        paid_leave_type = env['hr.leave.type'].search([('name', 'ilike', 'Annual')], limit=1)
    
    sick_leave_type = env['hr.leave.type'].search([('name', 'ilike', 'Sick Time Off')], limit=1)
    if not sick_leave_type:
        sick_leave_type = env['hr.leave.type'].search([('name', 'ilike', 'Sick')], limit=1)
        
    print(f"Using Leave Types: Paid='{paid_leave_type.name}', Sick='{sick_leave_type.name}'")
    
    # Create 12 days annual leave allocation for active BMT employees
    for emp in bmt_employees[:20]:
        alloc = env['hr.leave.allocation'].create({
            'name': f"Hak Cuti Tahunan 2026 - {emp.name}",
            'employee_id': emp.id,
            'holiday_status_id': paid_leave_type.id,
            'number_of_days': 12,
        })
        try:
            alloc.action_validate()
        except Exception:
            pass
    print("Created annual leave allocations for BMT employees.")
    
    # Create realistic approved leaves for several BMT staff
    sample_leaves = [
        (bmt_employees[1], paid_leave_type, date(2026, 11, 10), date(2026, 11, 12), "Cuti Keperluan Keluarga di Surabaya"),
        (bmt_employees[2], sick_leave_type, date(2026, 11, 5), date(2026, 11, 6), "Sakit Demam (Surat Dokter Terlampir)"),
        (bmt_employees[3], paid_leave_type, date(2026, 11, 16), date(2026, 11, 17), "Cuti Menghadiri Wisuda Adik"),
        (bmt_employees[4], sick_leave_type, date(2026, 11, 12), date(2026, 11, 13), "Istirahat Medis Pasca Pengobatan"),
        (bmt_employees[5], paid_leave_type, date(2026, 11, 20), date(2026, 11, 21), "Cuti Tahunan Pribadi"),
    ]
    
    for emp, l_type, d_from, d_to, desc in sample_leaves:
        try:
            days = (d_to - d_from).days + 1
            l = env['hr.leave'].create({
                'name': desc,
                'employee_id': emp.id,
                'holiday_status_id': l_type.id,
                'request_date_from': d_from,
                'request_date_to': d_to,
                'number_of_days': days,
            })
            l.action_validate()
        except Exception as e:
            print(f"Note creating leave for {emp.name}: {e}")
    print("Created 5 realistic leaves for BMT employees.")
    
    # 3. Clean and configure Discuss Channels
    # Rename channel 1 (general)
    general_channel = env['discuss.channel'].browse(1)
    if general_channel.exists():
        general_channel.write({
            'name': 'kc-kediri-pengumuman',
            'description': 'Saluran Resmi Pengumuman & Koordinasi Bank Mandiri Taspen KC Kediri',
        })
        
    # Archive/Unlink other demo channels
    other_demo_channels = env['discuss.channel'].search([
        ('id', '!=', 1),
        ('name', 'in', ['sales', 'board-meetings', 'rd', 'Welcome to the #general channel', 'Ideas & Suggestions', 'Troubleshooting', 'Public Community'])
    ])
    for c in other_demo_channels:
        try:
            c.unlink()
        except Exception:
            pass
        
    # Create official BMT discuss channels
    bmt_channels_data = [
        ('operasional-teller-cs', 'Koordinasi Operasional Teller, Customer Service, dan Kas Kantor KC Kediri'),
        ('marketing-kredit-dana', 'Pemasaran Kredit Mantap Pensiun, Deposito, dan Penjualan Reksa Dana'),
        ('sdm-umum-logistik', 'Pengelolaan SDM, Cuti, Pengadaan Warkat/Buku Tabungan, dan Aset Kantor'),
        ('it-helpdesk-support', 'Pelaporan Gangguan Jaringan, Core Banking, Mesin ATM, dan Mantap Mobile'),
    ]
    
    for ch_name, ch_desc in bmt_channels_data:
        existing = env['discuss.channel'].search([('name', '=', ch_name)], limit=1)
        if not existing:
            ch = env['discuss.channel'].create({
                'name': ch_name,
                'description': ch_desc,
                'channel_type': 'channel',
            })
            # Post welcome message
            ch.message_post(
                body=f"<b>[Sistem BMT KC Kediri]</b> Saluran <i>#{ch_name}</i> telah diaktifkan untuk: {ch_desc}. Silakan gunakan saluran ini untuk koordinasi resmi internal cabang.",
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
            )
            print(f"Created Discuss Channel: #{ch_name}")
            
    # Post broadcast on kc-kediri-pengumuman
    if general_channel.exists():
        general_channel.message_post(
            body="""<b>[PENGUMUMAN RESMI KEPALA CABANG]</b><br/>
            Selamat datang di Sistem ERP Terintegrasi Bank Mandiri Taspen KC Kediri (Odoo 19).<br/>
            Seluruh data nasabah pensiunan, layanan loket teller, warkat buku tabungan/ATM, evaluasi kinerja, hingga presensi harian telah terintegrasi penuh.<br/>
            Mari tingkatkan Service Excellence demi melayani para pensiunan dan nasabah UMKM Kota Kediri.<br/>
            <i>- Rifky Aditya Harun, Kepala Cabang KC Kediri</i>""",
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        print("Posted announcement on #kc-kediri-pengumuman.")

    cr.commit()
    print("Time Off and Discuss channels setup completed successfully!")
