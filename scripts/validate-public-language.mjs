import fs from "node:fs";

const telegramFeed = JSON.parse(fs.readFileSync("data/telegram-feed.json", "utf8"));
const socialSignals = JSON.parse(fs.readFileSync("data/social-signals.json", "utf8"));
const report = JSON.parse(fs.readFileSync("data/report.json", "utf8"));
const historyReports = JSON.parse(fs.readFileSync("data/history-reports.json", "utf8"));
const arabicPattern = /[\u0600-\u06ff\u0900-\u097f]/;

function validateBilingualItem(item, fields, label) {
  for (const field of fields) {
    if (!item[field] || typeof item[field] !== "string") {
      throw new Error(`${label} is missing ${field}: ${item.id}`);
    }
    if (arabicPattern.test(item[field])) {
      throw new Error(`${label} contains Arabic text in ${field}: ${item.id}`);
    }
  }
}

for (const item of telegramFeed.items) {
  validateBilingualItem(item, ["title", "summary", "titleEn", "summaryEn"], "Public Telegram item");
  if (item.translationStatus !== "双语已完成") {
    throw new Error(`Public Telegram item is not bilingual-gated: ${item.id}`);
  }
}

for (const item of socialSignals) {
  validateBilingualItem(item, ["title", "summary", "impact", "titleEn", "summaryEn", "impactEn"], "Reviewed social signal");
}

if (!report.periodEn || report.summaryEn?.length !== report.summary.length) {
  throw new Error("Briefing overview is not fully bilingual");
}
for (const [countryCode, country] of Object.entries(report.countries)) {
  if (!country.nameEn) throw new Error(`Briefing country name is missing English: ${countryCode}`);
  for (const section of country.sections) {
    if (!section.categoryEn) throw new Error(`Briefing section is missing English: ${countryCode}/${section.category}`);
    for (const item of section.items) {
      validateBilingualItem(item, ["title", "text", "titleEn", "textEn"], "Briefing news item");
      if (item.opportunity) validateBilingualItem(item, ["opportunity", "opportunityEn"], "Briefing opportunity");
    }
  }
}

for (const history of historyReports) {
  if (!history.periodEn || history.current !== false) throw new Error(`Historical issue metadata is invalid: ${history.issue}`);
  for (const section of history.countries.np.sections) {
    if (!section.categoryEn) throw new Error(`Historical section is missing English: ${history.issue}/${section.category}`);
    for (const item of section.items) {
      validateBilingualItem(item, ["title", "text", "titleEn", "textEn"], "Historical briefing item");
      if (item.opportunity) validateBilingualItem(item, ["opportunity", "opportunityEn"], "Historical briefing opportunity");
    }
  }
}

if (telegramFeed.messageCount !== telegramFeed.items.length) {
  throw new Error("Public Telegram message count does not match translated items");
}

const briefingItemCount = Object.values(report.countries).reduce((total, country) => total + country.sections.reduce((sectionTotal, section) => sectionTotal + section.items.length, 0), 0);
const historyItemCount = historyReports.reduce((total,history) => total + history.stats.news, 0);
console.log(`Public language validation passed: ${briefingItemCount} current and ${historyItemCount} historical briefing items plus ${telegramFeed.items.length + socialSignals.length} social signals are bilingual, with no Arabic text.`);
