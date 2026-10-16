"""Deterministic required-skill coverage, not an AI employment prediction."""
import json
import re

def normalize_skills(skills):
    if isinstance(skills, str):
        skills = re.split(r'[,\n]', skills)
    return {s.strip().casefold() for s in skills if isinstance(s, str) and s.strip()}

def rank_jobs(jobs, user_skills):
    owned = normalize_skills(user_skills)
    ranked = []
    for job in jobs:
        raw = job.get('requirements') or []
        if isinstance(raw, str):
            raw = json.loads(raw)
        required = normalize_skills(raw) if isinstance(raw, list) else set()
        matched, missing = sorted(required & owned), sorted(required - owned)
        score = 100 * len(matched) / len(required) if required else 0
        ranked.append(dict(job=job, matched=matched, missing=missing, total=len(required),
                           score=score, percent=round(score)))
    return sorted(ranked, key=lambda r: (-r['score'], r['job']['job_title'].casefold(), r['job']['job_id']))
