# Stories Bank: Danielle

The prep-sheet generator maps JD keywords to these. Each story: situation, what YOU did, the number. Seeded from your documented work; add, correct, and expand in your own words.

## Money and ownership

**PayNow end to end** — Took a one-product payment MVP and scaled it into the platform across GM Financial. Owned the Offer API SQL schema through the React frontend. $800K build, $1.5M+ written-off debt recovered in under 8 months, ~$700K profit. Non-MyAccount enablement saved $4.8M; $50M+ projection validated across two departments (say "projected," never "realized").

## Architecture decisions

**Quartz to CronJobs** — Always-on Quartz jobs competed with the Offer API for resources. Migrating into the dap-apis monorepo enabled refactoring them into isolated Kubernetes CronJobs that terminate per run: better performance, per-run logs, new jobs a scaffold away (copy a file, change four lines).
**Payment Domain Service generalization** — It was MyAccount-bound; generalized it into a true domain service, integrated Digital Payment Platform v2.1, Stripe 3DS, manual ACH.
**Module-based onboarding** — Shared machinery (micro-frontends, pipelines, feature flags, logger provider auto-onboarding clients to Splunk) built once; new-client work narrows to what actually diverges (document upload or not, token vs tokenless auth).

## Initiative without being asked

**The three agents** — Department's first agentic tooling: ADO sprint-planning agent (one-line ask to full PBI with acceptance criteria and tasks), implementation-spec agent (reads the repo, writes the plan), Splunk agent (investigates incidents on demand). Feature work went from 5-7 days to 1-2. Use this one on every "tell me about leadership" question.
**Reset-account endpoint** — Replaced a manual SQL process with one endpoint serving both the E2E suite and an admin-dashboard widget anyone could use. One piece of infrastructure, two audiences.

## Migration under constraint

**Angular to React in 3 months** — Plus the move onto a private AKS cluster; became SME for the platform infrastructure every DAP application integrates through.
**Testing transformation** — Manual regression of 7 core flows became a Playwright/SauceLabs E2E suite generating the TCR and CPR artifacts PROD sign-off requires.

## Debugging depth (Cisco)

**Personal Webex Calling VM** — Reproduced customer bugs end to end with a physical phone on the line, tracing logs to root cause instead of guessing from tickets.
**1M+ user observability** — Grafana dashboards for Webex Calling worldwide; custom call-processing metrics in Java; wrote the Prometheus YAML; webhook alerting that routed each alert to its owning team.

## Observability pipeline depth (Cisco)

**Webex metrics pipeline: Prometheus → Kafka → Elasticsearch → Grafana** — Call-processing metrics for 1M+ Webex Calling users flowed through that chain. I instrumented custom call-processing metrics in Java and wrote the Prometheus config (global settings, alert rules, scrape jobs) feeding the front of it. Kafka sat in the middle as the durable buffer: it decoupled collection from indexing so a slow Elasticsearch never back-pressured the collectors, replicated across nodes for fault tolerance, and its retention let us replay a stream when a dashboard showed a gap and we needed to know whether the data was lost or just late. Elasticsearch indexed it; Grafana read from there.
Framing (confirmed): the platform team owned brokers and topics; I instrumented the metrics going in and debugged the pipeline end to end when they did not come out. Verb: "instrumented and debugged," not "built."
Interview line for "explain Kafka": "It's the durable, replayable buffer between producers and consumers. Ours took Prometheus metrics in and fed Elasticsearch out, so the two sides scaled independently and we could replay history when troubleshooting."

**Jenkins to Harness migration** — Migrated Webex Calling deployment pipelines from Jenkins to Harness. [Fill in: your slice (N pipelines / shared template / rollout lead) and the outcome (deploy time, maintenance burden, rollout visibility)]

**Helm at Worlds, raw manifests at GMF** — Co-authored chart values and installed/upgraded Helm releases for the Prometheus/Grafana monitoring stack on the Worlds digital-twin platform, then at GMF hand-maintained raw Kubernetes CronJob manifests extending a dap-infra template. The story: "I've used the abstraction and I've written what it abstracts, so I know exactly what Helm buys you (templating, versioned releases, rollback) and what it costs (indirection when debugging a rendered manifest)."

## Range / unusual background

**BA who wrote the code (ZeOmega)** — Could do the BA work because of backend dev + SQL foundation; built a custom CRM for Managed Care Operations folding separate department processes into one flow. The story for "you communicate unusually well with non-engineers."
**Neuroscience to CS** — Why you're interested in why people click what they click.
**Personal projects with READMEs** — XLNT (MCP server for Ableton, 44K-file CLAP library, 170+ tests), NHL prediction model, this job pipeline itself.

## Gaps to prepare honest answers for

- "Why did you leave GMF?" — scope outgrew role + seeking growth; short version only, never the CAP narrative unless directly asked about termination
- [DS&A patterns: track prep progress here]
- [System design: pick 2-3 canonical designs to practice: payment system (you lived it), URL shortener, notification service]
