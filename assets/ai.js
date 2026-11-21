(()=>{const P=[["Home","/"],["Command center","/command-center/"],["Assistants","/assistants/"],["Architecture","/architecture/"],["Roadmap","/roadmap/"],["Status","/status/"],["Security","/security/"],["Sitemap","/sitemap.xml"]];
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e};
// assistant filter
const q=document.getElementById('q');if(q)q.addEventListener('input',()=>{const v=q.value.toLowerCase();document.querySelectorAll('#mx tbody tr').forEach(r=>r.hidden=v&&!r.textContent.toLowerCase().includes(v))});
// command palette (Ctrl/Cmd+K)
const ov=el('div','ov');ov.hidden=true;const bx=el('div','pal');const inp=el('input');inp.placeholder='Jump to a page...';inp.setAttribute('aria-label','Search pages');const ul=el('ul');bx.append(inp,ul);ov.append(bx);document.body.append(ov);
function rl(){const v=inp.value.toLowerCase();ul.textContent='';P.filter(p=>p[0].toLowerCase().includes(v)).forEach(p=>{const li=el('li'),a=el('a','',p[0]);a.href=p[1];li.append(a);ul.append(li)})}
function op(){ov.hidden=false;inp.value='';rl();inp.focus()}
addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();op()}if(e.key==='Escape')ov.hidden=true});
inp.addEventListener('input',rl);inp.addEventListener('keydown',e=>{if(e.key==='Enter'){const a=ul.querySelector('a');if(a)location.href=a.href}});ov.addEventListener('click',e=>{if(e.target===ov)ov.hidden=true});
// ask Jarwis dock
const api=(document.querySelector('meta[name=jarwis-api]')||{}).content||'';
const K=[["assistant|agent|99","Jarwis has 75 ready-made specialists in five clusters plus 24 forge slots. Browse them on the Assistants page."],["secur|approve|safe","Risky actions like deploys, pushes and sends always wait for your approval. See the Security page."],["architect|how|work","One commander plans a mission, assistants run it in sandboxes, and you approve the risky steps. See Architecture."],["model|router|groq|gemini","The router discovers available models, picks a fast or deep tier per task, and falls back or goes local."],["try|demo|command","Open the Command center to run a scripted mission preview."]];
const b=el('button','dock','Ask Jarwis');b.setAttribute('aria-expanded','false');const pn=el('div','chat');pn.hidden=true;const lg=el('div','cl');lg.setAttribute('aria-live','polite');const f=el('input');f.placeholder='Ask about Jarwis...';f.setAttribute('aria-label','Ask Jarwis');pn.append(lg,f);document.body.append(b,pn);
let vo=0;const say=(t,m)=>{if(!m&&vo&&window.speechSynthesis)speechSynthesis.speak(new SpeechSynthesisUtterance(t));const d=el('p',m?'me':'',t);lg.append(d);lg.scrollTop=1e5};
b.onclick=()=>{pn.hidden=!pn.hidden;b.setAttribute('aria-expanded',String(!pn.hidden));if(!pn.hidden){f.focus();if(!lg.children.length)say('Hi, I am Jarwis. Ask me about the assistants, security or architecture.')}};
async function send(){if(!f.value.trim())return;const m=f.value.trim();f.value='';say(m,1);
if(api){try{const r=await fetch(api,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});const j=await r.json();say(String(j.reply||'No reply.'));return}catch(_){}}
const k=K.find(x=>new RegExp(x[0],'i').test(m));say(k?k[1]:'I can answer questions about assistants, security, architecture and the model router.')}
f.addEventListener('keydown',e=>{if(e.key==='Enter')send()});
const SR=window.SpeechRecognition||window.webkitSpeechRecognition,mc=el('button','mic','Speak');pn.append(mc);mc.onclick=()=>{if(!SR){say('Voice input is not supported in this browser.');return}const r=new SR();r.lang='en-US';r.onresult=e=>{f.value=e.results[0][0].transcript;vo=1;send()};r.start()};
if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});
})();
