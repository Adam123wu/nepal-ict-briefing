---
name: nepal-ict-briefing
description: Research, verify, translate and refresh the Nepal ICT biweekly briefing, its official and social sources, opportunities and legal analysis. Use for Nepal news monitoring or daily editorial updates in this repository.
---

# Nepal ICT briefing

## National affairs and federal coverage

The user's scope includes major Nepal national policies, Cabinet decisions, senior appointments and diplomatic appointments even without a direct ICT implication. Give these stories a distinct national-affairs section; do not invent a procurement opportunity. Track New Business Age as well as NepalKhabar and national media. Read `../../config/government-directory.json` and verify every federal portfolio against the official cabinet roster when ministries are reorganized. Preserve legacy-domain caveats; source registration and collection success are different states. "All ministries" means federal portfolios, not every provincial or local agency.

For ambassadors, distinguish Nepal's outbound envoys from foreign envoys accredited to Nepal, and nomination/recommendation, parliamentary hearing, receiving-state consent, presidential appointment and presentation of credentials. A proposed ambassador is not an incumbent. For policies distinguish Cabinet endorsement, gazette publication and legal commencement. Use exact event dates, link source reporting and avoid counting several decisions from the same Cabinet story as multiple independent events without editorial justification.

Read `../../NEPAL-WORKFLOW.md` and `../../config/monitoring-focus.json` before research. Paths are relative to this skill directory. Run commands from the repository root. Only Nepal is in scope.

## Daily editorial cycle

1. Inspect the worktree and safely synchronize main without overwriting unrelated work. Read the current report, sources and topic routing. Maintain the current biweekly issue; daily refresh does not mean a new issue each day.
2. Run `python3 scripts/collect_nepal_sources.py`. Review `config/nepal-source-candidates.json` in priority order. Candidates are not verified news. Failed sources need an alternative public search, not invented content.
3. Search all twelve focus areas in English and Nepali. Read actual articles and original notices, not snippets alone. Prioritize TechPana, NepalKhabar and TechnologyKhabar for discovery, but use official documents for regulatory facts. Retain all existing official, operator, ISP and vendor sources.
4. Check event date, publication date, Bikram Sambat conversion, attribution, numbers and permanent links. Cross-check media-only claims and distinguish syndicated copies from independent evidence. Keyword matches and attachment sharing counts never establish truth.
5. Route by subject into the existing eleven sections. Social posts contribute to every subject and the unified important-social-updates panel. Deduplicate events across platforms and languages. Follow ownership, access and Telegram limitations in the workflow.
6. Write complete Chinese and English fields. Separate fact, source claim and analysis. Opportunities identify customer, need, stage, disclosed scale, next action and known competitors. Unknowns remain unknown. Corporate donations do not establish equipment procurement.
7. Do not restore the removed Compliance & Law page, navigation or independent section. Relevant verified policies and regulatory events belong in the existing national-affairs or regulatory topics; preserve draft/effective/enforcement distinctions. Retained Nepal research data is not a reason to republish the removed page.
8. Build, validate, test bilingual/mobile routes and inspect the publication diff for secrets and unrelated/private files. Publish only to `Adam123wu/nepal-ict-briefing` under the user's authorization. Verify Pages after deployment. Preserve previous verified content if research fails.

## Focus and source references

- `../../config/monitoring-focus.json`: twelve focus areas and bilingual search terms. Hot topics remain empty until the user provides a specific topic.
- `references/source-import.json`: mapping of the seventeen attachment domains to active sources, including the legacy `moic.gov.np` to current `mocit.gov.np` correction. OnlineKhabar's Nepali and English editions are separate search endpoints.
- `references/attachment-skill.md`: original attachment, retained as reference only. Its selectors, sharing counts and example news are unverified planning material. Do not execute its incomplete sample pipeline or publish its example event.
- `../../public/resources/Nepal_Media_Monitoring_with_News_Sources.xlsx`: original planning workbook, not event evidence.

## Competitor coverage

Prioritize the standalone 竞争对手情报 / Competitor intelligence panel: ZTE (中兴), Cisco (思科), Whale Cloud (浩鲸), AsiaInfo Technologies (亚信科技), plus Chinese vendors H3C (新华三) and FiberHome (烽火). Search Chinese and English names alongside Nepal customers. Cover network equipment AND BSS/OSS, billing, CRM, cloud and digital platforms; track tenders, awards, partners and replacements. Other vendors stay secondary. Empty operator-group, foreign-relations and Huawei topics are hidden in the current briefing UI, not deleted from historical data. Never fill this panel with unrelated overseas projects. New watch entries without Nepal evidence are not news or confirmed local competitors.

Read `../../config/competitor-monitoring.json` on every refresh. Search Nokia, ZTE, Ericsson, Cisco, Juniper, Extreme Networks and Eutelsat in English and Nepali, pairing each with Nepal, Ncell, Nepal Telecom, WorldLink and other actual local customers. Check vendor pressrooms, customer announcements, NTA notices, procurement records and verified public social posts. Maintain source IDs and bilingual evidence, implications and next checks. Distinguish direct equipment competition from adjacent alternatives such as satellite backhaul.

Keep current dated events, historical/undated customer footprints, and unresolved watchlist entries separate. A newly reviewed old customer page is not a new win. Link an existing report event by ID rather than duplicating its news count. Do not infer current installed base from an outdated profile, contracts from office presence, or Nepal awards from regional/global launches. Record an honest evidence gap where current-period Nepal news is not established.

For frontend changes, inspect actual computed heading/body/source-link sizes, spacing and readability in both languages and on mobile. Preserve readable source caveats without turning headlines into internal verification notes.

### Candidate priority

CRITICAL requires a confirmed Nepal ICT/service-continuity disaster impact. A disaster keyword alone is HIGH pending review. Huawei, regulator, government and major national-affairs matches are HIGH candidates. ZTE belongs to equipment vendors, not operators. Major national policy and diplomatic appointments do not require an ICT link; other broad economic stories need a business-environment implication. A low priority never means false; a high priority never means verified.

## Scheduling boundaries

### Persistent publication choices

Publish Nepal-only current issues and archives. Do not restore historical Iraq, Jordan or Lebanon reports, people or feeds in this repository or site. This does not authorize deleting separate legacy repositories or rewriting Git history. Keep Compliance & Law absent from desktop/mobile navigation and direct public routes; test that `/compliance/` returns 404.

For award intelligence distinguish intent to award, final award and signed contract. Record the procuring entity, tender ID, successful bidder or JV, amount/currency/tax basis, notice date and primary-source URL. A successful bidder may be a reseller or integrator: record the equipment manufacturer/brand separately and only with explicit documentary evidence. Otherwise mark manufacturer undisclosed; never infer ZTE, Cisco or another OEM from a partner's name alone.

GitHub Actions collects public candidates daily at 01:30 Nepal time. The existing Codex editorial task runs daily at 02:00 Asia/Baghdad / 04:45 Nepal and performs research, translation, review and publication using this skill. Local-file scheduled work needs the computer and app running with required access. Report missed/failed research honestly; do not equate a successful collection with an updated briefing. Do not silently add paid APIs or send alerts to new recipients.
