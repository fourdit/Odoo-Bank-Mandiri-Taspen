import sys, os, datetime
sys.path.insert(0, r"C:\Program Files\Odoo 19.0.20261118\server")

import openpyxl
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

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
    print("--- STARTING IMPORT ---")

    # Mappings
    emp_map = {}     # 'KAR001': employee_id
    partner_map = {} # 'NSB001': partner_id, 'INS001': partner_id
    rek_map = {}     # 'REK001': rekening_id
    bunga_map = {}   # 'SB001': bunga_id
    rd_prod_map = {} # 'PRD001': prod_id
    rso_map = {}     # 'RSO001': rso_id
    jso_map = {}     # 'JSO001': jso_id
    plg_map = {}     # 'PLG001': plg_id
    trm_map = {}     # 'TRM001': trm_id

    # 1. Jabatan -> hr.job
    jabatan_data = get_sheet_data('Jabatan')
    job_map = {}
    for d in jabatan_data:
        j_id = d.get('id_jabatan')
        j_name = d.get('nama_jabatan')
        job = env['hr.job'].search([('name', '=', j_name)], limit=1)
        if not job:
            job = env['hr.job'].create({'name': j_name})
        job_map[j_id] = job.id
    print(f"Loaded {len(job_map)} Jabatan / Jobs")

    # 2. Karyawan -> hr.employee
    karyawan_data = get_sheet_data('Karyawan')
    for d in karyawan_data:
        kar_code = d.get('id_karyawan')
        existing = env['hr.employee'].search([('id_karyawan_bmt', '=', kar_code)], limit=1)
        vals = {
            'name': d.get('nama_lengkap'),
            'id_karyawan_bmt': kar_code,
            'job_id': job_map.get(d.get('id_jabatan')),
            'nik': str(d.get('nik') or ''),
            'tempat_lahir': d.get('tempat_lahir'),
            'tanggal_lahir': d.get('tanggal_lahir'),
            'jenis_kelamin': d.get('jenis_kelamin'),
            'work_phone': str(d.get('no_telepon') or ''),
            'work_email': d.get('email'),
            'pendidikan_terakhir': d.get('pendidikan_terakhir'),
            'tanggal_masuk': d.get('tanggal_masuk'),
            'status_kepegawaian': d.get('status_kepegawaian'),
            'status_karyawan_bmt': d.get('status_karyawan'),
            'no_rekening_gaji': str(d.get('no_rekening_gaji') or ''),
            'npwp': str(d.get('npwp') or ''),
            'no_bpjs_kesehatan': str(d.get('no_bpjs_kesehatan') or ''),
            'no_bpjs_ketenagakerjaan': str(d.get('no_bpjs_ketenagakerjaan') or ''),
        }
        if existing:
            existing.write(vals)
            emp = existing
        else:
            emp = env['hr.employee'].create(vals)
        emp_map[kar_code] = emp.id
    print(f"Loaded {len(emp_map)} Employees")

    # 3. Instansi -> res.partner
    instansi_data = get_sheet_data('Instansi')
    for d in instansi_data:
        code = d.get('id_instansi')
        existing = env['res.partner'].search([('id_instansi', '=', code)], limit=1)
        vals = {
            'name': d.get('nama_instansi'),
            'id_instansi': code,
            'is_instansi': True,
            'is_company': True,
            'jenis_instansi': d.get('jenis_instansi'),
            'street': d.get('alamat'),
            'city': d.get('kota'),
            'phone': str(d.get('no_telepon') or ''),
            'email': d.get('email'),
            'nama_penanggung_jawab': d.get('nama_penanggung_jawab'),
            'jumlah_pegawai': d.get('jumlah_pegawai') or 0,
        }
        if existing:
            existing.write(vals)
            p = existing
        else:
            p = env['res.partner'].create(vals)
        partner_map[code] = p.id
    print(f"Loaded {len(instansi_data)} Instansi")

    # 4. Supplier -> res.partner
    supplier_data = get_sheet_data('Supplier')
    for d in supplier_data:
        code = d.get('id_supplier')
        existing = env['res.partner'].search([('id_supplier_bmt', '=', code)], limit=1)
        vals = {
            'name': d.get('nama_supplier'),
            'id_supplier_bmt': code,
            'is_company': True,
            'supplier_rank': 1,
            'kategori_barang': d.get('kategori_barang'),
            'street': d.get('alamat'),
            'city': d.get('kota'),
            'phone': str(d.get('no_telepon') or ''),
            'email': d.get('email'),
            'vat': str(d.get('npwp') or ''),
            'nama_kontak': d.get('nama_kontak'),
            'status_supplier': d.get('status_supplier'),
        }
        if existing:
            existing.write(vals)
            p = existing
        else:
            p = env['res.partner'].create(vals)
        partner_map[code] = p.id
    print(f"Loaded {len(supplier_data)} Suppliers")

    # 5. Nasabah -> res.partner
    nasabah_data = get_sheet_data('Nasabah')
    for d in nasabah_data:
        code = d.get('id_nasabah')
        existing = env['res.partner'].search([('id_nasabah', '=', code)], limit=1)
        vals = {
            'name': d.get('nama_lengkap'),
            'id_nasabah': code,
            'is_nasabah': True,
            'customer_rank': 1,
            'nik': str(d.get('nik') or ''),
            'tempat_lahir': d.get('tempat_lahir'),
            'tanggal_lahir': d.get('tanggal_lahir'),
            'jenis_kelamin': d.get('jenis_kelamin'),
            'street': d.get('alamat'),
            'city': d.get('kota'),
            'phone': str(d.get('no_telepon') or ''),
            'email': d.get('email'),
            'vat': str(d.get('npwp') or ''),
            'pekerjaan': d.get('pekerjaan'),
            'nama_ibu_kandung': d.get('nama_ibu_kandung'),
            'jenis_nasabah': d.get('jenis_nasabah'),
            'no_pensiun': str(d.get('no_pensiun') or ''),
            'status_prioritas': d.get('status_prioritas') or 'Reguler',
            'tanggal_registrasi': d.get('tanggal_registrasi'),
            'status_nasabah': d.get('status_nasabah') or 'Aktif',
        }
        if existing:
            existing.write(vals)
            p = existing
        else:
            p = env['res.partner'].create(vals)
        partner_map[code] = p.id
    print(f"Loaded {len(nasabah_data)} Nasabah")

    # 6. Suku Bunga -> bmt.suku.bunga
    bunga_data = get_sheet_data('Suku_Bunga')
    for d in bunga_data:
        code = d.get('id_suku_bunga')
        existing = env['bmt.suku.bunga'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'jenis_produk': d.get('jenis_produk'),
            'nama_produk': d.get('nama_produk'),
            'suku_bunga_persen_pa': float(d.get('suku_bunga_persen_pa') or 0.0),
            'tenor_minimum': int(d.get('tenor_minimum') or 0),
            'tenor_maksimum': int(d.get('tenor_maksimum') or 0),
            'plafon_minimum': float(d.get('plafon_minimum') or 0.0),
            'plafon_maksimum': float(d.get('plafon_maksimum') or 0.0),
            'tanggal_berlaku': d.get('tanggal_berlaku'),
            'tanggal_berakhir': d.get('tanggal_berakhir'),
            'status_bunga': d.get('status_bunga') or 'Aktif',
        }
        if existing:
            existing.write(vals)
            b = existing
        else:
            b = env['bmt.suku.bunga'].create(vals)
        bunga_map[code] = b.id
    print(f"Loaded {len(bunga_data)} Suku Bunga")

    # 7. Riwayat Perbankan SLIK -> bmt.riwayat.perbankan
    riwayat_data = get_sheet_data('Riwayat_Perbankan')
    for d in riwayat_data:
        code = d.get('id_riwayat')
        existing = env['bmt.riwayat.perbankan'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'nasabah_id': partner_map.get(d.get('id_nasabah')),
            'verifikator_id': emp_map.get(d.get('id_verifikator')),
            'tanggal_pengecekan': d.get('tanggal_pengecekan'),
            'kolektibilitas': str(d.get('kolektibilitas') or '1'),
            'jumlah_fasilitas_aktif': int(d.get('jumlah_fasilitas_aktif') or 0),
            'total_kewajiban': float(d.get('total_kewajiban') or 0.0),
            'status_daftar_hitam': d.get('status_daftar_hitam') or 'Tidak',
            'hasil_pengecekan': d.get('hasil_pengecekan') or 'Bersih',
            'keterangan': d.get('keterangan'),
        }
        if existing: existing.write(vals)
        else: env['bmt.riwayat.perbankan'].create(vals)
    print(f"Loaded {len(riwayat_data)} Riwayat Perbankan")

    # 8. Rekening Simpanan -> bmt.rekening
    rek_data = get_sheet_data('Rekening_Simpanan')
    for d in rek_data:
        code = d.get('no_rekening')
        existing = env['bmt.rekening'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'nasabah_id': partner_map.get(d.get('id_nasabah')),
            'jenis_rekening': d.get('jenis_rekening') or 'Tabungan',
            'nama_produk': d.get('nama_produk'),
            'tanggal_pembukaan': d.get('tanggal_pembukaan'),
            'setoran_awal': float(d.get('setoran_awal') or 0.0),
            'saldo': float(d.get('saldo') or 0.0),
            'saldo_minimum': float(d.get('saldo_minimum') or 50000.0),
            'status_rekening': d.get('status_rekening') or 'Aktif',
            'id_cs_pembuka': emp_map.get(d.get('id_cs_pembuka')),
            'id_penyetuju': emp_map.get(d.get('id_penyetuju')),
            'tanggal_penutupan': d.get('tanggal_penutupan'),
            'biaya_penutupan': float(d.get('biaya_penutupan') or 0.0),
            'alasan_penutupan': d.get('alasan_penutupan'),
        }
        if existing:
            existing.write(vals)
            r = existing
        else:
            r = env['bmt.rekening'].create(vals)
        rek_map[code] = r.id
    print(f"Loaded {len(rek_data)} Rekening")

    # 9. Deposito -> bmt.deposito
    dep_data = get_sheet_data('Deposito')
    for d in dep_data:
        code = d.get('no_bilyet')
        existing = env['bmt.deposito'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'no_rekening_sumber': rek_map.get(d.get('no_rekening_sumber')),
            'id_suku_bunga': bunga_map.get(d.get('id_suku_bunga')),
            'id_cs': emp_map.get(d.get('id_cs')),
            'nominal_penempatan': float(d.get('nominal_penempatan') or 0.0),
            'tenor_bulan': int(d.get('tenor_bulan') or 12),
            'suku_bunga_persen': float(d.get('suku_bunga_persen') or 5.0),
            'tanggal_mulai': d.get('tanggal_mulai'),
            'tanggal_jatuh_tempo': d.get('tanggal_jatuh_tempo'),
            'opsi_perpanjangan': d.get('opsi_perpanjangan') or 'Non-ARO',
            'status_deposito': d.get('status_deposito') or 'Aktif',
        }
        if existing: existing.write(vals)
        else: env['bmt.deposito'].create(vals)
    print(f"Loaded {len(dep_data)} Deposito")

    # 10. Kartu ATM -> bmt.kartu.atm
    atm_map = {}
    atm_data = get_sheet_data('Kartu_ATM')
    for d in atm_data:
        code = d.get('no_kartu')
        existing = env['bmt.kartu.atm'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'rekening_id': rek_map.get(d.get('no_rekening')),
            'jenis_kartu': d.get('jenis_kartu') or 'Debit Silver',
            'tanggal_terbit': d.get('tanggal_terbit'),
            'masa_berlaku': d.get('masa_berlaku'),
            'pin_terenkripsi': str(d.get('pin_terenkripsi') or ''),
            'batas_tarik_harian': float(d.get('batas_tarik_harian') or 5000000.0),
            'status_kartu': d.get('status_kartu') or 'Aktif',
            'id_cs': emp_map.get(d.get('id_cs')),
        }
        if existing:
            existing.write(vals)
            a = existing
        else:
            a = env['bmt.kartu.atm'].create(vals)
        atm_map[code] = a.id
    print(f"Loaded {len(atm_data)} Kartu ATM")

    # 11. Layanan Digital -> bmt.layanan.digital
    digi_data = get_sheet_data('Layanan_Digital_Banking')
    for d in digi_data:
        code = d.get('id_layanan')
        existing = env['bmt.layanan.digital'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'nasabah_id': partner_map.get(d.get('id_nasabah')),
            'rekening_id': rek_map.get(d.get('no_rekening')),
            'jenis_layanan': d.get('jenis_layanan'),
            'user_id': d.get('user_id'),
            'no_hp_terdaftar': str(d.get('no_hp_terdaftar') or ''),
            'email_terdaftar': d.get('email_terdaftar'),
            'tanggal_pengajuan': d.get('tanggal_pengajuan'),
            'hasil_verifikasi_identitas': d.get('hasil_verifikasi_identitas'),
            'tanggal_aktivasi': d.get('tanggal_aktivasi'),
            'status_layanan': d.get('status_layanan') or 'Aktif',
            'id_cs': emp_map.get(d.get('id_cs')),
            'id_pengaktivasi': emp_map.get(d.get('id_pengaktivasi')),
        }
        if existing: existing.write(vals)
        else: env['bmt.layanan.digital'].create(vals)
    print(f"Loaded {len(digi_data)} Layanan Digital")

    # 12. Pinjaman -> bmt.pinjaman
    pinj_data = get_sheet_data('Pinjaman')
    for d in pinj_data:
        code = d.get('no_pinjaman')
        existing = env['bmt.pinjaman'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'nasabah_id': partner_map.get(d.get('id_nasabah')),
            'id_suku_bunga': bunga_map.get(d.get('id_suku_bunga')),
            'jenis_pinjaman': d.get('jenis_pinjaman') or 'Pensiun',
            'tanggal_pengajuan': d.get('tanggal_pengajuan'),
            'tujuan_pinjaman': d.get('tujuan_pinjaman'),
            'status_kelengkapan_berkas': d.get('status_kelengkapan_berkas') or 'Lengkap',
            'plafon_diajukan': float(d.get('plafon_diajukan') or 0.0),
            'plafon_disetujui': float(d.get('plafon_disetujui') or 0.0),
            'tenor_bulan': int(d.get('tenor_bulan') or 36),
            'suku_bunga_persen': float(d.get('suku_bunga_persen') or 8.5),
            'angsuran_per_bulan': float(d.get('angsuran_per_bulan') or 0.0),
            'status_pinjaman': d.get('status_pinjaman') or 'Aktif',
            'alasan_penolakan': d.get('alasan_penolakan'),
            'no_surat_perjanjian': d.get('no_surat_perjanjian'),
            'tanggal_perjanjian': d.get('tanggal_perjanjian'),
            'tanggal_pencairan': d.get('tanggal_pencairan'),
            'id_cs_pemeriksa': emp_map.get(d.get('id_cs_pemeriksa')),
            'id_verifikator': emp_map.get(d.get('id_verifikator')),
            'id_penyetuju': emp_map.get(d.get('id_penyetuju')),
        }
        if existing: existing.write(vals)
        else: env['bmt.pinjaman'].create(vals)
    print(f"Loaded {len(pinj_data)} Pinjaman")

    # 13. Setoran -> bmt.transaksi.setoran
    setor_data = get_sheet_data('Transaksi_Setoran')
    for d in setor_data:
        code = d.get('id_setoran')
        existing = env['bmt.transaksi.setoran'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'no_rekening': rek_map.get(d.get('no_rekening')),
            'id_teller': emp_map.get(d.get('id_teller')),
            'tanggal_waktu': d.get('tanggal_waktu'),
            'nominal': float(d.get('nominal') or 0.0),
            'nama_penyetor': d.get('nama_penyetor'),
            'saluran': d.get('saluran') or 'Loket',
            'no_bukti': d.get('no_bukti'),
            'keterangan': d.get('keterangan'),
        }
        if existing: existing.write(vals)
        else: env['bmt.transaksi.setoran'].create(vals)
    print(f"Loaded {len(setor_data)} Setoran")

    # 14. Penarikan -> bmt.transaksi.penarikan
    tarik_data = get_sheet_data('Transaksi_Penarikan')
    for d in tarik_data:
        code = d.get('id_penarikan')
        existing = env['bmt.transaksi.penarikan'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'no_rekening': rek_map.get(d.get('no_rekening')),
            'no_kartu': atm_map.get(d.get('no_kartu')),
            'id_teller': emp_map.get(d.get('id_teller')),
            'tanggal_waktu': d.get('tanggal_waktu'),
            'nominal': float(d.get('nominal') or 0.0),
            'saluran': d.get('saluran') or 'Loket',
            'no_bukti': d.get('no_bukti'),
            'saldo_setelah_transaksi': float(d.get('saldo_setelah_transaksi') or 0.0),
        }
        if existing: existing.write(vals)
        else: env['bmt.transaksi.penarikan'].create(vals)
    print(f"Loaded {len(tarik_data)} Penarikan")

    # 15. Transfer -> bmt.transaksi.transfer
    trf_data = get_sheet_data('Transaksi_Transfer')
    for d in trf_data:
        code = d.get('id_transfer')
        existing = env['bmt.transaksi.transfer'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'no_rekening_asal': rek_map.get(d.get('no_rekening_asal')),
            'id_teller': emp_map.get(d.get('id_teller')),
            'bank_tujuan': d.get('bank_tujuan'),
            'no_rekening_tujuan': str(d.get('no_rekening_tujuan') or ''),
            'nama_penerima': d.get('nama_penerima'),
            'jenis_transfer': d.get('jenis_transfer') or 'Sesama Bank',
            'nominal': float(d.get('nominal') or 0.0),
            'biaya_transfer': float(d.get('biaya_transfer') or 0.0),
            'tanggal_waktu': d.get('tanggal_waktu'),
            'berita': d.get('berita'),
            'no_bukti': d.get('no_bukti'),
            'status_transfer': d.get('status_transfer') or 'Berhasil',
        }
        if existing: existing.write(vals)
        else: env['bmt.transaksi.transfer'].create(vals)
    print(f"Loaded {len(trf_data)} Transfer")

    # 16. Persediaan Kas -> bmt.persediaan.kas
    kas_data = get_sheet_data('Persediaan_Uang')
    for d in kas_data:
        code = d.get('id_persediaan_kas')
        existing = env['bmt.persediaan.kas'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_teller': emp_map.get(d.get('id_teller')),
            'tanggal': d.get('tanggal'),
            'saldo_awal_kas': float(d.get('saldo_awal_kas') or 0.0),
            'total_setoran': float(d.get('total_setoran') or 0.0),
            'total_penarikan': float(d.get('total_penarikan') or 0.0),
            'saldo_akhir_sistem': float(d.get('saldo_akhir_sistem') or 0.0),
            'saldo_fisik': float(d.get('saldo_fisik') or 0.0),
            'selisih': float(d.get('selisih') or 0.0),
            'keterangan_selisih': d.get('keterangan_selisih'),
        }
        if existing: existing.write(vals)
        else: env['bmt.persediaan.kas'].create(vals)
    print(f"Loaded {len(kas_data)} Persediaan Kas")

    # 17. Rencana Sosialisasi -> bmt.sosialisasi.rencana
    rso_data = get_sheet_data('Rencana_Sosialisasi')
    for d in rso_data:
        code = d.get('id_rencana_sosialisasi')
        existing = env['bmt.sosialisasi.rencana'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'tahun_anggaran': int(d.get('tahun_anggaran') or 2025),
            'judul_rencana': d.get('judul_rencana'),
            'tujuan': d.get('tujuan'),
            'target_peserta': int(d.get('target_peserta') or 0),
            'anggaran': float(d.get('anggaran') or 0.0),
            'tanggal_penyusunan': d.get('tanggal_penyusunan'),
            'status_persetujuan': d.get('status_persetujuan') or 'Disetujui',
            'tanggal_persetujuan': d.get('tanggal_persetujuan'),
            'id_penyusun': emp_map.get(d.get('id_penyusun')),
            'id_penyetuju': emp_map.get(d.get('id_penyetuju')),
        }
        if existing:
            existing.write(vals)
            r = existing
        else:
            r = env['bmt.sosialisasi.rencana'].create(vals)
        rso_map[code] = r.id
    print(f"Loaded {len(rso_data)} Rencana Sosialisasi")

    # 18. Jadwal Sosialisasi -> bmt.sosialisasi.jadwal
    jso_data = get_sheet_data('Jadwal_Sosialisasi')
    for d in jso_data:
        code = d.get('id_jadwal_sosialisasi')
        existing = env['bmt.sosialisasi.jadwal'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_rencana_sosialisasi': rso_map.get(d.get('id_rencana_sosialisasi')),
            'id_instansi': partner_map.get(d.get('id_instansi')),
            'no_surat_pengajuan': d.get('no_surat_pengajuan'),
            'tanggal_surat': d.get('tanggal_surat'),
            'tanggal_pelaksanaan': d.get('tanggal_pelaksanaan'),
            'waktu_mulai': str(d.get('waktu_mulai') or ''),
            'waktu_selesai': str(d.get('waktu_selesai') or ''),
            'lokasi': d.get('lokasi'),
            'materi': d.get('materi'),
            'status_pelaksanaan': d.get('status_pelaksanaan') or 'Selesai',
            'id_penanggung_jawab': emp_map.get(d.get('id_penanggung_jawab')),
        }
        if existing:
            existing.write(vals)
            j = existing
        else:
            j = env['bmt.sosialisasi.jadwal'].create(vals)
        jso_map[code] = j.id
    print(f"Loaded {len(jso_data)} Jadwal Sosialisasi")

    # 19. Hasil Sosialisasi -> bmt.sosialisasi.hasil
    hso_data = get_sheet_data('Hasil_Sosialisasi')
    for d in hso_data:
        code = d.get('id_hasil_sosialisasi')
        existing = env['bmt.sosialisasi.hasil'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_jadwal_sosialisasi': jso_map.get(d.get('id_jadwal_sosialisasi')),
            'tanggal_realisasi': d.get('tanggal_realisasi'),
            'jumlah_peserta': int(d.get('jumlah_peserta') or 0),
            'jumlah_calon_nasabah': int(d.get('jumlah_calon_nasabah') or 0),
            'ringkasan_hasil': d.get('ringkasan_hasil'),
            'kendala': d.get('kendala'),
            'tanggal_rekap': d.get('tanggal_rekap'),
            'id_penyusun': emp_map.get(d.get('id_penyusun')),
        }
        if existing: existing.write(vals)
        else: env['bmt.sosialisasi.hasil'].create(vals)
    print(f"Loaded {len(hso_data)} Hasil Sosialisasi")

    # 20. Doorprize -> bmt.doorprize
    dpz_data = get_sheet_data('Pembagian_Doorprize')
    for d in dpz_data:
        code = d.get('id_doorprize')
        existing = env['bmt.doorprize'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_nasabah': partner_map.get(d.get('id_nasabah')),
            'tahun_program': int(d.get('tahun_program') or 2025),
            'jenis_hadiah': d.get('jenis_hadiah'),
            'nilai_hadiah': float(d.get('nilai_hadiah') or 0.0),
            'status_persetujuan_daftar': d.get('status_persetujuan_daftar') or 'Disetujui',
            'status_persetujuan_pelaksanaan': d.get('status_persetujuan_pelaksanaan') or 'Disetujui',
            'tanggal_pembagian': d.get('tanggal_pembagian'),
            'status_penerimaan': d.get('status_penerimaan') or 'Sudah Diterima',
            'id_penyeleksi': emp_map.get(d.get('id_penyeleksi')),
            'id_pengelola': emp_map.get(d.get('id_pengelola')),
            'id_penyetuju': emp_map.get(d.get('id_penyetuju')),
        }
        if existing: existing.write(vals)
        else: env['bmt.doorprize'].create(vals)
    print(f"Loaded {len(dpz_data)} Doorprize")

    # 21. Promo Bunga -> bmt.promo.bunga
    prm_data = get_sheet_data('Promo_Bunga_Kompetitif')
    for d in prm_data:
        code = d.get('id_promo')
        existing = env['bmt.promo.bunga'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_nasabah': partner_map.get(d.get('id_nasabah')),
            'id_suku_bunga': bunga_map.get(d.get('id_suku_bunga')),
            'no_surat_promo': d.get('no_surat_promo'),
            'tanggal_surat': d.get('tanggal_surat'),
            'jenis_produk': d.get('jenis_produk') or 'Deposito',
            'suku_bunga_promo': float(d.get('suku_bunga_promo') or 0.0),
            'syarat_dana_minimum': float(d.get('syarat_dana_minimum') or 0.0),
            'periode_mulai': d.get('periode_mulai'),
            'periode_selesai': d.get('periode_selesai'),
            'status_persetujuan_nasabah': d.get('status_persetujuan_nasabah') or 'Setuju',
            'tanggal_tanda_tangan_kontrak': d.get('tanggal_tanda_tangan_kontrak'),
            'id_penyusun': emp_map.get(d.get('id_penyusun')),
            'id_penyetuju': emp_map.get(d.get('id_penyetuju')),
        }
        if existing: existing.write(vals)
        else: env['bmt.promo.bunga'].create(vals)
    print(f"Loaded {len(prm_data)} Promo Bunga")

    # 22. Keluhan & Saran -> bmt.keluhan & bmt.saran
    klh_data = get_sheet_data('Keluhan')
    for d in klh_data:
        code = d.get('id_keluhan')
        existing = env['bmt.keluhan'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_nasabah': partner_map.get(d.get('id_nasabah')),
            'tanggal_keluhan': d.get('tanggal_keluhan'),
            'kategori_keluhan': d.get('kategori_keluhan'),
            'media_penyampaian': d.get('media_penyampaian'),
            'uraian_keluhan': d.get('uraian_keluhan'),
            'status_penanganan': d.get('status_penanganan') or 'Selesai',
            'id_cs': emp_map.get(d.get('id_cs')),
            'hasil_evaluasi': d.get('hasil_evaluasi'),
            'tanggal_penyelesaian': d.get('tanggal_penyelesaian'),
        }
        if existing: existing.write(vals)
        else: env['bmt.keluhan'].create(vals)
    print(f"Loaded {len(klh_data)} Keluhan")

    srn_data = get_sheet_data('Saran')
    for d in srn_data:
        code = d.get('id_saran')
        existing = env['bmt.saran'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_nasabah': partner_map.get(d.get('id_nasabah')),
            'tanggal_saran': d.get('tanggal_saran'),
            'kategori_saran': d.get('kategori_saran'),
            'uraian_saran': d.get('uraian_saran'),
            'status_evaluasi': d.get('status_evaluasi') or 'Selesai Dievaluasi',
            'id_cs': emp_map.get(d.get('id_cs')),
            'hasil_evaluasi': d.get('hasil_evaluasi'),
            'tanggal_evaluasi': d.get('tanggal_evaluasi'),
        }
        if existing: existing.write(vals)
        else: env['bmt.saran'].create(vals)
    print(f"Loaded {len(srn_data)} Saran")

    # 23. Profil Risiko, Produk RD & Transaksi RD
    pr_data = get_sheet_data('Profil_Risiko')
    for d in pr_data:
        code = d.get('id_profil_risiko')
        existing = env['bmt.profil.risiko'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_nasabah': partner_map.get(d.get('id_nasabah')),
            'tanggal_asesmen': d.get('tanggal_asesmen'),
            'tujuan_investasi': d.get('tujuan_investasi'),
            'jangka_waktu_investasi': d.get('jangka_waktu_investasi'),
            'skor_risiko': int(d.get('skor_risiko') or 20),
            'kategori_profil': d.get('kategori_profil') or 'Konservatif',
            'masa_berlaku': d.get('masa_berlaku'),
            'id_tenaga_pemasar': emp_map.get(d.get('id_tenaga_pemasar')),
        }
        if existing: existing.write(vals)
        else: env['bmt.profil.risiko'].create(vals)
    print(f"Loaded {len(pr_data)} Profil Risiko")

    rd_data = get_sheet_data('Produk_Reksa_Dana')
    for d in rd_data:
        code = d.get('id_produk_rd')
        existing = env['bmt.produk.rd'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'nama_produk': d.get('nama_produk'),
            'jenis_reksa_dana': d.get('jenis_reksa_dana') or 'Pasar Uang',
            'nama_manajer_investasi': d.get('nama_manajer_investasi'),
            'tingkat_risiko': d.get('tingkat_risiko') or 'Rendah',
            'minimal_pembelian': float(d.get('minimal_pembelian') or 100000.0),
            'biaya_subscription_persen': float(d.get('biaya_subscription_persen') or 0.5),
            'nab_per_up': float(d.get('nab_per_up') or 1000.0),
            'tanggal_nab': d.get('tanggal_nab'),
            'status_produk': d.get('status_produk') or 'Aktif',
        }
        if existing:
            existing.write(vals)
            p = existing
        else:
            p = env['bmt.produk.rd'].create(vals)
        rd_prod_map[code] = p.id
    print(f"Loaded {len(rd_data)} Produk Reksa Dana")

    trd_data = get_sheet_data('Transaksi_Reksa_Dana')
    for d in trd_data:
        code = d.get('id_transaksi_rd')
        existing = env['bmt.transaksi.rd'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_nasabah': partner_map.get(d.get('id_nasabah')),
            'no_rekening': rek_map.get(d.get('no_rekening')),
            'id_produk_rd': rd_prod_map.get(d.get('id_produk_rd')),
            'id_tenaga_pemasar': emp_map.get(d.get('id_tenaga_pemasar')),
            'no_formulir_subscription': d.get('no_formulir_subscription'),
            'tanggal_pemesanan': d.get('tanggal_pemesanan'),
            'nominal_pembelian': float(d.get('nominal_pembelian') or 0.0),
            'biaya_subscription': float(d.get('biaya_subscription') or 0.0),
            'nab_per_up': float(d.get('nab_per_up') or 0.0),
            'jumlah_unit_penyertaan': float(d.get('jumlah_unit_penyertaan') or 0.0),
            'tanggal_setelmen': d.get('tanggal_setelmen'),
            'no_konfirmasi_kepemilikan': d.get('no_konfirmasi_kepemilikan'),
            'status_transaksi': d.get('status_transaksi') or 'Selesai',
        }
        if existing: existing.write(vals)
        else: env['bmt.transaksi.rd'].create(vals)
    print(f"Loaded {len(trd_data)} Transaksi Reksa Dana")

    # 24. Kompensasi & Penilaian Kinerja
    kom_data = get_sheet_data('Kompensasi')
    for d in kom_data:
        code = d.get('id_kompensasi')
        existing = env['bmt.kompensasi'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_karyawan': emp_map.get(d.get('id_karyawan')),
            'id_pengelola': emp_map.get(d.get('id_pengelola')),
            'periode_bulan': int(d.get('periode_bulan') or 9),
            'periode_tahun': int(d.get('periode_tahun') or 2026),
            'gaji_pokok': float(d.get('gaji_pokok') or 0.0),
            'tunjangan_jabatan': float(d.get('tunjangan_jabatan') or 0.0),
            'tunjangan_lain': float(d.get('tunjangan_lain') or 0.0),
            'upah_lembur': float(d.get('upah_lembur') or 0.0),
            'potongan_ketidakhadiran': float(d.get('potongan_ketidakhadiran') or 0.0),
            'potongan_bpjs': float(d.get('potongan_bpjs') or 0.0),
            'pph21': float(d.get('pph21') or 0.0),
            'gaji_bersih': float(d.get('gaji_bersih') or 0.0),
            'tanggal_pembayaran': d.get('tanggal_pembayaran'),
            'status_pembayaran': d.get('status_pembayaran') or 'Sukses',
        }
        if existing: existing.write(vals)
        else: env['bmt.kompensasi'].create(vals)
    print(f"Loaded {len(kom_data)} Kompensasi")

    nil_data = get_sheet_data('Penilaian')
    for d in nil_data:
        code = d.get('id_penilaian')
        existing = env['bmt.penilaian.kinerja'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_karyawan': emp_map.get(d.get('id_karyawan')),
            'id_penilai': emp_map.get(d.get('id_penilai')),
            'periode_penilaian': d.get('periode_penilaian'),
            'nilai_kehadiran': float(d.get('nilai_kehadiran') or 0.0),
            'nilai_pencapaian_target': float(d.get('nilai_pencapaian_target') or 0.0),
            'nilai_kualitas_pelayanan': float(d.get('nilai_kualitas_pelayanan') or 0.0),
            'nilai_sikap_kerja': float(d.get('nilai_sikap_kerja') or 0.0),
            'nilai_akhir': float(d.get('nilai_akhir') or 0.0),
            'predikat': d.get('predikat') or 'Baik',
            'catatan_penilai': d.get('catatan_penilai'),
            'tanggal_penilaian': d.get('tanggal_penilaian'),
        }
        if existing: existing.write(vals)
        else: env['bmt.penilaian.kinerja'].create(vals)
    print(f"Loaded {len(nil_data)} Penilaian Kinerja")

    # 25. Pelanggaran & PHK
    plg_data = get_sheet_data('Pelanggaran_Pegawai')
    for d in plg_data:
        code = d.get('id_pelanggaran')
        existing = env['bmt.pelanggaran'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_karyawan': emp_map.get(d.get('id_karyawan')),
            'id_pelapor': emp_map.get(d.get('id_pelapor')),
            'id_pemeriksa': emp_map.get(d.get('id_pemeriksa')),
            'no_laporan_kejadian': d.get('no_laporan_kejadian'),
            'tanggal_kejadian': d.get('tanggal_kejadian'),
            'jenis_pelanggaran': d.get('jenis_pelanggaran'),
            'uraian_pelanggaran': d.get('uraian_pelanggaran'),
            'hasil_audit_internal': d.get('hasil_audit_internal'),
            'memenuhi_syarat_phk': d.get('memenuhi_syarat_phk') or 'Tidak',
            'jenis_sanksi': d.get('jenis_sanksi'),
            'no_surat_peringatan': d.get('no_surat_peringatan'),
            'tanggal_sanksi': d.get('tanggal_sanksi'),
        }
        if existing:
            existing.write(vals)
            p = existing
        else:
            p = env['bmt.pelanggaran'].create(vals)
        plg_map[code] = p.id
    print(f"Loaded {len(plg_data)} Pelanggaran")

    phk_data = get_sheet_data('Pemutusan_Hubungan_Kerja')
    for d in phk_data:
        code = d.get('id_pemutusan')
        existing = env['bmt.pemutusan.kerja'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_karyawan': emp_map.get(d.get('id_karyawan')),
            'id_pelanggaran': plg_map.get(d.get('id_pelanggaran')),
            'id_otorisator': emp_map.get(d.get('id_otorisator')),
            'jenis_pemutusan': d.get('jenis_pemutusan') or 'PHK',
            'tanggal_pengajuan': d.get('tanggal_pengajuan'),
            'alasan': d.get('alasan'),
            'hasil_wawancara_retention': d.get('hasil_wawancara_retention'),
            'status_persetujuan': d.get('status_persetujuan') or 'Disetujui',
            'no_sk': d.get('no_sk'),
            'tanggal_sk': d.get('tanggal_sk'),
            'tanggal_efektif': d.get('tanggal_efektif'),
            'tanggal_deaktivasi_akses': d.get('tanggal_deaktivasi_akses'),
            'status_clearance_aset': d.get('status_clearance_aset') or 'Selesai',
            'nilai_hak_keuangan': float(d.get('nilai_hak_keuangan') or 0.0),
            'tanggal_pembayaran': d.get('tanggal_pembayaran'),
            'no_laporan_disnaker': d.get('no_laporan_disnaker'),
            'tanggal_lapor_disnaker': d.get('tanggal_lapor_disnaker'),
            'status_proses': d.get('status_proses') or 'Selesai',
        }
        if existing: existing.write(vals)
        else: env['bmt.pemutusan.kerja'].create(vals)
    print(f"Loaded {len(phk_data)} Pemutusan Hubungan Kerja")

    # 26. Pengaduan IT
    it_data = get_sheet_data('Pengaduan_Aplikasi')
    for d in it_data:
        code = d.get('id_pengaduan')
        existing = env['bmt.pengaduan.it'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_karyawan_pelapor': emp_map.get(d.get('id_karyawan_pelapor')),
            'id_penangan': emp_map.get(d.get('id_penangan')),
            'divisi_pelapor': d.get('divisi_pelapor'),
            'tanggal_pengaduan': d.get('tanggal_pengaduan'),
            'nama_aplikasi': d.get('nama_aplikasi'),
            'jenis_pengaduan': d.get('jenis_pengaduan') or 'Gangguan',
            'uraian_pengaduan': d.get('uraian_pengaduan'),
            'tingkat_prioritas': d.get('tingkat_prioritas') or 'Tinggi',
            'status_penanganan': d.get('status_penanganan') or 'Selesai',
            'hasil_analisis_atau_perbaikan': d.get('hasil_analisis_atau_perbaikan'),
            'tanggal_selesai': d.get('tanggal_selesai'),
        }
        if existing: existing.write(vals)
        else: env['bmt.pengaduan.it'].create(vals)
    print(f"Loaded {len(it_data)} Pengaduan IT")

    # 27. Logistik Buku & ATK
    pers_data = get_sheet_data('Persediaan_Buku_ATM')
    for d in pers_data:
        code = d.get('id_persediaan')
        existing = env['bmt.persediaan.buku.atm'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'jenis_item': d.get('jenis_item') or 'Buku Tabungan',
            'jumlah_stok': int(d.get('jumlah_stok') or 0),
            'stok_minimum': int(d.get('stok_minimum') or 20),
            'jumlah_terpakai': int(d.get('jumlah_terpakai') or 0),
            'lokasi_penyimpanan': d.get('lokasi_penyimpanan'),
            'tanggal_pembaruan': d.get('tanggal_pembaruan'),
            'id_pengelola': emp_map.get(d.get('id_pengelola')),
        }
        if existing: existing.write(vals)
        else: env['bmt.persediaan.buku.atm'].create(vals)
    print(f"Loaded {len(pers_data)} Persediaan Buku & Kartu")

    perm_data = get_sheet_data('Permintaan')
    for d in perm_data:
        code = d.get('id_permintaan')
        existing = env['bmt.permintaan.bahan'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_pemohon': emp_map.get(d.get('id_pemohon')),
            'id_operation_manager': emp_map.get(d.get('id_operation_manager')),
            'kode_barang': d.get('kode_barang'),
            'divisi_pemohon': d.get('divisi_pemohon'),
            'tanggal_permintaan': d.get('tanggal_permintaan'),
            'jumlah_diminta': int(d.get('jumlah_diminta') or 0),
            'jumlah_tersedia': int(d.get('jumlah_tersedia') or 0),
            'alasan_kebutuhan': d.get('alasan_kebutuhan'),
            'hasil_pengecekan': d.get('hasil_pengecekan') or 'Tidak Tersedia',
            'status_permintaan': d.get('status_permintaan') or 'Disetujui',
        }
        if existing: existing.write(vals)
        else: env['bmt.permintaan.bahan'].create(vals)
    print(f"Loaded {len(perm_data)} Permintaan Bahan")

    trm_data = get_sheet_data('Terima_Tabungan')
    for d in trm_data:
        code = d.get('id_penerimaan')
        existing = env['bmt.penerimaan.buku'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'no_surat_jalan': d.get('no_surat_jalan'),
            'tanggal_terima': d.get('tanggal_terima'),
            'asal_pengiriman': d.get('asal_pengiriman'),
            'jumlah_dikirim': int(d.get('jumlah_dikirim') or 0),
            'jumlah_diterima': int(d.get('jumlah_diterima') or 0),
            'selisih': int(d.get('selisih') or 0),
            'status_kesesuaian': d.get('status_kesesuaian') or 'Sesuai',
            'no_berita_acara_selisih': d.get('no_berita_acara_selisih'),
            'status_retur': d.get('status_retur') or 'Tidak Diperlukan',
            'id_penerima': emp_map.get(d.get('id_penerima')),
            'id_penyetuju': emp_map.get(d.get('id_penyetuju')),
            'tanggal_persetujuan': d.get('tanggal_persetujuan'),
        }
        if existing:
            existing.write(vals)
            t = existing
        else:
            t = env['bmt.penerimaan.buku'].create(vals)
        trm_map[code] = t.id
    print(f"Loaded {len(trm_data)} Penerimaan Buku")

    pakai_data = get_sheet_data('Pakai_Tabungan')
    for d in pakai_data:
        code = d.get('id_pemakaian')
        existing = env['bmt.pemakaian.buku'].search([('name', '=', code)], limit=1)
        vals = {
            'name': code,
            'id_penerimaan': trm_map.get(d.get('id_penerimaan')),
            'id_cs': emp_map.get(d.get('id_cs')),
            'id_pengarsip': emp_map.get(d.get('id_pengarsip')),
            'tanggal_alokasi': d.get('tanggal_alokasi'),
            'jumlah_dialokasikan': int(d.get('jumlah_dialokasikan') or 0),
            'jumlah_terpakai': int(d.get('jumlah_terpakai') or 0),
            'jumlah_rusak': int(d.get('jumlah_rusak') or 1),
            'sisa_stok': int(d.get('sisa_stok') or 0),
            'status_rekonsiliasi': d.get('status_rekonsiliasi') or 'Selesai',
            'tanggal_rekonsiliasi': d.get('tanggal_rekonsiliasi'),
        }
        if existing: existing.write(vals)
        else: env['bmt.pemakaian.buku'].create(vals)
    print(f"Loaded {len(pakai_data)} Pemakaian Buku")

    cr.commit()
    print("--- ALL DATA IMPORTED & COMMITTED SUCCESSFULLY! ---")
