# GenAI Usage Documentation

## Tools used

ChatGPT (Codex coding agent) assisted with implementation, documentation, test
creation, debugging, and packaging on October 16, 2026. No Claude, Gemini, or
other AI service is claimed. The application itself does not call a GenAI API.

## Actual user prompt and supplied instructions

The user supplied `Project_Specification.docx`, `AdvancedDBAssignments1-5.zip`,
and asked:

> Follow the instructions in this word document to make this project.

Additional supplied instructions required a GitHub repository URL, a recorded
video file, `app.py`, `database.py`, HTML templates, CSS, `schema.sql`,
`AI_USAGE.md`, `README.md`, and `requirements.txt`. They also directed starting
with one table, completing CRUD before proceeding, committing frequently,
testing features, and understanding generated code. The user added:

> Build the whole thing if possible, but I will tell you if I get stuck

These are the actual prompts. The following development decisions were made by
the coding agent; they are not invented additional prompts from the student.

## Assistance provided

- Read the final specification and supporting practice assignments; prioritized
  the final four-table schema where older exercises differed.
- Built Companies CRUD first and tested it against MySQL, then implemented and
  tested Jobs, Applications, and Contacts in successive commits.
- Wrote reusable table metadata, shared templates, parameterized SQL functions,
  form validation, dashboard JOIN/aggregate queries, and skill ranking.
- Added responsive CSS, confirmation pages, friendly error handling, CSRF checks,
  test fixtures, sample data, and setup/submission documentation.
- Prepared a recorded automated demonstration when supported by the environment;
  see `video/README.md` for the delivered recording and its provenance.

## What worked well

Shared form metadata reduced repeated code across four tables. Parameterized
queries separated SQL syntax from user values. Deterministic skill matching
made percentages easy to explain and test. Tests against an actual MySQL server
verified JSON serialization, foreign-key restrictions, transactions, and CRUD
rather than relying only on mocked database calls.

## Revisions made during AI-assisted development

These were agent-made corrections or design refinements, **not claims of edits
personally made by the student**:

- Followed the final specification's `job_url`, `requirements`, `interview_data`,
  and ENUM definitions instead of copying the older practice schema unchanged.
- Added salary-range validation, URL scheme checks, JSON-object validation,
  foreign-key dropdown validation, and database CHECK constraints.
- Chose RESTRICT deletion to prevent silently cascading through applications.
- Fixed the test schema loader interaction with a semicolon in a SQL comment.
- Made dropdown job names include company names to distinguish similar titles.
- Defined empty requirements as 0% and removed duplicate skills before scoring.
- Added explicit boundaries between the app database and destructive test data.

## Concepts to understand before submission

This list is a review guide, not a claim that the student has already learned it:

1. A foreign key connects a child row to an existing parent. RESTRICT prevents
   deleting a parent while children reference it.
2. `%s` placeholders bind data as values; trusted table identifiers come from a
   fixed metadata dictionary, not from arbitrary form input.
3. A transaction is committed on success and rolled back on failure. Connections
   and cursors must be closed in both cases.
4. POST changes data. GET lists, shows, or requests confirmation. CSRF tokens
   prevent another page from silently submitting a valid mutation form.
5. JSON columns store structured data. Python serializes lists/objects with
   `json.dumps` and reads them with `json.loads`.
6. Matching measures required-skill coverage: two of three skills is about 67%.
   Case and duplicates are normalized; synonyms are not inferred.
7. A passing automated test is evidence for a specific behavior, not proof that
   every possible environment or user input is correct.

## Student review — complete honestly before submission

- Code I personally reviewed and can explain: **To be completed by the student.**
- Changes I personally made after receiving AI output: **To be completed by the student; write “none” if none.**
- What I learned from using GenAI: **To be completed in my own words.**
- Problems I encountered locally and how I resolved them: **To be completed after running locally.**
- Date I ran the app and tests on my computer: **To be completed.**

The agent must not invent these personal experiences. The Git history preserves
agent-authored milestones under the Codex identity. Future student edits should
use the student's own configured Git identity.
