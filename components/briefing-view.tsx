"use client";

import { useState } from "react";
import { CompetitorWatch } from "./competitor-watch";
import monitoring from "@/config/competitor-monitoring.json";
import { Badge, Card } from "@/components/ui";
import { ChevronDown, ExternalLink } from "lucide-react";

type Item = {
  title: string;
  titleEn: string;
  date: string;
  badge: string;
  text: string;
  textEn: string;
  opportunity: string;
  opportunityEn: string;
  links: {label: string; url: string}[];
};
type Country = {
  name: string;
  nameEn: string;
  flag: string;
  sections: {category: string; categoryEn: string; displayCategory?:string; displayCategoryEn?:string; items: Item[]}[];
};

function englishBadge(badge: string) {
  if (!badge) return "";
  if (badge.includes("未核验")) return "Unverified";
  if (badge.includes("官方")) return "Official source";
  if (badge.includes("三源") || badge.includes("双源") || badge.includes("核验")) return "Cross-checked";
  return "Source verified";
}

export function BriefingView({ countries, language }: {countries: Record<string, Country>; language: "zh" | "en"}) {
  const [country, setCountry] = useState(Object.keys(countries)[0]);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const current = countries[country];
  const isEnglish = language === "en";

  return <>
    <div className="tabs">
      {Object.entries(countries).map(([key, item]) => <button key={key} data-country={key} aria-pressed={country === key} className={`tab ${country === key ? "active" : ""}`} onClick={() => { setCountry(key); setOpen({}); }}>
        {item.flag} {isEnglish ? item.nameEn : item.name}
      </button>)}
    </div>
    <div className="accordion" key={country}>
      {[...current.sections].sort((a,b)=>Number(a.category==='ICT 竞争对手最新动态')-Number(b.category==='ICT 竞争对手最新动态')).map((section, index) => {
        const competitor = section.category === 'ICT 竞争对手最新动态';
        if (!section.items.length && !competitor) return null;
        const active = open[index] ?? !competitor;
        return <Card className="accordion-section" key={`${country}-${index}-${section.category}`}>
          <button className="accordion-trigger" aria-expanded={active} aria-controls={`section-${index}`} onClick={() => setOpen((value) => ({...value, [index]: !active}))}>
            <span className="accordion-title">{competitor ? (isEnglish ? 'Competitor intelligence' : '竞争对手情报') : isEnglish ? (section.displayCategoryEn||section.categoryEn) : (section.displayCategory||section.category)}</span>
            <span style={{display: "flex", alignItems: "center", gap: 8}}><Badge>{competitor ? `${monitoring.vendors.length} ${isEnglish?'vendors watched':'家监控'}` : `${section.items.length} ${isEnglish?'items':'条'}`}</Badge><ChevronDown size={15} style={{transform: active ? "rotate(180deg)" : "none", transition: ".18s"}}/></span>
          </button>
          {active && <div className="accordion-body" id={`section-${index}`}>
            {competitor && <CompetitorWatch en={isEnglish}/>}
            {!competitor && !section.items.length && <p className="section-sub">{index===10 ? (isEnglish ? "See Important social updates above. Cross-platform mentions of existing stories are not counted as additional events." : "请见上方重要社媒快讯。同一事件的多平台传播不重复计入新闻。") : (isEnglish ? "No additional current-period event has been verified for this topic. Historical announcements and uncorroborated claims are excluded." : "本期未核实到本专题可新增的独立事件；不以历史公告或未证实线索填充。")}</p>}
            {section.items.map((item, itemIndex) => <article className="news-card" key={`${country}-${section.category}-${item.title}-${itemIndex}`}>
              <div className="feed-meta"><span>{item.date || (isEnglish ? "Current period" : "本期")}</span>{item.badge && <Badge tone="green">{isEnglish ? englishBadge(item.badge) : item.badge}</Badge>}</div>
              <h3 className="news-title">{isEnglish ? item.titleEn : item.title}</h3>
              <p className="news-text">{isEnglish ? item.textEn : item.text}</p>
              {item.links?.map((link) => <a className="feed-link" href={link.url} target="_blank" rel="noreferrer" key={link.url}>{isEnglish ? "Source" : link.label} <ExternalLink size={11} style={{display: "inline"}}/></a>)}
              {item.opportunity && <div className="opportunity">{isEnglish ? item.opportunityEn : item.opportunity}</div>}
            </article>)}
          </div>}
        </Card>;
      })}
    </div>
  </>;
}
