import json
import database as db

def add_company(post):
    post('/companies/new', {'company_name': 'TechCorp'})
    return db.list_records('companies')[0]['company_id']

def test_jobs_crud(client, post):
    company = add_company(post)
    values = {'company_id': str(company), 'job_title': 'Developer', 'job_type': 'Full-time',
              'salary_min': '80000', 'salary_max': '95000', 'requirements': 'Python, SQL, Flask', 'date_posted': '2026-10-01'}
    assert post('/jobs/new', values).status_code == 200
    job = db.list_records('jobs')[0]
    assert json.loads(job['requirements']) == ['python', 'sql', 'flask']
    assert b'TechCorp' in client.get('/jobs').data
    path = f'/jobs/{job["job_id"]}'
    assert b'Developer' in client.get(path).data
    assert b'python, sql, flask' in client.get(path + '/edit').data
    assert post(path + '/edit', {**values, 'job_title': 'Senior Developer'}).status_code == 200
    assert db.get_record('jobs', job['job_id'])['job_title'] == 'Senior Developer'
    assert post(f'/companies/{company}/delete', {'confirm': 'yes'}).status_code == 409
    assert post(path + '/delete', {'confirm': 'yes'}).status_code == 200
    assert not db.list_records('jobs')

def test_job_validation(client, post):
    company = add_company(post)
    valid = {'company_id': str(company), 'job_title': 'Analyst'}
    for invalid in [{'company_id':'999999'}, {'salary_min':'-1'}, {'salary_min':'5', 'salary_max':'4'},
                    {'salary_min':'999999999999'}, {'job_type':'Unknown'}, {'date_posted':'2026-02-30'}]:
        assert post('/jobs/new', {**valid, **invalid}).status_code == 422
    assert not db.list_records('jobs')
