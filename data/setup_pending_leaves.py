import psycopg2

conn = psycopg2.connect(dbname='odoo_db', user='odoo', password='odoo', host='localhost', port=5432)
cur = conn.cursor()

# 1. Set Rifky Aditya Harun (id=23, user_id=2) as manager for all active BMT employees
cur.execute("UPDATE hr_employee SET parent_id = 23, leave_manager_id = 2 WHERE id != 23 AND active = true;")
print("1. Set Kepala Cabang (user 2, emp 23) as leave manager for all employees.")

# 2. Add 3 pending leave requests with state = 'confirm'
pending_leaves = [
    (24, 'Cuti Tahunan - Urusan Keluarga Mendesak', '2026-11-27', '2026-11-28', 2.0, 16.0),
    (25, 'Cuti Ibadah / Keagamaan', '2026-11-25', '2026-11-27', 3.0, 24.0),
    (26, 'Cuti Tahunan - Menghadiri Acara Keluarga', '2026-11-30', '2026-12-01', 2.0, 16.0),
]

for emp_id, reason, d_from, d_to, days, hours in pending_leaves:
    cur.execute("""
        INSERT INTO hr_leave (
            holiday_status_id, employee_id, employee_company_id, company_id,
            resource_calendar_id, create_uid, write_uid, private_name,
            state, duration_display, request_date_from_period, request_date_to_period,
            request_date_from, request_date_to, date_from, date_to,
            number_of_days, number_of_hours, request_hour_from, request_hour_to,
            user_id, create_date, write_date
        ) VALUES (
            1, %s, 1, 1,
            1, 1, 1, %s,
            'confirm', %s, 'am', 'pm',
            %s, %s, %s, %s,
            %s, %s, 8.0, 17.0,
            NULL, NOW(), NOW()
        );
    """, (
        emp_id, reason, f"{int(days)} days",
        d_from, d_to, f"{d_from} 07:00:00", f"{d_to} 16:00:00",
        days, hours
    ))
    print(f"Added pending leave for employee {emp_id}: {reason}")

conn.commit()

# Check leaves now
cur.execute("SELECT id, employee_id, state, private_name FROM hr_leave ORDER BY id;")
rows = cur.fetchall()
print(f"\nTotal leaves in database now: {len(rows)}")
for r in rows:
    print(" ", r)
