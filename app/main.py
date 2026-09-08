import argparse,os
from dotenv import load_dotenv
from .approval import HumanApprovalGate
from .execution import SpotExecutionFirewall
from .journal import TradeJournal
from .mcp_client import MockBinanceClient,BinanceMCPClient
from .risk_engine import calculate_position_size,RiskError
from .scanner import MarketScanner
from .trade_proposal import build_proposal

def symbols(): return [x.strip().upper() for x in os.getenv("SYMBOLS","BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT").split(",") if x.strip()]
def print_proposal(p):
    print("\n=== TRADE PROPOSAL ===")
    print(f"{p.symbol} {p.direction} | entry {p.entry_zone.low:.4f}-{p.entry_zone.high:.4f} | stop {p.stop:.4f} | TP1 {p.tp1:.4f} | TP2 {p.tp2:.4f}")
    print(f"size={p.position_size:.8f} risk={p.risk_amount:.4f} ({p.risk_percent:.4f}%) R:R={p.rr:.2f} score={p.score:.2f} confidence={p.confidence:.2f}")
    print("SHA-256:",p.fingerprint)
    for r in p.rationale: print(" -",r)

def choose(results,balance,risk_pct,rr):
    if not results or results[0].score<60:return None
    best=results[0]; f=best.features; entry=f.price; stop=min(f.support,entry*.985); tp1=entry+(entry-stop)*1.5; tp2=entry+(entry-stop)*2.5
    try:r=calculate_position_size(balance,entry,stop,tp2,risk_pct,rr)
    except RiskError:return None
    return build_proposal(best.symbol,best.score,min(100,best.score*.9+10),entry*.9975,entry*1.0025,stop,tp1,tp2,r,[f"EMA5 {f.ema_fast:.4f} > EMA10 {f.ema_slow:.4f}",f"Momentum {f.momentum:.2f}/100",f"Volume ratio {f.volume_ratio:.2f}x"])

def demo():
    load_dotenv(); c=MockBinanceClient(); rs=MarketScanner(c).scan(symbols())
    print("SAFE DEMO: synthetic data only; no real orders can be placed.")
    for x in rs: print(f"{x.symbol:10} score={x.score:6.2f} price={x.features.price:.4f}")
    p=choose(rs,10000,float(os.getenv("MAX_RISK_PERCENT","1")),float(os.getenv("MIN_RR","2")))
    if not p: print("No qualifying setup."); return
    print_proposal(p); TradeJournal(os.getenv("JOURNAL_PATH","trade_journal.jsonl")).record_proposal(p)
    gate=HumanApprovalGate(); response=input("\nApprove this exact trade? YES/NO: "); print("Approval:",gate.request(p,response))
    try: SpotExecutionFirewall(False).execute(c,p,gate)
    except Exception as e: print("Execution blocked safely:",e)

def scan():
    load_dotenv(); c=BinanceMCPClient.from_env()
    try:
        for x in MarketScanner(c).scan(symbols()): print(x.symbol,x.score)
    finally:c.close()

if __name__=="__main__":
    a=argparse.ArgumentParser(); a.add_argument("--demo",action="store_true"); a.add_argument("--scan",action="store_true"); x=a.parse_args()
    if x.scan: scan()
    else: demo()
