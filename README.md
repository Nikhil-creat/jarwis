# Jarwis

One commander, 99 specialist AI assistants. Jarwis plans a mission, routes work to the right assistants, and waits for your approval before anything risky happens.

Designed and developed by **Nikhil Chary Sriramoju**.

## Features

| Area | Details |
|---|---|
| Home | Scanner belt: product cards dissolve into the compact code an AI agent reads (canvas particles, hover, drag) |
| Assistants | Commander-00 plus 99 assistants in six clusters. Search, filter, chat with any of them, route a task with AI, or forge your own |
| AI | Vercel function `api/chat.py`. Auto-detects Groq and Gemini models, picks a fast and a deep model, falls back between providers |
| Command center | Plan a mission with AI, run it with checkpoints, a token budget governor, an approval gate and saved missions |
| Chat dock | Multi-turn, voice input, spoken replies, saved history with Clear |
| Experience | Dark mode, Ctrl/Cmd+K page jumper, installable offline app (PWA), responsive mobile menu |
| Pages | Home, Assistants, Command center, Architecture, Security, Roadmap, Status, Builder, FAQ, Contact, Privacy, Terms, custom 404 |
| SEO | Titles, descriptions, canonical tags, one H1 per page, breadcrumbs, Open Graph and Twitter cards, JSON-LD (WebSite, Organization and local business, Person, FAQPage, BreadcrumbList), sitemap, robots, llms.txt, humans.txt, security.txt, favicons |

## Run locally

```
python3 build.py                  # regenerate all pages
python3 -m http.server 8080       # open http://localhost:8080
```

Build with your own details:

```
DOMAIN=https://yourdomain.com CONTACT_EMAIL=you@example.com \
BIZ_LOCALITY=City BIZ_REGION=State BIZ_COUNTRY=IN BIZ_PHONE=+91... python3 build.py
```

`CONTACT_EMAIL` enables the contact form and security.txt. The `BIZ_*` values add the business address to the structured data. Leave any of them out and that part is skipped.

## AI keys

Set these in Vercel (Settings, Environment Variables). Never commit keys.

- `GROQ_API_KEY` from console.groq.com/keys
- `GEMINI_API_KEY` from aistudio.google.com/app/apikey
- `ALLOWED_ORIGIN` optional, extra allowed site addresses separated by commas. The site's own address is always allowed.

Open `/status/` to see which models were detected.

## Project layout

```
index.html, */index.html   generated pages (edit build.py, then rebuild)
assets/                    site.css, belt.js (scanner), ai.js (chat, palette, theme), assistants.js
api/chat.py                Vercel serverless AI endpoint
backend/                   optional FastAPI, LangGraph commander and Docker sandbox starters
build.py                   page generator
```

## Privacy

No accounts and no trackers. Chats are sent to the AI provider only to answer you and are not stored in a database. Chat history, saved missions, custom assistants and the theme stay in your browser.

## License

MIT. See `LICENSE`.
