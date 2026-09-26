import { ExternalLink, Scale, Zap } from "lucide-react";
import { Badge, Card } from "./ui";

type PolicyItem = {
  id: string;
  category: string;
  categoryEn: string;
  status: string;
  statusEn: string;
  statusTone: string;
  facts: string[];
  factsEn: string[];
  nextChecks: string;
  nextChecksEn: string;
  sources: {label: string; labelEn: string; url: string}[];
};

export function IndustrialPolicyTracker({tracker, en}:{tracker:{title:string;titleEn:string;note:string;noteEn:string;updatedAt:string;items:PolicyItem[]};en:boolean}) {
  const t=(zh:string,english:string)=>en?english:zh;
  return <Card className="card-pad policy-tracker">
    <div className="policy-tracker-head">
      <div><div className="eyebrow">POLICY TRACKER · {tracker.updatedAt}</div><h2>{t(tracker.title,tracker.titleEn)}</h2><p className="section-sub">{t(tracker.note,tracker.noteEn)}</p></div>
      <Badge tone="amber">{tracker.items.length} {t("项持续追踪","live tracks")}</Badge>
    </div>
    <div className="policy-tracker-grid">
      {tracker.items.map((item,index)=><article className="policy-track-card" key={item.id}>
        <div className="policy-track-title">{index===0?<Scale size={18}/>:<Zap size={18}/>}<h3>{t(item.category,item.categoryEn)}</h3></div>
        <Badge tone={item.statusTone==="green"?"green":"amber"}>{t(item.status,item.statusEn)}</Badge>
        <ul>{(en?item.factsEn:item.facts).map(fact=><li key={fact}>{fact}</li>)}</ul>
        <div className="policy-next"><strong>{t("下一步监控：","Next checks: ")}</strong>{t(item.nextChecks,item.nextChecksEn)}</div>
        <div className="policy-sources">{item.sources.map(source=><a href={source.url} target="_blank" rel="noreferrer" key={source.url}>{t(source.label,source.labelEn)} <ExternalLink size={11}/></a>)}</div>
      </article>)}
    </div>
  </Card>;
}
