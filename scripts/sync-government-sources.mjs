import fs from 'node:fs';
const directory=JSON.parse(fs.readFileSync('config/government-directory.json','utf8'));
const sources=JSON.parse(fs.readFileSync('config/sources.json','utf8'));
const additions=[...directory.entries.map(e=>({...e,category:'联邦部委',categoryEn:'Federal ministries',tier:'T1'})),
 {id:'np-newbusinessage',name:'New Business Age',nameEn:'New Business Age',url:'https://www.newbusinessage.com/',category:'财经媒体',categoryEn:'Business media',tier:'T2'},
 {id:'np-president',name:'总统办公室',nameEn:'Office of the President',url:'https://www.presidentofnepal.gov.np/',category:'政府决策',categoryEn:'Government decisions',tier:'T1'},
 {id:'np-radio-nepal',name:'尼泊尔公共广播 Radio Nepal',nameEn:'Radio Nepal public broadcaster',url:'https://radionepalonline.com/en/',category:'主流媒体',categoryEn:'National media',tier:'T1'}];
for(const entry of additions){
 const existing=sources.find(s=>s.id===entry.id);
 if(existing)continue;
 sources.push({...entry,country:'尼泊尔',countryCode:'np',platform:'Website',handle:'',owner:entry.nameEn,enabled:true,status:'新增信源·待扫描',statusEn:'New source; scan pending',posts14d:null,verifiedBy:entry.category==='联邦部委'?'官方部委职责名录及机构网站；公告另行核验':'机构或出版方官网；新闻内容另行核验',verifiedByEn:entry.category==='联邦部委'?'Official portfolio roster and institution website; notices require review':'Institution or publisher website; article content requires review',lastCollectedAt:null,scope:'Nepal',verificationUrl:entry.url});
}
fs.writeFileSync('config/sources.json',JSON.stringify(sources,null,2)+'\n');
console.log(`Registered ${directory.entries.length} federal portfolios/offices; ${sources.length} total sources.`);
