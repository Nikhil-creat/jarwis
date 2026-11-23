"""Vercel serverless function: GET lists auto-detected models, POST chats. Keys come from Vercel env vars."""
import json, os, re, time, urllib.error, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

P = {"groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
     "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY")}
BAD = re.compile(r"whisper|guard|tts|playai|orpheus|embed|imagen|veo|image|live|aqa|robotics|audio|moderation|safeguard|distil", re.I)
SYS = ("You are Jarwis, the commander AI of a platform that coordinates 99+ specialised assistants. "
       "Answer in at most 4 short sentences. Be warm and clear. Risky actions always need user approval.")
PLAN = ("Return ONLY a JSON array of exactly 6 short strings: the steps a commander AI and its specialist assistants "
        "take for the user's goal. The last step must be 'Waiting for your approval to deploy'. No other text.")
ROUTE = ("From the list below pick the 3 assistants best suited to the user's task. Return ONLY a JSON array of exactly 3 names copied exactly from the list, no other text. List: ")
RESUME = ("You are the Resume and Career Coach assistant of Jarwis, an expert ATS resume writer. The input is JSON with a candidate's facts and a target job. "
          "Return ONLY one JSON object with keys: summary (max 2 sentences, tailored to the job, no pronouns), skills (array of {g: group name, items: array of strings}, max 5 groups, most job-relevant first), "
          "experience (array of {role, org, dates, bullets}), projects (array of {name, tech, bullets}, max 3), education (array of {degree, school, dates, detail}), "
          "extras (array of short strings for certifications or achievements), gaps (array of up to 8 important keywords from the job description that the candidate facts do not support). "
          "Rules: use ONLY facts present in the input. Never invent employers, titles, dates, metrics, tools or degrees. Use numbers only if given. "
          "Start bullets with a strong action verb (past tense, present tense for current work), max 22 words each, 2 to 3 bullets per item, plain text only. "
          "Use exact job-description keywords only where the facts support them. It must fit one page: at most 12 bullets in total. If there is no work experience, return an empty experience array.")
def S(x, k=300): return str(x or "")[:k]
def clean_resume(o):
    L = lambda x, n: (x if isinstance(x, list) else [])[:n]
    D = lambda x: x if isinstance(x, dict) else {}
    o = D(o)
    return {"summary": S(o.get("summary"), 400),
            "skills": [{"g": S(D(g).get("g"), 40), "items": [S(i, 40) for i in L(D(g).get("items"), 20)]} for g in L(o.get("skills"), 6)],
            "experience": [{"role": S(D(e).get("role"), 80), "org": S(D(e).get("org"), 80), "dates": S(D(e).get("dates"), 40), "bullets": [S(b, 220) for b in L(D(e).get("bullets"), 5)]} for e in L(o.get("experience"), 4)],
            "projects": [{"name": S(D(e).get("name"), 80), "tech": S(D(e).get("tech"), 120), "bullets": [S(b, 220) for b in L(D(e).get("bullets"), 5)]} for e in L(o.get("projects"), 4)],
            "education": [{"degree": S(D(e).get("degree"), 100), "school": S(D(e).get("school"), 100), "dates": S(D(e).get("dates"), 40), "detail": S(D(e).get("detail"), 160)} for e in L(o.get("education"), 3)],
            "extras": [S(x, 160) for x in L(o.get("extras"), 6)],
            "gaps": [S(x, 40) for x in L(o.get("gaps"), 8)]}
COVER = ("You are the Resume and Career Coach assistant of Jarwis. The input is JSON with a candidate's facts and a target job. Write a concise, honest cover letter in plain text: at most 250 words, three short paragraphs "
         "(why this role, the most relevant proof from the facts, a confident close). Use ONLY the facts provided and never invent employers, metrics or tools. If no company is given, address it to the Hiring Team. "
         "No placeholders in square brackets. Start with 'Dear' and end with 'Sincerely,' followed by the candidate's name.")
IQ = ("You are the Interview Prep Coach assistant of Jarwis. Return ONLY a JSON array of exactly 6 objects {\"q\": question, \"type\": \"Technical\" or \"Behavioral\" or \"Situational\"}. "
      "Tailor them to the role, level and job description. Make them realistic, specific and answerable in one to three minutes.")
IFB = ("You are an honest interview coach. Return ONLY one JSON object {\"score\": integer 1 to 10, \"strengths\": up to 3 short strings, \"improve\": up to 3 short strings, \"better\": a stronger sample answer under 120 words}. "
       "Judge the candidate's answer to the question for the role. Be specific. In the sample answer reuse only ideas from the candidate's answer plus general best practice, and do not invent employers or exact numbers.")
D = lambda x: x if isinstance(x, dict) else {}
MPLAN = ("You are Commander-00 of Jarwis. Break the user's goal into 3 to 5 independent tasks and assign each to the most suitable assistant from the list. "
         "Each task must be doable on its own from the goal alone, with no dependency on another task. Use a different assistant for each task. "
         "Return ONLY a JSON array of objects {\"assistant\": exact name from the list, \"task\": one clear sentence}. Assistants: ")
MFINAL = ("You are Commander-00, the lead of Jarwis. The input is JSON with a goal and results from specialist assistants. Combine them into ONE clear deliverable in plain text with these sections, each starting with '## ': "
          "Summary (2 sentences), Plan (numbered steps or a checklist that merges the specialists' work and removes duplicates), Risks and open questions, Next actions (3 to 5 items). "
          "Use only what the specialists provided plus common sense. These are plans and drafts: never claim anything was deployed, sent or completed outside this page. Keep it under 450 words.")
_C = {"t": 0, "v": {}}
RL = {}

def score(pid, tier):
    m, s = pid.lower(), 0
    table = ((("gpt-oss-120b", 9), (r"(?<!\d)70b", 8), ("pro", 8), (r"(?<!\d)120b", 8), ("deepseek", 5), ("qwen", 5), ("flash", 4), (r"(?<!\d)8b", 1))
             if tier == "deep" else
             (("flash-lite", 9), ("instant", 9), (r"(?<!\d)8b", 8), ("flash", 7), ("mini", 6), (r"(?<!\d)20b", 5), (r"(?<!\d)70b", 3)))
    for k, v in table:
        if re.search(k, m): s = max(s, v)
    if "preview" in m or "exp" in m: s -= 2
    v = re.search(r"-(\d\.\d)", m)
    return s + (float(v.group(1)) * 0.1 if v else 0)

def detect():
    if _C["v"] and time.time() - _C["t"] < 600: return _C["v"]
    out = {}
    for name, (url, env) in P.items():
        key = os.environ.get(env)
        if not key: continue
        try:
            req = urllib.request.Request(url + "/models", headers={"Authorization": "Bearer " + key, "User-Agent": "jarwis/1.0"})
            ids = [d["id"].replace("models/", "") for d in json.load(urllib.request.urlopen(req, timeout=6))["data"] if not BAD.search(d["id"])]
            if ids:
                out[name] = {"fast": max(ids, key=lambda i: score(i, "fast")), "deep": max(ids, key=lambda i: score(i, "deep")), "count": len(ids)}
        except Exception:
            pass
    _C.update(t=time.time(), v=out)
    return out

def complete(messages, tier, max_tokens=700):
    det, last = detect(), "no provider configured"
    for p in [x for x in ("groq", "gemini") if x in det]:
        url, env = P[p]
        model = det[p][tier]
        base = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.4}
        variants = [dict(base, reasoning_effort="low" if tier == "fast" else "medium"), base] if p == "groq" and "gpt-oss" in model else [base]
        for body in variants:
            req = urllib.request.Request(url + "/chat/completions", json.dumps(body).encode(), {"Authorization": "Bearer " + os.environ[env], "Content-Type": "application/json", "User-Agent": "jarwis/1.0"})
            try:
                text = json.load(urllib.request.urlopen(req, timeout=28))["choices"][0]["message"]["content"]
                if text: return text, p, model
                last = "empty reply"
                break
            except urllib.error.HTTPError as e:
                last = str(e)
                if e.code != 400: break
            except Exception as e:
                last = str(e)
                break
    raise RuntimeError(last)

TOOLENV = {"jobs": ("ADZUNA_APP_ID", "ADZUNA_APP_KEY"), "stock": ("FINNHUB_API_KEY",), "food": ("CALORIENINJAS_API_KEY",)}
def tools_on(): return [k for k, v in TOOLENV.items() if all(os.environ.get(e) for e in v)]
def _get(url, headers=None, timeout=9):
    req = urllib.request.Request(url, headers=dict({"User-Agent": "jarwis/1.0", "Accept": "application/json"}, **(headers or {})))
    return json.load(urllib.request.urlopen(req, timeout=timeout))
def _clean(x, k=80): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(x or ""))).strip()[:k]
def tool_jobs(q):
    cc = re.sub(r"[^a-z]", "", os.environ.get("ADZUNA_COUNTRY", "in").lower())[:2] or "in"
    qs = urllib.parse.urlencode({"app_id": os.environ["ADZUNA_APP_ID"], "app_key": os.environ["ADZUNA_APP_KEY"], "what": q, "results_per_page": 5, "content-type": "application/json"})
    d = D(_get("https://api.adzuna.com/v1/api/jobs/%s/search/1?%s" % (cc, qs)))
    rs = d.get("results") or []
    if not rs: raise ValueError("No jobs found for that search. Try a broader job title.")
    rows = []
    for r in rs[:5]:
        r = D(r); sal = ""
        if r.get("salary_min") and r.get("salary_max"): sal = " | salary %d to %d (local currency)" % (r["salary_min"], r["salary_max"])
        rows.append("%s at %s, %s%s | posted %s | %s" % (_clean(r.get("title")), _clean(D(r.get("company")).get("display_name"), 50), _clean(D(r.get("location")).get("display_name"), 50), sal, _clean(r.get("created"), 10), _clean(r.get("redirect_url"), 140)))
    return {"text": 'Job listings for "%s" (Adzuna, about %s matches): ' % (_clean(q, 50), d.get("count", "many")) + " || ".join(rows), "link": "https://www.adzuna.com/", "source": "Adzuna"}
def tool_stock(q):
    key, q = os.environ["FINNHUB_API_KEY"], q.strip()
    sym = q.upper() if re.fullmatch(r"[A-Za-z.\-]{1,6}", q) else None
    if not sym:
        res = D(_get("https://finnhub.io/api/v1/search?" + urllib.parse.urlencode({"q": q, "token": key}))).get("result") or []
        res = [x for x in res if D(x).get("type") == "Common Stock"] or res
        if not res: raise ValueError("No stock found. Try a US ticker such as AAPL.")
        sym = _clean(D(res[0]).get("symbol"), 12)
    d = D(_get("https://finnhub.io/api/v1/quote?" + urllib.parse.urlencode({"symbol": sym, "token": key})))
    if not d.get("c"): raise ValueError("No quote for that symbol. The free plan covers US stocks.")
    return {"text": "%s: price %s (change %s, %s%%), day range %s to %s, open %s, previous close %s. Free quotes cover US stocks and can be delayed. This is information, not financial advice." % (sym, d.get("c"), d.get("d"), d.get("dp"), d.get("l"), d.get("h"), d.get("o"), d.get("pc")), "link": "https://finnhub.io/", "source": "Finnhub"}
def tool_food(q):
    d = D(_get("https://api.calorieninjas.com/v1/nutrition?" + urllib.parse.urlencode({"query": q[:200]}), {"X-Api-Key": os.environ["CALORIENINJAS_API_KEY"]}))
    items = d.get("items") or []
    if not items: raise ValueError("No food found. Try: 2 eggs and 1 cup of rice")
    keys = (("calories", "kcal"), ("protein_g", "g protein"), ("carbohydrates_total_g", "g carbs"), ("fat_total_g", "g fat"), ("sugar_g", "g sugar"), ("fiber_g", "g fibre"), ("sodium_mg", "mg sodium"))
    rows = []
    for it in items[:8]:
        it = D(it)
        vals = ", ".join("%s %s" % (round(it[k], 1), u) for k, u in keys if isinstance(it.get(k), (int, float)))
        rows.append("%s (%s g serving): %s" % (_clean(it.get("name"), 40), it.get("serving_size_g", "?"), vals or "no numbers on this plan"))
    tot = sum(D(i).get("calories") for i in items if isinstance(D(i).get("calories"), (int, float)))
    return {"text": "Nutrition estimate (CalorieNinjas): " + " | ".join(rows) + (" | total about %d kcal" % tot if tot else ""), "link": "https://calorieninjas.com/", "source": "CalorieNinjas"}
TOOLS = {"jobs": tool_jobs, "stock": tool_stock, "food": tool_food}

class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        for k, v in (("Content-Type", "application/json"), ("Cache-Control", "no-store"), ("Content-Length", str(len(b)))): self.send_header(k, v)
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        d = detect(); self._send(200, {"ready": bool(d), "providers": d, "tools": tools_on(), "version": "2026-11-22-tools"})
    def do_POST(self):
        ip, now = self.headers.get("x-forwarded-for", "?").split(",")[0], time.time()
        RL[ip] = [t for t in RL.get(ip, []) if now - t < 60] + [now]
        if len(RL[ip]) > 20: return self._send(429, {"reply": "Slow down a little and try again in a minute."})
        org, host = self.headers.get("origin"), self.headers.get("host", "")
        extra = [x.strip() for x in os.environ.get("ALLOWED_ORIGIN", "").split(",") if x.strip()]
        if org and urlparse(org).netloc != host and org not in extra: return self._send(403, {"reply": "Origin not allowed."})
        try:
            n = min(int(self.headers.get("content-length", 0)), 30000)
            j = json.loads(self.rfile.read(n) or b"{}")
            mode = j.get("mode"); m = str(j.get("message", ""))[:12000 if mode in ("resume", "cover", "mission_final", "mission_plan") else 4000 if mode in ("iq", "ifb") else 3500 if isinstance(j.get("assistant"), dict) else 1500]
            if not m.strip(): return self._send(400, {"reply": "Say something first."})
            if mode == "cover":
                text, p, mod = complete([{"role": "system", "content": COVER}, {"role": "user", "content": m}], "deep", 1500)
                return self._send(200, {"reply": text.strip()[:3000], "provider": p, "model": mod})
            if mode == "iq":
                text, p, mod = complete([{"role": "system", "content": IQ}, {"role": "user", "content": m}], "deep", 1500)
                arr = json.loads(text[text.find("["):text.rfind("]") + 1])
                qs = [{"q": S(D(x).get("q")), "type": S(D(x).get("type"), 20)} for x in (arr if isinstance(arr, list) else [])[:8] if S(D(x).get("q"))]
                if not qs: raise ValueError("no questions")
                return self._send(200, {"questions": qs, "provider": p, "model": mod})
            if mode == "ifb":
                text, p, mod = complete([{"role": "system", "content": IFB}, {"role": "user", "content": m}], "deep", 1500)
                o = D(json.loads(text[text.find("{"):text.rfind("}") + 1]))
                try: sc = max(1, min(10, int(o.get("score"))))
                except (TypeError, ValueError): sc = 5
                li = lambda x, n: [S(i, 200) for i in (x if isinstance(x, list) else [])[:n]]
                return self._send(200, {"feedback": {"score": sc, "strengths": li(o.get("strengths"), 3), "improve": li(o.get("improve"), 3), "better": S(o.get("better"), 900)}, "provider": p, "model": mod})
            if mode == "resume":
                text, p, mod = complete([{"role": "system", "content": RESUME}, {"role": "user", "content": m}], "deep", 3000)
                a, b = text.find("{"), text.rfind("}")
                return self._send(200, {"resume": clean_resume(json.loads(text[a:b + 1])), "provider": p, "model": mod})
            clean = lambda s, k: re.sub(r"[^\w .,&/+'()-]", "", str(s))[:k]
            if mode == "tool":
                d = D(json.loads(m)); k = d.get("tool"); q = S(d.get("q"), 200).strip()
                if k not in TOOLS or k not in tools_on(): return self._send(404, {"reply": "That live data tool is not set up on this site yet."})
                if len(q) < 2: return self._send(400, {"reply": "Type what to look up first."})
                try: return self._send(200, TOOLS[k](q))
                except ValueError as e: return self._send(404, {"reply": str(e)})
                except Exception: return self._send(502, {"reply": "The live data service did not answer. Try again in a moment."})
            if mode == "mission_plan":
                d = D(json.loads(m))
                names = [clean(x, 60) for x in (d.get("names") or [])[:120]]
                text, p, mod = complete([{"role": "system", "content": MPLAN + "; ".join(names)}, {"role": "user", "content": S(d.get("goal"), 600)}], "deep", 1500)
                arr = json.loads(text[text.find("["):text.rfind("]") + 1])
                steps = [{"a": S(D(x).get("assistant"), 60), "t": S(D(x).get("task"), 300)} for x in (arr if isinstance(arr, list) else [])[:6]]
                steps = [x for x in steps if x["a"] in names and x["t"]]
                if len(steps) < 2: raise ValueError("bad plan")
                return self._send(200, {"steps": steps, "provider": p, "model": mod})
            if mode == "mission_final":
                text, p, mod = complete([{"role": "system", "content": MFINAL}, {"role": "user", "content": m}], "deep", 1800)
                return self._send(200, {"reply": text.strip()[:6000], "provider": p, "model": mod})
            hist = [{"role": h["role"], "content": str(h.get("content", ""))[:1000]} for h in (j.get("history") or [])[-8:] if isinstance(h, dict) and h.get("role") in ("user", "assistant")]
            sysmsg, tier = SYS, "fast"
            if mode == "plan": sysmsg, tier, hist = PLAN, "deep", []
            elif mode == "route":
                hist = []
                sysmsg = ROUTE + "; ".join(clean(x, 60) for x in (j.get("names") or [])[:120])
            elif isinstance(j.get("assistant"), dict):
                a = j["assistant"]
                sysmsg = (f"You are the {clean(a.get('name'), 60)} assistant on the Jarwis platform (cluster: {clean(a.get('cluster'), 40)}; tools: {clean(a.get('tools'), 300)}). "
                          "Stay in this specialist role, give practical step-by-step help, ask one clarifying question if the request is vague, keep answers under 200 words, "
                          "and never claim to have run tools or taken actions you cannot take. Risky actions need the user's approval.")
                tier = j.get("tier") if j.get("tier") in ("fast", "deep") else ("deep" if len(m) > 400 else "fast")
                hist = [{"role": h["role"], "content": str(h.get("content", ""))[:1000]} for h in (j.get("history") or [])[-8:] if isinstance(h, dict) and h.get("role") in ("user", "assistant")]
            text, p, mod = complete([{"role": "system", "content": sysmsg}] + hist + [{"role": "user", "content": m}], tier)
            self._send(200, {"reply": text, "provider": p, "model": mod})
        except Exception:
            self._send(502, {"reply": "The AI is unavailable right now. Check the API keys in Vercel."})
