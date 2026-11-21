"""Vercel serverless function: GET lists auto-detected models, POST chats. Keys come from Vercel env vars."""
import json, os, re, time, urllib.request
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
_C = {"t": 0, "v": {}}
RL = {}

def score(pid, tier):
    m, s = pid.lower(), 0
    table = ((("gpt-oss-120b", 9), ("70b", 8), ("pro", 8), ("120b", 8), ("deepseek", 5), ("qwen", 5), ("flash", 4), ("8b", 1))
             if tier == "deep" else
             (("flash-lite", 9), ("instant", 9), ("8b", 8), ("flash", 7), ("mini", 6), ("20b", 5), ("70b", 3)))
    for k, v in table:
        if k in m: s = max(s, v)
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
        body = json.dumps({"model": det[p][tier], "messages": messages, "max_tokens": max_tokens, "temperature": 0.4}).encode()
        req = urllib.request.Request(url + "/chat/completions", body, {"Authorization": "Bearer " + os.environ[env], "Content-Type": "application/json", "User-Agent": "jarwis/1.0"})
        try:
            j = json.load(urllib.request.urlopen(req, timeout=28))
            return j["choices"][0]["message"]["content"], p, det[p][tier]
        except Exception as e:
            last = str(e)
    raise RuntimeError(last)

class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        for k, v in (("Content-Type", "application/json"), ("Cache-Control", "no-store"), ("Content-Length", str(len(b)))): self.send_header(k, v)
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        d = detect(); self._send(200, {"ready": bool(d), "providers": d, "version": "2026-11-21-resume"})
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
            mode = j.get("mode"); m = str(j.get("message", ""))[:12000 if mode in ("resume", "cover") else 4000 if mode in ("iq", "ifb") else 1500]
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
                tier = "deep" if len(m) > 400 else "fast"
                hist = [{"role": h["role"], "content": str(h.get("content", ""))[:1000]} for h in (j.get("history") or [])[-8:] if isinstance(h, dict) and h.get("role") in ("user", "assistant")]
            text, p, mod = complete([{"role": "system", "content": sysmsg}] + hist + [{"role": "user", "content": m}], tier)
            self._send(200, {"reply": text, "provider": p, "model": mod})
        except Exception:
            self._send(502, {"reply": "The AI is unavailable right now. Check the API keys in Vercel."})
