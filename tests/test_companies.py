import database as db

def test_company_crud(client, post):
    assert client.get('/companies').status_code == 200
    assert b'No companies yet' in client.get('/companies').data
    response = post('/companies/new', {'company_name': 'First Company', 'city': 'Miami'})
    assert response.status_code == 200
    row = db.list_records('companies')[0]
    assert row['company_name'] == 'First Company'
    path = f'/companies/{row["company_id"]}'
    assert client.get(path).status_code == 200
    response = post(path + '/edit', {'company_name': 'Updated Company'})
    assert b'Updated Company' in response.data
    assert db.get_record('companies', row['company_id'])['company_name'] == 'Updated Company'
    assert client.get(path + '/delete').status_code == 200
    assert db.get_record('companies', row['company_id'])
    assert post(path + '/delete', {'confirm': 'yes'}).status_code == 200
    assert db.get_record('companies', row['company_id']) is None

def test_company_validation(client, post):
    assert post('/companies/new', {'company_name': '  '}).status_code == 422
    assert post('/companies/new', {'company_name': 'a' * 101}).status_code == 422
    assert post('/companies/new', {'company_name': 'Valid', 'website': 'javascript:alert(1)'}).status_code == 422
    assert not db.list_records('companies')

def test_csrf_and_missing(client):
    assert client.post('/companies/new', data={'company_name': 'Unsafe'}).status_code == 400
    assert client.get('/companies/999999').status_code == 404
    assert client.get('/secrets').status_code == 404
    assert client.post('/companies/new', data={'csrf_token': '☃'}).status_code == 400

def test_sql_and_html_injection(client, post):
    name = "<script>alert('x')</script>'; DROP TABLE companies;--"
    response = post('/companies/new', {'company_name': name})
    assert response.status_code == 200
    assert b'<script>' not in response.data
    assert db.list_records('companies')[0]['company_name'] == name
