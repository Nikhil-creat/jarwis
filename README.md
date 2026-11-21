# Jarwis

One commander, 99+ specialised AI assistants. Jarwis plans a mission, hands the work to the right assistants, checks it in a sandbox, and waits for your approval before anything risky happens.

This repo is a static site plus a small FastAPI backend.

## What is inside

| Area | Details |
|---|---|
| Home | Scanner belt: product cards dissolve into the compact code an AI agent reads (canvas particles, drag and hover) |
| Command center | Scripted mission preview with checkpoints, approval gate and a token budget governor |
| Assistants | Searchable matrix of 99 assistants in six clusters |
| Pages | Architecture, Security, Roadmap, Status (live checks), custom 404 |
| AI chat | "Ask Jarwis" dock with voice input and spoken replies; uses the backend when configured |
| Productivity | Ctrl/Cmd+K page jumper, installable offline app (PWA) |
| SEO | Canonical tags, Open Graph and Twitter cards, JSON-LD (WebSite, BreadcrumbList, ProfessionalService), `sitemap.xml`, `robots.txt`, `llms.txt`, favicon |
| Backend | `backend/`: model router (Groq, OpenAI, Ollama with fallback), LangGraph commander with approval interrupt, Docker sandbox runner |

## Run locally

```
python3 build.py                 # regenerate all pages
python3 -m http.server 8080      # open http://localhost:8080
```

Set your own domain before publishing:

```
DOMAIN=https://yourdomain.com python3 build.py
```

## Backend

```
cd backend
pip install -r requirements.txt
uvicorn main:app --port 8000
```

Copy `.env.example` to `.env` and add your own keys. Never commit `.env`. To connect the chat dock, set the `jarwis-api` meta tag in `build.py` to your deployed `/chat` URL, then rebuild.

Full stack with Redis, Postgres, Qdrant and Ollama: `docker compose up`.

## Deploy

Import the repo on Vercel (static, no build settings). The site expects to be served from the domain root, so use Vercel or a custom domain rather than a GitHub Pages project URL.

## Security

- Risky actions (deploys, pushes, sends) always wait for human approval.
- Keep API keys in your host's environment variables only.
- Generated code runs in a locked-down container with no network, a memory cap and dropped capabilities.

## License

MIT. See `LICENSE`.
