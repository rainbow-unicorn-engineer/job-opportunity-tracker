"""Normalize postings from any source into one shape; dedupe across sources."""
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Posting:
    source: str
    source_id: str
    company: str
    title: str
    location: str = ""
    work_mode: str = "unknown"
    salary_min: int | None = None
    salary_max: int | None = None
    posted_at: str | None = None
    apply_url: str = ""
    jd_text: str = ""
    level: str = "unknown"
    specialty: str = "other"
    dedupe_key: str = field(default="", init=False)

    def __post_init__(self):
        self.level = parse_level(self.title, self.jd_text)
        self.specialty = parse_specialty(self.title)
        self.dedupe_key = make_dedupe_key(self.company, self.title, self.location)


def _norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"\b(inc|llc|ltd|corp|co)\b\.?", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def make_dedupe_key(company: str, title: str, location: str) -> str:
    # Location reduced to first token (city) so "Dallas, TX" == "Dallas, Texas"
    city = _norm((location or "").split(",")[0])
    return f"{_norm(company)}|{_norm(title)}|{city}"


LEVEL_PATTERNS = [
    ("principal", r"\bprincipal\b"),
    ("staff", r"\bstaff\b"),
    ("senior", r"\bsenior\b|\bsr\.?\b|\biii\b"),
    ("mid", r"\bii\b|\bmid[- ]?level\b"),
    ("junior", r"\bjunior\b|\bjr\.?\b|\bentry[- ]?level\b|\bassociate\b|\bi\b$"),
    ("intern", r"\bintern(ship)?\b"),
]

YEARS_RE = re.compile(r"(\d+)\+?\s*(?:to\s*\d+\s*)?years?", re.I)


def parse_level(title: str, jd_text: str = "") -> str:
    t = title.lower()
    for level, pat in LEVEL_PATTERNS:
        if re.search(pat, t):
            return level
    return "unknown"


def level_inflation_flag(title_level: str, jd_text: str) -> str | None:
    """Title says one thing, requirements say another. Both directions matter."""
    years = [int(m.group(1)) for m in YEARS_RE.finditer(jd_text or "")]
    if not years:
        return None
    max_years = max(years)
    if title_level in ("junior", "mid", "unknown") and max_years >= 5:
        return "title-below-reqs"   # the meme: entry level, 5 years experience
    if title_level in ("senior", "staff") and max_years <= 2:
        return "title-above-reqs"   # hidden good target
    return None


SPECIALTY_PATTERNS = [
    ("ai", r"\bai\b|\bml\b|\bllm\b|\bagent\b|machine learning|applied ai|genai"),
    ("fullstack", r"full[- ]?stack"),
    ("frontend", r"front[- ]?end|\bui\b|react developer"),
    ("backend", r"back[- ]?end|\bapi\b engineer"),
    ("platform", r"\bplatform\b|\binfra(structure)?\b|\bdevops\b|\bsre\b"),
]


def parse_specialty(title: str) -> str:
    t = title.lower()
    for spec, pat in SPECIALTY_PATTERNS:
        if re.search(pat, t):
            return spec
    return "other"


def parse_work_mode(text: str) -> str:
    t = (text or "").lower()
    if "remote" in t:
        return "hybrid" if "hybrid" in t else "remote"
    if "hybrid" in t:
        return "hybrid"
    if "on-site" in t or "onsite" in t or "in office" in t:
        return "onsite"
    return "unknown"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
