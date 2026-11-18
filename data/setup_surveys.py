import sys
sys.path.insert(0, r"C:\Program Files\Odoo 19.0.20261118\server")
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

data_dir = r"C:\Users\Harun\.gemini\antigravity\brain\dd8d7e7b-535e-4ca1-8603-3183723e8ef9\scratch\odoo_data"
odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20261118\server\odoo.conf', '-d', 'odoo_db', f'--data-dir={data_dir}'])
odoo.tools.config['data_dir'] = data_dir

registry = Registry('odoo_db')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Clean demo surveys
    demo_surveys = env['survey.survey'].search([
        ('title', 'in', ['Burger Quiz', 'Food Preferences', "Let's connect!", 'Furniture Creation Certification', 'MyCompany Vendor Certification', 'Feedback Form'])
    ])
    print(f"Deleting {len(demo_surveys)} demo surveys...")
    demo_surveys.unlink()
    
    # 2. Create BMT Risk Profile Survey
    survey_risk = env['survey.survey'].search([('title', 'ilike', 'Profil Risiko')], limit=1)
    if not survey_risk:
        survey_risk = env['survey.survey'].create({
            'title': 'Kuesioner Profil Risiko Nasabah APERD Reksa Dana — KC Kediri',
            'description': '<p>Kuesioner penentuan profil risiko investor nasabah pensiunan & umum Bank Mandiri Taspen KC Kediri (Konservatif, Moderat, Agresif) sesuai regulasi OJK.</p>',
            'survey_type': 'survey',
            'is_attempts_limited': False,
        })
        # Add questions
        q1 = env['survey.question'].create({
            'survey_id': survey_risk.id,
            'title': 'Berapa lama jangka waktu rencana investasi Anda di Bank Mandiri Taspen?',
            'question_type': 'simple_choice',
            'suggested_answer_ids': [
                (0, 0, {'value': 'Kurang dari 1 tahun (Jangka Pendek)', 'answer_score': 1}),
                (0, 0, {'value': '1 sampai 3 tahun (Jangka Menengah)', 'answer_score': 2}),
                (0, 0, {'value': 'Lebih dari 3 tahun (Jangka Panjang)', 'answer_score': 3}),
            ]
        })
        q2 = env['survey.question'].create({
            'survey_id': survey_risk.id,
            'title': 'Bagaimana toleransi Anda terhadap potensi fluktuasi nilai investasi / NAB?',
            'question_type': 'simple_choice',
            'suggested_answer_ids': [
                (0, 0, {'value': 'Sangat rendah, mengutamakan keutuhan modal pokok (Konservatif)', 'answer_score': 1}),
                (0, 0, {'value': 'Siap menerima fluktuasi wajar demi imbal hasil di atas deposito (Moderat)', 'answer_score': 2}),
                (0, 0, {'value': 'Siap menghadapi fluktuasi tinggi demi potensi imbal hasil maksimal (Agresif)', 'answer_score': 3}),
            ]
        })
    print("Created BMT Risk Profile Survey.")

    # 3. Create BMT Recruitment Written Test
    survey_rec = env['survey.survey'].search([('title', 'ilike', 'Seleksi Kompetensi')], limit=1)
    if not survey_rec:
        survey_rec = env['survey.survey'].create({
            'title': 'Tes Tertulis Seleksi Calon Pegawai Bank Mandiri Taspen KC Kediri',
            'description': '<p>Ujian tertulis kompetensi dasar perbankan, pelayanan nasabah pensiunan, dan integritas kerja calon pegawai.</p>',
            'survey_type': 'assessment',
            'is_attempts_limited': True,
            'attempts_limit': 1,
        })
        q_rec1 = env['survey.question'].create({
            'survey_id': survey_rec.id,
            'title': 'Apa pilar utama nilai budaya kerja (Core Values) BUMN di Bank Mandiri Taspen?',
            'question_type': 'simple_choice',
            'suggested_answer_ids': [
                (0, 0, {'value': 'AKHLAK (Amanah, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif)', 'is_correct': True, 'answer_score': 10}),
                (0, 0, {'value': 'PRIMA (Profesional, Responsif, Integritas, Maju, Akuntabel)', 'is_correct': False, 'answer_score': 0}),
            ]
        })
        q_rec2 = env['survey.question'].create({
            'survey_id': survey_rec.id,
            'title': 'Produk simpanan utama yang ditujukan bagi para pensiunan ASN/TNI/Polri di Bank Mandiri Taspen adalah:',
            'question_type': 'simple_choice',
            'suggested_answer_ids': [
                (0, 0, {'value': 'Tabungan SiMantap Pensiun', 'is_correct': True, 'answer_score': 10}),
                (0, 0, {'value': 'Giro Valas Korporasi', 'is_correct': False, 'answer_score': 0}),
            ]
        })
    print("Created BMT Recruitment Assessment Survey.")
    
    cr.commit()
    print("Surveys fully configured!")
