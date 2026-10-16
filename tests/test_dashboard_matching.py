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
