# Nepal News Monitoring Skill

> 从 PACD 群聊分享记录中提取的尼泊尔本地新闻监控技能，涵盖 17 个新闻网站的关键信息抓取与关键词匹配。

## 触发条件

当用户需要以下操作时触发本技能：
- 监控尼泊尔本地新闻
- 抓取尼泊尔电信/科技/政策相关新闻
- 按关键词匹配新闻文章
- 生成新闻监控报告
- 提及"PACD""Nepal news""尼泊尔新闻""新闻监控"等关键词

## 本地新闻来源清单

### 高频来源（PACD 群分享 Top 3）

| 排名 | 网站名称 | 域名 | 语言 | 主要领域 | 分享次数 |
|------|----------|------|------|----------|----------|
| 1 | TechPana | techpana.com | English + Nepali | 科技、电信、5G、IT | 19 |
| 2 | NepalKhabar | nepalkhabar.com | Nepali + English | 经济、政治、社会、企业 | 18 |
| 3 | TechnologyKhabar | technologykhabar.com | Nepali | 科技、电信、IT | 17 |

### 中频来源（分享 2-4 次）

| 网站名称 | 域名 | 语言 | 主要领域 | 分享次数 |
|----------|------|------|----------|----------|
| Baahrakhari | baahrakhari.com | Nepali | 评论、分析、政治、经济 | 4 |
| The Kathmandu Post | kathmandupost.com | English | 全国、经济、国际 | 4 |
| eKantipur | ekantipur.com | Nepali + English | 新闻、商业、全国 | 3 |
| Clickmandu | clickmandu.com | Nepali | 娱乐、新闻、科技 | 3 |
| OnlineKhabar | onlinekhabar.com | Nepali + English | 新闻、科技、社会 | 3 |
| Bizmandu | bizmandu.com | Nepali | 商业、经济、金融 | 2 |
| Setopati | setopati.com | Nepali | 政治、经济、社会 | 2 |

### 低频来源（分享 1 次）

| 网站名称 | 域名 | 语言 | 主要领域 |
|----------|------|------|----------|
| MoIC Nepal | moic.gov.np | English + Nepali | 政府官方、电信政策、官方通告 |
| Rajdhani Daily | rajdhanidaily.com | Nepali | 新闻、政治、社会 |
| Karobar Daily | karobardaily.com | Nepali | 商业、经济 |
| UrjaKhabar | urjakhabar.com | Nepali | 能源、水电、经济 |
| NepalPurbadhar | nepalpurbadhar.com | Nepali | 新闻、商业 |
| Bizpati | bizpati.com | Nepali | 商业、经济 |
| KarmachariPress | karmacharipress.com | Nepali | 劳工、政府、采购 |

## 关键信息抓取方法

### 通用抓取流程

```
1. 获取文章 URL
2. 请求网页内容 (HTTP GET)
3. 解析 HTML (BeautifulSoup / lxml)
4. 提取关键字段：
   - 文章标题 (title)
   - 发布日期 (publish_date)
   - 文章正文 (body_text)
   - 作者/来源 (author)
   - 文章分类 (category)
5. 关键词匹配与分类
6. 输出结构化数据
```

### 各网站抓取选择器

#### 1. techpana.com（科技/电信 - 首选源）

```python
{
    "title": "h1.entry-title, .post-title",
    "body": ".entry-content, .post-content",
    "date": ".post-date, time[datetime]",
    "author": ".post-author, .author-name",
    "category": ".post-category, .breadcrumb"
}
```

- **URL 模式**: `techpana.com/{year}/{id}/{slug}`
- **特点**: 文章结构规范，URL slug 即为英文标题摘要
- **注意**: 部分文章含 Nepali 内容，需双语匹配

#### 2. nepalkhabar.com（综合新闻 - 次选源）

```python
{
    "title": "h1, .article-title",
    "body": ".article-content, .news-content",
    "date": ".published-date, time[datetime]",
    "author": ".article-author",
    "category": ".article-category, .breadcrumb"
}
```

- **URL 模式**: `nepalkhabar.com/{category}/{id}-{date}`
- **分类路径**: `/economy/`（经济）, `/politics/`（政治）, `/society/`（社会）, `/corporate/`（企业）, `/economy/science-tech/`（科技）
- **注意**: URL 中已包含分类信息，可直接从 URL 提取

#### 3. technologykhabar.com（尼泊尔语科技新闻）

```python
{
    "title": "h1.entry-title, h1",
    "body": ".entry-content, article",
    "date": ".post-date, time[datetime]",
    "author": ".post-author",
    "category": ".post-category"
}
```

- **URL 模式**: `technologykhabar.com/{year}/{month}/{day}/{id}/`
- **特点**: 纯尼泊尔语内容，需 Nepali 关键词匹配
- **注意**: 电信行业报道深度较高

#### 4. baahrakhari.com（评论/分析）

```python
{
    "title": "h1, .detail-title",
    "body": ".detail-content, .article-body",
    "date": ".publish-date",
    "author": ".article-author"
}
```

- **URL 模式**: `baahrakhari.com/detail/{id}`
- **特点**: 深度分析和评论文章，篇幅较长
- **注意**: 观点性内容较多，需区分事实与观点

#### 5. kathmandupost.com（英文大报）

```python
{
    "title": "h1.headline, h1",
    "body": ".article-body, .story-content",
    "date": ".published-at, time[datetime]",
    "author": ".author-name",
    "category": ".section-name"
}
```

- **URL 模式**: `kathmandupost.com/{section}/{year}/{month}/{day}/{slug}`
- **特点**: 英文内容，文章结构规范
- **注意**: 国际视角报道尼泊尔新闻

#### 6. ekantipur.com（Kantipur 日报）

```python
{
    "title": "h1, .article-title",
    "body": ".article-body, .news-content",
    "date": ".published-date, time[datetime]",
    "author": ".article-author"
}
```

- **URL 模式**: `ekantipur.com/{section}/{year}/{month}/{day}/{slug}.html`
- **英文版**: URL 含 `/en/` 路径为英文版
- **注意**: 尼泊尔最大媒体集团之一

#### 7-17. 其他来源通用模板

```python
{
    "title": "h1, .post-title, .news-title",
    "body": ".post-content, .news-content, .entry-content, .news-detail",
    "date": ".post-date, .news-date, .publish-date, time[datetime]",
    "author": ".post-author, .article-author"
}
```

### 政府官方来源

#### moic.gov.np（尼泊尔通信与信息技术部）

```python
{
    "title": "h1, .content-title",
    "body": ".content-body, .article-content",
    "date": ".content-date"
}
```

- **重要性**: 官批/政策/法规类信息的一手来源
- **注意**: 官方公告具有最高权威性

## 关键词匹配规则

### 匹配优先级

| 优先级 | 类别 | 触发条件 |
|--------|------|----------|
| 🔴 CRITICAL | 灾害/应急 | Flood, Landslide, Earthquake, Network Restoration, 灾害影响网络 |
| 🟠 HIGH | 华为相关 | Title 或 Body 含 Huawei/ह्वावे |
| 🟠 HIGH | 电信监管 | NTA, Telecom Policy, Licensing, Telecommunication Act |
| 🟠 HIGH | 政府政策 | Ministry of Communication, MoCIT, Government Telecom |
| 🟡 MEDIUM | 电信运营商 | Nepal Telecom, Ncell, UTL, Smart Telecom, ZTE |
| 🟡 MEDIUM | 5G/技术 | 5G, IoT, Smart City, Digital Nepal |
| 🟡 MEDIUM | 经济/商业 | Digital Transformation, Infrastructure, Solar, Renewable |
| 🟡 MEDIUM | 政治/地缘 | Nepal-China, Nepal-India, Nepal-US Relations |

### 关键词列表（英文 + 尼泊尔语）

#### 华为相关
- **English**: Huawei, Huawei Nepal, Huawei 5G, Huawei CSR, Huawei technology, Huawei criminal trial
- **Nepali**: ह्वावे, हुवावे, ह्वावे नेपाल, ह्वावे प्रौद्योगिकी, ह्वावे 5G, ह्वावे सीएसआर, ह्वावे दिगो विकास

#### 电信运营商
- **English**: Nepal Telecom, Ncell, CG Telecom, UTL, Smart Telecom, ZTE, Telecom Operators
- **Nepali**: नेपाल टेलिकम, एनसेल, सीजी टेलिकम, युटीएल, स्मार्ट, जेडटीई

#### 电信监管
- **English**: NTA, Nepal Telecommunications Authority, Telecom Regulation, Telecommunication Policy, Telecom Licensing, Telecom Standards
- **Nepali**: नेपाल दूरसञ्चार प्राधिकरण, एनटीए, टेलिकम नियमन, टेलिकम नीति, टेलिकम लाइसेन्सिङ

#### 5G 与技术
- **English**: 5G Technology, 5G spectrum, 5G launch, IoT, Smart City, Digital Power, Smart Education
- **Nepali**: 5G प्रौद्योगिकी, आईसीटी समाधान, डिजिटल नेपाल, स्मार्ट सिटी

#### 政府与政策
- **English**: Ministry of Communication, MoCIT, Government Telecom Projects, Digital Nepal Campaign
- **Nepali**: सूचना तथा सञ्चार प्रविधि मन्त्रालय, सरकारी टेलिकम परियोजना, डिजिटल नेपाल अभियान

#### 灾害与应急
- **English**: Flood, Landslide, Earthquake, Emergency, Disaster Recovery, Network Restoration, Bhotekoshi
- **Nepali**: बाढी, पहिरो, भूकम्प, आपत्कालीन, पुनर्स्थापना

## Agent 集成方案

### 数据抓取 Pipeline

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# 新闻源配置
NEWS_SOURCES = {
    "techpana.com": {
        "selectors": {
            "title": "h1.entry-title, .post-title",
            "body": ".entry-content, .post-content",
            "date": ".post-date, time[datetime]",
        },
        "language": "en+ne",
        "priority": "high"
    },
    "nepalkhabar.com": {
        "selectors": {
            "title": "h1, .article-title",
            "body": ".article-content, .news-content",
            "date": ".published-date, time[datetime]",
        },
        "language": "ne+en",
        "priority": "high"
    },
    "technologykhabar.com": {
        "selectors": {
            "title": "h1.entry-title, h1",
            "body": ".entry-content, article",
            "date": ".post-date, time[datetime]",
        },
        "language": "ne",
        "priority": "high"
    },
    # ... 其他来源同理
}

def scrape_article(url):
    """抓取单篇文章"""
    domain = extract_domain(url)
    config = NEWS_SOURCES.get(domain)
    if not config:
        return None
    
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 提取字段
    title = extract_text(soup, config["selectors"]["title"])
    body = extract_text(soup, config["selectors"]["body"])
    date = extract_text(soup, config["selectors"]["date"])
    
    # 关键词匹配
    category, priority = match_keywords(title, body)
    
    return {
        "url": url,
        "domain": domain,
        "title": title,
        "body": body,
        "date": date,
        "category": category,
        "priority": priority,
        "language": config["language"],
        "scraped_at": datetime.now().isoformat()
    }

def match_keywords(title, body):
    """关键词匹配，返回类别和优先级"""
    text = (title + " " + body).lower()
    
    # CRITICAL: 灾害相关
    if any(kw in text for kw in ["flood", "landslide", "bhotekoshi", "disaster"]):
        return "Disaster", "CRITICAL"
    
    # HIGH: 华为相关
    if any(kw in text for kw in ["huawei", "ह्वावे", "हुवावे"]):
        return "Huawei", "HIGH"
    
    # HIGH: 电信监管
    if any(kw in text for kw in ["nta", "telecom policy", "telecommunication act"]):
        return "Regulation", "HIGH"
    
    # MEDIUM: 电信运营商
    if any(kw in text for kw in ["nepal telecom", "ncell", "utl", "smart telecom"]):
        return "Telecom Operator", "MEDIUM"
    
    # MEDIUM: 5G
    if any(kw in text for kw in ["5g", "5G"]):
        return "5G Technology", "MEDIUM"
    
    return "General", "LOW"
```

### 监控工作流

```
1. 定时轮询新闻源（建议每 2-4 小时一次）
2. 对每个新闻源：
   a. 获取最新文章列表
   b. 与已抓取 URL 去重
   c. 抓取新文章内容
   d. 关键词匹配与分类
3. 按优先级排序输出：
   - CRITICAL → 立即推送告警
   - HIGH → 纳入日报
   - MEDIUM → 纳入周报
   - LOW → 归档备查
4. 生成监控报告（日报/周报/月报）
```

### 输出数据结构

```json
{
    "article_id": "uuid",
    "url": "https://techpana.com/2026/158220/...",
    "source": "techpana.com",
    "title": "Telecom Transformation Year: Nepal 5G Launch",
    "publish_date": "2026-08-02",
    "scrape_date": "2026-09-18T10:00:00",
    "category": "5G Technology",
    "priority": "MEDIUM",
    "language": "en",
    "keywords_matched": ["5G", "NTA", "Nepal Telecom"],
    "summary": "文章摘要...",
    "body_length": 1500,
    "related_to_huawei": false
}
```

## 配套文件

- **Excel 工作簿**: `Nepal_Media_Monitoring_with_News_Sources.xlsx`
  - Sheet 1: `Nepal_Monitoring categories` — 原始监控关键词分类
  - Sheet 2: `News Sources` — 17 个新闻网站来源清单
  - Sheet 3: `Scraping Guide` — 各网站 HTML 选择器参考
  - Sheet 4: `Keyword Matching Rules` — 关键词匹配规则与优先级

## 使用建议

1. **高频监控**: 对 techpana.com、nepalkhabar.com、technologykhabar.com 每日轮询
2. **官方源监控**: 对 moic.gov.np 每日检查，政策变更需即时告警
3. **灾害应急**: 监控到 flood/landslide 等关键词时立即触发 CRITICAL 告警
4. **双语匹配**: 同时使用英文和尼泊尔语关键词进行匹配，避免遗漏
5. **去重策略**: 以 URL 为唯一键，清理 fbclid 等跟踪参数后去重
6. **优先级排序**: CRITICAL > HIGH > MEDIUM > LOW，高优先级文章优先推送
