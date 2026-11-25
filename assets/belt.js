(()=>{const belt=document.querySelector('.belt');if(!belt)return;
const cards=[...belt.querySelectorAll('.card')],codes=[...belt.querySelectorAll('.code')],cv=belt.querySelector('canvas'),cx=cv.getContext('2d'),num=document.getElementById('num'),pct=document.getElementById('pct'),T=JSON.parse(belt.dataset.tokens),lt=document.getElementById('lt');
const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;let W,H,cw,ch,gap,L,dpr,off,vel=0,hover=0,drag=0,lx=0,lt0=0,shown=0,cur=-1,last=performance.now(),vis=true,lite=false,fn=0,fs=0,chk=false;
try{lite=localStorage.getItem('jw-lite')==='1'}catch(e){}if(navigator.deviceMemory&&navigator.deviceMemory<=2)lite=true;
const lab=()=>{if(lt)lt.textContent='Lite mode: '+(lite?'on':'off')};
const hash=(a,b,c)=>{let h=Math.imul(a,374761393)+Math.imul(b,668265263)+Math.imul(c+1,2147483647);h=Math.imul(h^(h>>>13),1274126177);return((h^(h>>>16))>>>0)/4294967295};
function size(){const r=belt.getBoundingClientRect();W=r.width;H=r.height;cw=cards[0].offsetWidth;ch=cards[0].offsetHeight;gap=parseFloat(getComputedStyle(belt).getPropertyValue('--gap'))*innerWidth/100;L=W/2;dpr=lite?1:Math.min(devicePixelRatio||1,1.5);cv.width=W*dpr;cv.height=H*dpr;if(off===undefined)off=W/2-.62*cw}
function setLite(v,save){lite=v;if(save){try{localStorage.setItem('jw-lite',v?'1':'0')}catch(e){}}lab();size()}
lab();size();addEventListener('resize',size);if(lt)lt.onclick=()=>setLite(!lite,true);
if('IntersectionObserver' in window)new IntersectionObserver(e=>{vis=e[0].isIntersecting},{threshold:0}).observe(belt);
belt.addEventListener('pointerenter',()=>hover=1);belt.addEventListener('pointerleave',()=>hover=0);
belt.addEventListener('pointerdown',e=>{drag=1;lx=e.clientX;lt0=e.timeStamp;belt.setPointerCapture(e.pointerId);belt.classList.add('drag')});
belt.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-lx;off+=dx;vel=dx/Math.max(8,e.timeStamp-lt0)*800+vel*.2;lx=e.clientX;lt0=e.timeStamp});
['pointerup','pointercancel'].forEach(n=>belt.addEventListener(n,()=>{drag=0;belt.classList.remove('drag')}));
belt.addEventListener('wheel',e=>{if(Math.abs(e.deltaX)>Math.abs(e.deltaY))vel-=e.deltaX*6},{passive:true});
const pos=(i,span,period)=>((off+i*span+span)%period+period)%period-span;
function hide(c,k){if(!c._h){c.style.visibility='hidden';k.style.visibility='hidden';c._h=1}}
function frame(t){requestAnimationFrame(frame);if(!vis||document.hidden){last=t;return}
if(lite&&t-last<32)return;
const raw=(t-last)/1e3,dt=Math.min(.05,raw);last=t;
if(!lite&&!chk){fn++;fs+=raw;if(fn===90){chk=true;if(fs/90>.03)setLite(true,false)}}
const S=lite?5:3,span=cw+gap,period=span*cards.length,auto=rm?0:-.075*innerWidth;
if(!drag){vel+=(auto*(1-.65*hover)-vel)*(1-Math.exp(-2.2*dt));off+=vel*dt}
cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);let crossing=-1;const r=innerWidth*.016+'px';
cards.forEach((c,i)=>{const x=pos(i,span,period),cut=Math.max(0,Math.min(cw,L-x)),k=codes[i];
if(x>W+20){hide(c,k);return}
c.style.transform=k.style.transform='translate3d('+x+'px,0,0)';
if(cut>=cw){c.style.visibility='hidden';c._h=1;k.style.visibility='visible';k.style.clipPath='none';return}
if(c._h){c.style.visibility='visible';c._h=0}
if(cut>0){c.style.clipPath='inset(0 0 0 '+cut+'px round 0 '+r+' '+r+' 0)';if(!lite)c.style.webkitMaskImage=c.style.maskImage='linear-gradient(90deg,transparent '+cut+'px,#000 '+(cut+26)+'px)';k.style.visibility='visible';k.style.clipPath='inset(0 '+(cw-cut)+'px 0 0)';crossing=i;
const w=Math.min(150,x+cw-L),g=cx.createLinearGradient(L,0,L+150,0);g.addColorStop(0,'rgba(255,96,40,.42)');g.addColorStop(1,'rgba(255,96,40,0)');cx.fillStyle=g;cx.fillRect(L,70,w,ch);
const R=.3*cw,rows=Math.ceil(ch/S);cx.fillStyle='#FF5A1F';
for(let gx=Math.floor(cut/S);gx<Math.ceil((cut+R)/S);gx++){const sx=x+gx*S,d=sx-L;if(d<0||d>R)continue;const p=Math.pow(1-d/R,1.7);
for(let ro=-5;ro<rows+5;ro++){const q=ro>=0&&ro<rows?p*.92:p*.12,h=hash(gx,ro,i);if(h<q){cx.globalAlpha=.4+.6*hash(ro,gx,i+9);cx.fillRect(sx,70+ro*S+(h-.5)*(d/R)*10,S-1,S-1)}}}cx.globalAlpha=1}
else{c.style.clipPath='none';c.style.webkitMaskImage=c.style.maskImage='none';k.style.visibility='hidden'}});
if(crossing>=0){const q=T[crossing],pr=Math.max(0,Math.min(1,(L-pos(crossing,span,period))/cw));if(cur!==crossing){cur=crossing;shown=0;pct.textContent=Math.round(q[2]/q[0]*100)+'% less'}shown+=(Math.round(q[2]*pr)-shown)*Math.min(1,dt*14);num.textContent='\u2212'+Math.round(shown).toLocaleString('en-US')}}
requestAnimationFrame(frame)})();
