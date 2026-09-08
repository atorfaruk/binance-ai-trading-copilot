import pytest
from app.approval import HumanApprovalGate,ApprovalError
from app.risk_engine import calculate_position_size
from app.trade_proposal import build_proposal
def p():
    r=calculate_position_size(10000,100,95,110)
    return build_proposal("BTCUSDT",85,90,99,101,95,107,110,r,["test"])
def test_yes(): 
    x=p(); g=HumanApprovalGate(); assert g.request(x,"YES"); assert g.is_approved(x)
def test_lowercase_rejected():
    x=p(); assert not HumanApprovalGate().request(x,"yes")
def test_changed_invalidates():
    x=p(); g=HumanApprovalGate(); g.request(x,"YES"); x.stop=94; assert not g.is_approved(x)
def test_bad_fingerprint():
    x=p(); x.fingerprint="bad"
    with pytest.raises(ApprovalError): HumanApprovalGate().request(x,"YES")
