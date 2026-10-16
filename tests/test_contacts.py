import database as db

def test_contacts_crud(client, post):
    post('/companies/new', {'company_name':'Contact Co'})
    cid = db.list_records('companies')[0]['company_id']
    values = {'company_id':str(cid), 'contact_name':'Jordan Lee', 'email':'jordan@example.com'}
    assert post('/contacts/new', values).status_code == 200
    row = db.list_records('contacts')[0]
    path = f'/contacts/{row["contact_id"]}'
    assert client.get('/contacts').status_code == 200
    assert b'Jordan Lee' in client.get(path).data
    assert client.get(path+'/edit').status_code == 200
    assert post(path+'/edit', {**values, 'title':'Recruiter'}).status_code == 200
    assert db.get_record('contacts', row['contact_id'])['title'] == 'Recruiter'
    assert post(f'/companies/{cid}/delete', {'confirm':'yes'}).status_code == 409
    assert post(path+'/delete', {'confirm':'yes'}).status_code == 200
    assert not db.list_records('contacts')

def test_contacts_validation(client, post):
    post('/companies/new', {'company_name':'Contact Co'})
    cid = db.list_records('companies')[0]['company_id']
    values = {'company_id':str(cid), 'contact_name':'Jordan'}
    for bad in [{'email':'bad'}, {'phone':'1'*21}, {'contact_name':''}, {'company_id':'999999'}]:
        assert post('/contacts/new', {**values, **bad}).status_code == 422
