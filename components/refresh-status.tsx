import status from '@/data/refresh-status.json';
import {Card} from './ui';

export function RefreshStatus({en}:{en:boolean}) {
 const failed=status.failedSources;
 const stamp=new Intl.DateTimeFormat(en?'en-GB':'zh-CN',{timeZone:'Asia/Baghdad',dateStyle:'medium',timeStyle:'short'}).format(new Date(status.generatedAt));
 return <Card className="card-pad"><h2>{en?'Daily search status':'每日检索状态'}</h2>
 <p>{en?'Last collection completed':'最近采集完成'}：{stamp} · Asia/Baghdad</p>
 <p>{en?`${status.candidateCount} candidate links · ${failed} failed sources`:`${status.candidateCount} 条候选链接 · ${failed} 个信源扫描失败`}</p>
 <p>{en?'Scheduled daily at 00:00 Baghdad (02:45 Nepal); execution may be delayed. Candidates are not verified news. Editorial review starts at 00:20 Baghdad and depends on the local app being available. Each completed 14-day issue is sealed once and remains selectable inside the Briefing page.':'每天巴格达时间00:00（尼泊尔02:45）计划采集，实际执行可能延迟。候选不等于已核验新闻；00:20开始编辑复核，依赖本地应用可用。每个14天完整期只封存一次，并持续在“双周简报”页面内可选。'}</p>
 <a href="https://github.com/Adam123wu/nepal-ict-briefing/actions/workflows/nepal-sources.yml" target="_blank" rel="noreferrer">{en?'Check latest runs and failures':'查看最新运行与失败记录'}</a>
 </Card>;
}
