import data from '@/data/nepal.json';
import {Card} from './ui';

export function IssueDigest({en}:{en:boolean}) {
 const t=(zh:string,english:string)=>en?english:zh;
 const sections=data.report.countries.np.sections;
 const news=sections.reduce((n,s)=>n+s.items.length,0);
 const facebook=data.sources.filter(s=>s.platform==='Facebook');
 const pending=facebook.filter(s=>!s.lastCollectedAt).length;
 return <Card className="card-pad issue-digest">
  <h2>{t('本期要点','This issue at a glance')}</h2>
  <p className="section-sub">{t(`${news} 条独立事件 · ${sections.filter(s=>s.items.length).length} 个有新闻的专题 · 社媒转述不重复计数`,`${news} distinct events · ${sections.filter(s=>s.items.length).length} populated topics · social mentions are not counted twice`)}</p>
  <ol style={{listStyle:'decimal',paddingLeft:24,lineHeight:1.85,margin:'16px 0'}}>{(en?data.report.summaryEn:data.report.summary).map((summary,i)=><li style={{marginBottom:8}} key={i}>{summary}</li>)}</ol>
  <nav aria-label={t('本期导航','Issue navigation')} style={{display:'flex',gap:16,flexWrap:'wrap'}}>
   <a href="#issue-news">{t('专题新闻与影响','News & implications')}</a>
   <a href="#issue-social">{t('社媒补充','Social context')}</a>
   <a href="../compliance/">{t('法律与合规','Legal & compliance')}</a>
  </nav>
  <details style={{marginTop:16}}><summary>{t('内容覆盖与采集缺口','Coverage & collection gaps')}</summary>
   <p>{t(`Facebook 已登记 ${facebook.length} 个信源，其中 ${pending} 个尚无帖子扫描完成记录。登记账号不等于读取帖子；当前网站采集器不自动采集 Facebook。`,`${facebook.length} Facebook sources are registered; ${pending} have no completed post-scan record. Registering an account does not mean reading its posts. The website collector does not automatically collect Facebook.`)}</p>
   <p>{t('本次调整是重新编排已有内容，并未新增已核验新闻。没有独立新闻的专题暂不展示，竞争监控名单单独折叠。','This revision reorganizes existing coverage; it does not add verified events. Empty topics are omitted and the competitor watchlist is collapsed separately.')}</p>
  </details>
 </Card>;
}
