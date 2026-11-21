(()=>{
const $=id=>document.getElementById(id),T=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e};
let Q=[],i=0;const st=m=>{$('ist').textContent=m};
const post=b=>fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(async r=>{const j=await r.json();if(!r.ok)throw new Error(j.reply||'error');return j});
function showQ(){const q=Q[i];$('iq').hidden=false;$('iqh').textContent='Question '+(i+1)+' of '+Q.length;$('iqt').textContent=q.q;$('iqk').textContent=q.type;$('ian').value='';$('ifo').hidden=true;$('inx').textContent=i>=Q.length-1?'Finish':'Next question';$('iq').scrollIntoView({behavior:'smooth'})}
$('igo').onclick=async()=>{const role=$('iro').value.trim();if(!role){$('iro').focus();st('Please add the job title.');return}
$('igo').disabled=true;st('Jarwis is preparing your questions...');
try{const j=await post({mode:'iq',message:JSON.stringify({role:role.slice(0,120),level:$('ilv').value,job_description:$('ijd').value.trim().slice(0,1800)})});if(!(j.questions&&j.questions.length))throw 0;Q=j.questions;i=0;st('Say your answer out loud first, then type the main points for feedback.');showQ()}
catch(e){st('Could not prepare questions right now. Check the Status page, then try again.')}
$('igo').disabled=false};
$('ifb').onclick=async()=>{const a=$('ian').value.trim();if(a.length<20){st('Write at least a couple of sentences first.');return}
$('ifb').disabled=true;st('Reviewing your answer...');
try{const j=await post({mode:'ifb',message:JSON.stringify({role:$('iro').value.trim().slice(0,120),question:Q[i].q,answer:a.slice(0,1800)})}),f=j.feedback,o=$('ifo');if(!f)throw 0;o.textContent='';
o.append(T('h3','','Score: '+f.score+' / 10'),T('p','','Strengths: '+(f.strengths.join('; ')||'none noted')),T('p','','Improve: '+(f.improve.join('; ')||'none noted')),T('p','','A stronger answer: '+f.better));o.hidden=false;st('Feedback ready. Rewrite your answer and try again, or move on.')}
catch(e){st('Could not review the answer right now. Try again in a moment.')}
$('ifb').disabled=false};
$('inx').onclick=()=>{if(i>=Q.length-1){$('iq').hidden=true;st('Session complete. Change the job or start again any time.');return}i++;showQ()};
})();
