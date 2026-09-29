# Automatic public-article updates

Implemented 29 September 2026 following the user's request to use the existing backend DeepSeek binding for automatic updates.

Successful daily collection now triggers the editorial watchdog. Its scheduled run remains a backup. A same-day marker prevents duplicate successful API calls; jobs are serialized. No new service credential is required. One bounded model call handles up to five readable articles selected from twelve priority candidates. Fetches are restricted to configured public HTTPS source hosts, reject redirects/private addresses, and impose time/body limits. Only public extracted text is sent to DeepSeek; raw pages and API secrets are not published.

The UI displays Chinese/English summaries and conditional analysis under **Daily AI news update (pending review)**. This is a separate machine-generated feed, not independently verified news. URL-derived dates remain unverified. Formal report counts, immutable history, and the Codex completion date are unchanged. Failed fetching or malformed included output preserves the previous digest and fails the workflow. Rejected items need no translation; included items retain strict bilingual and verbatim-evidence validation. An exact quote check establishes text provenance, not truth or full entailment.

The former title-only flow failed when model output contained invalid translated titles. Supporting minimal excluded records and explicitly specifying limits removes one avoidable failure mode without weakening included-item checks. The removed public/archive staging path was fixed separately in 10ce400.

Limitations: public website access and extraction are incomplete; Facebook/Telegram are not newly enabled. Machine analysis can still be wrong and must not be treated as an award, verified supplier, legal advice or Codex-approved briefing. The user-authorized Codex review still promotes qualified items into the formal bilingual issue. Completed formal issues remain on their existing fourteen-day preservation cycle.
