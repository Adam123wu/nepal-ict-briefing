#!/usr/bin/env python3
"""Compare tracked Nepal ICT topics with the last daily snapshot and email the result."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ITEM_ID_RE = re.compile(r"^np-[a-z0-9-]{3,120}$")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def report_items(report: dict) -> dict[str, dict]:
    result = {}
    for country in report.get("countries", {}).values():
        for section in country.get("sections", []):
            for item in section.get("items", []):
                if item.get("id"):
                    result[item["id"]] = item
    return result


def requested_item_ids(path: Path | None, items: dict[str, dict]) -> list[str]:
    if not path or not path.exists():
        return []
    ids = []
    for issue in read_json(path):
        match = re.search(r"(?m)^REPORT_ITEM_ID:\s*(\S+)\s*$", issue.get("body") or "")
        item_id = match.group(1) if match else ""
        if ITEM_ID_RE.fullmatch(item_id) and item_id in items and item_id not in ids:
            ids.append(item_id)
    return ids


def candidate_text(candidate: dict) -> str:
    fields = ("titleOriginal", "title", "summary", "description", "url")
    return " ".join(str(candidate.get(field, "")) for field in fields).lower()


def topic_snapshot(topic: dict, item: dict, candidates: list[dict]) -> tuple[str, list[dict]]:
    keywords = [word.lower() for word in topic.get("keywords", []) if word.strip()]
    matches = []
    for candidate in candidates:
        text = candidate_text(candidate)
        if any(keyword in text for keyword in keywords):
            matches.append({
                "title": candidate.get("titleOriginal") or candidate.get("title") or "Untitled",
                "url": candidate.get("url") or candidate.get("evidenceUrl"),
                "publishedAt": candidate.get("publishedAt"),
                "observedAt": candidate.get("observedAt"),
            })
    matches.sort(key=lambda value: (value.get("publishedAt") or "", value.get("url") or ""))
    payload = {
        "report": {
            key: item.get(key)
            for key in ("date", "title", "titleEn", "text", "textEn", "opportunity", "opportunityEn", "links")
        },
        "matches": matches,
    }
    digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return digest, matches


def dynamic_topic(item: dict) -> dict:
    keywords = list(dict.fromkeys(filter(None, [item["id"], item.get("titleEn"), item.get("title")])))
    return {
        "id": f"issue-{item['id']}",
        "reportItemId": item["id"],
        "title": item.get("title", item["id"]),
        "titleEn": item.get("titleEn", item["id"]),
        "enabled": True,
        "keywords": keywords,
    }


def build_email(results: list[dict], checked_at: str) -> tuple[str, str]:
    changed = [result for result in results if result["changed"]]
    subject = f"[尼泊尔 ICT 跟踪] {'发现新变化' if changed else '今日无更新'} · {checked_at[:10]}"
    lines = ["尼泊尔 ICT 专题每日跟踪", f"检查时间：{checked_at}", ""]
    for result in results:
        lines.extend([
            f"{'【发现变化】' if result['changed'] else '【今日无更新】'}{result['title']}",
            f"当前正式简报：{result['reportTitle']}",
            f"相关候选线索：{result['matchCount']} 条（候选线索仍需编辑核验）",
        ])
        for evidence in result["newEvidence"][:5]:
            lines.append(f"- {evidence.get('title')}: {evidence.get('url')}")
        lines.append("")
    lines.append("简报：https://adam123wu.github.io/nepal-ict-briefing/briefings/")
    return subject, "\n".join(lines)


def send_email(subject: str, body: str) -> None:
    username = os.environ.get("SMTP_USERNAME", "").strip()
    password = os.environ.get("SMTP_APP_PASSWORD", "").strip()
    recipient = os.environ.get("TRACKING_EMAIL_TO", "").strip()
    if not username or not password or not recipient:
        raise RuntimeError("SMTP_USERNAME, SMTP_APP_PASSWORD and TRACKING_EMAIL_TO are required")
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ.get("TRACKING_EMAIL_FROM", username)
    message["To"] = recipient
    message.set_content(body)
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context(), timeout=30) as smtp:
        smtp.login(username, password)
        smtp.send_message(message)


def run(config_path: Path, state_path: Path, issues_path: Path | None, now: datetime) -> tuple[list[dict], dict]:
    config = read_json(config_path)
    report = read_json(ROOT / "config/nepal-report.json")
    candidates_doc = read_json(ROOT / "config/nepal-source-candidates.json")
    items = report_items(report)
    topics = [topic for topic in config.get("topics", []) if topic.get("enabled")]
    configured_ids = {topic.get("reportItemId") for topic in topics}
    for item_id in requested_item_ids(issues_path, items):
        if item_id not in configured_ids:
            topics.append(dynamic_topic(items[item_id]))
    old_state = read_json(state_path) if state_path.exists() else {"version": 1, "topics": {}}
    new_state = {"version": 1, "lastCheckedAt": now.isoformat(), "topics": {}}
    results = []
    for topic in topics:
        item_id = topic["reportItemId"]
        if item_id not in items:
            raise ValueError(f"Tracked report item does not exist: {item_id}")
        item = items[item_id]
        digest, evidence = topic_snapshot(topic, item, candidates_doc.get("candidates", []))
        previous = old_state.get("topics", {}).get(topic["id"], {})
        changed = bool(previous.get("fingerprint") and previous["fingerprint"] != digest)
        old_urls = set(previous.get("evidenceUrls", []))
        new_evidence = [entry for entry in evidence if entry.get("url") and entry["url"] not in old_urls]
        new_state["topics"][topic["id"]] = {
            "reportItemId": item_id,
            "fingerprint": digest,
            "lastCheckedAt": now.isoformat(),
            "lastChangeAt": now.isoformat() if changed else previous.get("lastChangeAt"),
            "evidenceUrls": [entry["url"] for entry in evidence if entry.get("url")],
        }
        results.append({
            "id": topic["id"], "title": topic.get("title", item["title"]),
            "reportTitle": item["title"], "changed": changed,
            "matchCount": len(evidence), "newEvidence": new_evidence,
        })
    return results, new_state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/tracked-topics.json")
    parser.add_argument("--state", type=Path, default=ROOT / "config/tracking-state.json")
    parser.add_argument("--issues-json", type=Path)
    parser.add_argument("--send-email", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    now = datetime.now(ZoneInfo("Asia/Kathmandu")).replace(microsecond=0)
    results, state = run(args.config, args.state, args.issues_json, now)
    subject, body = build_email(results, now.isoformat())
    print(subject)
    print(body)
    if not args.dry_run:
        args.state.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.send_email:
        send_email(subject, body)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write(f"## {subject}\n\n````text\n{body}\n````\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
