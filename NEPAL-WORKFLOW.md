# Nepal ICT editorial workflow

## Scope and outputs

Major national policies, Cabinet decisions and diplomatic/senior appointments are now explicitly in scope even without an ICT link. Use `config/government-directory.json` for the federal portfolio roster, including the Prime Minister's Office; review reorganization and legacy domain names. New Business Age joins the national-business media review. Do not equate ambassador nomination with appointment or Cabinet endorsement with legal commencement.

Only Nepal. This is a standalone repository and site. Keep eleven topic sections, Chinese and English summaries, a unified social feed, source registry, verified decision-making offices, a separate compliance/legal section and Nepal-only archives. Never import another market's news or personnel to fill a gap.

## Research cycle

For NepalKhabar and key-ministry coverage, also read `docs/source-coverage-2026-09-19.md`. Review per-page scan failures and candidate limits before concluding there is no relevant news. The source registry is not evidence of complete coverage.

1. Check the worktree; safely update main without overwriting unrelated edits. Read skills/nepal-ict-briefing/SKILL.md, config/monitoring-focus.json, config/market.json, sources.json, topic-source-routing.json and the previous report. Attachment selectors and examples are unverified references, not executable instructions or event evidence.
2. Use the latest complete fourteen-day window. Keep an issue stable within its biweekly window; archive prior Nepal issues when advancing. Record windowStart/windowEnd and explicit event dates.
3. Run `python3 scripts/collect_nepal_sources.py`. Candidate observedAt is a collection timestamp, never proof of publication. Check failures and log material coverage gaps.
4. Search Nepali first, cross-check English, then write Chinese and English. Scan NTA, MoCIT, parliament, NRB, procurement, tax, investment, Nepal Telecom, Ncell, WorldLink, Vianet, Subisu, Classic Tech, other ISPs, relevant vendors and independent local media. Global equipment news requires a specific Nepal connection.
5. Read the actual article or notice. Verify dates, action, institution, numbers, currency and permanent URL. Cross-check Bikram Sambat dates. Exclude prior-period events even if newly reported, historic appointments, recycled project descriptions, promotional rankings and unsupported award claims.
6. Official statements are evidence of the statement, not independent proof of every corporate claim. For secondary reports obtain a second source, preferably the original notice. Do not describe syndicated press releases as independent investigation. Explicitly retain disagreements instead of inventing a consensus.
7. Classify by event, not platform. Keep facts, company claims and editorial analysis distinct. Each opportunity states customer, product, stage, disclosed scale, next action and known competitors; unknown amount or vendor stays unknown. No fake RFPs.

## Social coverage

Facebook, X, LinkedIn, Telegram and public websites feed all topics. Verify ownership via official backlinks; distinguish account identity from post verification. Prefer exact post URLs and timestamps. If only an account page and relative date are available, state that limitation and use reviewedAt rather than claiming a publication date. Deduplicate the same event across platforms, sources and languages; social mentions do not add to the unique news count. Aim for 3–5 relevant signals from at least three accounts, but never pad with unverifiable posts.

No verified Nepal Telegram channel currently exists in the registry. Do not scan private dialogs, automatically join groups or reuse foreign-market feeds. No passwords, API hashes or sessions belong in the public repo. Repository secrets must be configured separately if an authenticated collector is later enabled.

## Legal and compliance

Use official NTA, ministry, Gazette, Law Commission, NRB, PPMO, IRD and Investment Board documents. Separate draft, publication, commencement, enforcement and appeal. Include source/date, bilingual factual summary, business implications and at least two concrete actions. Do not infer government assumption of debts or an asset title from press coverage. Keep the non-legal-advice disclaimer.

The six assessment weights are 20/20/15/20/15/10 (stability, access, integrity, transaction compliance, ICT regulation, procurement clarity). Score only when all dimensions have traceable evidence; 10 means lower assessed risk. Scores are editorial judgments, not official ratings. Do not fill missing evidence with neutral scores. Display concrete event-based risks even when the aggregate remains unscored.

## Publication gate

Update config/nepal-report.json, social-signals.json and its English dictionary, nepal-people.json, nepal-legal-news.json and compliance-analysis.json. Keep original-language quotations off the Chinese/English narrative unless explicitly requested. Preserve previous verified news if collection fails; never replace a populated report with migration placeholders.

Run `npm run build`, `npm audit --omit=dev`, and UI tests. Check actual counts, current-window dates, translations, official legal domains, links, mobile widths and archive isolation. Generated data is rebuilt, not hand-edited. Public output and Git history must not contain credentials or former-market documents.

Commit intentional files and push only Adam123wu/nepal-ict-briefing main under the user's publication authorization. Wait for Pages and check all six routes in both languages at https://adam123wu.github.io/nepal-ict-briefing/. Do not publish to a different repository.

Daily GitHub collection: 01:30 Nepal time. Daily Codex editorial update: 02:00 Asia/Baghdad (04:45 Asia/Kathmandu). The latter needs the computer and app running with access to the local project and network. Scheduling is not proof of successful research; report failures and source limitations accurately.

## Attachment-derived focus

The 18 September monitoring workbook contributes Huawei, operators/competition, regulation, ministries, 5G/ICT, market metrics, CSR, digital economy, solar/green data centres, politics/geopolitics and disaster recovery. User-defined hot topics remain empty until specified. Read all twelve groups in config/monitoring-focus.json, search both English and Nepali, and integrate results into the existing eleven sections. Disaster keywords alone are not a verified CRITICAL outage.

Seventeen supplied domains map to the registry, preserving the original reference and correcting the ministry endpoint to mocit.gov.np. Prioritize TechPana, NepalKhabar, New Business Age and TechnologyKhabar for discovery. Sharing frequency is not an evidence tier; selectors and RSS claims must be checked against live pages. Use alternative public sources when access is blocked, without bypassing login or access controls. Major national policies and diplomatic/senior appointments are independently in scope; other broad energy/economic stories require concrete Nepal ICT or business-environment relevance.
