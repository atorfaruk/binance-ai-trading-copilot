from dataclasses import dataclass
from enum import Enum
class TradeState(str,Enum):
    OPEN="OPEN"; TP1_HIT="TP1_HIT"; TP2_HIT="TP2_HIT"; STOPPED="STOPPED"; CLOSED="CLOSED"
@dataclass
class PositionMonitor:
    symbol:str; entry:float; stop:float; tp1:float; tp2:float; state:TradeState=TradeState.OPEN
    def update(self,price):
        if self.state in {TradeState.STOPPED,TradeState.TP2_HIT,TradeState.CLOSED}: return self.state
        if price<=self.stop: self.state=TradeState.STOPPED
        elif price>=self.tp2: self.state=TradeState.TP2_HIT
        elif price>=self.tp1: self.state=TradeState.TP1_HIT
        return self.state
    def close(self): self.state=TradeState.CLOSED; return self.state
