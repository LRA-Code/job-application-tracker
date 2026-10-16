"""MySQL persistence: parameterized values, trusted identifiers, short transactions."""
import os
from contextlib import contextmanager
import mysql.connector
from models import TABLES

@contextmanager
def connection():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'), port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'job_tracker_app'), password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'job_tracker'), connection_timeout=5,
        charset='utf8mb4', autocommit=False)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def query(sql, params=(), write=False):
    with connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            return cursor.lastrowid if write else cursor.fetchall()
        finally:
            cursor.close()

def list_records(table):
    meta = TABLES[table]
    if table == 'contacts':
        return query('SELECT p.*, c.company_name FROM contacts p JOIN companies c ON p.company_id=c.company_id ORDER BY p.contact_id DESC')
    if table == 'applications':
        return query('SELECT a.*, j.job_title, c.company_name FROM applications a JOIN jobs j ON a.job_id=j.job_id JOIN companies c ON j.company_id=c.company_id ORDER BY a.application_date DESC, a.application_id DESC')
    if table == 'jobs':
        return query('SELECT j.*, c.company_name FROM jobs j JOIN companies c ON j.company_id=c.company_id ORDER BY j.job_id DESC')
    return query(f'SELECT * FROM `{table}` ORDER BY `{meta["pk"]}` DESC')

def get_record(table, record_id):
    pk = TABLES[table]['pk']
    rows = query(f'SELECT * FROM `{table}` WHERE `{pk}`=%s', (record_id,))
    return rows[0] if rows else None

def save_record(table, values, record_id=None):
    meta = TABLES[table]
    columns = [f['name'] for f in meta['fields']]
    params = tuple(values[c] for c in columns)
    if record_id is None:
        names = ', '.join(f'`{c}`' for c in columns)
        placeholders = ', '.join(['%s'] * len(columns))
        return query(f'INSERT INTO `{table}` ({names}) VALUES ({placeholders})', params, True)
    assignments = ', '.join(f'`{c}`=%s' for c in columns)
    query(f'UPDATE `{table}` SET {assignments} WHERE `{meta["pk"]}`=%s', params + (record_id,), True)
    return record_id

def delete_record(table, record_id):
    pk = TABLES[table]['pk']
    query(f'DELETE FROM `{table}` WHERE `{pk}`=%s', (record_id,), True)

def dashboard_data():
    # A single connection keeps these reads in one consistent transaction.
    with connection() as conn:
        cur = conn.cursor(dictionary=True)
        try:
            counts = {}
            for table in TABLES:
                cur.execute(f'SELECT COUNT(*) AS n FROM `{table}`')
                counts[table] = cur.fetchone()['n']
            cur.execute('SELECT status, COUNT(*) AS n FROM applications GROUP BY status')
            statuses = {r['status']: r['n'] for r in cur.fetchall()}
            cur.execute('''SELECT a.application_id, a.application_date, a.status, j.job_title, c.company_name
                           FROM applications a JOIN jobs j ON a.job_id=j.job_id
                           JOIN companies c ON j.company_id=c.company_id
                           ORDER BY a.application_date DESC, a.application_id DESC LIMIT 5''')
            recent = cur.fetchall()
            return dict(counts=counts, statuses=statuses, recent=recent)
        finally:
            cur.close()
