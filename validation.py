"""Server-side validation shared by create and edit forms."""
import json
import re
from datetime import date
from urllib.parse import urlsplit

def validate(fields, form):
    values, errors = {}, {}
    for f in fields:
        name, kind = f['name'], f['kind']
        raw = form.get(name, '').strip()
        value = raw or None
        try:
            if f['required'] and not raw:
                raise ValueError('This field is required.')
            if raw and f['maximum'] and len(raw) > f['maximum']:
                raise ValueError(f'Maximum {f["maximum"]} characters.')
            if kind == 'checkbox':
                value = 1 if raw == '1' else 0
            elif raw and kind in ('number', 'foreign'):
                if not re.fullmatch(r'\d+', raw):
                    raise ValueError('Enter a whole, non-negative number.')
                value = int(raw)
                if value > 2147483647 or (kind == 'foreign' and value == 0):
                    raise ValueError('Number is outside the allowed range.')
            elif raw and kind == 'date':
                parsed = date.fromisoformat(raw)
                if parsed.year < 1000:
                    raise ValueError('Use a date in year 1000 or later.')
                value = parsed.isoformat()
            elif raw and kind == 'select' and raw not in f['choices']:
                raise ValueError('Choose a listed option.')
            elif raw and kind == 'url':
                url = urlsplit(raw)
                if url.scheme not in ('http', 'https') or not url.netloc or any(c.isspace() for c in raw):
                    raise ValueError('Enter a full http:// or https:// URL.')
            elif raw and kind == 'email' and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', raw):
                raise ValueError('Enter a valid email address.')
            elif kind == 'skills':
                skills = list(dict.fromkeys(s.strip().casefold() for s in re.split(r'[,\n]', raw) if s.strip()))
                if len(skills) > 100 or any(len(s) > 100 for s in skills):
                    raise ValueError('Use at most 100 skills, each at most 100 characters.')
                value = json.dumps(skills)
            elif kind == 'json':
                obj = json.loads(raw) if raw else {}
                if not isinstance(obj, dict):
                    raise ValueError('Enter a JSON object, for example {"round": "Technical"}.')
                value = json.dumps(obj)
        except (ValueError, OverflowError) as exc:
            errors[name] = str(exc) if not isinstance(exc, json.JSONDecodeError) else 'Enter valid JSON.'
        values[name] = value
    low, high = values.get('salary_min'), values.get('salary_max')
    if isinstance(low, int) and isinstance(high, int) and low > high:
        errors['salary_max'] = 'Maximum salary must be at least the minimum salary.'
    return values, errors
