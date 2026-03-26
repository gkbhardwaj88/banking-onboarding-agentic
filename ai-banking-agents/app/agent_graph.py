from langgraph.graph import StateGraph
from typing import TypedDict
from . import agent

class KYCState(TypedDict):
    pan_number: str | None
    aadhaar_number: str | None
    aadhaar_verified: bool
    kyc_ok: bool
    deposit_amount: int
    payment_order: dict | None
    action: str | None


def router(state: KYCState):
    decision = agent.decide(state)
    state["action"] = decision.get("action")
    state["decision"] = decision
    return state


def runner(state: KYCState):
    act = state.get("action")
    if not act or act == "idle":
        return state
    res = agent.run_tool(act, state.get("tool_params", {}))
    if "order_id" in res:
        state["payment_order"] = res
    if res.get("parsed", {}).get("pan"):
        state["pan_number"] = res["parsed"]["pan"]
    if res.get("success"):
        state["aadhaar_verified"] = True
    return state


graph = StateGraph(KYCState)
graph.add_node("route", router)
graph.add_node("run_tool", runner)
graph.add_edge("route", "run_tool")
graph.add_edge("run_tool", "route")
workflow = graph.compile()
