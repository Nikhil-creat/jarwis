"""Vercel serverless function: GET lists auto-detected models, POST chats. Keys come from Vercel env vars."""
import json, os, re, time, urllib.request
from http.server import BaseHTTPRequestHandler

P = {"groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
     "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY")}
BAD = re.compile(r"whisper|guard|tts|playai|orpheus|embed|imagen|veo|image|live|aqa|robotics|audio|moderation|safeguard|distil", re.I)
SYS = ("You are Jarwis, the commander AI of a platform that coordinates 99+ specialised assistants. "
       "Answer in at most 4 short sentences. Be warm and clear. Risky actions always need user approval.")
PLAN = ("Return ONLY a JSON array of exactly 6 short strings: the steps a commander AI and its specialist assistants "
        "take for the user's goal. The last step must be 'Waiting for your approval to deploy'. No other text.")
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

def complete(messages, tier):
    det, last = detect(), "no provider configured"
    for p in [x for x in ("groq", "gemini") if x in det]:
        url, env = P[p]
        body = json.dumps({"model": det[p][tier], "messages": messages, "max_tokens": 500, "temperature": 0.4}).encode()
        req = urllib.request.Request(url + "/chat/completions", body, {"Authorization": "Bearer " + os.environ[env], "Content-Type": "application/json", "User-Agent": "jarwis/1.0"})
        try:
            j = json.load(urllib.request.urlopen(req, timeout=25))
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
        d = detect(); self._send(200, {"ready": bool(d), "providers": d})
    def do_POST(self):
        ip, now = self.headers.get("x-forwarded-for", "?").split(",")[0], time.time()
        RL[ip] = [t for t in RL.get(ip, []) if now - t < 60] + [now]
        if len(RL[ip]) > 12: return self._send(429, {"reply": "Slow down a little and try again in a minute."})
        allowed = os.environ.get("ALLOWED_ORIGIN")
        if allowed and self.headers.get("origin") not in (None, allowed): return self._send(403, {"reply": "Origin not allowed."})
        try:
            n = min(int(self.headers.get("content-length", 0)), 4000)
            j = json.loads(self.rfile.read(n) or b"{}")
            m, plan = str(j.get("message", ""))[:1500], j.get("mode") == "plan"
            if not m.strip(): return self._send(400, {"reply": "Say something first."})
            text, p, mod = complete([{"role": "system", "content": PLAN if plan else SYS}, {"role": "user", "content": m}], "deep" if plan else "fast")
            self._send(200, {"reply": text, "provider": p, "model": mod})
        except Exception:
            self._send(502, {"reply": "The AI is unavailable right now. Check the API keys in Vercel."})
