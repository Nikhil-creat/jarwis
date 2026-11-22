# Jarwis: build, push and deploy (from Termux)

## 1. Update the site
```
cd ~/jarwis
DOMAIN=https://jarwis-six.vercel.app CONTACT_EMAIL="your@email" BIZ_LOCALITY="Warangal" BIZ_REGION="Telangana" BIZ_COUNTRY="IN" python3 build.py
git add .
git status        # check: no .ssh, .env or .bash_history
git commit -m "Update Jarwis"
git push
```
Vercel redeploys automatically in about a minute.

## 2. Keys (one time)
Vercel -> Project -> Settings -> Environment Variables: add GROQ_API_KEY and GEMINI_API_KEY, then Deployments -> Redeploy.

## 3. Custom domain (optional)
Vercel -> Settings -> Domains -> add it and copy the DNS records to your registrar. Then rebuild with DOMAIN=https://yourdomain and push.

## 4. After launch
- Open /status/ and confirm both AI providers are green.
- Add the site to Google Search Console and submit /sitemap.xml.
- Test the social preview by sharing a link in WhatsApp or LinkedIn.
- Rotate any API key that was ever pasted into a chat or a repo.

## Before every push
```
python3 check.py      # must print: OK: ready to push
```
Then open https://jarwis-six.vercel.app/status/ after Vercel finishes. The line "Site build" must show a new date and time. Always use this production address. Long addresses with random letters are frozen old deployments.

## Which address to open
Always test on https://jarwis-six.vercel.app (the main address). Vercel also shows long addresses with random letters, for example ending in -nikhil-creats-projects.vercel.app. Those are frozen copies of one old deployment, so they never show your latest work.

## Live data sources
No keys are needed. Sources: GitHub API, Open-Meteo, Frankfurter, Hacker News API, Crossref, Wikipedia. Open-Meteo is free for non-commercial use and needs the credit line that is already on the Live data page. If you ever make the site commercial, check each source's terms first.
