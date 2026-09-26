"""Adzuna client. Docs: https://developer.adzuna.com/docs/search"""
import requests

from ..normalize import Posting, parse_work_mode

BASE = "https://api.adzuna.com/v1/api/jobs/us/search/{page}"


def search(app_id: str, app_key: str, what: str, where: str = "",
           max_pages: int = 2, results_per_page: int = 50) -> list[Posting]:
    postings: list[Posting] = []
    for page in range(1, max_pages + 1):
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": what,
            "results_per_page": results_per_page,
            "content-type": "application/json",
        }
        if where:
            params["where"] = where
        r = requests.get(BASE.format(page=page), params=params, timeout=30)
        r.raise_for_status()
        results = r.json().get("results", [])
        if not results:
            break
        for j in results:
            postings.append(Posting(
                source="adzuna",
                source_id=str(j.get("id", "")),
                company=(j.get("company") or {}).get("display_name", ""),
                title=j.get("title", ""),
                location=(j.get("location") or {}).get("display_name", ""),
                work_mode=parse_work_mode(j.get("description", "")),
                salary_min=int(j["salary_min"]) if j.get("salary_min") else None,
                salary_max=int(j["salary_max"]) if j.get("salary_max") else None,
                posted_at=j.get("created"),
                apply_url=j.get("redirect_url", ""),
                jd_text=j.get("description", ""),
            ))
    return postings
