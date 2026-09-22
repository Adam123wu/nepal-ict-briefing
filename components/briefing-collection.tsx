"use client";

import {useState} from "react";
import data from "@/data/nepal.json";
import {BriefingView} from "./briefing-view";
import {IssueDigest} from "./issue-digest";
import {SocialUpdates} from "./social-updates";
import {Badge, Card} from "./ui";

type Signal={id:string;title:string;titleEn:string;summary:string;summaryEn:string;url:string;date?:string;platform?:string;account?:string;impact?:string;impactEn?:string};

export function BriefingCollection({language}:{language:"zh"|"en"}){
 const en=language==="en",t=(zh:string,english:string)=>en?english:zh;
 const [issueId,setIssueId]=useState(data.issues[0].issue);
 const issue=data.issues.find(item=>item.issue===issueId)??data.issues[0];
 const signals=[...data.signals,...data.telegram.items] as Signal[];
 return <>
  <Card className="card-pad issue-picker">
   <div className="issue-picker-head">
    <div><h2>{t('全部双周简报','All biweekly issues')}</h2><p className="section-sub">{t('当前期与历史期统一展示；切换期数即可查看该期全部核验项目。','Current and historical issues are shown together. Select an issue to view every reviewed item from that period.')}</p></div>
    <Badge>{data.issues.reduce((total,item)=>total+item.stats.news,0)} {t('条历史项目','items across all issues')}</Badge>
   </div>
   <div className="tabs issue-tabs" aria-label={t('选择简报期数','Select briefing issue')}>
    {data.issues.map(item=><button type="button" data-issue={item.issue} aria-pressed={item.issue===issue.issue} className={`tab ${item.issue===issue.issue?'active':''}`} key={item.issue} onClick={()=>setIssueId(item.issue)}>
     <strong>{item.issue}</strong><span>{t(item.period,item.periodEn)}</span><small>{item.stats.news} {t('条','items')} · {item.current?t('当前期','Current'):t('历史完整期','Completed')}</small>
    </button>)}
   </div>
  </Card>
  {issue.current?<IssueDigest en={en}/>:<div data-history-summary><Card className="card-pad historical-issue-note">
   <div><Badge tone="green">{t('历史完整期','Completed issue')}</Badge><h2>{t(issue.period,issue.periodEn)}</h2></div>
   <p>{t(issue.status,issue.statusEn)}</p>
   <p className="section-sub">{t('下列内容为封存时已经核验的完整项目，保留当期事实、来源和商机研判，不会被后续更新覆盖。','The complete set below was verified when the issue was sealed. Its facts, sources and opportunity analysis are preserved and are not overwritten by later updates.')}</p>
  </Card></div>}
  <div id="issue-news"><BriefingView countries={issue.countries} language={language} showCompetitorWatch={issue.current}/></div>
  {issue.current&&<div id="issue-social"><SocialUpdates signals={signals} en={en}/></div>}
 </>;
}
