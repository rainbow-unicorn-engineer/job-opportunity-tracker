"""Discovery: query aggregators with the config's criteria, dedupe, store.

Run:  python -m pipeline.discover
"""
import json
import sys
from pathlib import Path

import yaml

from .db import init_db
from .normalize import Posting, level_inflation_flag, now_iso, _norm
from .sources import adzuna, jsearch, jooble

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        sys.exit("config.yaml not found. Copy config.example.yaml and fill in keys.")
    return yaml.safe_load(CONFIG_PATH.read_text())


def gather(cfg: dict) -> list[Posting]:
    postings: list[Posting] = []
    src = cfg.get("sources", {})
    titles = cfg["search"]["titles_preferred"] + cfg["search"].get("titles_acceptable", [])
    locations = cfg["search"].get("locations", [""])

    az = src.get("adzuna", {})
    if az.get("app_id"):
        for title in titles:
            for loc in locations:
                try:
                    postings += adzuna.search(az["app_id"], az["app_key"], title, loc)
                except Exception as e:
                    print(f"[adzuna] {title!r}/{loc!r} failed: {e}")

    js = src.get("jsearch", {})
    if js.get("api_key") or js.get("rapidapi_key"):
        jsearch_key = js.get("api_key") or js.get("rapidapi_key")
        for title in titles:
            for loc in locations:
                q = f"{title} in {loc}" if loc else title
                try:
                    postings += jsearch.search(jsearch_key, q)
                except Exception as e:
                    print(f"[jsearch] {q!r} failed: {e}")

    jb = src.get("jooble", {})
    if jb.get("api_key"):
        for title in titles:
            for loc in locations:
                try:
                    postings += jooble.search(jb["api_key"], title, loc)
                except Exception as e:
                    print(f"[jooble] {title!r}/{loc!r} failed: {e}")
    return postings


def store(postings: list[Posting], cfg: dict) -> tuple[int, int]:
    conn = init_db()
    inserted = duplicates = 0
    seen_keys = {r["dedupe_key"] for r in conn.execute("SELECT dedupe_key FROM jobs")}

    for p in postings:
        if p.dedupe_key in seen_keys:
            duplicates += 1
            continue
        company_norm = _norm(p.company)
        if not company_norm:
            continue
        conn.execute(
            "INSERT OR IGNORE INTO companies (name, name_normalized) VALUES (?, ?)",
            (p.company, company_norm),
        )
        company_row = conn.execute(
            "SELECT id FROM companies WHERE name_normalized = ?", (company_norm,)
        ).fetchone()
        if company_row is None:
            print(f"[discover] skipping {p.title!r}: could not resolve company {p.company!r}")
            continue
        company_id = company_row["id"]

        conn.execute(
            """INSERT OR IGNORE INTO jobs
               (profile_id, company_id, source, source_id, dedupe_key, title, level,
                specialty, location, work_mode, salary_min, salary_max, posted_at,
                first_seen_at, apply_url, jd_text, level_inflation_flag)
               VALUES (1,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (company_id, p.source, p.source_id, p.dedupe_key, p.title, p.level,
             p.specialty, p.location, p.work_mode, p.salary_min, p.salary_max,
             p.posted_at, now_iso(), p.apply_url, p.jd_text,
             level_inflation_flag(p.level, p.jd_text)),
        )
        seen_keys.add(p.dedupe_key)
        inserted += 1

    conn.commit()
    return inserted, duplicates


def main():
    cfg = load_config()
    postings = gather(cfg)
    inserted, duplicates = store(postings, cfg)
    print(f"fetched {len(postings)} postings | new {inserted} | cross-source dupes {duplicates}")


if __name__ == "__main__":
    main()
