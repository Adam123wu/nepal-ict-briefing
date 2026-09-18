import monitoring from '@/config/competitor-monitoring.json';
import {ExternalLink} from 'lucide-react';
export function CompetitorWatch({en}:{en:boolean}){
 const t=(zh:string,english:string)=>en?english:zh;
 const priority=['zte','cisco','whale-cloud','asiainfo','h3c','fiberhome'];
 const card=(v:typeof monitoring.vendors[number])=><article className="competitor-card" key={v.id} data-evidence-kind={v.kind}>
   <span className={`badge ${v.kind==='current'?'green':''}`}>{t(v.status,v.statusEn)}</span>
   <h3>{'nameEn' in v ? t(v.name,v.nameEn as string):v.name}</h3><p className="feed-meta">{t(v.scope,v.scopeEn)}</p><p>{t(v.summary,v.summaryEn)}</p>
   <p className="watch-action">{t('跟进重点：','Next check: ')}{t(v.action,v.actionEn)}</p>
   <a className="story-source" href={v.evidenceUrl} target="_blank" rel="noreferrer">{t(v.kind==='watch'?'监控入口':'核验来源',v.kind==='watch'?'Monitoring source':'Evidence source')} <ExternalLink size={13}/></a>
  </article>;
 return <section className="competitor-intro" aria-label={t('竞争对手监控','Competitor watch')}>
  <p className="section-sub">{t(monitoring.note,monitoring.noteEn)} {t('最近核验','Last reviewed')}: {monitoring.reviewedAt}</p>
  <h3>{t('重点竞争厂家','Priority competitors')}</h3>
  <p className="section-sub">{t('跟踪尼泊尔客户、招标与中标、合作伙伴及产品替换；覆盖网络设备、BSS/OSS、云与数字化平台。','Track Nepal customers, tenders, awards, partners and replacements across networking, BSS/OSS, cloud and digital platforms.')}</p>
  <div className="competitor-grid" data-primary-competitors>{priority.map(id=>monitoring.vendors.find(v=>v.id===id)).filter(v=>v!==undefined).map(card)}</div>
  <details><summary>{t('其他设备商与替代技术跟踪','Other vendors and alternative technologies')}</summary><div className="competitor-grid">{monitoring.vendors.filter(v=>!priority.includes(v.id)).map(card)}</div></details>
 </section>;
}
