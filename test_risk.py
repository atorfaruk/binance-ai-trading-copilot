import pytest
from app.risk_engine import calculate_position_size,RiskError
def test_one_percent(): 
    r=calculate_position_size(10000,100,95,110); assert r.risk_percent<=1; assert r.risk_amount<=100; assert r.rr==pytest.approx(2)
def test_rr_rejected():
    with pytest.raises(RiskError): calculate_position_size(10000,100,95,109)
def test_risk_over_one_rejected():
    with pytest.raises(RiskError): calculate_position_size(10000,100,95,110,1.1)
