import json
import database as db

def add_job(post):
    post('/companies/new', {'company_name': 'Acme'})
    cid = db.list_records('companies')[0]['company_id']
    post('/jobs/new', {'company_id': str(cid), 'job_title': 'Engineer'})
    return db.list_records('jobs')[0]['job_id']

def test_applications_crud(client, post):
    jid = add_job(post)
    values = {'job_id': str(jid), 'application_date': '2026-10-16', 'status':'Applied',
              'cover_letter_sent':'1', 'interview_data':'{"round":"Phone"}'}
    assert post('/applications/new', values).status_code == 200
    row = db.list_records('applications')[0]
    assert row['cover_letter_sent'] == 1
    assert json.loads(row['interview_data']) == {'round':'Phone'}
    path = f'/applications/{row["application_id"]}'
    assert client.get('/applications').status_code == 200
    assert client.get(path).status_code == 200
    assert client.get(path + '/edit').status_code == 200
    assert post(path + '/edit', {**values, 'status':'Interview', 'cover_letter_sent':''}).status_code == 200
    updated = db.get_record('applications', row['application_id'])
    assert updated['status'] == 'Interview' and updated['cover_letter_sent'] == 0
    assert post(f'/jobs/{jid}/delete', {'confirm':'yes'}).status_code == 409
    assert post(path + '/delete', {'confirm':'yes'}).status_code == 200
    assert not db.list_records('applications')

def test_application_validation(client, post):
    jid = add_job(post)
    values = {'job_id':str(jid), 'application_date':'2026-10-16', 'status':'Applied'}
    for bad in [{'status':'Hired'}, {'interview_data':'not json'}, {'interview_data':'[]'},
                {'application_date':''}, {'job_id':'999999'}]:
        assert post('/applications/new', {**values, **bad}).status_code == 422
    assert not db.list_records('applications')
