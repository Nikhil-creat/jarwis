from fastapi import FastAPI
app=FastAPI(title="Jarwis API",docs_url=None)
CLUSTERS=[{"name":"Software, Cloud & Security","count":18},{"name":"AI, Data & Research","count":14},{"name":"Productivity & Daily Ops","count":16},{"name":"Creative & Communication","count":13},{"name":"Business, Finance & Risk","count":14},{"name":"User-Forged","count":24}]
@app.get("/api/health")
def health():return {"status":"ok"}
@app.get("/api/clusters")
def clusters():return CLUSTERS
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["https://jarwis-six.vercel.app"], allow_methods=["POST"], allow_headers=["*"])
class Msg(BaseModel):
    message: str
@app.post("/chat")
async def chat(m: Msg):
    from router import discover, complete
    av = await discover()
    return {"reply": await complete("fast", "You are Jarwis, a concise assistant. " + m.message[:2000], av)}
