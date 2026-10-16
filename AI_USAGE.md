# GenAI Usage Documentation

## Tools used

ChatGPT (Codex coding agent) assisted with implementation, documentation,
test creation, debugging, and packaging on October 16, 2026. The
application itself does not call a GenAI API.

## Actual user prompt and supplied instructions

I supplied `Project_Specification.docx` and supporting assignment
materials. My original request included:

> Follow the instructions in this word document to help me make this project.

The supplied instructions required a GitHub repository URL, a recorded
video file, `app.py`, `database.py`, HTML templates, CSS, `schema.sql`,
`AI_USAGE.md`, `README.md`, and `requirements.txt`.

They also directed starting with one table, completing CRUD before
moving to the next, committing frequently, testing features, and
understanding the generated code.

## Assistance provided

- Read the specification and supporting assignments, using the final
  project schema where earlier exercises differed.
- Built and tested Companies CRUD first, followed by Jobs, Applications,
  and Contacts in separate local commits.
- Generated database functions, shared form definitions, HTML templates,
  input checks, dashboard queries, and skill-matching code.
- Added CSS, deletion confirmation, error messages, CSRF checks, tests,
  sample data, and setup instructions.
- Guided me through local setup and helped when I encountered problems
  with terminal commands and configuration.
- Explained how the files, functions, and database tables work together.
- Provided guidance for recording the demonstration. I recorded the
  submitted video myself without narration.

## What worked well

Shared forms and templates reduced repeated code across the four tables.
Parameterized queries kept submitted values separate from SQL commands.

The matching calculation was easy to check with examples. Matching two
of three required skills produced a result of about 67%.

The setup instructions helped me connect Flask to MySQL. Browser checks
let me test the features myself, and the automated tests checked database
operations, input validation, relationships, and matching.

## Revisions made during AI-assisted development

The coding agent made these changes while developing the application:

- Followed the final specification's `job_url`, `requirements`,
  `interview_data`, and ENUM definitions.
- Added salary-range checks, URL checks, JSON-object validation,
  foreign-key dropdown checks, and database CHECK constraints.
- Used RESTRICT deletion to prevent removing records that still had
  related records.
- Fixed a schema-loading issue involving a semicolon in a SQL comment.
- Added company names to job dropdown labels.
- Removed repeated skills before calculating matches and assigned 0%
  when a job had no listed requirements.
- Kept the test database separate from the application database.

These were changes made by the coding agent. My changes involved local
configuration and data entered through the application.

## Concepts to understand before submission

1. A foreign key links a record to a record in another table. RESTRICT
   prevents deleting the parent while related records still reference it.
2. `%s` placeholders pass values separately from SQL instructions.
   Table and column names come from the app's defined metadata.
3. A transaction commits changes when an operation succeeds and rolls
   them back when it fails. Connections and cursors must be closed.
4. GET requests display pages and forms. POST requests submit data.
   CSRF tokens help protect form submissions.
5. JSON columns store structured data. Python uses `json.dumps` and
   `json.loads` to convert between JSON text and Python values.
6. Matching measures how many required skills the user has. Two of
   three required skills gives about 67%. Case and repeated skills
   are handled, but synonyms are not inferred.
7. Passing tests show that the checked behaviors worked. They do not
   guarantee that every possible input or environment will work.

## Student review — complete honestly before submission

- **Code I personally reviewed and can explain:** I went through a
  walkthrough of the database tables, Flask routes, CRUD functions,
  form checks, and matching code. I still need to practice explaining
  the implementation on my own.

- **Changes I personally made after receiving AI output:** I configured
  the MySQL user and permissions, entered the database settings in
  `.env`, and generated the Flask secret key. I added, edited, and
  deleted records through the app. I also prepared the test database.

- **What I learned from using GenAI:** AI can explain code and guide me
  through setup, but I need to test its output. Running the app showed
  me how Flask connects to MySQL and how record changes affect the
  dashboard. Deleting related records showed why their order matters.

- **Problems I encountered locally and how I resolved them:** I included
  a step number when copying a terminal command, which caused a
  “command not found” error. ChatGPT explained the mistake, and I ran
  the command without the number. It also guided me through database
  configuration and testing.

- **Date I ran the app and tests on my computer:** October 16, 2026.
  I checked the features in my browser and ran `python -m pytest -q`.
  All 16 tests passed.

The Git history preserves agent-authored commits under the Codex
identity. Future code changes I make will use my own Git identity
and will be documented here.
