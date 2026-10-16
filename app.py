"""Job Application Tracker: Flask routes and presentation."""
import json
import os
import secrets
import hmac
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from mysql.connector import Error, IntegrityError
import database as db
from models import TABLES, STATUSES
from matching import rank_jobs
from validation import validate

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.getenv('SECRET_KEY') or secrets.token_hex(32),
                      MAX_CONTENT_LENGTH=64 * 1024, SESSION_COOKIE_HTTPONLY=True,
                      SESSION_COOKIE_SAMESITE='Lax', FEATURES=['job_match'])
    if test_config:
        app.config.update(test_config)

    @app.context_processor
    def shared():
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(32)
        return dict(tables=TABLES, csrf_token=session['csrf_token'])

    @app.before_request
    def check_csrf():
        if request.method == 'POST':
            expected, actual = session.get('csrf_token', ''), request.form.get('csrf_token', '')
            if not expected or not hmac.compare_digest(expected.encode(), actual.encode()):
                abort(400, 'Form expired. Reload the page and try again.')

    def metadata(table):
        if table not in TABLES:
            abort(404)
        return TABLES[table]

    def record_or_404(table, record_id):
        metadata(table)
        row = db.get_record(table, record_id)
        if row is None:
            abort(404)
        return row

    def options_for(meta):
        options = {}
        for f in meta['fields']:
            if f['kind'] == 'foreign':
                target = 'companies' if f['name'] == 'company_id' else 'jobs'
                tm = TABLES[target]
                options[f['name']] = [(str(r[tm['pk']]), r[tm['title']] + (' — ' + r['company_name'] if target == 'jobs' else '')) for r in db.list_records(target)]
        return options

    @app.route('/')
    def dashboard():
        return render_template('dashboard.html', data=db.dashboard_data(), statuses=STATUSES)

    @app.route('/job-match', methods=['GET', 'POST'])
    def job_match():
        skills = request.form.get('skills', '').strip() if request.method == 'POST' else ''
        results, error = None, None
        if request.method == 'POST':
            if not skills or not any(s.strip() for s in skills.replace('\n', ',').split(',')):
                error = 'Enter at least one skill.'
            elif len(skills) > 10000:
                error = 'Keep the skills list under 10,000 characters.'
            else:
                results = rank_jobs(db.list_records('jobs'), skills)
        return render_template('job_match.html', skills=skills, results=results, error=error), (422 if error else 200)

    @app.route('/<table>')
    def records(table):
        meta = metadata(table)
        return render_template('records.html', table=table, meta=meta, rows=db.list_records(table))

    @app.route('/<table>/<int:record_id>')
    def detail(table, record_id):
        row = record_or_404(table, record_id)
        return render_template('detail.html', table=table, meta=TABLES[table], row=row)

    @app.route('/<table>/new', methods=['GET', 'POST'])
    @app.route('/<table>/<int:record_id>/edit', methods=['GET', 'POST'])
    def edit(table, record_id=None):
        meta = metadata(table)
        row = record_or_404(table, record_id) if record_id is not None else {}
        options = options_for(meta)
        errors = {}
        if request.method == 'POST':
            row = request.form.to_dict()
            values, errors = validate(meta['fields'], request.form)
            for name, choices in options.items():
                if str(values.get(name)) not in {key for key, _ in choices}:
                    errors[name] = 'Choose an existing record.'
            if not errors:
                try:
                    saved_id = db.save_record(table, values, record_id)
                    flash(f'{meta["singular"]} saved.', 'success')
                    return redirect(url_for('detail', table=table, record_id=saved_id))
                except IntegrityError:
                    errors['_form'] = 'A related record changed. Refresh and choose it again.'
        else:
            row = dict(row)
            if 'requirements' in row:
                obj = row['requirements']
                row['requirements'] = ', '.join(json.loads(obj) if isinstance(obj, str) else (obj or []))
            if 'interview_data' in row:
                obj = row['interview_data']
                row['interview_data'] = json.dumps(json.loads(obj) if isinstance(obj, str) else (obj or {}), indent=2)
        return render_template('form.html', table=table, meta=meta, row=row,
                               record_id=record_id, options=options, errors=errors), (422 if errors else 200)

    @app.route('/<table>/<int:record_id>/delete', methods=['GET', 'POST'])
    def delete(table, record_id):
        row = record_or_404(table, record_id)
        error = None
        if request.method == 'POST':
            if request.form.get('confirm') != 'yes':
                abort(400, 'Please confirm deletion.')
            try:
                db.delete_record(table, record_id)
                flash(f'{TABLES[table]["singular"]} deleted.', 'success')
                return redirect(url_for('records', table=table))
            except IntegrityError:
                error = 'This record has related records. Delete or reassign them first.'
        return render_template('delete.html', table=table, meta=TABLES[table], row=row, error=error), (409 if error else 200)

    @app.errorhandler(Error)
    def database_error(error):
        app.logger.exception('Database operation failed')
        return render_template('error.html', message='Database unavailable. Check your MySQL service and .env settings, then retry.'), 503

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(413)
    def http_error(error):
        return render_template('error.html', message=error.description), error.code

    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
