import pytest
from app.execution import SpotExecutionFirewall,ExecutionError,validate_tool_name
from app.approval import HumanApprovalGate
from app.mcp_client import MockBinanceClient
from app.risk_engine import calculate_position_size
from app.trade_proposal import build_proposal
def p():
    r=calculate_position_size(10000,100,95,110)
    return build_proposal("BTCUSDT",90,90,99,101,95,107,110,r,["test"])
def test_default_off(): assert SpotExecutionFirewall().allow_live_execution is False
def test_needs_yes():
    with pytest.raises(ExecutionError): SpotExecutionFirewall(True).execute(MockBinanceClient(),p(),HumanApprovalGate())
def test_mock_refuses_order():
    with pytest.raises(Exception,match="refuses all order"): MockBinanceClient().call_tool("spot.newOrder",{})
def test_spot_only():
    with pytest.raises(ExecutionError): validate_tool_name("futures.newOrder")
    with pytest.raises(ExecutionError): validate_tool_name("margin.newOrder")
    with pytest.raises(ExecutionError): validate_tool_name("spot.withdraw")
