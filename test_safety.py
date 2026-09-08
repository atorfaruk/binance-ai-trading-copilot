import pytest
from app.execution import SpotExecutionFirewall,ExecutionError,validate_tool_name
from app.approval import HumanApprovalGate
from app.mcp_client import MockBinanceClient
from app.risk_engine import calculate_position_size,RiskError
from app.trade_proposal import build_proposal
def p():
    r=calculate_position_size(10000,100,95,110)
    return build_proposal("ETHUSDT",88,90,99,101,95,107,110,r,["safety"])
def test_no_execution_without_approval():
    with pytest.raises(ExecutionError): SpotExecutionFirewall(True).execute(MockBinanceClient(),p(),HumanApprovalGate())
def test_changed_proposal_invalidates():
    x=p(); g=HumanApprovalGate(); assert g.request(x,"YES"); x.tp2=111
    with pytest.raises(ExecutionError): SpotExecutionFirewall(True).execute(MockBinanceClient(),x,g)
def test_live_default_false(): assert not SpotExecutionFirewall().allow_live_execution
def test_risk_limit():
    with pytest.raises(RiskError): calculate_position_size(10000,100,95,110,2)
def test_rr_floor():
    with pytest.raises(RiskError): calculate_position_size(10000,100,95,109)
def test_forbidden():
    for x in ["futures.newOrder","margin.newOrder","wallet.withdraw","spot.transfer","spot.deposit"]:
        with pytest.raises(ExecutionError): validate_tool_name(x)
