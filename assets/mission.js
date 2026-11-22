(()=>{
const $=id=>document.getElementById(id),T=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e};
const AS=JSON.parse($('aj').textContent),N=AS.map(a=>a.n),est=s=>Math.ceil(String(s).length/4),HK='jw-missions2';
let ac=null,busy=false,final='',steps=[],spent=0,ui=[];
const st=m=>{$('mst').textContent=m},use=()=>{$('mu').textContent='Used about '+spent.toLocaleString()+' of '+(+$('mb').value).toLocaleString()+' tokens (estimated)'};
const post=(b,sig)=>fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b),signal:sig}).then(async r=>{const j=await r.json();if(!r.ok)throw new Error(j.reply||'error');return j});
const load=()=>{try{return JSON.parse(localStorage.getItem(HK)||'[]')}catch(e){return[]}},save=h=>{try{localStorage.setItem(HK,JSON.stringify(h))}catch(e){}};
function paint(box,text){box.textContent='';let ul=null;String(text).split('\n').forEach(l=>{l=l.trim();if(!l){ul=null;return}if(/^#+\s/.test(l)){ul=null;box.append(T('h3','',l.replace(/^#+\s*/,'').replace(/\*\*/g,'')));return}const m=l.match(/^(?:[-*]|\d+[.)])\s+(.*)/);if(m){if(!ul){ul=T('ul');box.append(ul)}ul.append(T('li','',m[1].replace(/\*\*/g,'')));return}ul=null;box.append(T('p','',l.replace(/\*\*/g,'')))})}
function card(k,s){const d=T('article','sc'),h=T('h3','',(k+1)+'. '+s.a),b=T('span','bd','Waiting'),o=T('div','so');h.append(b);o.hidden=true;d.append(h,T('p','',s.t),o);$('mt').append(d);return{b,o}}
function setU(u,label,cls){u.b.textContent=label;u.b.className='bd '+cls}
async function work(s,k,goal,sig){const u=ui[k],a=AS.find(x=>x.n===s.a)||{n:s.a,c:'',t:''};setU(u,'Working','run');
try{const j=await post({message:'Overall goal: '+goal+'\nYour task: '+s.t+'\nGive a concrete, usable result in under 180 words.',assistant:{name:a.n,cluster:a.c,tools:a.t},tier:'fast'},sig);setU(u,'Done','ok');u.o.hidden=false;paint(u.o,j.reply);spent+=est(j.reply)+est(goal)+est(s.t)+300;use();return{a:s.a,t:s.t,o:j.reply}}
catch(e){setU(u,sig.aborted?'Stopped':'Failed','no');return null}}
async function start(){if(busy)return;const goal=$('mg').value.trim();if(goal.length<8){$('mg').focus();st('Describe your goal in a sentence or more.');return}
busy=true;ac=new AbortController();const sig=ac.signal;$('mgo').disabled=true;$('mab').hidden=false;$('mt').textContent='';$('mfw').hidden=true;$('mex').hidden=true;$('mok').hidden=false;spent=est(goal)+1500;final='';ui=[];use();
try{st('Commander-00 is choosing specialists from the 99...');
const pl=await post({mode:'mission_plan',message:JSON.stringify({goal:goal.slice(0,600),names:N})},sig);let sts=pl.steps;
const maxN=Math.max(1,Math.floor((+$('mb').value-4000)/1800));if(sts.length>maxN){sts=sts.slice(0,maxN);st('Your token budget limits this mission to '+maxN+' specialists.')}
sts.forEach((s,k)=>ui.push(card(k,s)));$('mtw').hidden=false;st('Specialists are working in parallel...');
const done=(await Promise.all(sts.map((s,k)=>work(s,k,goal,sig)))).filter(Boolean);if(!done.length)throw new Error('no specialist finished');
st('Commander-00 is combining the results...');
const fj=await post({mode:'mission_final',message:JSON.stringify({goal:goal.slice(0,600),results:done.map(r=>({assistant:r.a,task:r.t,output:r.o.slice(0,900)}))})},sig);
final=fj.reply;steps=done;spent+=est(final)+est(JSON.stringify(done));use();paint($('mf'),final);$('mfw').hidden=false;$('mfw').scrollIntoView({behavior:'smooth'});st('Mission complete. Review the deliverable, then approve it to save and export.')}
catch(e){st(sig.aborted?'Mission stopped.':'The mission could not finish ('+(e.message||'error')+'). Check the Status page and try again.')}
busy=false;$('mgo').disabled=false;$('mab').hidden=true}
function md(){return '# Mission: '+$('mg').value.trim()+'\n\n'+final+'\n\n## Specialist notes\n'+steps.map(s=>'\n### '+s.a+'\nTask: '+s.t+'\n\n'+s.o).join('\n')}
function rH(){const h=$('mh');h.textContent='';const L=load().slice().reverse();if(!L.length){h.append(T('li','','No saved missions yet.'));return}L.slice(0,8).forEach(m=>{const li=T('li'),b=T('button','chip',m.g.slice(0,70)+' ('+m.w+')');b.type='button';b.onclick=()=>openH(m);li.append(b);h.append(li)})}
function openH(m){$('mt').textContent='';ui=[];steps=m.s.map(x=>({a:x.a,t:x.t,o:x.o}));$('mg').value=m.g;steps.forEach((s,k)=>{const u=card(k,s);ui.push(u);setU(u,'Done','ok');u.o.hidden=false;paint(u.o,s.o)});final=m.f;paint($('mf'),final);$('mtw').hidden=false;$('mfw').hidden=false;$('mok').hidden=true;$('mex').hidden=false;st('Opened a saved mission.')}
$('mgo').onclick=start;$('mab').onclick=()=>{if(ac)ac.abort()};
$('mb').oninput=()=>{$('mbo').textContent=(+$('mb').value).toLocaleString()};
$('mxs').addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-g]');if(b){$('mg').value=b.dataset.g;$('mg').focus()}});
$('mok').onclick=()=>{if(!final)return;const H=load();H.push({g:$('mg').value.trim(),w:new Date().toLocaleDateString(),f:final,s:steps});save(H.slice(-15));$('mok').hidden=true;$('mex').hidden=false;st('Approved and saved to your history. You can now copy or download it.');rH()};
$('mrj').onclick=()=>{final='';$('mfw').hidden=true;st('Discarded. Change the goal and run again.')};
$('mcp').onclick=async()=>{try{await navigator.clipboard.writeText(md());st('Copied.')}catch(e){st('Copy is blocked by your browser. Use Download instead.')}};
$('mdl').onclick=()=>{const u=URL.createObjectURL(new Blob([md()],{type:'text/markdown'})),a=T('a');a.href=u;a.download='jarwis-mission.md';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),2000)};
rH();
})();
