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
