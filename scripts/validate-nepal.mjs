import fs from 'node:fs';
import assert from 'node:assert/strict';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const d=read('data/nepal.json');
assert.deepEqual(Object.keys(d.report.countries),['np']);
assert.equal(d.report.countries.np.sections.length,11);
for(const group of [d.sources,d.people,d.signals,d.telegram.items,d.legal.sources])for(const item of group)assert.equal(item.country,'尼泊尔');
const ids=new Set();
for(const s of d.sources){assert(!ids.has(s.id));ids.add(s.id);assert(s.id.startsWith('np-'));assert.equal(new URL(s.url).protocol,'https:');if(s.platform==='Telegram')assert(s.identityVerified&&s.verificationUrl);}
const imported=read('skills/nepal-ict-briefing/references/source-import.json').sources;
assert.equal(imported.length,17);
for(const s of imported)assert(ids.has(s.sourceId),'Imported source mapping missing: '+s.sourceId);
const focus=read('config/monitoring-focus.json').focusAreas;
assert.equal(focus.length,12);assert.equal(new Set(focus.map(f=>f.id)).size,12);
for(const f of focus)assert(f.label&&f.labelEn&&Array.isArray(f.keywords));
assert.equal(focus.find(f=>f.id==='hot-topics').keywords.length,0);
assert(!JSON.stringify(d.focus).match(/[\u0900-\u097f]/),'Raw research keywords must not leak into public focus labels');
for(const t of read('config/topic-source-routing.json').topics)assert.deepEqual(t.countries,['尼泊尔']);
const hosts=new Set(d.legal.sources.map(s=>new URL(s.url).hostname));
for(const s of d.legal.sources)assert(new URL(s.url).hostname.endsWith('.gov.np')||new URL(s.url).hostname.endsWith('.org.np'));
for(const i of d.legal.items){assert(hosts.has(new URL(i.url).hostname));assert(i.title&&i.titleEn&&i.summary&&i.summaryEn&&i.status&&i.statusEn&&i.businessImpact&&i.businessImpactEn&&i.actions.length>=2&&i.actionsEn.length===i.actions.length);}
for(const c of d.compliance.countries){assert.equal(c.code,'np');const score=c.dimensions.reduce((n,x)=>n+x.score*d.compliance.method.find(m=>m.id===x.id).weight/100,0);assert(Math.abs(c.score-Math.round(score*10)/10)<0.001);}
const count=d.report.countries.np.sections.reduce((n,s)=>n+s.items.length,0);assert.equal(d.report.stats.news,count);
assert(count>0,'Do not publish an empty migration edition');
const events=new Set();
for(const s of d.report.countries.np.sections)for(const i of s.items){assert(!events.has(i.id));events.add(i.id);assert(i.date>=d.report.windowStart&&i.date<=d.report.windowEnd);assert(i.links.length>=1);assert(i.titleEn&&i.textEn);}
const competition=read('config/competitor-monitoring.json');
const government=read('config/government-directory.json');
assert.equal(new Set(government.entries.map(e=>e.id)).size,government.entries.length);
for(const office of government.entries){assert(ids.has(office.id),'Missing federal ministry source '+office.id);assert(office.name&&office.nameEn);assert(new URL(office.url).hostname.endsWith('.gov.np'));}
assert(ids.has('np-newbusinessage'));assert(ids.has('np-president'));
assert.equal(competition.country,'尼泊尔');
assert.equal(new Set(competition.vendors.map(v=>v.id)).size,competition.vendors.length);
for(const v of competition.vendors){
 assert(['current','baseline','watch'].includes(v.kind));
 for(const id of v.sourceIds)assert(ids.has(id),'Missing competitor source '+id);
 for(const id of v.relatedEventIds)assert(events.has(id),'Missing related news '+id);
 if(v.kind==='current')assert(v.relatedEventIds.length>0);
 for(const field of ['status','statusEn','scope','scopeEn','summary','summaryEn','action','actionEn'])assert(v[field]&&!/[\u0900-\u097f\u0600-\u06ff]/.test(v[field]));
 assert.equal(new URL(v.evidenceUrl).protocol,'https:');
}
assert(d.archive.every(i=>/^nepal-/.test(i.file)),'Foreign archive blocked');
for(const file of fs.readdirSync('public/archive'))assert(/^nepal-/.test(file),'Foreign archive asset blocked: '+file);
assert.equal(d.telegram.messageCount,d.telegram.items.length);
console.log('Nepal country, source, legal-domain, routing, score and news-count checks passed.');
