import directory from '@/config/government-directory.json';
import data from '@/data/nepal.json';
import {Card} from './ui';
export function GovernmentDirectory({en}:{en:boolean}){
 const t=(zh:string,english:string)=>en?english:zh;
 return <Card className="card-pad"><h2>{t('联邦部委官网全目录','Federal ministry website directory')}</h2><p>{t(directory.note,directory.noteEn)}</p><p className="section-sub">{directory.reviewedAt} · <a href={directory.rosterEvidence} target="_blank" rel="noreferrer">{t('官方内阁职责名录','Official cabinet portfolio roster')}</a></p><div className="table-wrap"><table className="data-table"><thead><tr><th>{t('部委／机构','Ministry / office')}</th><th>{t('采集状态','Collection status')}</th></tr></thead><tbody>{directory.entries.map(entry=>{const source=data.sources.find(s=>s.id===entry.id);return <tr key={entry.id}><td><a href={entry.url} target="_blank" rel="noreferrer">{t(entry.name,entry.nameEn)}</a></td><td>{source?t(source.status,source.statusEn):t('尚未登记','Not registered')}</td></tr>})}</tbody></table></div></Card>;
}
