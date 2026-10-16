"""Trusted form/table metadata. Never take SQL identifiers from user input."""
def field(name, label, kind='text', required=False, maximum=None, choices=None):
    return dict(name=name, label=label, kind=kind, required=required,
                maximum=maximum, choices=choices or [])

TABLES = {
    'companies': dict(singular='Company', pk='company_id', title='company_name', fields=[
        field('company_name', 'Company name', required=True, maximum=100),
        field('industry', 'Industry', maximum=50), field('website', 'Website', 'url', maximum=200),
        field('city', 'City', maximum=50), field('state', 'State', maximum=50),
        field('notes', 'Notes', 'textarea', maximum=10000),
    ]),
}
JOB_TYPES = ['Full-time', 'Part-time', 'Contract', 'Internship']
TABLES['jobs'] = dict(singular='Job', pk='job_id', title='job_title', fields=[
    field('company_id', 'Company', 'foreign', True),
    field('job_title', 'Job title', required=True, maximum=100),
    field('job_type', 'Job type', 'select', choices=JOB_TYPES),
    field('salary_min', 'Minimum annual salary ($)', 'number'),
    field('salary_max', 'Maximum annual salary ($)', 'number'),
    field('job_url', 'Job URL', 'url', maximum=300), field('date_posted', 'Date posted', 'date'),
    field('requirements', 'Required skills', 'skills', maximum=10000),
])
STATUSES = ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn']
TABLES['applications'] = dict(singular='Application', pk='application_id', title='application_date', fields=[
    field('job_id', 'Job', 'foreign', True), field('application_date', 'Application date', 'date', True),
    field('status', 'Status', 'select', True, choices=STATUSES),
    field('resume_version', 'Resume version', maximum=50),
    field('cover_letter_sent', 'Cover letter sent', 'checkbox'),
    field('interview_data', 'Interview details (JSON)', 'json', maximum=10000),
])
TABLES['contacts'] = dict(singular='Contact', pk='contact_id', title='contact_name', fields=[
    field('company_id', 'Company', 'foreign', True),
    field('contact_name', 'Contact name', required=True, maximum=100),
    field('title', 'Title', maximum=100), field('email', 'Email', 'email', maximum=100),
    field('phone', 'Phone', maximum=20), field('linkedin_url', 'LinkedIn URL', 'url', maximum=200),
    field('notes', 'Notes', 'textarea', maximum=10000),
])
