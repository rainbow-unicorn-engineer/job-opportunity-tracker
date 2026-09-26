"""JSearch client (OpenWebNinja). Returns results from Google's job index,
which is how Workday/iCIMS enterprise career sites enter the pipeline."""
import requests

from ..normalize import Posting

BASE = "https://api.openwebninja.com/jsearch/search-v2"


def search(api_key: str, query: str, num_pages: int = 1,
           remote_only: bool = False) -> list[Posting]:
    headers = {
        "X-API-Key": api_key,
    }
    params = {
        "query": query,                 # e.g. "software engineer in Dallas, TX"
        "num_pages": num_pages,
        "date_posted": "week",
    }
    if remote_only:
        params["work_from_home"] = "true"
    r = requests.get(BASE, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    postings: list[Posting] = []
    payload = r.json() or {}
    data = payload.get("data")
    if isinstance(data, dict):
        rows = data.get("jobs") or data.get("data") or []
    elif isinstance(data, list):
        rows = data
    else:
        rows = payload.get("jobs") or []
    if isinstance(rows, dict):
        rows = rows.get("jobs") or rows.get("data") or []
    if not isinstance(rows, list):
        rows = []
    for j in rows:
        if not isinstance(j, dict):
            continue
        mode = "remote" if j.get("job_is_remote") else "unknown"
        salary_min = j.get("job_min_salary")
        salary_max = j.get("job_max_salary")
        postings.append(Posting(
            source="jsearch",
            source_id=str(j.get("job_id", "")),
            company=j.get("employer_name", ""),
            title=j.get("job_title", ""),
            location=", ".join(filter(None, [j.get("job_city"), j.get("job_state")])),
            work_mode=mode,
            salary_min=int(salary_min) if salary_min else None,
            salary_max=int(salary_max) if salary_max else None,
            posted_at=j.get("job_posted_at_datetime_utc"),
            apply_url=j.get("job_apply_link", ""),
            jd_text=j.get("job_description", ""),
        ))
    return postings
