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
