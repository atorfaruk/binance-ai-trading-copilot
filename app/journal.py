import json
from datetime import datetime,timezone
from pathlib import Path
class TradeJournal:
    def __init__(self,path="trade_journal.jsonl"): self.path=Path(path)
    def record(self,event,**data):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        row={"timestamp":datetime.now(timezone.utc).isoformat(),"event":event,**data}
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(row,separators=(",",":"),default=str)+"\n")
    def record_proposal(self,p): self.record("proposal",proposal=p.model_dump())
    def record_execution(self,p,e): self.record("execution",proposal_fingerprint=p.fingerprint,execution=str(e))
    def record_monitor_state(self,symbol,price,state): self.record("monitor",symbol=symbol,price=price,state=state)
