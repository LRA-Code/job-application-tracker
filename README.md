# Job Application Tracker

A Flask + MySQL application for managing companies, job postings, applications,
and professional contacts. Built for the COP4751 course project using the final
Project Specification. The earlier practice assignments have different columns;
this project uses the final specification (including `requirements` and
`interview_data` JSON columns). Do not point it at an old assignment schema
without reviewing the differences.

## Features

- Full create, list, detail, edit, and confirmed-delete workflows for all four tables.
- Dashboard with live totals, status counts, and five recent applications.
- Job Match ranks saved jobs by required-skill coverage, showing percentages,
  matched skills, and missing skills.
- Required fields, length limits, dates, salary ranges, enums, emails, URLs,
  JSON, and foreign keys are validated on the server.
- Parameterized SQL, transaction rollback, connection cleanup, HTML escaping,
  and session-based CSRF protection.
- Foreign keys restrict parent deletion; delete or reassign children first.
- Responsive HTML/CSS, empty states, and useful database-error messages.
- Fictional sample data and automated MySQL integration tests.

This is a local, single-user course application. Run on `127.0.0.1`; it has no
login or per-user isolation and is not configured for public hosting. GitHub
stores the source; GitHub Pages cannot run Flask or MySQL.

## Requirements

Python 3.12 recommended, MySQL 8.0.16 or newer, and Git. MySQL must be running.
MySQL Workbench is optional for inspecting the database. SQLite is not used.

## Ubuntu / WSL setup (recommended)

### 1. Extract and open the project

Download the project ZIP, extract it, and open Ubuntu. For a ZIP in your Windows
Downloads folder, adjust the Windows account name if yours differs:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server git unzip
mkdir -p ~/cop4751
unzip /mnt/c/Users/lucas/Downloads/Job_Application_Tracker_Lucas_Ramos.zip -d ~/cop4751
cd ~/cop4751/job-application-tracker
sudo service mysql start
```

If you cloned from GitHub instead, `cd` into the cloned directory. The ZIP includes
its local `.git` history. Keep this hidden directory when extracting. Do not
initialize another repository inside it.

### 2. Create a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

### 3. Create the database and a local application user

For a fresh installation (do not overwrite an existing assignment database):

```bash
sudo mysql < schema.sql
sudo mysql
```

At the MySQL prompt, choose your own password and run:

```sql
CREATE USER 'job_tracker_app'@'localhost' IDENTIFIED BY 'choose-your-own-password';
GRANT SELECT, INSERT, UPDATE, DELETE ON job_tracker.* TO 'job_tracker_app'@'localhost';
EXIT;
```

If the user already exists, use `ALTER USER ... IDENTIFIED BY ...` instead of
`CREATE USER`. If `sudo mysql` is not supported by your installation, use
`mysql -u root -p` and enter the root password you set when installing MySQL.

The schema script creates missing tables; it does not change existing table
structures. Back up any old `job_tracker` database before using a fresh schema.
You can create a separate database by changing both `CREATE DATABASE` and `USE`
in a copy of `schema.sql`, and setting the same `DB_NAME` in `.env`.

### 4. Configure `.env`

```bash
nano .env
```

Set `DB_PASSWORD` to the password chosen above. Keep `DB_HOST=127.0.0.1`,
`DB_PORT=3306`, `DB_USER=job_tracker_app`, and `DB_NAME=job_tracker` unless your
installation differs. Generate a secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY`. Save nano with Ctrl+O, Enter, Ctrl+X.
Never commit `.env`; it is excluded by `.gitignore`. Quote dotenv values that
contain spaces or `#`.

### 5. Optional sample data, then run

```bash
python seed.py
python app.py
```

Open **http://127.0.0.1:5000** in your Windows browser. Leave the Ubuntu terminal
running. Stop the app with Ctrl+C. `seed.py` refuses to modify a nonempty database.
Skipping it gives you an empty tracker.

For future sessions:

```bash
cd ~/cop4751/job-application-tracker
source .venv/bin/activate
sudo service mysql start
python app.py
```

## Native Windows alternative

Install Python and MySQL Server as described in Assignment 1. In PowerShell:

```powershell
cd path\to\job-application-tracker
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

In MySQL Workbench, open `schema.sql` and execute the entire file. Create the
application user and grant permissions using the SQL above. Edit `.env`, then
run `python seed.py` (optional) and `python app.py`. If PowerShell blocks virtual
environment activation, run `.\.venv\Scripts\python.exe` directly instead.

## How to use it

1. Add a company.
2. Add a job and choose its company. Enter required skills separated by commas.
3. Add an application and choose a job. Track its status and resume version.
4. Add contacts and associate them with companies.
5. Click a row's title/date to open its details, or use Edit/Delete.
6. Visit Job Match and enter your skills, such as `Python, SQL, Flask`.

Interview details accept a JSON object, for example:

```json
{"round": "Technical", "date": "2026-10-23", "notes": "Review SQL joins"}
```

Applications do not send emails or upload resumes. `resume_version` is a text
label, and interview JSON stores notes rather than scheduling external events.

### Skill matching

`matching.py` normalizes case, trims whitespace, and removes duplicate skills.
It computes `100 × matched required skills / total required skills`. The UI
rounds to the nearest whole percent; sorting uses the unrounded score. Ties are
ordered by job title and ID. A job with no listed requirements scores 0% and is
labeled accordingly. Extra user skills do not lower a score. Exact names are
required: `JS` does not automatically mean `JavaScript`, and `C` differs from
`C++`. This is explainable skill overlap, not an AI prediction of hiring success.

With sample data, `Python, SQL, Flask` matches Software Developer at 100%, Data
Analyst at 67% (missing Tableau), Platform Engineer at 33%, and Frontend Developer
at 0%. No AI API key or paid service is required.

## Database design

| Table | Primary key | Relationship | Special columns |
|---|---|---|---|
| companies | company_id | Parent of jobs and contacts | company_name is required |
| jobs | job_id | company_id → companies | job_type ENUM, requirements JSON |
| applications | application_id | job_id → jobs | status ENUM, interview_data JSON, cover_letter_sent BOOLEAN |
| contacts | contact_id | company_id → companies | contact_name is required |

All tables use InnoDB. Foreign keys use `ON DELETE RESTRICT`, preventing silent
loss of applications or contacts. MySQL indexes foreign keys; additional indexes
cover job titles and application status/date. Salary CHECK constraints protect
values even if someone bypasses the web forms. Each database operation commits
on success, rolls back on failure, and closes its cursor and connection.

## Project files

```text
app.py                 Flask routes, CSRF checks, form flow, error pages
database.py           MySQL connections, CRUD and JOIN/report queries
models.py             Trusted table and form definitions
validation.py         Server-side validation and JSON conversion
matching.py           Skill normalization and ranking
schema.sql            Database and all four tables
seed.py               Optional fictional sample data
templates/            Shared list/detail/edit/delete templates, dashboard, matching
static/style.css      Responsive styling (no CDN required)
tests/                MySQL integration and matching tests
.github/workflows/    CI test workflow
AI_USAGE.md           Transparent AI development record
docs/                 Walkthrough, test report, and submission checklist
video/                Recorded demonstration (see video/README.md)
requirements.txt      Runtime Python dependencies
requirements-dev.txt  Test dependencies
.env.example          Configuration template; no real credentials
```

The same generic templates serve all four tables, so there is no duplicated
companies/jobs/applications/contacts form logic. Table identifiers come only
from `models.py`; submitted values use MySQL `%s` parameters.

## Tests

Tests **delete all rows in the dedicated test database** at the beginning of each
test. They never use the application database. The name defaults to
`job_tracker_test` and must end in `_test`. Use a separate disposable test database.

As a MySQL administrator, run once:

```sql
CREATE DATABASE IF NOT EXISTS job_tracker_test;
GRANT ALL PRIVILEGES ON job_tracker_test.* TO 'job_tracker_app'@'localhost';
```

Then, from the active Python environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests use `.env` connection settings and create the test tables automatically.
They cover actual MySQL reads/writes, all CRUD workflows, validation, foreign-key
restrictions, SQL/HTML injection handling, CSRF, matching, and rollback. The
included GitHub Actions workflow runs these against a MySQL 8.0 service when
pushed; that hosted run is not claimed to have occurred yet.

## Publish to GitHub

The existing commits are honestly attributed to Codex; they represent sequential
implementation and test checkpoints, not a fabricated student work history.
Before publishing, review and understand the code and update `AI_USAGE.md` with
what you personally changed and learned.

Create an **empty** GitHub repository named `job-application-tracker` (do not add
a README, license, or .gitignore on GitHub if pushing this existing history).
Choose public, or private and add your instructor as a collaborator. Then:

```bash
git status
git log --oneline
# Replace YOUR_USERNAME with your GitHub username:
git remote add origin https://github.com/YOUR_USERNAME/job-application-tracker.git
git push -u origin main
```

Authenticate using your normal GitHub credential flow, SSH, or a personal access
token; do not paste credentials into source code or send them to ChatGPT. If a
remote already exists, inspect `git remote -v` before changing it. Do not
force-push over an existing course repository. If you already have one, ask for
help merging this project into it.

Configure your own identity for future commits (this does not rewrite earlier
commits):

```bash
git config user.name "Lucas Ramos"
git config user.email "YOUR_GITHUB_EMAIL"
```

For your future changes, commit and push meaningful milestones:

```bash
git add app.py database.py templates static AI_USAGE.md
git commit -m "Describe the feature or fix you actually made"
git push
```

Check that the actual recorded video file is visible in the repository. Submit
`https://github.com/YOUR_USERNAME/job-application-tracker`, not the ZIP or localhost
URL. See `docs/SUBMISSION_CHECKLIST.md` before submission.

## Troubleshooting

- **Database unavailable / 503:** run `sudo service mysql status`, verify `.env`,
  confirm the database was created, and inspect the terminal error.
- **Access denied:** the password or MySQL user/host grant does not match. Verify
  with `mysql -h 127.0.0.1 -u job_tracker_app -p job_tracker`.
- **Unknown column:** you likely pointed the app at the earlier assignment schema.
  Compare it with `schema.sql`; use a fresh database after backing up your work.
- **Cannot delete:** delete/reassign applications before jobs, then jobs and
  contacts before companies. The confirmation page explains the restriction.
- **Form expired:** reload the form, especially after restarting the server.
- **Invalid JSON:** use double quotes and a JSON object, not a list or Python dict.
- **Port 5000 busy:** stop the earlier server or use
  `python -m flask --app app run --port 5001` and open that port.
- **Missing Python package:** activate `.venv` and reinstall requirements.

## Development assistance

See `AI_USAGE.md` for the actual AI assistance used. The student should review,
run, explain, and personalize this project before submitting it.
