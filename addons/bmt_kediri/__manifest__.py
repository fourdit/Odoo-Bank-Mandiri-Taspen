# -*- coding: utf-8 -*-
{
    'name': 'Bank Mandiri Taspen KC Kediri - Enterprise Suite',
    'version': '19.0.1.0.0',
    'category': 'Banking',
    'summary': 'Simulasi Proses Bisnis dan Core Banking Bank Mandiri Taspen KC Kediri',
    'description': '''
        Modul Sistem Enterprise Bank Mandiri Taspen KC Kediri:
        - Core Banking: Rekening Simpanan, Kartu ATM, Deposito, Pinjaman, Transaksi Teller, Suku Bunga, Riwayat Perbankan
        - Pemasaran & CRM: Sosialisasi Instansi, Promo Bunga Kompetitif, Doorprize, Reksa Dana APERD, Keluhan & Saran
        - Operasional & HCM: Kompensasi Gaji, Penilaian Kinerja, Pelanggaran Disiplin, Pemutusan Hubungan Kerja (PHK/Resign), Pengaduan IT, Persediaan & Pemakaian Buku Tabungan
    ''',
    'author': 'Kelompok 1 - Sistem Enterprise UB',
    'depends': ['base', 'contacts', 'hr', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/partner_views.xml',
        'views/rekening_views.xml',
        'views/deposito_views.xml',
        'views/pinjaman_views.xml',
        'views/teller_views.xml',
        'views/crm_views.xml',
        'views/reksa_dana_views.xml',
        'views/hcm_views.xml',
        'views/logistik_views.xml',
        'views/dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
