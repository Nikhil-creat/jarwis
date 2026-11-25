(()=>{
const WID=[278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584];
const MAPC={'\u2018':"'",'\u2019':"'",'\u201c':'"','\u201d':'"','\u2013':'-','\u2014':'-','\u2026':'...','\u00a0':' ','\u20b9':'Rs ','\u00d7':'x','\u2192':'->','\u2713':'v','\u2714':'v','\u2022':'-','\u00b7':'-','\u200b':''};
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const strip=s=>String(s).replace(/\*\*|__|`/g,'');
function blocks(text){const out=[];String(text||'').replace(/\r/g,'').split('\n').forEach(l=>{const s=l.trim();if(!s){out.push({t:'br'});return}let m;
if(m=s.match(/^#{1,3}\s+(.*)/))out.push({t:'h',s:strip(m[1])});
else if(m=s.match(/^(\d+)[.)]\s+(.*)/))out.push({t:'li',n:m[1],s:strip(m[2])});
else if(m=s.match(/^[-*\u2022]\s+(.*)/))out.push({t:'li',n:null,s:strip(m[1])});
else out.push({t:'p',s:strip(s)})});return out}
function plain(text){return blocks(text).map(b=>b.t==='br'?'':b.t==='h'?b.s.toUpperCase():b.t==='li'?(b.n?b.n+'. ':'- ')+b.s:b.s).join('\n').replace(/\n{3,}/g,'\n\n').trim()}
function doc(title,text){let h='<h1>'+esc(title)+'</h1>',ul=false;const close=()=>{if(ul){h+='</ul>';ul=false}};
blocks(text).forEach(b=>{if(b.t==='br'){close();return}if(b.t==='h'){close();h+='<h2>'+esc(b.s)+'</h2>';return}if(b.t==='li'&&!b.n){if(!ul){h+='<ul>';ul=true}h+='<li>'+esc(b.s)+'</li>';return}close();h+='<p>'+esc((b.n?b.n+'. ':'')+b.s)+'</p>'});close();
return '<html><head><meta charset="utf-8"><title>'+esc(title)+'</title><style>body{font-family:Arial,sans-serif;font-size:11pt;line-height:1.4}h1{font-size:18pt}h2{font-size:13pt;margin:14pt 0 4pt}</style></head><body>'+h+'</body></html>'}
function md(title,text){return '# '+title+'\n\n'+String(text||'').trim()+'\n'}
function pdfSafe(s){let bad=false,o='';for(const ch of String(s)){let c=MAPC[ch]!==undefined?MAPC[ch]:ch;for(const x of c){const k=x.charCodeAt(0);if(k>=32&&k<=126)o+=x;else if(k>=160&&k<=255)o+=x;else if(k===9)o+='    ';else if(k>255){bad=true;o+='?'}}}return{s:o,bad}}
const wid=(s,sz,bold)=>{let w=0;for(const c of s){const k=c.charCodeAt(0);w+=k>=32&&k<=126?WID[k-32]:556}return w*sz/1000*(bold?1.08:1)};
const pesc=s=>s.replace(/[\\()]/g,'\\$&').replace(/[\u00a0-\u00ff]/g,c=>'\\'+('00'+c.charCodeAt(0).toString(8)).slice(-3));
function wrap(s,sz,bold,max){const lines=[];let cur='';s.split(/\s+/).filter(Boolean).forEach(w=>{while(wid(w,sz,bold)>max){let i=w.length-1;while(i>1&&wid(w.slice(0,i),sz,bold)>max)i--;if(cur){lines.push(cur);cur=''}lines.push(w.slice(0,i));w=w.slice(i)}const t=cur?cur+' '+w:w;if(wid(t,sz,bold)<=max)cur=t;else{lines.push(cur);cur=w}});if(cur)lines.push(cur);return lines}
function pdf(title,text){const all=pdfSafe(title+'\n'+text);if(all.bad)return{ok:false,reason:'non-latin'};
const T=pdfSafe(title).s,pages=[[]],L=56,R=56,TOP=842-56,BOT=60,W=595-L-R;let y=TOP,pg=0;
const need=h=>{if(y-h<BOT){pages.push([]);pg++;y=TOP}};
const put=(txt,x,sz,bold)=>{pages[pg].push({txt,x,y,sz,bold})};
wrap(T,18,true,W).forEach(l=>{need(24);y-=22;put(l,L,18,true)});y-=6;
blocks(text).forEach(b=>{if(b.t==='br'){y-=5;return}const s=pdfSafe(b.s).s;
if(b.t==='h'){y-=8;wrap(s,12.5,true,W).forEach(l=>{need(18);y-=17;put(l,L,12.5,true)});y-=2;return}
if(b.t==='li'){const ind=18,lab=b.n?b.n+'.':'\u0095';wrap(s,10.5,false,W-ind).forEach((l,i)=>{need(15);y-=14.5;if(i===0)put(lab,L+2,10.5,false);put(l,L+ind,10.5,false)});return}
wrap(s,10.5,false,W).forEach(l=>{need(15);y-=14.5;put(l,L,10.5,false)})});
const objs=[null,'<< /Type /Catalog /Pages 2 0 R >>',null,'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>','<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>'];
const kids=[];pages.forEach((p,i)=>{let c='';p.forEach(o=>{c+='BT /F'+(o.bold?2:1)+' '+o.sz+' Tf 1 0 0 1 '+o.x.toFixed(2)+' '+o.y.toFixed(2)+' Tm ('+pesc(o.txt)+') Tj ET\n'});
c+='BT /F1 8 Tf 1 0 0 1 '+L+' 32 Tm (Created with Jarwis) Tj ET\nBT /F1 8 Tf 1 0 0 1 '+(595-R-60)+' 32 Tm (Page '+(i+1)+' of '+pages.length+') Tj ET\n';
const pid=5+i*2;kids.push(pid+' 0 R');objs[pid]='<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents '+(pid+1)+' 0 R >>';objs[pid+1]='<< /Length '+c.length+' >>\nstream\n'+c+'endstream'});
objs[2]='<< /Type /Pages /Kids ['+kids.join(' ')+'] /Count '+pages.length+' >>';const info=objs.length;objs[info]='<< /Title ('+pesc(T)+') /Producer (Jarwis) >>';
let out='%PDF-1.4\n';const off=[0];for(let i=1;i<objs.length;i++){off[i]=out.length;out+=i+' 0 obj\n'+objs[i]+'\nendobj\n'}
const xr=out.length;out+='xref\n0 '+objs.length+'\n0000000000 65535 f \n';for(let i=1;i<objs.length;i++)out+=('0000000000'+off[i]).slice(-10)+' 00000 n \n';
out+='trailer\n<< /Size '+objs.length+' /Root 1 0 R /Info '+info+' 0 R >>\nstartxref\n'+xr+'\n%%EOF';
return{ok:true,pages:pages.length,data:out,blob:typeof Blob!=='undefined'?new Blob([out],{type:'application/pdf'}):null}}
function cleanSvg(s){s=String(s||'');const a=s.indexOf('<svg'),b=s.lastIndexOf('</svg>');if(a<0||b<0)return'';s=s.slice(a,b+6);
if(/<!DOCTYPE|<!ENTITY|<\?xml-stylesheet/i.test(s))return'';
s=s.replace(/<script[\s\S]*?<\/script>/gi,'').replace(/<(foreignObject|iframe|object|embed|image|audio|video|animate|set)[\s\S]*?(<\/\1>|\/>)/gi,'').replace(/\son\w+\s*=\s*("[^"]*"|'[^']*')/gi,'').replace(/javascript:/gi,'').replace(/(xlink:)?href\s*=\s*("(?!#)[^"]*"|'(?!#)[^']*')/gi,'').replace(/@import[^;]*;?/gi,'').replace(/url\(\s*['"]?\s*(https?:|data:|\/\/)[^)]*\)/gi,'none');
if(!/xmlns=/.test(s.slice(0,200)))s=s.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"');return s.length>30000?'':s}
const api={blocks,plain,doc,md,pdf,pdfSafe,cleanSvg,WID};
if(typeof window==='undefined'){module.exports=api;return}
const dl=(name,data,type)=>{const u=URL.createObjectURL(data instanceof Blob?data:new Blob([data],{type}));const a=document.createElement('a');a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),3000)};
const copy=async t=>{try{await navigator.clipboard.writeText(t);return true}catch(e){return false}};
const printDoc=(title,text)=>{let r=document.getElementById('jw-print');if(!r){r=document.createElement('div');r.id='jw-print';document.body.append(r)}r.innerHTML=doc(title,text).replace(/^[\s\S]*<body>|<\/body>[\s\S]*$/g,'');document.body.classList.add('jw-printing');const done=()=>{document.body.classList.remove('jw-printing');removeEventListener('afterprint',done)};addEventListener('afterprint',done);window.print()};
const slug=t=>(t||'jarwis').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40)||'jarwis';
Object.assign(api,{dl,copy,printDoc,slug,svgPng:(svg,w,h)=>new Promise((ok,no)=>{const i=new Image(),u=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'}));i.onload=()=>{const c=document.createElement('canvas');c.width=w||1200;c.height=h||900;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.drawImage(i,0,0,c.width,c.height);URL.revokeObjectURL(u);c.toBlob(b=>b?ok(b):no(new Error('png')),'image/png')};i.onerror=()=>{URL.revokeObjectURL(u);no(new Error('svg'))};i.src=u})});
window.JWExport=api})();
