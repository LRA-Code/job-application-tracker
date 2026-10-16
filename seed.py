"""Optional fictional sample data. Refuses to run on any nonempty table."""
from dotenv import load_dotenv
import json
import database as db
load_dotenv()

def seed():
    with db.connection() as conn:
        cur = conn.cursor()
        try:
            for table in db.TABLES:
                cur.execute(f'SELECT COUNT(*) FROM `{table}`')
                if cur.fetchone()[0]:
                    raise RuntimeError('Sample data requires four empty tables. Existing data was not changed.')
            companies = [('TechCorp', 'Software', 'Miami', 'FL'), ('DataCo', 'Analytics', 'Austin', 'TX'),
                         ('Northstar Studio', 'Design', 'New York', 'NY')]
            ids = []
            for name, industry, city, state in companies:
                cur.execute('INSERT INTO companies (company_name, industry, city, state) VALUES (%s,%s,%s,%s)',
                            (name, industry, city, state))
                ids.append(cur.lastrowid)
            jobs = [(ids[0], 'Software Developer', 85000, 110000, ['Python','SQL','Flask']),
                    (ids[1], 'Data Analyst', 70000, 95000, ['Python','SQL','Tableau']),
                    (ids[2], 'Frontend Developer', 80000, 105000, ['JavaScript','HTML','CSS']),
                    (ids[0], 'Platform Engineer', 95000, 130000, ['Python','Docker','Linux'])]
            job_ids = []
            for cid, title, low, high, skills in jobs:
                cur.execute('''INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, date_posted, requirements)
                               VALUES (%s,%s,'Full-time',%s,%s,'2026-10-01',%s)''',
                            (cid,title,low,high,json.dumps(skills)))
                job_ids.append(cur.lastrowid)
            for jid, status, day in [(job_ids[0],'Interview','2026-10-14'), (job_ids[1],'Screening','2026-10-12'),
                                     (job_ids[2],'Applied','2026-10-10')]:
                cur.execute('''INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
                               VALUES (%s,%s,%s,'resume_v1.pdf',TRUE,%s)''',
                            (jid, day, status, json.dumps({'round':'Technical','date':'2026-10-21'} if status=='Interview' else {})))
            for cid, name in [(ids[0],'Jordan Lee'),(ids[1],'Alex Morgan')]:
                cur.execute('INSERT INTO contacts (company_id,contact_name,title,email) VALUES (%s,%s,%s,%s)',
                            (cid,name,'Recruiter',name.lower().replace(' ','.')+'@example.com'))
        finally:
            cur.close()

if __name__ == '__main__':
    seed()
    print('Added fictional sample data: 3 companies, 4 jobs, 3 applications, 2 contacts.')
