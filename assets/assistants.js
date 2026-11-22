(()=>{const g=document.getElementById('ag');if(!g)return;
const q=document.getElementById('q'),chips=[...document.querySelectorAll('[data-f]')],el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e};let f='';
function flt(){const v=q.value.toLowerCase();g.querySelectorAll('.ac').forEach(c=>{c.hidden=!((!f||c.dataset.c===f)&&(!v||c.textContent.toLowerCase().includes(v)||(c.dataset.t||'').toLowerCase().includes(v)))})}
q.addEventListener('input',flt);chips.forEach(b=>b.onclick=()=>{f=b.dataset.f;chips.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));flt()});
const K='jarwis-custom';let cu=[];try{cu=JSON.parse(localStorage.getItem(K)||'[]')}catch(e){}
const mk=a=>{const b=el('button','ac');b.type='button';b.dataset.n=a.n;b.dataset.c='Custom';b.dataset.t=a.t;b.append(el('span','','Custom'),el('strong','',a.n),el('small','','Forged by you'));g.append(b);return b};cu.forEach(mk);
document.getElementById('fg').onclick=()=>{const n=document.getElementById('fn'),r=document.getElementById('fr');const a={n:n.value.trim().slice(0,40),t:r.value.trim().slice(0,300)};if(!a.n||!a.t)return;cu.push(a);try{localStorage.setItem(K,JSON.stringify(cu))}catch(e){}n.value=r.value='';const b=mk(a);b.scrollIntoView({block:'center'});b.click()};
const sh=el('div','am');sh.hidden=true;const hd=el('div','ah'),ti=el('strong'),tl=el('a','tla'),cc=el('button','','Clear'),cl=el('button','','Close');cc.type=cl.type='button';hd.append(ti,tl,cc,cl);
const lg=el('div','cl');lg.setAttribute('aria-live','polite');const ip=el('input');ip.placeholder='Message this assistant...';ip.setAttribute('aria-label','Message');
const qa=el('div','sg');['Make a step-by-step plan','Create a checklist','Review what I paste','Explain it simply'].forEach(x=>{const b=el('button','',x);b.type='button';b.onclick=()=>{ip.value=x+': ';ip.focus()};qa.append(b)});
sh.append(hd,lg,qa,ip);document.body.append(sh);
const TOOL={'Resume & Career Coach':['/resume/','Open Resume Builder'],'Interview Prep Coach':['/interview/','Open Interview Practice'],'Commander-00':['/command-center/','Start a mission']};
let cur=null,H=[],log=[];const SK=n=>'jw-a-'+n,saveL=()=>{try{localStorage.setItem(SK(cur.name),JSON.stringify(log.slice(-30)))}catch(e){}};
const say=(t,me,meta,keep)=>{const p=el('p',me?'me':'',t);if(meta)p.append(el('small','',meta));if(!me&&keep){const b=el('button','cpb','Copy');b.type='button';b.onclick=async()=>{try{await navigator.clipboard.writeText(t);b.textContent='Copied'}catch(e){b.textContent='Blocked'}};p.append(b)}lg.append(p);lg.scrollTop=lg.scrollHeight;if(keep){log.push({t,me:me?1:0,meta:meta||''});saveL()}return p};
g.addEventListener('click',e=>{const c=e.target.closest('.ac');if(!c)return;cur={name:c.dataset.n,cluster:c.dataset.c,tools:c.dataset.t||''};H=[];log=[];lg.textContent='';ti.textContent=cur.name;const tool=TOOL[cur.name];tl.hidden=!tool;if(tool){tl.href=tool[0];tl.textContent=tool[1]}
let old=[];try{old=JSON.parse(localStorage.getItem(SK(cur.name))||'[]')}catch(x){}
if(old.length){old.forEach(x=>say(x.t,x.me,x.meta,1));H=old.map(x=>({role:x.me?'user':'assistant',content:x.t}))}else say('Hi, I am the '+cur.name+'. What do you need?');
sh.hidden=false;ip.focus()});
cl.onclick=()=>sh.hidden=true;cc.onclick=()=>{if(!cur)return;try{localStorage.removeItem(SK(cur.name))}catch(e){}H=[];log=[];lg.textContent='';say('Cleared. What do you need?')};
const post=b=>fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(async r=>{const j=await r.json();if(!r.ok)throw new Error(j.reply||'error');return j});
ip.addEventListener('keydown',async e=>{if(e.key!=='Enter'||!ip.value.trim()||!cur)return;const m=ip.value.trim();ip.value='';say(m,1,'',1);const w=say('Thinking...');w.className='typing';
try{const j=await post({message:m,assistant:cur,history:H.slice(-8)}),r=String(j.reply||'No reply.');H.push({role:'user',content:m},{role:'assistant',content:r});w.remove();say(r,0,j.model?j.provider+' / '+j.model:'',1)}
catch(err){w.remove();say(String(err.message||'').slice(0,120)||'I cannot reach the AI right now. Check the Status page.')}});
document.getElementById('rtb').onclick=async()=>{const t=document.getElementById('rt').value.trim(),o=document.getElementById('rto');if(!t)return;o.textContent='Thinking...';try{const j=await post({message:t,mode:'route',names:[...g.querySelectorAll('.ac')].map(c=>c.dataset.n)});const a=JSON.parse(String(j.reply).replace(/```json|```/g,'').trim());g.querySelectorAll('.ac').forEach(c=>c.classList.toggle('hit',a.includes(c.dataset.n)));o.textContent='Best matches highlighted: '+a.join(', ');const h=g.querySelector('.hit');if(h)h.scrollIntoView({block:'center'})}catch(_){o.textContent='Routing needs the AI backend. Browse the list instead.'}};
})();
