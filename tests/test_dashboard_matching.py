import json
import pytest
import database as db
from matching import rank_jobs

def test_ranking_algorithm():
    jobs = [dict(job_id=1, job_title='Developer', requirements='["Python","SQL","Flask"]'),
            dict(job_id=2, job_title='Analyst', requirements='["Python","SQL","Tableau"]'),
            dict(job_id=3, job_title='Empty', requirements=None)]
    ranked = rank_jobs(jobs, ' PYTHON, sql, flask, Python, C++ ')
    assert [r['percent'] for r in ranked] == [100, 67, 0]
    assert ranked[1]['missing'] == ['tableau']
    assert rank_jobs(jobs, '')[0]['percent'] == 0
    assert rank_jobs([dict(job_id=4, job_title='C', requirements='["C++","C++","C#"]')], 'C++')[0]['percent'] == 50
    assert rank_jobs(jobs, 'Py')[0]['percent'] == 0

def test_dashboard_and_match(client, post):
    assert client.get('/').status_code == 200
    post('/companies/new', {'company_name':'Demo Co'})
    cid = db.list_records('companies')[0]['company_id']
    post('/jobs/new', {'company_id':str(cid), 'job_title':'Developer', 'requirements':'Python, SQL, Flask'})
    jid = db.list_records('jobs')[0]['job_id']
    post('/applications/new', {'job_id':str(jid), 'application_date':'2026-10-16', 'status':'Interview'})
    data = db.dashboard_data()
    assert data['counts'] == dict(companies=1,jobs=1,applications=1,contacts=0)
    assert data['statuses'] == {'Interview':1}
    assert b'Developer' in client.get('/').data
    assert b'100%' in post('/job-match', {'skills':'Python, SQL, Flask'}).data
    assert post('/job-match', {'skills':' , '}).status_code == 422

def test_transaction_rollback(client):
    with pytest.raises(RuntimeError):
        with db.connection() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO companies (company_name) VALUES (%s)', ('Rollback test',))
            cur.close()
            raise RuntimeError('Simulated interrupted transaction')
    assert not db.list_records('companies')

def test_database_unavailable_page(client, monkeypatch):
    from mysql.connector import OperationalError
    def unavailable():
        raise OperationalError('Simulated database outage')
    monkeypatch.setattr(db, 'dashboard_data', unavailable)
    response = client.get('/')
    assert response.status_code == 503
    assert b'Check your MySQL service' in response.data

def test_database_constraints(client, post):
    from mysql.connector import Error
    post('/companies/new', {'company_name':'Constraint Co'})
    cid = db.list_records('companies')[0]['company_id']
    with pytest.raises(Error):
        db.query('INSERT INTO jobs (company_id,job_title,salary_min) VALUES (%s,%s,%s)', (cid,'Invalid',-1), True)
    with pytest.raises(Error):
        db.query('INSERT INTO jobs (company_id,job_title) VALUES (%s,%s)', (999999,'Orphan'), True)
    with pytest.raises(Error):
        db.query('INSERT INTO jobs (company_id,job_title,requirements) VALUES (%s,%s,%s)', (cid,'Invalid JSON','not JSON'), True)
    assert not db.list_records('jobs')

def test_seed_refuses_existing_records(client, post):
    from seed import seed
    post('/companies/new', {'company_name':'Keep Me'})
    with pytest.raises(RuntimeError, match='empty tables'):
        seed()
    assert [r['company_name'] for r in db.list_records('companies')] == ['Keep Me']
