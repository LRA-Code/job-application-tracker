"""Integration tests use only a dedicated database ending in _test."""
import os
from pathlib import Path
import pytest
import mysql.connector
from app import create_app
import database as db

@pytest.fixture(scope='session', autouse=True)
def test_schema():
    name = os.getenv('TEST_DB_NAME', 'job_tracker_test')
    if not name.endswith('_test') or not name.replace('_', '').isalnum():
        raise RuntimeError('TEST_DB_NAME must be a safe identifier ending in _test')
    os.environ['DB_NAME'] = name
    conn = mysql.connector.connect(host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '3306')), user=os.getenv('DB_USER', 'job_tracker_app'),
        password=os.getenv('DB_PASSWORD', ''))
    cur = conn.cursor()
    sql = Path('schema.sql').read_text().replace('job_tracker', name)
    for statement in sql.split(';'):
        if statement.strip():
            cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()
    yield

@pytest.fixture
def client():
    # Delete children first; the normal schema never cascades deletes.
    for table in reversed(list(db.TABLES)):
        db.query(f'DELETE FROM `{table}`', write=True)
    app = create_app({'TESTING': True, 'SECRET_KEY': 'test-only'})
    with app.test_client() as client:
        yield client

@pytest.fixture
def post(client):
    def send(path, data):
        client.get(path)
        with client.session_transaction() as sess:
            token = sess['csrf_token']
        return client.post(path, data={**data, 'csrf_token': token}, follow_redirects=True)
    return send
