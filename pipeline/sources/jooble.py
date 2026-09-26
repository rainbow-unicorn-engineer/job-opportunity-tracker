"""Jooble client.

Jooble uses POST https://jooble.org/api/{api_key} with a JSON body.
"""
import requests

from ..normalize import Posting, parse_work_mode

BASE = "https://jooble.org/api/{api_key}"


def search(api_key: str, keywords: str, location: str = "", radius: int = 80,
           page: int = 1, companysearch: bool = False) -> list[Posting]:
    payload = {
        "keywords": keywords,
        "location": location,
        "radius": str(radius),
        "page": str(page),
        "companysearch": "true" if companysearch else "false",
    }
    r = requests.post(BASE.format(api_key=api_key), json=payload, timeout=30)
    r.raise_for_status()

    data = r.json() or {}
    postings: list[Posting] = []
    for j in data.get("jobs", []):
        title = j.get("title", "")
        location_value = j.get("location", "")
        snippet = j.get("snippet", "")
        postings.append(Posting(
            source="jooble",
            source_id=str(j.get("id") or j.get("link") or ""),
            company=j.get("company", ""),
            title=title,
            location=location_value,
            work_mode=parse_work_mode(f"{title} {snippet} {location_value}"),
            salary_min=None,
            salary_max=None,
            posted_at=j.get("updated"),
            apply_url=j.get("link", ""),
            jd_text=snippet,
        ))
    return postings