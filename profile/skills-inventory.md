# Skills Inventory: Danielle

FINAL (all rulings applied 2026-09-24). This is the tailoring engine's honesty boundary:
- **Have:** can be mirrored into a resume when a JD asks. Test: five minutes at a whiteboard, with study time from the interview notes
- **Adjacent:** flagged for a judgment call per JD; each has a talk track, not a claim
- **Do not claim:** never added

Study notes for every Have item are being added to the interview-prep docs in batches (React/Next/TS first, then .NET/SQL/payments, K8s/Azure/observability, testing, AI/agents).

## Have (defendable)

**Frontend**
- React (Angular-to-React migration in 3 months at GMF; micro-frontend module architecture)
- Next.js (frontend monorepo at GMF + personal work)
- Node.js
- TypeScript, JavaScript, HTML, CSS
- Angular (migrated away from it; still know it)

**Backend**
- .NET / C# (Offer API, BFF, Payment Domain Service)
- REST APIs, BFF pattern, domain-centric design
- SQL: schema ownership (customer, offer, offer party, payment, payment arrangement, payment method, party type, quartz jobs, quartz triggers, campaigns; extended for mail-in as a new payment method)
- PostgreSQL, SQL Server
- Java (Cisco: custom call-processing metrics)
- Python (XLNT, NHL model, job pipeline)
- Bash, Linux

**Systems built (not skills, but JD-matchable as domain experience)**
- Offer API, BFF API, Payment Domain Service (PayNow)

**Payments**
- ACH (manual ACH integration), immediate vs scheduled payments
- Stripe with 3DS
- Digital Payment Platform v2.1 integration

**Platform / infra**
- Kubernetes: AKS, CronJobs (Quartz-to-CronJobs refactor; hand-maintained manifests from dap-infra template)
- Docker
- Azure (deep: AKS, APIM security headers, Azure App Configuration feature flags; ARM/Bicep templates at Worlds)
- Azure DevOps pipelines; monorepo CI/CD across dap-ui (frontend), dap-infra (infrastructure), dap-apis (backend)
- Terraform (Cisco, hands-on; plus a GCP provider project)
- Helm (Worlds: co-authored chart values and installed/upgraded releases for the Prometheus/Grafana monitoring stack; GMF: hand-maintained raw CronJob manifests, so both sides of the abstraction)
- Jenkins and Harness (Cisco: migrated pipelines from Jenkins to Harness)
- Ansible (Cisco: automated global deployments)
- Istio, Gateway, Virtual Services, Calico config (centralized in dap-infra)
- Azure Application Gateway (AGW), Akamai integration
- GitHub, Git

**Observability**
- Splunk (+ logger provider that auto-onboards clients)
- OpenTelemetry instrumentation
- Prometheus (wrote the YAML: global settings, alert rules, scrape jobs)
- Kafka (Cisco Webex metrics pipeline: Prometheus → Kafka → Elasticsearch → Grafana; instrumented the metrics feeding it and debugged the pipeline end to end; platform team owned brokers and topics)
- Elasticsearch (same pipeline: indexed metrics and logs feeding Grafana)
- Grafana (1M+ user Webex Calling dashboards)
- Webhook alert routing, incident response
- Application Insights, Kubernetes logs, Serilog (GMF, pre- and alongside OTel)

**Testing**
- Vitest + React Testing Library (component/functional layer at GMF)
- Playwright + SauceLabs E2E (replaced manual regression; TCR/CPR generation)
- Module-boundary mocking (vi.mock), fake timers
- JUnit (Cisco: wrote JUnit tests in Java). At GMF the tests were Vitest/RTL in TypeScript; the PR pipeline published results in JUnit-format XML (Vitest junit reporter into Azure DevOps). Keep the two straight: JUnit tests at Cisco, JUnit report format at GMF
- Test-data infrastructure (reset-account endpoint serving E2E + admin dashboard)
- Postman API testing
- Checkmarx (SAST gate in the PR pipeline: static scan of source for injection, XSS, secrets)
- Unit, component, integration, functional, E2E (the whole pyramid)

**AI / agents**
- MCP servers (XLNT for Ableton Live; several others)
- Agentic workflows: ADO sprint-planning agent, implementation-spec agent, Splunk incident agent
- Claude / LLM tool-use, prompt design
- GitHub Copilot, M365 Copilot

**Healthcare (ZeOmega)**
- Jiva platform (certified), HL7, X12, EDI, ADT compliance

## Adjacent (talk track, not a claim)

- **MSW:** GMF-wanted; discovered after moving to module-level mocks as the next step (one handler set reused across every test, real fetch code still runs). Never implemented before leaving. Line: "I pushed for it; I know why it's better; I didn't get to ship it"
- **MongoDB:** touched, know it well conceptually, never ran it in prod
- **GCP:** Terraform provider side project + course during Cisco; not production. Line: "I've provisioned GCP with Terraform, not operated it in prod"
- **AWS:** real usage at Cisco (legacy-to-AWS migration) and Worlds (EC2/EKS/S3); Azure is the deep cloud. Position as "production experience in both, primary in Azure"
- **ML:** NHL prediction model is real personal work (feature engineering, evaluation, NHL API ingestion); not production ML
- **PowerShell, Power BI/Power Query, C++, Xamarin:** removed from resume; available for specific JDs on request

## Do not claim (JDs will ask; the answer is no)

- Spring Boot, Maven
- SFCC/SCAPI, MuleSoft, SFMC, GA/GTM
- RAG pipelines (agents yes, RAG no; the XLNT search_docs build would flip this)
- [grows as postings surface gaps]

## Synonym map (JD term = your true term)

- "CI/CD" = Azure DevOps pipelines, Jenkins, Harness (incl. the Jenkins-to-Harness migration)
- "IaC" = Terraform (Cisco, GCP project), Azure DevOps pipeline-driven infra
- "observability" = Splunk, OpenTelemetry, Prometheus/Grafana, App Insights
- "event streaming / streaming data" = Kafka (Webex metrics pipeline)
- "microservices" = .NET domain services, BFF, dap-apis monorepo services
- "GenAI / AI-assisted development / agentic AI" = MCP servers; ADO, spec, and Splunk agents; Copilot in the dev workflow
- "payment rails / fintech" = ACH, Stripe 3DS, immediate/scheduled payments, DPP v2.1
- "cloud-native" = AKS, CronJobs, Istio/Gateway, containerized .NET services
- "quality engineering" = Playwright/SauceLabs E2E, Vitest/RTL, JUnit, TCR/CPR automation
- "SAST / secure SDLC" = Checkmarx in the PR pipeline
