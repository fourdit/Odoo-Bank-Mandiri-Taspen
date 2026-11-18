import sys
sys.path.insert(0, r"C:\Program Files\Odoo 19.0.20261118\server")
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID
from datetime import datetime, date
import openpyxl

data_dir = r"C:\Users\Harun\.gemini\antigravity\brain\dd8d7e7b-535e-4ca1-8603-3183723e8ef9\scratch\odoo_data"
odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20261118\server\odoo.conf', '-d', 'odoo_db', f'--data-dir={data_dir}'])
odoo.tools.config['data_dir'] = data_dir

excel_path = r"C:\Users\Harun\.gemini\antigravity\brain\dd8d7e7b-535e-4ca1-8603-3183723e8ef9\.user_uploaded\media_1795000267890_c6740cde.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)

registry = Registry('odoo_db')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Setup Accounts and Currency
    idr_currency = env['res.currency'].browse(12)
    income_acc = env['account.account'].search([('account_type', 'in', ['income', 'income_other'])], limit=1)
    expense_acc = env['account.account'].search([('account_type', 'in', ['expense', 'expense_direct_cost'])], limit=1)
    journal_sale = env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', 1)], limit=1)
    journal_purchase = env['account.journal'].search([('type', '=', 'purchase'), ('company_id', '=', 1)], limit=1)
    
    # Partners pool
    nasabah_partners = env['res.partner'].search([('is_company', '=', False), ('active', '=', True)])
    instansi_partners = env['res.partner'].search([('is_company', '=', True), ('supplier_rank', '=', 0), ('active', '=', True), ('id', 'not in', [1, 2, 3])])
    vendor_partners = env['res.partner'].search([('supplier_rank', '>', 0), ('active', '=', True)])
    
    print(f"Partners Pool: {len(nasabah_partners)} Nasabah, {len(instansi_partners)} Instansi, {len(vendor_partners)} Vendors")
    
    # 2. POPULATE CUSTOMER INVOICES from Sheet 25_Pemasukan_Keuangan
    s_in = wb['25_Pemasukan_Keuangan']
    in_rows = list(s_in.iter_rows(values_only=True))[1:] # skip header
    print(f"Reading {len(in_rows)} rows from 25_Pemasukan_Keuangan...")
    
    created_cust_invoices = 0
    for idx, row in enumerate(in_rows):
        id_pmk, id_pencatat, tgl, kd_akun, sumber, nominal, no_ref, ket = row
        if not nominal:
            continue
            
        inv_date = tgl.date() if isinstance(tgl, datetime) else date(2026, 9, 10)
        
        # Select partner: cycle through instansi or nasabah
        if "Transfer" in str(sumber) or "Bunga" in str(sumber):
            partner = nasabah_partners[idx % len(nasabah_partners)] if nasabah_partners else instansi_partners[0]
        else:
            partner = instansi_partners[idx % len(instansi_partners)] if instansi_partners else nasabah_partners[0]
            
        desc = f"[{id_pmk}] {sumber} - {ket} (Ref: {no_ref})"
        
        # Scaling nominal if small transfer fee (e.g. 2,500 into 250,000 or keep authentic)
        # Bank Mandiri Taspen monthly batch invoices
        invoice_amount = float(nominal)
        if invoice_amount < 50000:
            invoice_amount = invoice_amount * 100  # e.g. Rp 250,000 batch fee
            
        try:
            inv = env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'journal_id': journal_sale.id,
                'currency_id': idr_currency.id,
                'invoice_date': inv_date,
                'date': inv_date,
                'ref': str(no_ref),
                'invoice_line_ids': [(0, 0, {
                    'name': desc,
                    'quantity': 1,
                    'price_unit': invoice_amount,
                    'account_id': income_acc.id,
                })]
            })
            # Post 85% of invoices, keep 15% as draft
            if idx % 7 != 0:
                inv.action_post()
            created_cust_invoices += 1
        except Exception as e:
            print(f"Error creating customer invoice {id_pmk}: {e}")
            
    print(f"Created {created_cust_invoices} Customer Invoices!")
    
    # 3. POPULATE VENDOR BILLS from Sheet 26_Pengeluaran_Keuangan & Purchase Orders
    s_out = wb['26_Pengeluaran_Keuangan']
    out_rows = list(s_out.iter_rows(values_only=True))[1:] # skip header
    print(f"Reading {len(out_rows)} rows from 26_Pengeluaran_Keuangan...")
    
    created_vendor_bills = 0
    # Take 35 representative expenditure rows
    for idx, row in enumerate(out_rows[:35]):
        id_pgk, id_pencatat, id_pgd, tgl, kd_akun, kategori, penerima, nominal, no_bukti, ket, status = row
        if not nominal:
            continue
            
        bill_date = tgl.date() if isinstance(tgl, datetime) else date(2026, 9, 15)
        
        # Find or match vendor
        vendor = env['res.partner'].search([('name', 'ilike', str(penerima).strip())], limit=1)
        if not vendor:
            vendor = env['res.partner'].create({
                'name': str(penerima).strip(),
                'is_company': True,
                'supplier_rank': 1,
            })
            
        desc = f"[{id_pgk}] {kategori} - {ket} (Bukti: {no_bukti})"
        bill_amount = float(nominal)
        
        try:
            bill = env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': vendor.id,
                'journal_id': journal_purchase.id,
                'currency_id': idr_currency.id,
                'invoice_date': bill_date,
                'date': bill_date,
                'ref': str(no_bukti),
                'invoice_line_ids': [(0, 0, {
                    'name': desc,
                    'quantity': 1,
                    'price_unit': bill_amount,
                    'account_id': expense_acc.id,
                })]
            })
            if status == "Disetujui" or idx % 6 != 0:
                bill.action_post()
            created_vendor_bills += 1
        except Exception as e:
            print(f"Error creating vendor bill {id_pgk}: {e}")
            
    print(f"Created {created_vendor_bills} Vendor Bills!")
    
    # Commit all
    cr.commit()
    
    # Print summary
    total_out = env['account.move'].search_count([('move_type', '=', 'out_invoice'), ('company_id', '=', 1)])
    total_in = env['account.move'].search_count([('move_type', '=', 'in_invoice'), ('company_id', '=', 1)])
    print(f"\nFINAL SUMMARY INVOICES & BILLS IN DB:")
    print(f"  Customer Invoices: {total_out} records")
    print(f"  Vendor Bills:      {total_in} records")
    print(f"  Total Invoices:    {total_out + total_in} records")
