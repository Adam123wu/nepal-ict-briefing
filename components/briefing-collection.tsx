import data from "@/data/nepal.json";
import {BriefingView} from "./briefing-view";
import {IssueDigest} from "./issue-digest";
import {SocialUpdates} from "./social-updates";
import {Badge, Card} from "./ui";

type Signal={id:string;title:string;titleEn:string;summary:string;summaryEn:string;url:string;date?:string;platform?:string;account?:string;impact?:string;impactEn?:string};

export function BriefingCollection({language}:{language:"zh"|"en"}){
 const en=language==="en",t=(zh:string,english:string)=>en?english:zh;
 const signals=[...data.signals,...data.telegram.items] as Signal[];
 return <>
  <Card className="card-pad issue-picker">
   <div className="issue-picker-head">
    <div><h2>{t('全部双周简报项目','All biweekly briefing items')}</h2><p className="section-sub">{t('当前期与全部历史期按时间连续展开，不再把历史项目放入独立归档。','The current issue and every historical issue are expanded chronologically, with no separate archive.')}</p></div>
    <Badge>{data.issues.reduce((total,item)=>total+item.stats.news,0)} {t('条全部项目','items in total')}</Badge>
   </div>
   <nav className="issue-index" aria-label={t('简报期数目录','Briefing issue index')}>
    {data.issues.map(item=><a href={`#issue-${item.issue.toLowerCase()}`} className={item.current?'current':''} key={item.issue}>
     <strong>{item.issue}</strong><span>{item.stats.news} {t('条','items')}</span><small>{item.current?t('当前期','Current'):t('历史期','Historical')}</small>
    </a>)}
   </nav>
  </Card>
  <div className="all-issues">
   {data.issues.map(issue=><section className="briefing-issue" data-issue={issue.issue} id={`issue-${issue.issue.toLowerCase()}`} key={issue.issue}>
    <div data-history-summary={issue.current?undefined:"true"}><Card className={`card-pad issue-heading ${issue.current?'current':'historical'}`}>
     <div>
      <Badge tone={issue.current?'amber':'green'}>{issue.current?t('当前更新期','Current issue'):t('历史期','Historical issue')}</Badge>
      <h2>{issue.issue} · {t(issue.period,issue.periodEn)}</h2>
     </div>
     <strong>{issue.stats.news} {t('条核验项目','reviewed items')}</strong>
     {!issue.current&&<p className="section-sub">{t('以下为本期全部已核验项目，事实、来源与商机研判均完整保留。','Every reviewed item from this issue is shown below with its facts, sources and opportunity analysis intact.')}</p>}
    </Card></div>
    {issue.current&&<IssueDigest en={en}/>}
    <div id={`issue-news-${issue.issue.toLowerCase()}`}><BriefingView countries={issue.countries} language={language} showCompetitorWatch={issue.current} idPrefix={issue.issue.toLowerCase()}/></div>
    {issue.current&&<div id="issue-social"><SocialUpdates signals={signals} en={en}/></div>}
   </section>)}
  </div>
 </>;
}
