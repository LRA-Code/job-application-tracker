# Validation report

Prepared October 16, 2026 by the coding agent. These checks ran in the development
environment; they are not claims of a student-run test or a GitHub-hosted CI run.

## Environment

- Python 3.12.
- Flask 3.1.3 and mysql-connector-python 26.7.0.
- MySQL Community Server 8.0.46, InnoDB, actual SQL persistence.
- Chromium 134 through Playwright for browser workflow checks.

## Automated suite

Run with `python -m pytest -q` using the dedicated `job_tracker_test` database.
**Final result: 16 passed** against MySQL 8.0.46. All tests completed successfully.

Coverage includes:

- Create/read/update/delete through Flask routes for all four tables.
- Required names, maximum lengths, email/URL validation, salary limits/ranges,
  invalid dates, invalid enums, nonexistent foreign keys, and malformed JSON.
- MySQL persistence and JSON round-trips; unchecked cover-letter state.
- Parent-deletion refusal for companies/jobs with dependent rows.
- Safe handling of literal SQL/HTML injection strings and missing CSRF tokens.
- Missing-record 404 pages and unknown-table rejection.
- Dashboard aggregate totals and status counts.
- Skill-match 100%/67% examples, empty requirements, duplicates, case normalization,
  exact token matching, C++/C# distinction, and empty input.
- Rollback after an interrupted database transaction.
- Database outage handling, database-enforced checks/foreign keys/JSON validity,
  and refusal to seed a nonempty database.

## Browser workflow

Passed a complete browser run against the live Flask/MySQL application:

1. Loaded the dashboard with fictional sample data.
2. Created, viewed, and edited a company, job, application, and contact.
3. Confirmed updated application status and interview JSON.
4. Matched Python/SQL/Flask and asserted 100% and 67% results.
5. Attempted to delete a parent with dependents and verified refusal.
6. Deleted all four demonstration records in dependency order using confirmation.
7. Inspected actual SQL JOIN/aggregate/foreign-key output and server request logs.
8. Checked browser JavaScript errors: none.
9. Inspected desktop and 390-pixel mobile screenshots; mobile dashboard has no
   page-wide horizontal overflow. Navigation can scroll horizontally on mobile.

## Scope and remaining checks

The app is for local single-user use and has no authentication. No external AI API
is used. Tests and the recording use fictional data. Your own MySQL installation,
credentials, GitHub upload, instructor access, and classroom submission still
need to be verified. The GitHub Actions configuration is supplied but has not
been run on GitHub by this agent.

## Recording verification

The MP4 was successfully encoded as H.264 and inspected. Its duration is 221.56
seconds (3:42), inside the required 3–7 minute range. A sampled frame confirms
readable application content and captions. The file is approximately 2.8 MiB.
