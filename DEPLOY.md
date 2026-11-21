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
