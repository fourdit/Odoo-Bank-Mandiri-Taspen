import psycopg2

conn = psycopg2.connect(dbname='odoo_db', user='odoo', password='odoo', host='localhost', port=5432)
cur = conn.cursor()

# 1. Deactivate demo companies (ID Company & My Company (Chicago))
cur.execute("UPDATE res_company SET active = false WHERE id IN (2, 3);")
print("1. Deactivated demo companies 2 & 3 in res_company.")

# 2. Delete demo company relations for users so Odoo NEVER allows switching to Company 2 or 3
cur.execute("DELETE FROM res_company_users_rel WHERE cid IN (2, 3);")
print("2. Removed demo companies from res_company_users_rel.")

# 3. Ensure all users have company_id = 1
cur.execute("UPDATE res_users SET company_id = 1;")
print("3. Set default company_id = 1 for all res_users.")

# 4. Link User 2 (Rifky Aditya Harun) to Employee 23
cur.execute("UPDATE hr_employee SET user_id = NULL WHERE user_id = 2;")
cur.execute("""
    UPDATE hr_employee 
    SET user_id = 2, 
        name = 'Rifky Aditya Harun (Kepala Cabang)', 
        work_email = 'aditharun95@gmail.com', 
        company_id = 1,
        active = true 
    WHERE id = 23;
""")
print("4. Linked User 2 to Employee 23 (Rifky Aditya Harun).")

# 5. Validate all leave allocations and leaves
cur.execute("UPDATE hr_leave_allocation SET state = 'validate';")
cur.execute("UPDATE hr_leave SET state = 'validate';")
print("5. Validated all leave allocations and leaves.")

# 6. Insert approved leave for Employee 23
cur.execute("SELECT id FROM hr_leave WHERE employee_id = 23;")
existing = cur.fetchone()
if not existing:
    cur.execute("""
        INSERT INTO hr_leave (
            holiday_status_id, employee_id, employee_company_id, company_id,
            resource_calendar_id, create_uid, write_uid, private_name,
            state, duration_display, request_date_from_period, request_date_to_period,
            request_date_from, request_date_to, date_from, date_to,
            number_of_days, number_of_hours, request_hour_from, request_hour_to,
            user_id, create_date, write_date
        ) VALUES (
            1, 23, 1, 1,
            1, 1, 1, 'Cuti Tahunan - Koordinasi Kantor Wilayah BMT',
            'validate', '3 days', 'am', 'pm',
            '2026-11-24', '2026-11-26', '2026-11-24 07:00:00', '2026-11-26 16:00:00',
            3.0, 24.0, 8.0, 17.0,
            2, NOW(), NOW()
        );
    """)
    print("6. Created approved leave for Rifky Aditya Harun (Nov 24-26, 2026).")
else:
    print(f"6. Leave for Employee 23 already exists (id {existing[0]}).")

conn.commit()
print("\nAll database fixes committed successfully!")
