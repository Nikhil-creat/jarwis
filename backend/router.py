"""Model router: discover models, route by task tier, fall back, go offline to Ollama."""
import os, httpx
TIERS = {"fast": ["llama-3.1-8b-instant", "gemini-2.0-flash"], "deep": ["gpt-4.1", "claude-sonnet-4-5", "gemini-2.5-pro"]}
PROVIDERS = {
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
    "ollama": (os.getenv("OLLAMA_URL", "http://ollama:11434") + "/v1", None),
}
async def discover() -> dict[str, list[str]]:
    found = {}
    async with httpx.AsyncClient(timeout=5) as c:
        for name, (url, key) in PROVIDERS.items():
            token = os.getenv(key) if key else "ollama"
            if not token: continue
            try:
                r = await c.get(f"{url}/models", headers={"Authorization": f"Bearer {token}"})
                found[name] = [m["id"] for m in r.json().get("data", [])]
            except Exception:
                continue
    return found
async def complete(task_tier: str, prompt: str, available: dict[str, list[str]], offline: bool = False) -> str:
    order = ["ollama"] if offline else [p for p in PROVIDERS if p in available] + (["ollama"] if "ollama" in available else [])
    async with httpx.AsyncClient(timeout=60) as c:
        for p in dict.fromkeys(order):
            url, key = PROVIDERS[p]
            model = next((m for m in TIERS[task_tier] if m in available[p]), available[p][0])
            try:
                r = await c.post(f"{url}/chat/completions", headers={"Authorization": f"Bearer {os.getenv(key) if key else 'ollama'}"},
                                 json={"model": model, "messages": [{"role": "user", "content": prompt}]})
                if r.status_code == 429: continue
                return r.json()["choices"][0]["message"]["content"]
            except Exception:
                continue
    raise RuntimeError("all providers failed")
