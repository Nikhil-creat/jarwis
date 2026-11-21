# Deploy Jarwis safely
1. Make a NEW private-then-public repo. Never run git in your home folder.
2. cd into this folder only:  cd ~/jarwis && git init && git add . && git status   (check no .ssh or .env appear)
3. git commit -m "Jarwis site" && git branch -M main && git remote add origin <new-repo-url> && git push -u origin main
4. GitHub Pages: Settings -> Pages -> main / root. Add your custom domain there, then DNS CNAME to <user>.github.io.
5. AI chat: deploy backend/ on Render, then set content="https://your-api/chat" in the jarwis-api meta tag (build.py), rebuild with
   DOMAIN=https://yourdomain python3 build.py. Keep API keys only in Render env vars, never in this repo.
