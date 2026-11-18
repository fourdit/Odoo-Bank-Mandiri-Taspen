import psycopg2

conn = psycopg2.connect(dbname='odoo_db', user='odoo', password='odoo', host='localhost', port=5432)
cur = conn.cursor()

# 1. Update IDR currency settings in res_currency
cur.execute("""
    UPDATE res_currency 
    SET symbol = 'Rp', 
        position = 'before', 
        active = true,
        full_name = 'Indonesian Rupiah'
    WHERE id = 12;
""")
print("1. Configured IDR (id 12) with symbol 'Rp' and position 'before'.")

# 2. Update company currency to IDR
cur.execute("UPDATE res_company SET currency_id = 12 WHERE id = 1;")
print("2. Set Bank Mandiri Taspen KC Kediri base currency to IDR.")

# 3. Update account_move and account_move_line
cur.execute("UPDATE account_move SET currency_id = 12 WHERE company_id = 1;")
cur.execute("UPDATE account_move_line SET currency_id = 12, company_currency_id = 12 WHERE company_id = 1;")
print("3. Updated account moves and journal lines to IDR.")

# 4. Update purchase orders
cur.execute("UPDATE purchase_order SET currency_id = 12 WHERE company_id = 1;")
cur.execute("UPDATE product_supplierinfo SET currency_id = 12;")
print("4. Updated purchase orders and vendor pricelists to IDR.")

# 5. Configure currency rates for Company 1
# Remove old IDR rates for company 1
cur.execute("DELETE FROM res_currency_rate WHERE company_id = 1 AND currency_id = 12;")
# Insert base rate for IDR = 1.0
cur.execute("""
    INSERT INTO res_currency_rate (currency_id, rate, name, company_id, create_date, write_date, create_uid, write_uid)
    VALUES (12, 1.0, '2020-01-01', 1, NOW(), NOW(), 1, 1);
""")
# Update USD rate to market exchange (1 USD = ~15,800 IDR -> rate = 0.00006329)
cur.execute("UPDATE res_currency_rate SET rate = 0.00006329 WHERE company_id = 1 AND currency_id = 1;")
print("5. Configured IDR base rate = 1.0 and USD exchange rate for KC Kediri.")

conn.commit()

# Verify
cur.execute("SELECT c.name, cur.name, cur.symbol FROM res_company c JOIN res_currency cur ON c.currency_id = cur.id WHERE c.id = 1;")
print("\nVerified Company Currency:", cur.fetchall())

cur.execute("SELECT id, name, currency_id FROM purchase_order WHERE company_id = 1 LIMIT 3;")
print("Sample Purchase Orders:", cur.fetchall())

cur.execute("SELECT id, name, currency_id FROM account_move WHERE company_id = 1 LIMIT 3;")
print("Sample Account Moves:", cur.fetchall())
