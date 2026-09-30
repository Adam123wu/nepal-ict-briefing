import context from "@/config/operator-context.json";
import {Badge, Card} from "./ui";

export function OperatorContext({issue,en}:{issue:string;en:boolean}) {
 if(issue!==context.issue)return null;
 return <Card className="card-pad operator-context" >
  <article data-operator-context>
   <div className="feed-meta"><span>{context.date}</span><Badge>{en?'Prior-period · not counted':'跨期背景 · 不计新增'}</Badge></div>
   <h3 className="news-title">{en?context.titleEn:context.title}</h3>
   <p className="news-text">{en?context.textEn:context.text}</p>
   {context.links.map(link=><a key={link.url} className="feed-link" href={link.url} target="_blank" rel="noreferrer">{en?link.labelEn:link.label} ↗</a>)}
   <div className="opportunity">{en?context.analysisEn:context.analysis}</div>
  </article>
 </Card>;
}
