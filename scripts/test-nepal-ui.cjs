const fs=require('node:fs');
const http=require('node:http');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve('out');
const server=http.createServer((req,res)=>{
 let route=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/nepal-ict-briefing/,'');
 if(route.endsWith('/'))route+='index.html';
 const file=path.resolve(root,'.'+route);
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404).end();return;}
 res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':file.endsWith('.html')?'text/html':'application/octet-stream');res.end(fs.readFileSync(file));
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 let browser;
 try{
 browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const base=process.env.NEPAL_LIVE_BASE||`http://127.0.0.1:${server.address().port}/nepal-ict-briefing`;
 for(const route of ['','briefings','sources','people']){
  await page.goto(base+'/'+(route?route+'/':''));await page.getByRole('button',{name:'English',exact:true}).click();
  await page.getByRole('heading',{level:1}).first().waitFor();
  assert((await page.locator('h1').innerText()).match(/Nepal|Historical/));
  await page.getByRole('button',{name:'中文',exact:true}).click();
  assert((await page.locator('h1').innerText()).match(/尼泊尔|历史/));
  assert(!/伊拉克|约旦|黎巴嫩/.test(await page.locator('main').innerText()));
 }
 const sections=JSON.parse(fs.readFileSync('config/nepal-report.json','utf8')).countries.np.sections;
 const portal=JSON.parse(fs.readFileSync('data/nepal.json','utf8'));
 const fallbackCount=JSON.parse(fs.readFileSync('config/deepseek-fallback-digest.json','utf8')).items.length;
 await page.goto(base+'/briefings/');assert.equal(await page.locator('[data-country="np"]').count(),portal.issues.length);assert.equal(await page.locator('[data-issue]').count(),portal.issues.length);
 const expectedAccordions=portal.issues.reduce((total,issue)=>total+issue.countries.np.sections.filter(s=>s.items.length||(issue.current&&s.category==='ICT 竞争对手最新动态')).length,0);
 assert.equal(await page.locator('.accordion-trigger').count(),expectedAccordions);
 assert.equal(await page.locator('[data-fallback-digest]').count(),fallbackCount>0?1:0,'Fallback card visibility must match its data');
 assert.equal(await page.locator('.news-card').count(),portal.issues.reduce((total,issue)=>total+issue.stats.news,0),'All current and historical projects must be visible together');
 const history=portal.issues.find(issue=>!issue.current);assert(history,'Expected one integrated historical issue');
 await page.locator('[data-history-summary]').waitFor();
 assert.equal(await page.locator('[data-history-summary]').count(),1);
 assert.equal(await page.locator(`[data-issue="${history.issue}"] .news-card`).count(),history.stats.news,'Historical issue must show every reviewed item without a tab click');
 assert((await page.locator(`[data-issue="${history.issue}"] .accordion`).innerText()).includes('Nepal Telecom 发布宪法日套餐'));
 for(const language of ['中文','English']){
  await page.getByRole('button',{name:language,exact:true}).click();
  const typography=await page.locator('.news-card').first().evaluate(card=>{const style=selector=>getComputedStyle(card.querySelector(selector));return {title:parseFloat(style('.news-title').fontSize),body:parseFloat(style('.news-text').fontSize),link:parseFloat(style('.feed-link').fontSize),line:parseFloat(style('.news-text').lineHeight)};});
  assert(typography.title>typography.body&&typography.body>typography.link);assert(typography.body>=12&&typography.line/typography.body>=1.7);
  for(const width of [1440,390]){await page.setViewportSize({width,height:1000});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));}
 }
 assert((await page.locator(`[data-issue="${history.issue}"] .accordion`).innerText()).includes('Nepal Telecom announces Constitution Day plans'));
 await page.getByRole('button',{name:'中文',exact:true}).click();
 assert.equal(await page.locator('.competitor-card').count(),0);
 await page.locator('.accordion-trigger').filter({hasText:'竞争对手情报'}).click();
 for(const title of ['运营商集团战略','华为在尼泊尔']) assert(!(await page.locator(`[data-issue="${portal.report.issue}"] .accordion`).innerText()).includes(title));
 assert((await page.locator(`[data-issue="${portal.report.issue}"] .accordion`).innerText()).includes('对外关系与市场影响'));
 for(const language of ['English','中文']){
  await page.getByRole('button',{name:language,exact:true}).click();
  const typography=await page.locator('.social-story').first().evaluate(el=>{
   const style=s=>getComputedStyle(el.querySelector(s));
   return {title:parseFloat(style('h3').fontSize),body:parseFloat(style('.story-summary').fontSize),link:parseFloat(style('.story-source').fontSize),line:parseFloat(style('.story-summary').lineHeight)};
  });
  assert(typography.title>typography.body&&typography.body>typography.link);
  assert(typography.body>=15&&typography.line/typography.body>=1.7);
  assert.equal(await page.locator('[data-primary-competitors] .competitor-card').count(),6);
  assert.equal(await page.locator('.competitor-card').count(),11);
  for(const name of ['ZTE','Cisco','Whale Cloud','AsiaInfo','H3C','FiberHome']) assert((await page.locator('[data-primary-competitors]').innerText()).includes(name));
  assert.equal(await page.locator('[data-evidence-kind="current"]').count(),0);
  assert.equal(await page.locator('[data-evidence-kind="watch"]').count(),5);
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:1000});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
   if(process.env.NEPAL_READING_SHOTS)await page.screenshot({path:`${process.env.NEPAL_READING_SHOTS}-${language==='English'?'en':'zh'}-${width}.png`,fullPage:false});
  }
 }
 assert.equal(await page.locator('a[href*="/compliance"]').count(),0,'Removed compliance section must not have navigation links');
 const removedPage=await page.request.get(base+'/compliance/');assert.equal(removedPage.status(),404,'Removed compliance page must not remain published');
 assert.equal(await page.locator('a[href*="/archive"]').count(),0,'Separate archive navigation must stay removed');
 const removedArchive=await page.request.get(base+'/archive/');assert.equal(removedArchive.status(),404,'Historical issues must live inside Briefing, not a separate archive page');
 await page.goto(base+'/sources/');assert((await page.locator('main').innerText()).includes('监控关注点与附件'));
 await page.getByRole('textbox').fill('New Business Age');assert.equal(await page.locator('tbody tr').count(),1);
 await page.getByRole('textbox').fill('');
 const attachment=await page.request.get(base+'/resources/Nepal_Media_Monitoring_with_News_Sources.xlsx');assert(attachment.ok());assert.equal((await attachment.body()).subarray(0,2).toString(),'PK');
 await page.getByRole('textbox').fill('TechnologyKhabar');assert.equal(await page.locator('tbody tr').count(),1);
 await page.getByRole('textbox').fill('Ncell');assert.equal(await page.locator('tbody tr').count(),3);
 await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
 await page.goto(base+'/people/');assert.equal(await page.locator('tbody tr').count(),18);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
 if(process.env.NEPAL_SCREENSHOT){await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/sources/');await page.screenshot({path:process.env.NEPAL_SCREENSHOT,fullPage:false});}
 assert.deepEqual(errors,[]);console.log('Four routes, integrated issue history, Chinese/English, removed archive/compliance pages, Nepal isolation, source filtering and mobile width passed.');
 }finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
