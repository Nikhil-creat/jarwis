(()=>{
const ST=new Set('a an and are as at be by for from has have in is it of on or that the to with will you your we our their this these those they not but can may must should would about into over than then them such using use used work working experience years year team teams strong ability skills skill role job responsibilities requirements preferred plus including etc also more other well new who what when where which across within per any all each both need needs daily looking seeking join ensure support help make good great ideal candidate company position opportunity'.split(' '));
const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function kws(t){const c={};((t||'').toLowerCase().match(/[a-z][a-z0-9+#.\-]+/g)||[]).forEach(w=>{w=w.replace(/[.\-]+$/,'');if(w.length<2||ST.has(w))return;c[w]=(c[w]||0)+1});return Object.entries(c).sort((a,b)=>b[1]-a[1]||a[0].length-b[0].length).slice(0,25).map(x=>x[0])}
function has(l,w){return new RegExp('(^|[^a-z0-9+#])'+esc(w)+'($|[^a-z0-9+#])').test(l)}
function score(txt,k){const l=txt.toLowerCase(),hit=k.filter(w=>has(l,w));return{pct:k.length?Math.round(hit.length/k.length*100):0,hit,miss:k.filter(w=>!hit.includes(w))}}
function lines(s){return(s||'').split(/\n+/).map(x=>x.replace(/^[\s\-*\u2022\u00b7]+/,'').replace(/^\d+[.)]\s+/,'').trim()).filter(Boolean)}
function draft(v){const k=kws(v.rj);const sk=(v.rs||'').split(/[,;\n]/).map(x=>x.trim()).filter(Boolean);sk.sort((a,b)=>k.includes(b.toLowerCase())-k.includes(a.toLowerCase()));
return{summary:'',skills:[{g:'Skills',items:sk}],experience:v.rex?[{role:'Experience',org:'',dates:'',bullets:lines(v.rex).slice(0,6)}]:[],projects:v.rpr?[{name:'Projects',tech:'',bullets:lines(v.rpr).slice(0,8)}]:[],education:lines(v.red).map(l=>({degree:l,school:'',dates:'',detail:''})),extras:lines(v.rc).slice(0,6),gaps:[]}}
function plain(r,v){const o=[v.rn,[v.re,v.rp,v.rl,v.rli,v.rg,v.rw].filter(Boolean).join(' | ')];const add=(t,a)=>{if(a&&a.length)o.push('',t.toUpperCase(),...a)};
add('Summary',r.summary?[r.summary]:[]);add('Skills',(r.skills||[]).map(g=>(g.g?g.g+': ':'')+(g.items||[]).join(', ')));
add('Experience',(r.experience||[]).flatMap(e=>[[e.role,e.org,e.dates].filter(Boolean).join(' | '),...(e.bullets||[]).map(b=>'- '+b)]));
add('Projects',(r.projects||[]).flatMap(p=>[[p.name,p.tech].filter(Boolean).join(' | '),...(p.bullets||[]).map(b=>'- '+b)]));
add('Education',(r.education||[]).map(e=>[e.degree,e.school,e.dates,e.detail].filter(Boolean).join(' | ')));add('Certifications and achievements',(r.extras||[]).map(x=>'- '+x));return o.join('\n')}
if(typeof document==='undefined'){module.exports={kws,score,draft,plain,lines};return}
const $=id=>document.getElementById(id),T=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e};
const ids=['rn','re','rp','rl','rg','rli','rw','rt','rj','rco','rq','red','rs','rpr','rex','rc'],K='jw-resume';
const val=()=>{const v={};ids.forEach(i=>v[i]=($(i).value||'').trim());return v};
try{const s=JSON.parse(localStorage.getItem(K)||'{}');ids.forEach(i=>{if(s[i])$(i).value=s[i]})}catch(e){}
let tm,last='';ids.forEach(i=>$(i).addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(()=>{try{localStorage.setItem(K,JSON.stringify(val()))}catch(e){}},400)}));
const st=m=>{$('rst').textContent=m};
const need=[['rn','your name'],['re','your email'],['rp','your phone number'],['rt','the target job title'],['red','your education'],['rs','your skills']];
function check(v){for(const[i,n]of need)if(!v[i]){$(i).focus();st('Please add '+n+'.');return false}if(!v.rpr&&!v.rex){$('rpr').focus();st('Add at least one project or work experience.');return false}return true}
function render(r,v){const a=$('rv');a.textContent='';a.append(T('h2','',v.rn),T('p','rc',[v.re,v.rp,v.rl,v.rli,v.rg,v.rw].filter(Boolean).join(' | ')));
const sec=t=>a.append(T('h3','',t.toUpperCase())),row=(l,rt)=>{const d=T('div','rr');d.append(T('span','',l),T('span','',rt||''));a.append(d)},ul=b=>{const u=T('ul');(b||[]).filter(Boolean).forEach(x=>u.append(T('li','',x)));if(u.children.length)a.append(u)};
if(r.summary){sec('Summary');a.append(T('p','',r.summary))}
if((r.skills||[]).length){sec('Skills');r.skills.forEach(g=>a.append(T('p','',(g.g?g.g+': ':'')+(g.items||[]).join(', '))))}
if((r.experience||[]).length){sec('Experience');r.experience.forEach(e=>{row([e.role,e.org].filter(Boolean).join(', '),e.dates);ul(e.bullets)})}
if((r.projects||[]).length){sec('Projects');r.projects.forEach(p=>{row([p.name,p.tech].filter(Boolean).join(' | '),'');ul(p.bullets)})}
if((r.education||[]).length){sec('Education');r.education.forEach(e=>{row([e.degree,e.school].filter(Boolean).join(', '),e.dates);if(e.detail)a.append(T('p','',e.detail))})}
if((r.extras||[]).length){sec('Certifications and achievements');ul(r.extras)}}
function fit(){const a=$('rv');let s=10;a.style.fontSize=s+'pt';while(a.scrollHeight>1124&&s>8){s-=0.25;a.style.fontSize=s+'pt'}return a.scrollHeight<=1124}
function show(r,v,label){render(r,v);const one=fit();last=plain(r,v);const hasJd=!!v.rj,k=kws(hasJd?v.rj:v.rt),sc=score(last,k),words=last.split(/\s+/).length,ats=$('ats');ats.textContent='';
if(hasJd){ats.append(T('h3','','Keyword match: '+sc.pct+'% ('+sc.hit.length+' of '+k.length+' job keywords)'));const bar=T('div','bar'),i=T('i');i.style.width=sc.pct+'%';bar.append(i);ats.append(bar)}else ats.append(T('h3','','Paste the job description to get a keyword match score.'));
const ck=[[one,'Fits on one A4 page'],[true,'Single column, no tables, images or icons'],[true,'Standard section headings'],[!!(v.re&&v.rp),'Name, email and phone in the header'],[words>=250&&words<=700,'Length is '+words+' words (250 to 700 is ideal)']];if(hasJd)ck.push([sc.pct>=80,'At least 80% of job keywords covered']);
const u=T('ul','ck');ck.forEach(c=>u.append(T('li',c[0]?'ok':'no',(c[0]?'Yes: ':'Check: ')+c[1])));ats.append(u);
const gaps=[...new Set([...(r.gaps||[]),...(hasJd?sc.miss:[])])].slice(0,12);if(gaps.length)ats.append(T('p','','Job keywords not covered. Add them only if they are true for you: '+gaps.join(', ')));
$('fitnote').textContent=one?'':'This resume is slightly longer than one page. Trim a bullet or two before sending.';$('out').hidden=false;st(label+'. Review every line before you send it.');$('out').scrollIntoView({behavior:'smooth'})}
async function gen(){const v=val();if(!check(v))return;const b=$('rgen');b.disabled=true;st('Jarwis is tailoring your resume. This can take up to 30 seconds...');
const msg=JSON.stringify({target_role:v.rt.slice(0,120),job_description:v.rj.slice(0,1800),extra_request:v.rq.slice(0,300),education:v.red.slice(0,600),skills:v.rs.slice(0,600),projects:v.rpr.slice(0,2200),experience:v.rex.slice(0,1800),certifications_achievements:v.rc.slice(0,500)});
try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:'resume',message:msg})});const j=await r.json();if(!j.resume)throw 0;show(j.resume,v,'Tailored by AI ('+j.provider+' / '+j.model+')')}catch(_){show(draft(v),v,'The AI was unavailable, so this is a quick draft built from your details')}
b.disabled=false}
$('rgen').onclick=gen;$('rdraft').onclick=()=>{const v=val();if(check(v))show(draft(v),v,'Quick draft')};
$('rclr').onclick=()=>{ids.forEach(i=>{$(i).value=''});try{localStorage.removeItem(K)}catch(e){}$('out').hidden=true;st('Saved data cleared.')};
const dl=(n,t,m)=>{const u=URL.createObjectURL(new Blob([t],{type:m})),a=T('a');a.href=u;a.download=n;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),2000)};
$('rpdf').onclick=()=>window.print();$('rtxt').onclick=()=>dl('resume.txt',last,'text/plain');
$('rdoc').onclick=()=>dl('resume.doc','<html><head><meta charset="utf-8"><style>body{font-family:Arial;font-size:10pt}h2{text-align:center}h3{border-bottom:1px solid #000}</style></head><body>'+$('rv').innerHTML+'</body></html>','application/msword');
$('rcl').onclick=async()=>{const v=val();if(!check(v))return;st('Writing your cover letter...');
const msg=JSON.stringify({name:v.rn,company:v.rco.slice(0,80),target_role:v.rt.slice(0,120),job_description:v.rj.slice(0,1800),extra_request:v.rq.slice(0,300),education:v.red.slice(0,500),skills:v.rs.slice(0,500),projects:v.rpr.slice(0,1500),experience:v.rex.slice(0,1200),achievements:v.rc.slice(0,400)});
try{const x=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:'cover',message:msg})});const j=await x.json();if(!x.ok||!j.reply)throw 0;$('rcv').value=j.reply;$('cvw').hidden=false;st('Cover letter ready. Edit it, then copy or download.');$('cvw').scrollIntoView({behavior:'smooth'})}catch(_){st('The AI could not write the letter right now. Try again in a moment.')}};
$('rcvc').onclick=async()=>{try{await navigator.clipboard.writeText($('rcv').value);st('Letter copied.')}catch(e){st('Copy is blocked by your browser. Select the text and copy it.')}};
$('rcvd').onclick=()=>dl('cover-letter.txt',$('rcv').value,'text/plain');
$('rcp').onclick=async()=>{try{await navigator.clipboard.writeText(last);st('Copied.')}catch(e){st('Copy is blocked by your browser. Use Download .txt instead.')}};
})();
