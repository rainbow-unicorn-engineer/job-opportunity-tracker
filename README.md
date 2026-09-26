# Job Opportunity Tracker

An automated job search pipeline: discovers software engineering roles across the market, monitors company ATS boards directly, tailors a resume to each job description without fabricating experience, tracks every application through interview and offer, and surfaces it all in a filterable dashboard.

Built because the manual loop (search boards, read JDs, rewrite resume, track spreadsheet, chase email) does not scale, and the interesting parts of a job search are the decisions, not the data entry.

## How it works

```mermaid
flowchart TD
    A["Aggregator APIs<br/>Adzuna · JSearch · Jooble"] -->|search titles + criteria| B["DISCOVERY<br/>new postings across the market"]
    B --> C["ENRICHMENT<br/>detect ATS from apply URL<br/>research each company once"]
    C --> DB[("SQLite<br/>companies · jobs · applications · emails")]
    C -->|adds company slug| P["Poll list<br/>Greenhouse · Lever · Ashby · …"]
    P --> M["MONITORING (daily)<br/>poll each company's ATS directly<br/>flag new · closed · stale"]
    M --> DB
    DB --> S["MATCH SCORING<br/>fit score · coverage score<br/>level-inflation flag · exclude filters"]
    S --> T["TAILORING<br/>tailored resume · change table<br/>interview prep sheet"]
    T --> APP["APPLICATIONS<br/>you review and apply"]
    APP --> DB
    G["GMAIL POLLER<br/>classify mail · link to application<br/>auto-update status"] --> DB
    DB --> D["DASHBOARD + DAILY DIGEST<br/>action queue · CRM · trends · map"]
```

**1. Discovery.** Aggregator APIs (Adzuna, JSearch over Google's job index, Jooble) search the whole market by title, level, location, and salary. Solves the "companies I don't know exist" problem and reaches enterprise postings on Workday and iCIMS through Google's crawl.

**2. Enrichment.** Each posting's apply URL identifies the company's ATS (Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee; Workday and iCIMS as a fragile second tier) and yields the board slug. The poll list grows itself from search results. Per-company research (industry, size, culture links) runs once and is cached.

**3. Monitoring.** Daily polls of every discovered company's public ATS endpoint catch postings at the source instead of days later through aggregators. Seen-ID diffing means only new jobs flow downstream; postings that disappear are marked closed, which also yields time-to-fill data per company.

**4. Tailoring.** For each greenlit job: extract JD keywords weighted by importance (title > requirements > nice-to-have), match against the base resume with synonym detection, rewrite in the JD's vocabulary with a hard rule against fabricating experience, and emit the tailored resume plus a change table (keyword | importance | present before | what changed | where | why). The change table doubles as an interview prep sheet.

**5. Gmail integration.** Read-only OAuth scoped to a job label. Classifies mail (confirmation, rejection, interview invite, scheduling, recruiter outreach, offer), links messages to application records by sender domain, and feeds a prioritized action queue: time-sensitive first, aging unanswered second, new inbound third.

**6. Dashboard.** SQLite under everything; a filterable CRM showing every captured field (company, posted date, level, specialty, stack, remote/hybrid, location, salary, company profile, apply URL) plus tracking: interest, applied date, match score, responses, interview schedule and contacts, and exactly which resume version was sent.

## Feature set

- Cross-aggregator dedupe (fuzzy match on company + title + location)
- Closed-job detection with per-company time-to-fill stats
- Resume version archival: the exact file sent with each application, retrievable when the interview lands
- Match scoring (level fit, stack overlap, salary floor, remote preference) so the queue sorts by "apply first," not "newest"
- Outbound follow-up reminders (applied N days ago, silence since)
- Per-job interview prep sheet generated from the keyword analysis
- Morning digest: new matches, status changes, today's action queue

## What this deliberately does not do

- No LinkedIn scraping or bot-detection evasion. LinkedIn coverage comes from its own alert emails, parsed from the owner's inbox.
- No auto-submitted applications. Every application is reviewed and sent by a human.
- No fabricated resume content. Tailoring rewords true experience into the JD's vocabulary; the change table makes every edit auditable.

## Stack

Python, SQLite, public ATS posting APIs, Adzuna / JSearch / Jooble APIs, Gmail API (read-only OAuth), Claude API for JD analysis, email classification, and tailoring.

## Status

| Milestone | State |
|---|---|
| Discovery: aggregator clients + search config | in progress |
| Tailoring: keyword engine + change table | next |
| Monitoring: ATS pollers + dedupe + closed-job detection | queued |
| Gmail: classification + action queue | queued |
| Enrichment: company research cache | queued |
| Dashboard | last, data-first on purpose |

Build order is compressed for time-to-first-application: get real postings flowing and applications out the door, then layer in monitoring, email, and UI behind them.

## Setup

1. API keys: Adzuna (developer.adzuna.com), OpenWebNinja JSearch API key (app.openwebninja.com), both free tiers
2. `cp config.example.yaml config.yaml` and set search criteria: titles, level range, locations, remote stance, salary floor
3. `pip install -r requirements.txt`
4. `python -m pipeline.discover` to run the first search

See `docs/SPEC.md` for the full technical specification.
