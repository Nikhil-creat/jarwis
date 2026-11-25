(()=>{const P=[["Home","/"],["Mission control","/command-center/"],["Assistants","/assistants/"],["Architecture","/architecture/"],["Builder","/builder/"],["Roadmap","/roadmap/"],["Studio","/studio/"],["Resume","/resume/"],["Interview","/interview/"],["Live data","/tools/"],["Status","/status/"],["Security","/security/"],["FAQ","/faq/"],["Contact","/contact/"]];
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e};
const mb=document.querySelector('.mb');if(mb)mb.onclick=()=>{const o=document.querySelector('.nav nav').classList.toggle('open');mb.setAttribute('aria-expanded',String(o))};
const cn=(document.querySelector('link[rel=canonical]')||{}).href;if(cn){try{const ch=new URL(cn).host;if(location.host!==ch&&location.host.endsWith('.vercel.app')){const bn=el('div','old');bn.append('You are viewing an old copy of this site. ');const al=el('a','','Open the live site');al.href='https://'+ch+location.pathname;bn.append(al);document.body.prepend(bn)}}catch(e){}}
const tg=document.querySelector('.tg');if(tg){tg.setAttribute('aria-pressed',String(document.documentElement.dataset.theme==='dark'));tg.onclick=()=>{const d=document.documentElement,n=d.dataset.theme==='dark'?'light':'dark';d.dataset.theme=n;try{localStorage.setItem('jw-theme',n)}catch(e){}tg.setAttribute('aria-pressed',String(n==='dark'))}}
const ov=el('div','ov');ov.hidden=true;const bx=el('div','pal');const inp=el('input');inp.placeholder='Jump to a page...';inp.setAttribute('aria-label','Search pages');const ul=el('ul');bx.append(inp,ul);ov.append(bx);document.body.append(ov);
function rl(){const v=inp.value.toLowerCase();ul.textContent='';P.filter(p=>p[0].toLowerCase().includes(v)).forEach(p=>{const li=el('li'),a=el('a','',p[0]);a.href=p[1];li.append(a);ul.append(li)})}
function op(){ov.hidden=false;inp.value='';rl();inp.focus()}
addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();op()}if(e.key==='Escape')ov.hidden=true});
inp.addEventListener('input',rl);inp.addEventListener('keydown',e=>{if(e.key==='Enter'){const a=ul.querySelector('a');if(a)location.href=a.href}});ov.addEventListener('click',e=>{if(e.target===ov)ov.hidden=true});
const api=(document.querySelector('meta[name=jarwis-api]')||{}).content||'';
const K=[["assistant|agent|99","Jarwis has 99 specialist assistants plus Commander-00. Browse and chat with them on the Assistants page."],["secur|approve|safe","Risky actions like deploys, pushes and sends always wait for your approval. See the Security page."],["architect|how|work","One commander plans a mission, assistants run it, and you approve the risky steps. See Architecture."],["model|router|groq|gemini","The router discovers available models, picks a fast or deep tier per task, and falls back to the other provider."],["try|demo|command","Open the Command center to run a mission preview."]];
const b=el('button','dock','Ask Jarwis');b.type='button';b.setAttribute('aria-expanded','false');b.setAttribute('aria-controls','jw-chat');
const pn=el('section','chat');pn.id='jw-chat';pn.hidden=true;pn.setAttribute('aria-label','Chat with Jarwis');
const hd=el('div','ch'),tt=el('strong','','Jarwis'),xb=el('button','','Close'),cb=el('button','','Clear'),ac=el('span');xb.type=cb.type='button';xb.setAttribute('aria-label','Close chat');cb.setAttribute('aria-label','Clear chat history');ac.append(cb,xb);hd.append(tt,ac);
const lg=el('div','cl');lg.setAttribute('role','log');lg.setAttribute('aria-live','polite');
const sg=el('div','sg');['What can you do?','Which assistant helps with interviews?','How is it secure?'].forEach(t=>{const c=el('button','',t);c.type='button';c.onclick=()=>send(t);sg.append(c)});
const row=el('form','crow'),f=el('input');f.placeholder='Ask about Jarwis...';f.setAttribute('aria-label','Message');f.autocomplete='off';f.maxLength=1000;
const sb=el('button','sbtn','Send');sb.type='submit';const mc=el('button','mic','Mic');mc.type='button';mc.setAttribute('aria-label','Speak your message');row.append(f,mc,sb);
pn.append(hd,lg,sg,row);document.body.append(b,pn);
let log=[];try{log=JSON.parse(localStorage.getItem('jw-dock')||'[]')}catch(e){}
const save=()=>{try{localStorage.setItem('jw-dock',JSON.stringify(log.slice(-40)))}catch(e){}};
let H=log.map(x=>({role:x.me?'user':'assistant',content:x.t})),vo=0,busy=0;
const say=(t,me,meta,keep)=>{const d=el('p',me?'me':'',t);if(meta)d.append(el('small','',meta));lg.append(d);lg.scrollTop=lg.scrollHeight;if(keep){log.push({t,me:me?1:0,meta:meta||''});save()}return d};
log.forEach(x=>say(x.t,x.me,x.meta));if(log.length)sg.hidden=true;
cb.onclick=()=>{log=[];H=[];save();lg.textContent='';sg.hidden=false;say('Chat cleared. How can I help?')};
function open(v){pn.hidden=!v;b.setAttribute('aria-expanded',String(v));if(v){if(!lg.children.length)say('Hi, I am Jarwis. Ask me about the assistants, security or architecture.');f.focus()}}
b.onclick=()=>open(pn.hidden);xb.onclick=()=>{open(false);b.focus()};
addEventListener('keydown',e=>{if(e.key==='Escape'&&!pn.hidden)open(false)});
async function send(m){m=(m||f.value).trim();if(!m||busy)return;f.value='';sg.hidden=true;say(m,1,'',1);if(/\b(resume|cv)\b/i.test(m)){H.push({role:'user',content:m});const d=say('I can build a one-page, ATS-friendly resume tailored to a job. It needs a few details first.',0,'',1),l=el('a','','Open the Resume Builder');l.href='/resume/';l.style.cssText='display:block;margin-top:6px;color:#FF5A1F';d.append(l);return}busy=1;sb.disabled=true;const w=say('Thinking...');w.className='typing';let t,meta='';
try{if(!api)throw 0;const r=await fetch(api,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m,history:H.slice(-8)})});const j=await r.json();t=String(j.reply||'No reply.');if(j.model)meta=j.provider+' / '+j.model}
catch(_){const k=K.find(y=>new RegExp(y[0],'i').test(m));t=k?k[1]:'I am offline right now, but I can answer questions about assistants, security, architecture and the model router.';meta='offline answer'}
w.remove();H.push({role:'user',content:m},{role:'assistant',content:t});say(t,0,meta,1);if(vo&&window.speechSynthesis)speechSynthesis.speak(new SpeechSynthesisUtterance(t));busy=0;sb.disabled=false;f.focus()}
row.addEventListener('submit',e=>{e.preventDefault();send()});
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;mc.onclick=()=>{if(!SR){say('Voice input is not supported in this browser.');return}const r=new SR();r.lang='en-US';r.onresult=e=>{vo=1;send(e.results[0][0].transcript)};r.start()};
if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});
})();
