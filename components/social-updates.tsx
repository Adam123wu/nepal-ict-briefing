import {ExternalLink} from 'lucide-react';
import {Card} from './ui';

type Signal={id:string;title:string;titleEn:string;summary:string;summaryEn:string;url:string;date?:string;platform?:string;account?:string;impact?:string;impactEn?:string};
export function SocialUpdates({signals,en}:{signals:Signal[];en:boolean}){
 const t=(zh:string,english:string)=>en?english:zh;
 return <section className="social-desk" aria-labelledby="social-heading">
  <header className="editorial-section-head"><div><h2 id="social-heading">{t('重要社媒快讯','Social media highlights')}</h2><p>{t('企业与机构公开动态 · 与专题新闻按事件去重','Public updates from companies and institutions · deduplicated against topic coverage')}</p></div><span className="badge">{signals.length} {t('条线索','signals')}</span></header>
  <div className="social-list">{signals.length?signals.map(s=><Card className="social-story" key={s.id}>
   <div className="feed-meta"><span className="platform-label">{s.platform}</span><span>{s.account}</span><span>{t('核验于','Reviewed')} <time>{s.date}</time></span></div>
   <h3>{t(s.title,s.titleEn)}</h3><p className="story-summary">{t(s.summary,s.summaryEn)}</p>
   {s.impact&&<div className="story-analysis"><span>{t('业务观察','Business context')}</span><p>{t(s.impact,s.impactEn||s.impact).replace(/^(研判：|Analysis:\s*)/,'')}</p></div>}
   <a className="story-source" href={s.url} target="_blank" rel="noreferrer">{t('查看帖文／账号','View post / account')}<ExternalLink size={13}/></a>
  </Card>):<Card className="card-pad"><p>{t('本期暂无完成核验的社媒快讯。','No verified social updates for this issue.')}</p></Card>}</div>
 </section>;
}
