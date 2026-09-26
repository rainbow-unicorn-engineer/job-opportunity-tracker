"""SQLite schema and helpers. One DB, every layer reads/writes through here."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "jobtracker.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    base_resume_path TEXT,
    criteria_json TEXT,
    synonym_map_json TEXT,
    skills_inventory_json TEXT
);

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL UNIQUE,
    ats_type TEXT,               -- greenhouse|lever|ashby|smartrecruiters|workable|recruitee|workday|icims|unknown
    ats_slug TEXT,
    industry TEXT,
    size TEXT,
    hq TEXT,
    careers_url TEXT,
    research_json TEXT,
    researched_at TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    profile_id INTEGER NOT NULL DEFAULT 1 REFERENCES profiles(id),
    company_id INTEGER REFERENCES companies(id),
    source TEXT NOT NULL,        -- adzuna|jsearch|jooble|ats:<type>|linkedin-alert|manual
    source_id TEXT NOT NULL,
    dedupe_key TEXT NOT NULL,
    title TEXT NOT NULL,
    level TEXT,                  -- parsed: intern|junior|mid|senior|staff|principal|unknown
    specialty TEXT,              -- fullstack|frontend|backend|ai|platform|other
    stack_json TEXT,
    location TEXT,
    work_mode TEXT,              -- remote|hybrid|onsite|unknown
    salary_min INTEGER,
    salary_max INTEGER,
    posted_at TEXT,
    first_seen_at TEXT NOT NULL,
    closed_at TEXT,
    apply_url TEXT,
    jd_text TEXT,
    match_score REAL,
    level_inflation_flag TEXT,   -- null | 'title-below-reqs' | 'title-above-reqs'
    stale_flag TEXT,             -- null | reason: age|company-median|repost-cycle
    UNIQUE(source, source_id)
);
CREATE INDEX IF NOT EXISTS idx_jobs_dedupe ON jobs(dedupe_key);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    status TEXT NOT NULL DEFAULT 'saved',
    -- saved|applied|screening|interviewing|offer|rejected|withdrawn|ghosted
    interested INTEGER,
    applied_at TEXT,
    resume_version_id INTEGER,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS resume_versions (
    id INTEGER PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    file_path TEXT NOT NULL,
    change_table_json TEXT,
    prep_sheet_path TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    gmail_msg_id TEXT UNIQUE,
    thread_id TEXT,
    sender TEXT,
    classification TEXT,
    -- confirmation|rejection|interview_invite|scheduling|recruiter_outreach|offer|noise
    received_at TEXT,
    action_needed INTEGER DEFAULT 0,
    responded_at TEXT
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    name TEXT,
    role TEXT,
    email TEXT,
    linkedin_url TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL REFERENCES applications(id),
    type TEXT NOT NULL,          -- screen|interview|onsite|offer|deadline
    scheduled_at TEXT,
    with_whom TEXT,
    outcome TEXT
);
"""


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = connect(db_path)
    conn.executescript(SCHEMA)
    conn.execute(
        "INSERT OR IGNORE INTO profiles (id, name) VALUES (1, 'danielle')"
    )
    conn.commit()
    return conn
