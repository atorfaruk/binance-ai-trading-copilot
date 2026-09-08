from dataclasses import dataclass

class RiskError(ValueError): pass

@dataclass(frozen=True)
class RiskResult:
    entry: float
    stop: float
    take_profit: float
    position_size: float
    risk_amount: float
    risk_percent: float
    reward_amount: float
    rr: float

def calculate_position_size(account_balance,entry,stop,take_profit,max_risk_percent=1.0,min_rr=2.0):
    if account_balance<=0 or entry<=0 or stop<=0 or take_profit<=0: raise RiskError("positive values required")
    if stop>=entry: raise RiskError("LONG stop must be below entry")
    if take_profit<=entry: raise RiskError("LONG take-profit must be above entry")
    if not 0<max_risk_percent<=1: raise RiskError("risk maximum must be <= 1%")
    if min_rr<2: raise RiskError("minimum R:R policy cannot be below 1:2")
    unit_risk=entry-stop; unit_reward=take_profit-entry; rr=unit_reward/unit_risk
    if rr<min_rr: raise RiskError(f"R:R {rr:.2f} is below required {min_rr:.2f}")
    risk=account_balance*max_risk_percent/100
    size=risk/unit_risk; actual=size*unit_risk; reward=size*unit_reward
    pct=actual/account_balance*100
    if pct>max_risk_percent+1e-9: raise RiskError("risk exceeds maximum")
    return RiskResult(entry,stop,take_profit,size,actual,pct,reward,rr)
