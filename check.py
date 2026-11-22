"""Pre-push check: run `python3 check.py` inside the project folder."""
import os, re, sys
need = ["index.html", "404.html", "faq/index.html", "contact/index.html", "resume/index.html", "assistants/index.html",
        "api/chat.py", "assets/ai.js", "assets/resume.js", "assets/interview.js", "assets/mission.js", "interview/index.html", "assets/site.css", "sitemap.xml", "robots.txt", "llms.txt",
        "favicon.ico", "og.png", "vercel.json"]
bad = [f"missing file: {f}" for f in need if not os.path.exists(f)]
api = open("api/chat.py").read() if os.path.exists("api/chat.py") else ""
if "urlparse" not in api:
    bad.append("api/chat.py is an old version (no origin fix)")
if "COVER" not in api or "MFINAL" not in api:
    bad.append("api/chat.py has no cover letter or interview support")
pat = re.compile(r"gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{30,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
    for f in files:
        if f.endswith((".png", ".ico", ".zip")):
            continue
        path = os.path.join(root, f)
        try:
            if pat.search(open(path, errors="ignore").read()):
                bad.append("possible secret in " + path)
        except OSError:
            pass
for d in (".ssh", ".config"):
    if os.path.isdir(d):
        bad.append(f"private folder present: {d}")
if os.path.exists(".bash_history"):
    bad.append("private file present: .bash_history")
print("OK: ready to push" if not bad else "PROBLEMS:\n- " + "\n- ".join(bad))
sys.exit(1 if bad else 0)
