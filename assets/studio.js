(()=>{
const $=id=>document.getElementById(id),W=typeof window!=='undefined'?window:{},X=W.JWExport;
const post=b=>fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(async r=>{const j=await r.json();if(!r.ok)throw new Error(j.reply||'error');return j});
fetch('/api/chat').catch(()=>{});
const SK='jw-studio-doc',say=(id,m)=>{$(id).textContent=m};
let undo=[],svg='',svgUrl='';
// document
try{const d=JSON.parse(localStorage.getItem(SK)||'null');if(d){$('sd').value=d.text||'';$('stl').value=d.title||''}}catch(e){}
const save=()=>{try{localStorage.setItem(SK,JSON.stringify({title:$('stl').value,text:$('sd').value}))}catch(e){}};$('sd').addEventListener('input',save);$('stl').addEventListener('input',save);
const T=()=>$('stl').value.trim()||'Document',D=()=>$('sd').value;
$('scp').onclick=async()=>say('sst',await X.copy(X.plain(D()))?'Copied as clean text.':'Copy is blocked by your browser.');
$('scm').onclick=async()=>say('sst',await X.copy(X.md(T(),D()))?'Copied as Markdown.':'Copy is blocked by your browser.');
$('smd').onclick=()=>X.dl(X.slug(T())+'.md',X.md(T(),D()),'text/markdown');$('stx').onclick=()=>X.dl(X.slug(T())+'.txt',X.plain(D()),'text/plain');
$('sdc').onclick=()=>X.dl(X.slug(T())+'.doc',X.doc(T(),D()),'application/msword');
$('spf').onclick=()=>{if(!D().trim()){say('sst','Write or paste something first.');return}const r=X.pdf(T(),D());if(r.ok){X.dl(X.slug(T())+'.pdf',r.blob);say('sst','PDF downloaded ('+r.pages+' page'+(r.pages>1?'s':'')+').')}else{say('sst','This text has characters a simple PDF cannot hold, so the print view opens. Choose Save as PDF.');X.printDoc(T(),D())}};
$('spr').onclick=()=>X.printDoc(T(),D());
async function revise(ins){if(D().trim().length<5){say('sst','Write or paste something first.');return}ins=(ins||'').trim();if(ins.length<3){$('sri').focus();return}
$('srb').disabled=true;say('sst','Jarwis is revising...');try{const j=await post({mode:'mission_revise',message:JSON.stringify({instruction:ins,text:D().slice(0,7000)})});undo.push(D());$('sd').value=j.reply;save();say('sst','Revised. Use Undo to go back.')}catch(e){say('sst','Could not revise right now. Try again in a moment.')}$('srb').disabled=false}
$('srb').onclick=()=>revise($('sri').value);$('sq').addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-i]');if(b)revise(b.dataset.i)});
$('sun').onclick=()=>{if(!undo.length){say('sst','Nothing to undo.');return}$('sd').value=undo.pop();save();say('sst','Undone.')};
// visuals
function showSvg(s){svg=X.cleanSvg(s);if(!svg){say('vst','The drawing could not be displayed. Try a simpler description.');return false}if(svgUrl)URL.revokeObjectURL(svgUrl);svgUrl=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'}));$('vi').src=svgUrl;$('vw').hidden=false;return true}
async function draw(prompt,cur){if(prompt.trim().length<4){$('vp').focus();say('vst','Describe what to draw.');return}
$('vg').disabled=true;$('veb').disabled=true;say('vst','Jarwis is drawing. This can take up to 30 seconds...');
try{const j=await post({mode:'svg',message:JSON.stringify({prompt:prompt.slice(0,800),svg:cur||''})});if(showSvg(j.svg))say('vst','Done. Describe a change below to edit it, or download it.')}catch(e){say('vst',String(e.message||'').slice(0,120)||'Could not draw that right now.')}
$('vg').disabled=false;$('veb').disabled=false}
$('vg').onclick=()=>draw($('vp').value);$('veb').onclick=()=>{const i=$('ve').value.trim();if(!svg){say('vst','Draw something first.');return}if(i.length<3){$('ve').focus();return}draw('Edit instruction: '+i,svg)};
$('vuse').onclick=()=>{const t=D().trim();if(!t){say('vst','Write or paste a document above first.');return}$('vp').value='A clear diagram or infographic that summarises: '+X.plain(t).slice(0,500)};
$('vsv').onclick=()=>{if(svg)X.dl('jarwis-visual.svg',svg,'image/svg+xml')};
$('vpn').onclick=async()=>{if(!svg)return;try{X.dl('jarwis-visual.png',await X.svgPng(svg,1600,1200))}catch(e){say('vst','Could not make a PNG here. Download the SVG instead.')}};
// AI art (Pollinations, free third-party)
let wait=0;
$('ag').onclick=()=>{const p=$('ap').value.trim();if(p.length<4){$('ap').focus();say('ast','Describe the image first.');return}
const sz={sq:[1024,1024],ls:[1280,720],pt:[768,1152]}[$('az').value]||[1024,1024],url='https://image.pollinations.ai/prompt/'+encodeURIComponent(p.slice(0,400)+', '+$('as').value)+'?width='+sz[0]+'&height='+sz[1]+'&nologo=true&model=flux&seed='+Math.floor(Math.random()*1e6);
const im=$('ai');im.onload=()=>{say('ast','Done. Tap Open image to view it full size, then press and hold to save.');$('aw').hidden=false;$('adl').href=url};im.onerror=()=>say('ast','The free image service is busy or has changed. Wait 15 seconds and try again.');
say('ast','Generating... the free service can take 10 to 30 seconds.');$('ag').disabled=true;wait=15;const iv=setInterval(()=>{wait--;$('ag').textContent=wait>0?'Wait '+wait+'s':'Generate image';if(wait<=0){clearInterval(iv);$('ag').disabled=false}},1000);im.src=url};
// photo editor (all in the browser)
let pimg=null,rot=0,flip=false;
function pdraw(){if(!pimg)return;const w=Math.max(16,Math.min(+$('pw').value||pimg.width,4000)),h=Math.round(pimg.height*w/pimg.width),c=$('pc'),r=rot%2;c.width=r?h:w;c.height=r?w:h;const x=c.getContext('2d');x.save();
try{x.filter=($('pg').checked?'grayscale(1) ':'')+'brightness('+$('pb').value+'%) contrast('+$('pk').value+'%)'}catch(e){}
x.translate(c.width/2,c.height/2);x.rotate(rot*Math.PI/2);if(flip)x.scale(-1,1);x.drawImage(pimg,-w/2,-h/2,w,h);x.restore();$('pcw').hidden=false;say('pst',c.width+' x '+c.height+' px')}
$('pf').onchange=e=>{const f=e.target.files&&e.target.files[0];if(!f)return;if(f.size>15e6){say('pst','Choose an image under 15 MB.');return}const u=URL.createObjectURL(f),i=new Image();i.onload=()=>{pimg=i;rot=0;flip=false;$('pw').value=Math.min(i.width,1600);pdraw();URL.revokeObjectURL(u)};i.onerror=()=>say('pst','That file could not be read as an image.');i.src=u};
['pw','pb','pk','pg'].forEach(i=>$(i).addEventListener('input',pdraw));$('pr').onclick=()=>{rot=(rot+1)%4;pdraw()};$('pfl').onclick=()=>{flip=!flip;pdraw()};
$('pd').onclick=()=>{if(!pimg){say('pst','Choose a photo first.');return}const f=$('pfm').value,m={png:'image/png',jpg:'image/jpeg',webp:'image/webp'}[f];$('pc').toBlob(b=>{if(!b){say('pst','Could not export that format here.');return}X.dl('edited-photo.'+f,b);say('pst','Saved '+Math.round(b.size/1024)+' KB.')},m,(+$('pq').value)/100)};
})();
