import fs from 'node:fs/promises';
import {load} from 'cheerio';
const read=async p=>JSON.parse(await fs.readFile(p,'utf8'));
const save=(p,v)=>fs.writeFile(p,JSON.stringify(v,null,2)+'\n');

async function readHistory(manifest,currentReport){
 const reports=[];
 for(const entry of manifest){
  const html=await fs.readFile(`public/archive/${entry.file}`,'utf8');
  const $=load(html);
  const readLanguage=lang=>{
   const root=$(`section[lang="${lang}"]`);if(root.length!==1)throw Error(`Missing ${lang} history: ${entry.file}`);
   const sections=[];let active;
   root.children().each((_,element)=>{
    if(element.tagName==='h2'){
     active={category:$(element).text().trim(),items:[]};sections.push(active);return;
    }
    if(element.tagName!=='article')return;
    if(!active)throw Error(`Historical item without section: ${entry.file}`);
    const article=$(element),paragraphs=article.children('p').map((_,node)=>$(node).text().trim()).get();
    active.items.push({title:article.children('h3').first().text().trim(),date:paragraphs[0]||'',text:paragraphs[1]||'',opportunity:paragraphs[2]||'',links:article.children('a').map((_,node)=>({label:$(node).text().trim(),url:$(node).attr('href')})).get()});
   });
   return {period:root.children('h1').first().text().trim(),sections};
  };
  const zh=readLanguage('zh'),en=readLanguage('en');
  if(zh.sections.length!==en.sections.length)throw Error(`Historical section mismatch: ${entry.file}`);
  const match=entry.file.match(/^nepal-(\d{4}-\d{2}-\d{2})-(\d{4}-\d{2}-\d{2})\.html$/);
  if(!match)throw Error(`Invalid sealed history filename: ${entry.file}`);
  const sections=zh.sections.map((section,sectionIndex)=>{
   const translated=en.sections[sectionIndex];
   const currentSection=currentReport.countries.np.sections.find(item=>item.category===section.category);
   if(section.items.length!==translated.items.length)throw Error(`Historical item mismatch: ${entry.file}/${section.category}`);
   return {category:section.category,categoryEn:translated.category,displayCategory:currentSection?.displayCategory||section.category,displayCategoryEn:currentSection?.displayCategoryEn||translated.category,
    items:section.items.map((item,itemIndex)=>{const translatedItem=translated.items[itemIndex];return {
     id:`${entry.week.toLowerCase()}-${sectionIndex+1}-${itemIndex+1}`,date:item.date,title:item.title,titleEn:translatedItem.title,
     text:item.text,textEn:translatedItem.text,opportunity:item.opportunity,opportunityEn:translatedItem.opportunity,badge:'',links:item.links
    };})};
  });
  const count=sections.reduce((total,section)=>total+section.items.length,0);
  reports.push({issue:entry.week,generated:entry.archivedAt,windowStart:match[1],windowEnd:match[2],period:zh.period,periodEn:en.period,
   sourceFile:entry.file,current:false,status:`历史期已封存，共 ${count} 条核验事件。`,statusEn:`Sealed historical issue with ${count} reviewed events.`,summary:[],summaryEn:[],
   countries:{np:{name:'尼泊尔',nameEn:'Nepal',flag:'🇳🇵',sections}},stats:{news:count,opportunities:sections.flatMap(section=>section.items).filter(item=>item.opportunity).length,telegram:0,countryCounts:{np:count}}});
 }
 return reports;
}
export async function syncNepal(){
 const market=await read('config/market.json');
 const focus=await read('config/monitoring-focus.json');
 const report=await read('config/nepal-report.json');
 const sources=await read('config/sources.json');
 const people=await read('config/nepal-people.json');
 const compliance=await read('config/compliance-analysis.json');
 const legal=await read('config/nepal-legal-news.json');
 const signals=await read('config/social-signals.json');
 const editorial=await read('config/editorial-status.json');
 const fallback=await read('config/deepseek-fallback-digest.json');
 const signalEn=await read('config/social-signal-translations-en.json');
 const raw=await read('config/telegram-feed.json');
 const zh=await read('config/telegram-translations.json'),en=await read('config/telegram-translations-en.json');
 for(const group of [sources,people,signals,raw.items])for(const item of group)if(item.country!=='尼泊尔')throw Error('Non-Nepal data in active inputs: '+(item.id||item.name));
 const social=signals.map(s=>{const e=signalEn[s.id];if(!e?.title||!e?.summary||!e?.impact)throw Error('Missing English signal: '+s.id);return {...s,titleEn:e.title,summaryEn:e.summary,impactEn:e.impact,accountEn:e.account};});
 const tg=raw.items.filter(i=>zh[i.id]?.title&&zh[i.id]?.summary&&en[i.id]?.title&&en[i.id]?.summary).map(i=>({...i,...zh[i.id],titleEn:en[i.id].title,summaryEn:en[i.id].summary,translationStatus:'双语已完成'}));
 const reviewed=new Set(social.flatMap(i=>i.sourceMessageIds||[]));
 const urls=new Set(social.map(i=>i.url));
 const feed={...raw,items:tg.filter(i=>!reviewed.has(i.id)&&!urls.has(i.url))};feed.messageCount=feed.items.length;
 const sealed=await read('config/archive-manifest.json');
 const history=await readHistory(sealed,report);
 const items=report.countries.np.sections.flatMap(s=>s.items);
 report.stats={news:items.length,opportunities:items.filter(i=>i.opportunity).length,telegram:feed.items.length,countryCounts:{np:items.length}};
 await fs.mkdir('data',{recursive:true});
 const collected=await read('config/nepal-source-candidates.json');
 await save('data/refresh-status.json',{generatedAt:collected.generatedAt,candidateCount:collected.candidates.length,failedSources:sources.filter(s=>s.scanError).length});
 await save('data/report.json',report);await save('data/sources.json',sources);await save('data/people.json',people);
 await save('data/social-signals.json',social);await save('data/telegram-feed.json',feed);await save('data/compliance-analysis.json',compliance);
 await save('data/nepal-legal-news.json',legal);await save('data/history-reports.json',history);
 await save('data/editorial-status.json',editorial);await save('data/deepseek-fallback-digest.json',fallback);
 await save('data/nepal.json',{market,report,issues:[{...report,current:true},...history],sources,people,compliance,legal,signals:social,telegram:feed,editorial,fallback,focus:focus.focusAreas.map(({id,label,labelEn,priority})=>({id,label,labelEn,priority}))});
 console.log(`Nepal: ${sources.length} sources, ${people.length} monitored offices; ${report.stats.news} reviewed news.`);
}
