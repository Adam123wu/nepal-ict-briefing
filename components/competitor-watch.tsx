import monitoring from '@/config/competitor-monitoring.json';
import {ExternalLink} from 'lucide-react';
export function CompetitorWatch({en}:{en:boolean}){
 const t=(zh:string,english:string)=>en?english:zh;
 return <section className="competitor-intro" aria-label={t('竞争对手监控','Competitor watch')}>
  <p className="section-sub">{t(monitoring.note,monitoring.noteEn)} {t('最近核验','Last reviewed')}: {monitoring.reviewedAt}</p>
  <div className="competitor-grid">{monitoring.vendors.map(v=><article className="competitor-card" key={v.id} data-evidence-kind={v.kind}>
   <span className={`badge ${v.kind==='current'?'green':''}`}>{t(v.status,v.statusEn)}</span>
   <h3>{v.name}</h3><p className="feed-meta">{t(v.scope,v.scopeEn)}</p><p>{t(v.summary,v.summaryEn)}</p>
   <p className="watch-action">{t('跟进重点：','Next check: ')}{t(v.action,v.actionEn)}</p>
   <a className="story-source" href={v.evidenceUrl} target="_blank" rel="noreferrer">{t(v.kind==='watch'?'监控入口':'核验来源',v.kind==='watch'?'Monitoring source':'Evidence source')} <ExternalLink size={13}/></a>
  </article>)}</div>
 </section>;
}
