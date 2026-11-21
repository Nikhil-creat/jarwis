"""Commander-00: plan -> delegate -> verify -> human approval -> finish (LangGraph)."""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
class Mission(TypedDict):
    goal: str; plan: list[str]; results: dict; spent: int; approved: bool
BUDGET = 200_000
def plan(s: Mission): return {"plan": ["design", "build", "test", "security"]}
def delegate(s: Mission):
    # A2A hook: send each task to the matching assistant card; replace with real calls
    return {"results": {t: f"{t}: done" for t in s["plan"]}, "spent": s["spent"] + 5_000}
def verify(s: Mission):
    if s["spent"] > BUDGET: raise RuntimeError("budget exceeded")
    return {}
def gate(s: Mission):
    ok = interrupt({"ask": "Approve deploy?", "summary": s["results"]})  # HITL pause
    return {"approved": bool(ok)}
g = StateGraph(Mission)
for n, f in [("plan", plan), ("delegate", delegate), ("verify", verify), ("gate", gate)]: g.add_node(n, f)
g.set_entry_point("plan"); g.add_edge("plan", "delegate"); g.add_edge("delegate", "verify"); g.add_edge("verify", "gate"); g.add_edge("gate", END)
app = g.compile(checkpointer=MemorySaver())
