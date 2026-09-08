from dataclasses import dataclass
from statistics import mean

def sma(values, period):
    if len(values) < period: raise ValueError("not enough values")
    return mean(values[-period:])

def ema(values, period):
    if len(values) < period: raise ValueError("not enough values")
    k=2/(period+1); x=float(values[0])
    for v in values[1:]: x=(float(v)-x)*k+x
    return x

def momentum_score(closes, lookback=5):
    if len(closes)<=lookback: raise ValueError("not enough closes")
    change=float(closes[-1])/float(closes[-1-lookback])-1
    return max(0,min(100,50+change*1000))

@dataclass(frozen=True)
class MarketFeatures:
    price: float
    ema_fast: float
    ema_slow: float
    momentum: float
    volume_ratio: float
    support: float
    resistance: float
    trend_score: float
    momentum_score_value: float
    volume_score: float
    structure_score: float

def calculate_features(closes, volumes, fast_period=5, slow_period=10, structure_period=10):
    if len(closes)!=len(volumes): raise ValueError("length mismatch")
    n=max(slow_period,structure_period,6)
    if len(closes)<n: raise ValueError(f"need at least {n} candles")
    price=float(closes[-1]); ef=ema(closes,fast_period); es=ema(closes,slow_period)
    av=mean(float(x) for x in volumes[-slow_period:])
    vr=float(volumes[-1])/av if av else 0
    w=[float(x) for x in closes[-structure_period:]]; support=min(w); resistance=max(w)
    trend=100 if ef>es else 25
    mom=momentum_score(closes)
    vol=max(0,min(100,50+(vr-1)*50))
    width=resistance-support
    structure=50 if width<=0 else max(0,min(100,100-abs((price-support)/width-.65)*100))
    return MarketFeatures(price,ef,es,mom,vr,support,resistance,trend,mom,vol,structure)

def setup_score(f):
    return round(max(0,min(100,f.trend_score*.35+f.momentum_score_value*.25+f.volume_score*.2+f.structure_score*.2)),2)
