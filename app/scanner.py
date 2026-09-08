from dataclasses import dataclass
from .scoring import calculate_features,setup_score
@dataclass(frozen=True)
class ScanResult:
    symbol:str; features:object; score:float
def _extract(klines):
    return [float(c[4]) for c in klines],[float(c[5]) for c in klines]
class MarketScanner:
    def __init__(self,client,interval="1h",limit=100): self.client=client; self.interval=interval; self.limit=limit
    def scan_symbol(self,symbol):
        k=self.client.call_tool("spot.klines",{"symbol":symbol.upper(),"interval":self.interval,"limit":self.limit})
        closes,volumes=_extract(k); f=calculate_features(closes,volumes)
        return ScanResult(symbol.upper(),f,setup_score(f))
    def scan(self,symbols): return sorted([self.scan_symbol(s) for s in symbols],key=lambda x:x.score,reverse=True)
