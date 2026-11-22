(()=>{
const TOOLS={
github:{label:'GitHub username',ph:'e.g. torvalds',src:'GitHub API',url:'https://docs.github.com/rest'},
weather:{label:'City',ph:'e.g. Hyderabad',src:'Open-Meteo.com',url:'https://open-meteo.com/'},
fx:{label:'Amount and currencies',ph:'e.g. 100 USD to INR',src:'Frankfurter',url:'https://frankfurter.dev'},
hn:{label:'Topic filter (optional)',ph:'e.g. AI',src:'Hacker News API',url:'https://github.com/HackerNews/API'},
papers:{label:'Research topic',ph:'e.g. retrieval augmented generation',src:'Crossref',url:'https://www.crossref.org/documentation/retrieve-metadata/rest-api/'},
wiki:{label:'Topic',ph:'e.g. Binary search',src:'Wikipedia',url:'https://en.wikipedia.org/api/rest_v1/'}};
const MAP={github:['GitHub Portfolio Curator','Git & GitHub Fixer','Open-Source Maintainer'],
weather:['Time-Blocker','Route Planner','Wellness Advisor','Event Coordinator','Errand Scout','Fitness & Habit Coach'],
fx:['Budget Watchdog','Personal Finance Planner','Cashflow Modeler','Fuel & Expense Tracker','Pricing Strategist','Unit Economics Analyst','Freelance Proposal Writer'],
hn:['Trend Scout','Launch Strategist','Startup Ops Advisor','Growth Experimenter','Vendor Evaluator','Startup Pitch Reviewer'],
papers:['Deep Researcher','Citation Verifier','Paper & Repo Summarizer','Research Paper Writer','LLM Eval Judge','ML Training Engineer'],
wiki:['Study Tutor','Math & Stats Tutor','Language Practice Partner','Placement Aptitude Tutor','Cybersecurity Mentor','Brainstorm Partner']};
const toolOf=n=>Object.keys(MAP).find(k=>MAP[k].includes(n))||null;
const J=async(u,ms)=>{const c=new AbortController(),t=setTimeout(()=>c.abort(),ms||9000);try{const r=await fetch(u,{signal:c.signal});if(!r.ok)throw new Error('The service answered with HTTP '+r.status+'.');return await r.json()}catch(e){throw new Error(e.name==='AbortError'?'The service took too long to answer.':e.message)}finally{clearTimeout(t)}};
const E=encodeURIComponent,cut=(s,n)=>String(s||'').replace(/\s+/g,' ').trim().slice(0,n);
const WC=c=>c===0?'clear':c<=3?'partly cloudy':c<=48?'fog':c<=57?'drizzle':c<=67?'rain':c<=77?'snow':c<=82?'rain showers':c<=86?'snow showers':'thunderstorm';
const run={
async github(v){const u=v.trim().replace(/^@/,'').replace(/^https?:\/\/github\.com\//i,'').split('/')[0];if(!/^[A-Za-z0-9-]{1,39}$/.test(u))throw new Error('Enter a valid GitHub username.');
const [p,r]=await Promise.all([J('https://api.github.com/users/'+u),J('https://api.github.com/users/'+u+'/repos?per_page=100&sort=updated')]);
const own=r.filter(x=>!x.fork),lang={};own.forEach(x=>{if(x.language)lang[x.language]=(lang[x.language]||0)+1});const top=own.slice().sort((a,b)=>b.stargazers_count-a.stargazers_count).slice(0,5);
return{link:'https://github.com/'+u,text:['Profile: '+cut(p.name||p.login,60)+'; bio: '+cut(p.bio||'none',120)+'; public repos: '+p.public_repos+'; followers: '+p.followers+'; joined: '+cut(p.created_at,10),
'Original repos checked: '+own.length+'; without description: '+own.filter(x=>!x.description).length+'; without homepage link: '+own.filter(x=>!x.homepage).length+'; archived: '+own.filter(x=>x.archived).length,
'Top languages: '+(Object.entries(lang).sort((a,b)=>b[1]-a[1]).slice(0,5).map(x=>x[0]+' ('+x[1]+')').join(', ')||'none'),
'Top repos: '+top.map(x=>x.name+' ['+(x.language||'n/a')+', '+x.stargazers_count+' stars, last push '+cut(x.pushed_at,10)+'] '+cut(x.description||'no description',80)).join(' | ')].join('\n')}},
async weather(v){const g=await J('https://geocoding-api.open-meteo.com/v1/search?count=1&name='+E(v.trim()));const p=(g.results||[])[0];if(!p)throw new Error('City not found. Try a larger nearby city.');
const w=await J('https://api.open-meteo.com/v1/forecast?latitude='+p.latitude+'&longitude='+p.longitude+'&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&timezone=auto&forecast_days=3');
const c=w.current||{},d=w.daily||{time:[]};
return{link:'https://open-meteo.com/',text:'Location: '+cut([p.name,p.admin1,p.country].filter(Boolean).join(', '),80)+'. Now: '+c.temperature_2m+' C (feels like '+c.apparent_temperature+' C), '+WC(c.weather_code)+', wind '+c.wind_speed_10m+' km/h.\nNext days: '+d.time.map((t,i)=>t+': '+d.temperature_2m_min[i]+' to '+d.temperature_2m_max[i]+' C, rain chance '+d.precipitation_probability_max[i]+'%, '+WC(d.weather_code[i])).join(' | ')+'\nToday sunrise '+cut((d.sunrise||[''])[0],16).slice(-5)+', sunset '+cut((d.sunset||[''])[0],16).slice(-5)+' (local time).'}},
async fx(v){const m=v.match(/^\s*([\d.,]+)?\s*([A-Za-z]{3})\s*(?:to|in|->|=)?\s*([A-Za-z]{3})\s*$/i);if(!m)throw new Error('Try something like: 100 USD to INR');
const a=parseFloat((m[1]||'1').replace(/,/g,''))||1,b=m[2].toUpperCase(),q=m[3].toUpperCase();let rate,date='';
try{const d=await J('https://api.frankfurter.dev/v2/rate/'+b.toLowerCase()+'/'+q.toLowerCase());rate=d.rate;date=d.date||''}catch(e){const d=await J('https://api.frankfurter.dev/v1/latest?base='+b+'&symbols='+q);rate=d.rates&&d.rates[q];date=d.date||''}
if(!rate)throw new Error('That currency pair is not available.');
return{link:'https://frankfurter.dev',text:a+' '+b+' = '+(a*rate).toFixed(2)+' '+q+' (rate '+rate+', '+(date||'latest')+'). These are daily reference rates, not trading quotes.'}},
async hn(v){const ids=await J('https://hacker-news.firebaseio.com/v0/topstories.json');const items=(await Promise.all(ids.slice(0,20).map(i=>J('https://hacker-news.firebaseio.com/v0/item/'+i+'.json').catch(()=>null)))).filter(x=>x&&x.title);
const f=v.trim().toLowerCase();let pick=f?items.filter(x=>x.title.toLowerCase().includes(f)):items,note='';if(!pick.length){pick=items;note=' (nothing matched "'+cut(f,30)+'", showing the top stories)'}
return{link:'https://news.ycombinator.com/',text:'Hacker News top stories right now'+note+': '+pick.slice(0,8).map(x=>cut(x.title,90)+' ['+x.score+' points, '+(x.descendants||0)+' comments]').join(' | ')}},
async papers(v){const q=v.trim();if(q.length<3)throw new Error('Enter a research topic.');const d=await J('https://api.crossref.org/works?rows=6&select=title,issued,DOI,is-referenced-by-count,container-title&query='+E(q));const it=(d.message&&d.message.items)||[];if(!it.length)throw new Error('No papers found for that topic.');
return{link:'https://search.crossref.org/?q='+E(q),text:'Scholarly results for "'+cut(q,60)+'" (Crossref): '+it.map(i=>cut((i.title||['Untitled'])[0],110)+' ('+(((i.issued||{})['date-parts']||[[]])[0][0]||'n/a')+', '+cut((i['container-title']||['n/a'])[0],50)+', '+(i['is-referenced-by-count']||0)+' citations) https://doi.org/'+i.DOI).join(' | ')}},
async wiki(v){const q=v.trim();if(!q)throw new Error('Enter a topic.');const s=await J('https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&origin=*&search='+E(q)),t=(s[1]||[])[0];if(!t)throw new Error('No Wikipedia article found.');
const d=await J('https://en.wikipedia.org/api/rest_v1/page/summary/'+E(t.replace(/ /g,'_')));return{link:(d.content_urls&&d.content_urls.desktop&&d.content_urls.desktop.page)||'https://en.wikipedia.org/',text:'Wikipedia: '+cut(d.title,80)+' - '+cut(d.extract,900)}}};
const go=async(k,v)=>{if(!run[k])throw new Error('Unknown tool.');const r=await run[k](v||'');r.text=cut(r.text.replace(/ \| /g,' | '),1500).length<r.text.length?r.text.slice(0,1500):r.text;return r};
const api={TOOLS,MAP,toolOf,run:go};
if(typeof window!=='undefined')window.JWTools=api;else module.exports=api;
})();
