# Understand the project before submitting

## Follow one request through the code

Start with Companies. Visit `/companies/new` in your browser.

1. Flask calls `edit()` in `app.py`, with `table='companies'` and no record ID.
2. `metadata()` checks that the table is one of the four allowed names.
3. `form.html` builds inputs from the fields in `models.py`.
4. Clicking Save submits a POST request with the form's CSRF token.
5. `check_csrf()` verifies the token against the current browser session.
6. `validate()` strips whitespace, checks required values and lengths, and
   validates each field according to its type.
7. `save_record()` in `database.py` builds an INSERT using trusted column names.
   The actual form values are passed separately as `%s` parameters.
8. `connection()` commits on success, rolls back on error, and always closes.
9. The browser is redirected to `/companies/<id>`, which reads the new row and
   renders `detail.html`.

Editing is the same flow with a record ID: it reads the current values first,
then executes UPDATE. The list route reads records and displays `records.html`.
The delete route uses GET for confirmation and POST for actual deletion.

## Why separate files?

- `app.py`: HTTP requests, responses, session tokens, navigation, error handling.
- `database.py`: SQL and connection lifetime.
- `models.py`: which fields each table has and how forms represent them.
- `validation.py`: convert and reject submitted values before SQL runs.
- `matching.py`: pure ranking logic, easy to test separately.
- `templates/`: HTML presentation; Jinja automatically escapes displayed values.
- `static/style.css`: presentation and responsive layouts.

## How the four tables connect

A company can have many jobs and contacts. A job can have many applications.
The child stores its parent's ID. For example, `jobs.company_id` references
`companies.company_id`; the IDs must refer to an existing parent.

To delete a company with applications, first delete its applications, then its
jobs and contacts, then the company. Alternatively, edit children to point to a
different parent. RESTRICT prevents silent deletion of related information.

## SQL to try in MySQL Workbench

```sql
USE job_tracker;
SHOW TABLES;
SHOW CREATE TABLE jobs;
SELECT j.job_title, c.company_name, j.requirements
FROM jobs AS j JOIN companies AS c ON j.company_id = c.company_id;
SELECT status, COUNT(*) AS application_count
FROM applications GROUP BY status;
SELECT job_title, JSON_EXTRACT(requirements, '$[0]') AS first_skill FROM jobs;
```

The dashboard uses COUNT and GROUP BY. Recent applications use a three-table
JOIN to display the job title and company name rather than just foreign-key IDs.

## Explain the matching algorithm

For a job requiring Python, SQL, and Tableau, a user with Python, SQL, and Flask
matches two of three required skills: `2 / 3 * 100 = 66.67`, displayed as 67%.
The missing skill is Tableau. Flask does not count against the user. Duplicate
skills do not inflate the numerator or denominator. `SQL` and `sql` are equal,
but `C` and `C++` are different.

## Suggested personal practice

- Add a company, job, application, and contact from scratch.
- Change the application from Applied to Interview.
- Try an invalid salary range and explain the validation error.
- Try deleting the company before deleting children and explain the refusal.
- Run tests and locate one assertion for each CRUD operation.
- Make one small useful change you understand, test it, commit it, and record it
  truthfully in AI_USAGE.md.

These are suggested learning steps, not claims that you have already done them.
