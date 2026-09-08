import hashlib,json
from datetime import datetime,timezone
from pydantic import BaseModel,ConfigDict,Field
from .risk_engine import RiskResult

class EntryZone(BaseModel):
    low: float=Field(gt=0)
    high: float=Field(gt=0)

class TradeProposal(BaseModel):
    model_config=ConfigDict(extra="forbid")
    symbol:str
    direction:str
    entry_zone:EntryZone
    stop:float=Field(gt=0)
    tp1:float=Field(gt=0)
    tp2:float=Field(gt=0)
    position_size:float=Field(gt=0)
    risk_amount:float=Field(gt=0)
    risk_percent:float=Field(gt=0,le=1)
    rr:float=Field(ge=2)
    score:float=Field(ge=0,le=100)
    confidence:float=Field(ge=0,le=100)
    rationale:list[str]
    created_at:str
    fingerprint:str

def fingerprint_payload(p):
    d=p.model_dump() if isinstance(p,TradeProposal) else dict(p)
    return {"symbol":d["symbol"],"direction":d["direction"],
            "entry_low":d["entry_zone"]["low"],"entry_high":d["entry_zone"]["high"],
            "stop":d["stop"],"tp1":d["tp1"],"tp2":d["tp2"],
            "position_size":d["position_size"],"risk_amount":d["risk_amount"],
            "risk_percent":d["risk_percent"],"rr":d["rr"]}

def calculate_fingerprint(p):
    raw=json.dumps(fingerprint_payload(p),sort_keys=True,separators=(",",":"),allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()

def proposal_fingerprint(p): return calculate_fingerprint(p)

def build_proposal(symbol,score,confidence,entry_low,entry_high,stop,tp1,tp2,risk,rationale):
    if entry_low>entry_high: raise ValueError("bad entry zone")
    p=TradeProposal(symbol=symbol,direction="LONG",entry_zone={"low":entry_low,"high":entry_high},
        stop=stop,tp1=tp1,tp2=tp2,position_size=risk.position_size,risk_amount=risk.risk_amount,
        risk_percent=risk.risk_percent,rr=risk.rr,score=score,confidence=confidence,
        rationale=rationale,created_at=datetime.now(timezone.utc).isoformat(),fingerprint="pending")
    p.fingerprint=calculate_fingerprint(p); return p
