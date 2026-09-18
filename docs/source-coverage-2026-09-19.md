# Source coverage correction — 19 September 2026

NepalKhabar was registered as `np-nepalkhabar`, but the previous 18 September run retained only 14 homepage candidates. These were not verified articles. Homepage-only scanning and strict headline keyword filtering caused a coverage gap.

The collector now scans the homepage plus verified economy, politics and science/technology category URLs. Numeric article URLs are retained even without a keyword match. Cross-page duplicates are merged, per-page successes/failures and candidate limits are recorded, and dates remain unverified until the original article is read. This is bounded discovery, not a complete site/archive crawl or automatic news publication.

Added official ministry sources:

- Finance: budgets, public spending and external finance — https://www.mof.gov.np/
- Energy, Water Resources and Irrigation: power continuity and energy infrastructure — https://www.moewri.gov.np/
- Industry, Commerce and Supplies: investment, industrial and technology-transfer policy — https://www.moics.gov.np/
- Home Affairs: disaster coordination and public-service continuity — https://www.moha.gov.np/
- Foreign Affairs: bilateral agreements and economic cooperation — https://www.mofa.gov.np/

Existing MoCIT, Prime Minister's Office, NTA, PPMO, Investment Board and tax/legal sources remain. Registration, page access, candidate extraction and verified publication are separate states. Review `scanPages` and `candidateCount`, not just source totals. Ministry identity does not establish the truth, effective date or business relevance of an individual announcement. Broad political and energy coverage requires a concrete Nepal ICT or business-environment implication before publication.

## Verification run

Scope update: the user's subsequent request explicitly adds major national policies and ambassador/senior appointments even without an ICT implication. Use `config/government-directory.json` for the current federal coverage; it supersedes the earlier five-ministry expansion described above. Old media/department English labels may lag portfolio changes. Read official pages and date changes before relabeling an office. Do not treat nominee names as incumbent ambassadors.

The revised run found 134 unique NepalKhabar candidates across the homepage, politics and science/technology pages; the economy category returned HTTP 403. This is not 134 new or current-period verified news items. Finance, Energy and MoCIT timed out in a subsequent direct check. Industry, Home Affairs, Foreign Affairs and the Prime Minister's Office returned candidates. Industry and Foreign Affairs reached the 60-candidate per-page limit; coverage is explicitly incomplete and requires targeted editorial follow-up. Public search may supplement inaccessible official pages, but snippets alone do not verify an announcement.
