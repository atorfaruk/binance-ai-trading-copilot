from dataclasses import dataclass
from .trade_proposal import calculate_fingerprint

class ExecutionError(RuntimeError): pass
ALLOWED_MCP_TOOLS=frozenset({"spot.exchangeInfo","spot.tickerPrice","spot.getAccount","spot.newOrder","spot.getOrder","spot.getOpenOrders","spot.deleteOrder","spot.deleteOpenOrders"})
FORBIDDEN_FRAGMENTS=("futures","margin","withdraw","transfer","deposit")

def validate_tool_name(name):
    low=name.lower()
    if any(x in low for x in FORBIDDEN_FRAGMENTS): raise ExecutionError(f"Forbidden capability: {name}")
    if name not in ALLOWED_MCP_TOOLS: raise ExecutionError(f"MCP tool is not allow-listed: {name}")

@dataclass(frozen=True)
class ExecutionResult:
    order:object
    proposal_fingerprint:str

class SpotExecutionFirewall:
    def __init__(self,allow_live_execution=False): self.allow_live_execution=allow_live_execution
    def execute(self,client,proposal,approval_gate):
        current=calculate_fingerprint(proposal)
        if proposal.fingerprint!=current: raise ExecutionError("Proposal fingerprint mismatch")
        if not approval_gate.is_approved(proposal): raise ExecutionError("Exact proposal has not received explicit YES approval")
        if proposal.direction!="LONG": raise ExecutionError("MVP supports LONG Spot trades only")
        if proposal.risk_percent>1: raise ExecutionError("Risk exceeds 1% maximum")
        if proposal.rr<2: raise ExecutionError("R:R is below 1:2")
        if not self.allow_live_execution: raise ExecutionError("Live execution is disabled")
        validate_tool_name("spot.newOrder")
        order=client.call_tool("spot.newOrder",{"symbol":proposal.symbol,"side":"BUY","type":"MARKET","quantity":proposal.position_size,"newOrderRespType":"FULL"})
        return ExecutionResult(order,current)
