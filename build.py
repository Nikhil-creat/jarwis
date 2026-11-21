import os,json,html,datetime
D=os.environ.get("DOMAIN","https://jarwis.ai").rstrip("/")
NAME="Jarwis";TODAY=datetime.date.today().isoformat()
FONTS="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap"
LOGO='<svg width="19" height="23" viewBox="0 0 19 23" aria-hidden="true"><path d="M9.5 1C6 7 1.5 10 1.5 14.5a8 8 0 0 0 16 0C17.5 10 13 7 9.5 1Z" fill="currentColor"/><path d="M5.5 15a4 4 0 0 0 3.5 3.6" stroke="#EEF0F2" stroke-width="1.7" stroke-linecap="round" fill="none"/></svg>'
NAV=[("/command-center/","Command center"),("/assistants/","Assistants"),("/architecture/","Architecture"),("/status/","Status"),("/security/","Security")]
CL=[("Software, Cloud & Security",18,"System Architect, Full-Stack Builder, DevOps & CI/CD Engineer, AppSec Auditor, Root-Cause Debugger"),
("AI, Data & Research",14,"Deep Researcher, Citation Verifier, RAG Curator, CNN Vision Specialist, LLM Eval Judge"),
("Productivity & Daily Ops",16,"Time-Blocker, Triage Coach, Study Tutor, Budget Watchdog, Reminder Keeper"),
("Creative & Communication",13,"UX Copywriter, Slide Deck Builder, Diagram Artist, Meeting Action Extractor, Translator"),
("Business, Finance & Risk",14,"PRD Writer, Pricing Strategist, Cashflow Modeler, Policy Analyzer, Compliance Auditor"),
("User-Forged Assistants",24,"Created from plain language or YAML blueprints, with their own tools, memory and triggers")]
def ld(path,title,desc,crumbs):
    org={"@type":["ProfessionalService","Organization"],"@id":D+"/#org","name":NAME,"url":D+"/","logo":D+"/favicon.svg","image":D+"/og.png","description":"Software studio building a multi-agent AI platform: one commander coordinating 99+ specialised assistants.","areaServed":"Worldwide","priceRange":"$$"}
    bl={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":D+u} for i,(n,u) in enumerate(crumbs)]}
    g=[org,{"@type":"WebSite","@id":D+"/#site","url":D+"/","name":NAME,"publisher":{"@id":D+"/#org"}},{"@type":"WebPage","url":D+path,"name":title,"description":desc,"isPartOf":{"@id":D+"/#site"}},bl]
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":g})+'</script>'
def head(path,title,desc,crumbs,extra=""):
    t=html.escape(title);d=html.escape(desc)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t}</title><meta name="description" content="{d}"><link rel="canonical" href="{D}{path}"><meta name="theme-color" content="#EEF0F2">
<meta name="jarwis-api" content="/api/chat"><link rel="manifest" href="/manifest.webmanifest"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="sitemap" href="/sitemap.xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{D}{path}"><meta property="og:image" content="{D}/og.png"><meta property="og:image:alt" content="Jarwis: a commander AI coordinating 99+ assistants"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{D}/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="/assets/site.css">
{ld(path,title,desc,crumbs)}{extra}</head>'''
def navbar(path):
    ls="".join(f'<a href="{u}"{" aria-current=page" if path==u else ""}>{n}</a>' for u,n in NAV)
    return f'<a class="skip" href="#main">Skip to content</a><header class="nav"><a class="logo" href="/" aria-label="{NAME} home">{LOGO}Jarwis</a><nav aria-label="Main">{ls}</nav><button class="mb" type="button" aria-label="Menu" aria-expanded="false">Menu</button><a class="btn" href="/assistants/">Meet the assistants</a></header>'
def foot():
    return f'''<footer><div><strong style="color:#fff">{NAME}</strong><p style="margin-top:8px;max-width:38ch">One commander, 99+ specialised assistants, and a sandbox that checks the work before you see it.</p></div><div><h2>Explore</h2><a href="/">Home</a><a href="/assistants/">Assistants</a><a href="/architecture/">Architecture</a><a href="/security/">Security</a><a href="/roadmap/">Roadmap</a><a href="/builder/">Builder</a></div><div><h2>Site</h2><a href="/sitemap.xml">Sitemap</a><a href="/llms.txt">llms.txt</a><a href="/robots.txt">robots.txt</a><p style="margin-top:10px">&copy; {datetime.date.today().year} {NAME}</p></div></footer>'''
def crumbs(cs):
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>'+"".join(f'<li><a href="{u}">{n}</a></li>' if i<len(cs)-1 else f'<li aria-current="page">{n}</li>' for i,(n,u) in enumerate(cs))+'</ol></nav>'
def w(path,s):
    fp=("."+path+"index.html") if path.endswith("/") else "."+path
    os.makedirs(os.path.dirname(fp) or ".",exist_ok=True);open(fp,"w",encoding="utf-8").write(s)
# ---- home cards
C=[("Commander-00","Mission control",[("100","agents"),("1","commander")],"One commander for every mission.","Plans the work, hands it to the right assistants, and reports back in plain language.",70411,6140,"jarwis.ai/commander"),
("Registry","Assistants",[("99+","assistants"),("6","clusters")],"A hundred roles, one registry.","Search, clone or forge an assistant from plain language.",41208,4960,"jarwis.ai/assistants"),
("Mission","Run report",[("34","tasks"),("0","blocked")],"Missions that finish and explain themselves.","Every plan, task and approval is logged and replayable.",98432,6300,"jarwis.ai/missions"),
("Sandbox","Verified builds",[("100%","isolated"),("3","retries max")],"Code runs in a sandbox first.","Tests and linters pass before anything reaches you.",55870,8215,"jarwis.ai/sandbox"),
("Router","Models",[("5","providers"),("1","gateway")],"The right model for each task.","Fast models for routing, frontier models for architecture, local fallback offline.",63904,5512,"jarwis.ai/router"),
("Memory","Context",[("3","tiers"),("0","shared secrets")],"Remembers decisions, not secrets.","Working, episodic and semantic memory with per-assistant visibility.",47316,7602,"jarwis.ai/memory")]
def card(i,c):
    n,m,st,h,p,o,dd,u=c;s="".join(f'<div>{a}<small>{b}</small></div>' for a,b in st)
    return f'<article class="card c{i+1}" aria-hidden="true"><div class="k"><div class="n"><strong>{n}</strong><span>{m}</span></div><div class="st">{s}</div><h3>{h}</h3><p>{p}</p></div></article>'
def code(i,c):
    n,m,st,h,p,o,dd,u=c
    return f'<div class="code" aria-hidden="true"><pre>&lt;h1&gt;{n}&lt;/h1&gt;\n&lt;p&gt;{h}\n{p}&lt;/p&gt;\n&lt;ul&gt;\n'+"".join(f'  &lt;li&gt;{a} {b}&lt;/li&gt;\n' for a,b in st)+f'&lt;/ul&gt;\n&lt;a href="/assistants/"&gt;Explore&lt;/a&gt;</pre><pre class="m">&lt;!-- distilled: {dd:,} tokens --&gt;\n&lt;!-- original: {o:,} tokens --&gt;\n&lt;!-- {u} --&gt;</pre></div>'
tok=json.dumps([[c[5],c[6],c[5]-c[6]] for c in C])
ht="Jarwis | One commander, 99+ AI assistants";hd="Jarwis is a multi-agent platform: one commander plans missions and 99+ specialised assistants build, research and automate, with human approval on every risky step."
home=head("/",ht,hd,[("Home","/")])+f'''<body class="home">{navbar("/")}<main id="main"><div class="stage"><section class="hero"><div><p class="eyebrow">Multi-agent platform</p><h1>One commander.<br><em>A hundred assistants.</em></h1></div><div><p>Jarwis turns a single goal into finished software, research and daily workflows, and shows you every step the agents take.</p><a class="btn" href="/architecture/">See how it works</a></div></section>
<div class="belt" data-tokens='{tok}' role="img" aria-label="Animated belt of six Jarwis modules turning from product pages into the compact code agents read"><div class="codes">{"".join(code(i,c) for i,c in enumerate(C))}</div><div class="cards">{"".join(card(i,c) for i,c in enumerate(C))}</div><canvas class="fx" aria-hidden="true"></canvas></div>
<div class="scan" aria-hidden="true"><i></i></div><div class="badge" aria-live="off">Token reduction<div class="pill"><b id="num">&minus;0</b><span id="pct">0% less</span></div></div>
<div class="homefoot"><a href="/assistants/">Assistants</a><a href="/architecture/">Architecture</a><a href="/security/">Security</a><a href="/sitemap.xml">Sitemap</a></div></div></main><script src="/assets/belt.js" defer></script><script src="/assets/ai.js" defer></script></body></html>'''
w("/",home)
# ---- inner pages
def inner(path,title,desc,h1,body,label):
    cs=[("Home","/"),(label,path)]
    w(path,head(path,title,desc,cs)+f'<body>{navbar(path)}{crumbs(cs)}<main id="main" class="page"><h1>{h1}</h1><p style="margin-top:12px;max-width:62ch">{desc}</p>{body}</main>{foot()}<script src="/assets/ai.js" defer></script></body></html>')
rows="".join(f'<tr><td>{n}</td><td>{c}+</td><td>{e}</td></tr>' for n,c,e in CL)
inner("/architecture/","System Architecture | Jarwis","How Jarwis connects a commander agent, an A2A mesh, MCP tools, hybrid RAG, a vision worker and Docker sandboxes.","Architecture",
'''<section><h2>Flow of a mission</h2><pre class="mm">You (voice / chat / PWA)
  -> Commander-00 (LangGraph supervisor, budget governor)
      -> A2A mesh -> 99+ assistants
           -> MCP bus: files, Git, DB, calendar, browser
           -> Hybrid RAG: Qdrant + BM25 + reranker + graph
           -> Vision worker (PyTorch / ONNX)
           -> Docker sandbox + tests -> self-repair (max 3)
      -> HITL approval gate -> deploy / send / push
  Telemetry: OpenTelemetry -> Prometheus -> Grafana</pre></section>
<section><h2>Building blocks</h2><div class="grid"><div class="tile"><h3>Control plane</h3><p>Next.js command centre with live swarm graph and approval queue.</p></div><div class="tile"><h3>Execution plane</h3><p>FastAPI, LangGraph, Redis Streams and Docker sandbox runner.</p></div><div class="tile"><h3>Model router</h3><p>Auto-discovers Gemini, Groq, OpenAI, Anthropic and Ollama, with fallback.</p></div><div class="tile"><h3>Storage</h3><p>PostgreSQL, Qdrant, MinIO and signed audit logs.</p></div></div></section><section><h2>Next</h2><p>Read how we protect it on the <a href="/security/">security page</a>.</p></section>''',"Architecture")
inner("/security/","Security and Human Approval | Jarwis","Every risky action waits for your approval. See the guardrails: prompt-injection defence, secret scrubbing, spend caps and isolated sandboxes.","Security",
'<section><div class="grid"><div class="tile"><h3>Approval first</h3><p>Deploys, pushes, external sends and deletions pause until you approve.</p></div><div class="tile"><h3>Spend caps</h3><p>Per-mission token limits and loop breakers stop runaway agents.</p></div><div class="tile"><h3>Isolation</h3><p>Generated code runs in resource-limited containers with rollback.</p></div><div class="tile"><h3>Privacy</h3><p>PII masking, secret scrubbing and per-assistant memory visibility.</p></div></div></section><section><h2>Related</h2><p>See the <a href="/architecture/">architecture</a> and the <a href="/assistants/">assistant registry</a>.</p></section>',"Security")
# ---- full 99-assistant matrix
G=[("Software, Cloud & Security","System Architect|Full-Stack Builder|Frontend UI Crafter|Backend API Engineer|Database Architect|DevOps & CI/CD Engineer|Docker & Kubernetes Orchestrator|QA & E2E Tester|Code Reviewer|Root-Cause Debugger|AppSec Auditor|API Docs Writer|Mobile & Termux Builder|Performance Profiler|Release Manager|Legacy Modernizer|Edge & IoT Integrator|Open-Source Maintainer","repo, shell, git"),
("AI, Data & Research","Deep Researcher|Citation Verifier|RAG Curator|Data Analyst|Chart Designer|ML Training Engineer|CNN Vision Specialist|LLM Eval Judge|Trend Scout|Paper & Repo Summarizer|ETL Engineer|Synthetic Data Generator|Experiment Tracker|Prompt Optimizer","web, vector DB, SQL"),
("Productivity & Daily Ops","Time-Blocker|Triage Coach|Deep-Work Guardian|Route Planner|Fuel & Expense Tracker|Reminder Keeper|Study Tutor|Second-Brain Organizer|Wellness Advisor|Shopping Coordinator|Decision Analyst|Inbox Triage|Event Coordinator|Budget Watchdog|Form Automator|Errand Scout","calendar, mail, notes"),
("Creative & Communication","UX Copywriter|Script Writer|Brand Stylist|Slide Deck Builder|Diagram Artist|Accessibility Critic|Launch Strategist|Email Drafter|Meeting Action Extractor|Translator|Brainstorm Partner|Demo Coach|Asset Director","docs, slides, media"),
("Business, Finance & Risk","PRD Writer|Pricing Strategist|Growth Experimenter|Cashflow Modeler|Unit Economics Analyst|Risk Assessor|Policy Reader|Vendor Evaluator|OKR Tracker|Feedback Synthesizer|Scenario Modeler|Outreach Strategist|Startup Ops Advisor|Compliance Auditor","sheets, CRM, docs"),("Career, Learning & Growth","Resume & Career Coach|Interview Prep Coach|Job & Internship Scout|GitHub Portfolio Curator|LinkedIn Profile Optimizer|Placement Aptitude Tutor|DSA Practice Coach|SQL Practice Coach|Kaggle Strategist|Hackathon Planner|Startup Pitch Reviewer|Freelance Proposal Writer|Linux & Termux Helper|Git & GitHub Fixer|Cloud Cost Optimizer|Cybersecurity Mentor|Math & Stats Tutor|Research Paper Writer|Report Formatter|Presentation Q&A Coach|Public Speaking Coach|Language Practice Partner|Fitness & Habit Coach|Personal Finance Planner","notes, docs, web")]
cards=['<button class="ac" type="button" data-n="Commander-00" data-c="Commander" data-t="all assistants, planner"><span>#00</span><strong>Commander-00</strong><small>Plans and routes everything</small></button>'];n=1
for cl,names,tools in G:
    for nm in names.split("|"):
        cards.append(f'<button class="ac" type="button" data-n="{html.escape(nm)}" data-c="{html.escape(cl)}" data-t="{html.escape(tools)}"><span>#{n:02d}</span><strong>{html.escape(nm)}</strong><small>{html.escape(cl)}</small></button>');n+=1
chips='<button type="button" class="chip" data-f="" aria-pressed="true">All</button>'+"".join(f'<button type="button" class="chip" data-f="{html.escape(c)}" aria-pressed="false">{html.escape(c)}</button>' for c,_,_ in G)
AB=f'''<section><h2>Find the right assistants</h2><label for="rt">Describe your task</label><input id="rt" class="in" placeholder="e.g. prepare me for a data analyst interview"><button class="btn" id="rtb" type="button" style="margin:10px 0 0;border:0;cursor:pointer">Route with AI</button><p id="rto" aria-live="polite" style="margin-top:8px"></p></section><section><h2>Browse {n-1} assistants</h2><label for="q">Search</label><input id="q" class="in" placeholder="security, budget, resume..."><div class="chips">{chips}</div><div class="grid ag" id="ag">{"".join(cards)}</div></section><section><h2>Forge your own</h2><p>Describe a role and it becomes a working assistant, saved in this browser.</p><label for="fn">Name</label><input id="fn" class="in" maxlength="40"><label for="fr">What does it do?</label><textarea id="fr" class="in" maxlength="300" rows="3"></textarea><button class="btn" id="fg" type="button" style="margin:10px 0 0;border:0;cursor:pointer">Create assistant</button></section><script src="/assets/assistants.js" defer></script>'''
inner("/assistants/","AI Assistants Directory | Jarwis","Chat with any of 99 specialist assistants plus Commander-00, route a task to the best ones with AI, or forge your own.","The assistant registry",AB,"Assistants")
# ---- command center
CCB='''<section><h2>Mission preview</h2><p>This is a scripted preview that runs in your browser. It shows how Jarwis plans, delegates and waits for your approval. It does not call any AI model.</p>
<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;margin-top:16px" id="cc"><div class="tile"><canvas id="sw" width="640" height="420" style="width:100%;height:auto" role="img" aria-label="Swarm graph: Jarwis at the centre, linked to assistant nodes that light up as tasks run"></canvas></div>
<div class="tile"><label for="goal"><h3>Give Jarwis a goal</h3></label><input id="goal" value="Build a landing page and ship it" style="width:100%;margin:10px 0;padding:10px;border:1px solid #cfd4da;border-radius:10px;font:14px Inter,sans-serif"><button class="btn" id="go" style="margin:0;border:0;cursor:pointer">Run mission</button><button class="btn" id="ai" style="margin:0 0 0 8px;border:0;cursor:pointer;background:#0F1115">Plan with AI</button><label for="bg" style="display:block;margin-top:12px;font-size:13px">Token budget: <output id="bo">200,000</output></label><input id="bg" type="range" min="50000" max="300000" step="10000" value="200000" style="width:100%"><ol id="log" aria-live="polite" style="margin:14px 0 0 18px;font-size:13.5px"></ol><button class="btn" id="ok" hidden style="margin:12px 0 0;border:0;cursor:pointer;background:#0F1115">Approve deploy</button></div></div></section>
<script>(()=>{const c=document.getElementById('sw'),x=c.getContext('2d'),N=24,A=['Architect','Builder','UI Crafter','API Engineer','QA Tester','Reviewer','Security','Docs','Researcher','Verifier','Designer','Copywriter'],act=new Set();let t=0;
const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
function d(){x.clearRect(0,0,640,420);t+=rm?0:.01;for(let i=0;i<N;i++){const a=i/N*6.283+t*.15,px=320+Math.cos(a)*190,py=210+Math.sin(a)*140,on=act.has(i%12);x.strokeStyle=on?'#FF5A1F':'#cfd4da';x.lineWidth=on?2:1;x.beginPath();x.moveTo(320,210);x.lineTo(px,py);x.stroke();x.fillStyle=on?'#FF5A1F':'#8B9098';x.beginPath();x.arc(px,py,on?7:4,0,7);x.fill();if(i<12){x.fillStyle='#2A2E35';x.font='11px Inter,sans-serif';x.fillText(A[i],px+9,py+4)}}
const g=x.createRadialGradient(320,210,4,320,210,34);g.addColorStop(0,'#ff7a3c');g.addColorStop(1,'rgba(255,90,31,.1)');x.fillStyle=g;x.beginPath();x.arc(320,210,26+Math.sin(t*6)*2,0,7);x.fill();requestAnimationFrame(d)}d();
const L=document.getElementById('log'),ok=document.getElementById('ok');let busy=0,stop=0,spent=0;const bg=document.getElementById('bg'),bo=document.getElementById('bo');bg.oninput=()=>bo.textContent=(+bg.value).toLocaleString();
let S=['Commander plans the mission','Architect drafts the structure','Builder and UI Crafter write the page','Tester and Reviewer check it in the sandbox','Security scans dependencies','Waiting for your approval to deploy'];
let cp=0;const add=s=>{const li=document.createElement('li');li.textContent='Checkpoint '+(++cp)+': '+s;L.appendChild(li)};
document.getElementById('go').onclick=()=>{if(busy)return;busy=1;L.innerHTML='';cp=0;ok.hidden=true;act.clear();stop=0;spent=0;S.forEach((s,i)=>setTimeout(()=>{if(stop)return;spent+=45000;if(spent>+bg.value){stop=1;busy=0;act.clear();add('Budget governor stopped the mission at '+spent.toLocaleString()+' tokens');return}add(s+' ('+spent.toLocaleString()+' tokens used)');[[0],[7,0],[1,2],[4,5],[6],[]][i].forEach(k=>act.add(k));if(i==5)ok.hidden=false},i*900))};
document.getElementById('ai').onclick=async()=>{L.innerHTML='';cp=0;add('Asking the AI commander to plan...');try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:document.getElementById('goal').value,mode:'plan'})});const j=await r.json();const a=JSON.parse(j.reply.replace(/```json|```/g,'').trim());if(Array.isArray(a)&&a.length>=6){S=a.slice(0,6).map(String);add('Plan ready ('+j.provider+' / '+j.model+'). Press Run mission.')}else throw 0}catch(e){add('AI planning is not available here, so the default plan will run.')}};
ok.onclick=()=>{ok.hidden=true;add('Approved. Deploy finished and logged.');act.clear();busy=0}})()</script>'''
inner("/command-center/","Command Center Preview | Jarwis","Try a scripted preview of the Jarwis command center: a goal becomes a plan, assistants light up, and nothing deploys until you approve.","Command center",CCB,"Command center")

STB='''<section><h2>Live checks</h2><p>These checks run in your browser right now.</p><ul id="st" style="list-style:none;padding:0;margin-top:14px;display:grid;gap:8px"></ul></section><script>(()=>{const T=[["Site pages","/"],["Sitemap","/sitemap.xml"],["Scanner script","/assets/belt.js"],["Assistant matrix","/assistants/"]],u=document.getElementById("st"),api=(document.querySelector("meta[name=jarwis-api]")||{}).content||"";
const row=(n,ok,x)=>{const l=document.createElement("li");l.className="tile";l.textContent=n+": "+(ok?"operational":"unreachable")+(x||"");l.style.borderLeft="4px solid "+(ok?"#2E9E5B":"#D9430F");u.appendChild(l)};
T.forEach(async t=>{try{const r=await fetch(t[1],{method:"HEAD"});row(t[0],r.ok)}catch(e){row(t[0],false)}});
if(api){fetch("/api/chat").then(r=>r.json()).then(d=>{const k=Object.keys(d.providers||{});if(!k.length){row("AI backend",false," (add GROQ_API_KEY or GEMINI_API_KEY)");return}k.forEach(p=>row("AI: "+p,true," ("+d.providers[p].fast+" / "+d.providers[p].deep+")"))}).catch(()=>row("AI backend",false))}else{const l=document.createElement("li");l.className="tile";l.textContent="AI backend: not connected yet (chat uses built-in answers)";u.appendChild(l)}})()</script>'''
inner("/status/","System Status | Jarwis","Live status checks for the Jarwis site and its AI backend, run in your browser.","Status",STB,"Status")
inner("/roadmap/","Roadmap | Jarwis","What Jarwis ships now, next and later: the live preview, the AI backend, voice, checkpoints and per-user missions.","Roadmap",
'<section><div class="grid"><div class="tile"><h3>Now</h3><p>Scanner home page, 99-assistant matrix, command center preview with budget governor, status checks, voice chat and an installable offline app.</p></div><div class="tile"><h3>Next</h3><p>Live backend missions through the model router, real approval queue, and saved checkpoints with rollback.</p></div><div class="tile"><h3>Later</h3><p>Sign-in with passkeys, per-user memory, MCP tool connectors and a vision worker for wireframes. See <a href="/architecture/">architecture</a> and <a href="/security/">security</a>.</p></div></div></section>',"Roadmap")
GH="https://github.com/Nikhil-creat";LI="https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a"
PJ=[("CloudPulse AI","Multi-cloud FinOps, security auto-remediation and AI observability."),("ExoMind-X","Kepler exoplanet CNN with LangGraph, hybrid RAG and human review."),("APEX-AI","Agentic multimodal assistant with GraphRAG and six Docker services."),("BastionMesh AI","Multi-agent mesh with CNN vision, CRAG and MCP tools."),("PharmAi Vision","Medicine identifier using CNN, OCR and an agentic assistant."),("ModelRoute","Fine-tuned small model behind an intelligent router."),("StreamGuard","Real-time fraud detection with Kafka, Airflow and Delta Lake."),("AMITH","JARVIS-style assistant site with a Groq and Gemini proxy.")]
tl="".join(f'<div class="tile"><h3>{a}</h3><p>{b}</p></div>' for a,b in PJ)
person={"@context":"https://schema.org","@type":"Person","name":"Nikhil Chary Sriramoju","url":D+"/builder/","jobTitle":"Computer Science engineering student","sameAs":[GH,LI]}
bt="Builder | Jarwis";bd="Jarwis is designed and built by Nikhil Chary Sriramoju, a final-year B.Tech computer science student who ships agentic AI, RAG and computer vision projects."
bc=[("Home","/"),("Builder","/builder/")]
w("/builder/",head("/builder/",bt,bd,bc,'<script type="application/ld+json">'+json.dumps(person)+'</script>')+f'<body>{navbar("/builder/")}{crumbs(bc)}<main id="main" class="page"><h1>Built by Nikhil Chary Sriramoju</h1><p style="margin-top:12px;max-width:62ch">{bd}</p><section><h2>Profiles</h2><p><a href="{GH}" rel="me noopener">GitHub</a> &middot; <a href="{LI}" rel="me noopener">LinkedIn</a></p></section><section><h2>Experience</h2><div class="grid"><div class="tile"><h3>Data Analyst Intern</h3><p>Bluestock Fintech, remote, part-time. Nov 2026 to Jan 2027.</p></div><div class="tile"><h3>B.Tech, Computer Science</h3><p>Final year.</p></div></div></section><section><h2>Selected projects</h2><div class="grid">{tl}</div></section><section><h2>Stack</h2><p>Python, FastAPI, LangGraph, PyTorch, RAG with Qdrant, Docker, Next.js, Groq and Gemini APIs. See how it fits together on the <a href="/architecture/">architecture</a> page.</p></section></main>{foot()}<script src="/assets/ai.js" defer></script></body></html>')
# ---- 404
w("/404.html",head("/404.html","Page not found | Jarwis","This page does not exist. Return to the Jarwis home page or browse the assistants.",[("Home","/")],'<meta name="robots" content="noindex">')+f'<body>{navbar("")}<main id="main" class="page"><h1>This page is not here</h1><p style="margin-top:12px">The link may be old or mistyped. Try the <a href="/">home page</a>, the <a href="/assistants/">assistants</a> or the <a href="/architecture/">architecture</a>.</p></main>{foot()}<script src="/assets/ai.js" defer></script></body></html>')
# ---- seo files
urls=["/","/command-center/","/builder/","/roadmap/","/status/","/assistants/","/architecture/","/security/"]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)+"</urlset>")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {D}/sitemap.xml\n")
open("llms.txt","w").write(f"# {NAME}\n> Multi-agent AI platform: one commander (Commander-00) coordinating 99+ specialised assistants with human approval for risky actions.\n\n## Pages\n- [Home]({D}/): overview\n- [Command center]({D}/command-center/): live preview\n- [Status]({D}/status/): live checks\n- [Roadmap]({D}/roadmap/): what ships next\n- [Builder]({D}/builder/): who built Jarwis\n- [Assistants]({D}/assistants/): six clusters of assistants\n- [Architecture]({D}/architecture/): how missions flow\n- [Security]({D}/security/): guardrails and approvals\n")
open("favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#0F1115"/><path d="M16 5c-5 8-9 11-9 16a9 9 0 0 0 18 0c0-5-4-8-9-16Z" fill="#FF5A1F"/></svg>')
open("CNAME","w").write(D.split("//")[1]+"\n")
open(".nojekyll","w").write("")
open("vercel.json","w").write(json.dumps({"headers":[{"source":"/assets/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=3600, stale-while-revalidate=86400"}]},{"source":"/(.*)","headers":[{"key":"X-Content-Type-Options","value":"nosniff"},{"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"}]}]}))
try:
    from PIL import Image,ImageDraw
    im=Image.new("RGB",(1200,630),"#EEF0F2");d=ImageDraw.Draw(im);d.rectangle((596,0,604,630),fill="#FF5A1F");d.text((60,260),"Jarwis",fill="#0F1115");d.text((60,300),"One commander. A hundred assistants.",fill="#2A2E35");im.save("og.png")
except Exception as e:print("og skipped",e)

open("manifest.webmanifest","w").write(json.dumps({"name":"Jarwis","short_name":"Jarwis","start_url":"/","display":"standalone","background_color":"#EEF0F2","theme_color":"#FF5A1F","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]}))
open("sw.js","w").write("const C='jarwis-v1',F=['/','/assistants/','/command-center/','/architecture/','/security/','/status/','/assets/site.css','/assets/belt.js','/assets/ai.js','/404.html'];self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting())));self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x))))));self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{const y=r.clone();caches.open(C).then(c=>c.put(e.request,y));return r}).catch(()=>caches.match(e.request).then(m=>m||caches.match('/404.html'))))});")
try:
    from PIL import Image,ImageDraw,ImageFont
    def fnt(n):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
            try:return ImageFont.truetype(p,n)
            except Exception:pass
        return ImageFont.load_default()
    im=Image.new("RGB",(1200,630),"#EEF0F2");d=ImageDraw.Draw(im);d.rectangle((596,0,604,630),fill="#FF5A1F")
    for i in range(0,560,7):d.rectangle((604+i,150+(i*37%300),607+i,153+(i*37%300)),fill="#FF5A1F")
    d.text((60,200),"Jarwis",font=fnt(110),fill="#0F1115");d.text((60,340),"One commander.",font=fnt(44),fill="#2A2E35");d.text((60,400),"A hundred assistants.",font=fnt(44),fill="#FF5A1F");im.save("og.png")
    for n in (192,512):
        ic=Image.new("RGB",(n,n),"#0F1115");g=ImageDraw.Draw(ic);g.ellipse((n*.28,n*.18,n*.72,n*.82),fill="#FF5A1F");ic.save(f"icon-{n}.png")
except Exception as e:print("img skipped",e)
