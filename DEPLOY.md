# Deploy Jarwis on Vercel (free)
1. vercel.com -> Add New -> Project -> import the `jarwis` repo. No build settings needed. Deploy.
2. Get free keys: Groq at console.groq.com/keys, Gemini at aistudio.google.com/app/apikey.
3. Vercel -> Project -> Settings -> Environment Variables: add GROQ_API_KEY and GEMINI_API_KEY (and optionally ALLOWED_ORIGIN). Redeploy.
4. Open /status/ on your site. It lists the models Jarwis auto-detected for each provider.
5. Open the chat dock or Command center -> Plan with AI.
Never put keys in the repo.
