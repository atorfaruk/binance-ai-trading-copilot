import json,os,shlex,subprocess
class MCPError(RuntimeError): pass
class MCPClientProtocol:
    def call_tool(self,name,arguments): raise NotImplementedError

class MockBinanceClient(MCPClientProtocol):
    def __init__(self): self.prices={"BTCUSDT":100000.0,"ETHUSDT":4000.0,"BNBUSDT":900.0,"SOLUSDT":200.0}
    def call_tool(self,name,arguments):
        if name=="spot.tickerPrice": return {"symbol":arguments["symbol"],"price":self.prices.get(arguments["symbol"],100)}
        if name=="spot.klines":
            b=self.prices.get(arguments["symbol"],100); out=[]
            for i in range(40):
                c=b*(.965+i*.001); out.append([0,c*.997,c*1.003,c*.995,c,1000+i*20])
            return out
        if name=="spot.getAccount": return {"balances":[{"asset":"USDT","free":"10000"}]}
        if name=="spot.depth": return {"bids":[[self.prices.get(arguments["symbol"],100),10]],"asks":[]}
        if name=="spot.exchangeInfo": return {"symbols":[{"symbol":arguments.get("symbol","BTCUSDT")}]}
        if name=="spot.newOrder": raise MCPError("Mock client refuses all order placement")
        if name in {"spot.getOrder","spot.getOpenOrders"}: return {}
        raise MCPError(f"Mock client does not implement {name}")

class BinanceMCPClient(MCPClientProtocol):
    def __init__(self,command,args): self.command=command; self.args=args; self.process=None; self.request_id=0
    @classmethod
    def from_env(cls):
        raw=os.getenv("BINANCE_MCP_ARGS","")
        return cls(os.getenv("BINANCE_MCP_COMMAND","").strip(),shlex.split(raw,posix=False) if raw else [])
    def start(self):
        if not self.command: raise MCPError("BINANCE_MCP_COMMAND is required")
        self.process=subprocess.Popen([self.command,*self.args],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",bufsize=1)
        self._request("initialize",{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"binance-ai-trading-copilot","version":"1.0"}})
        self._notify("notifications/initialized",{})
    def close(self):
        if self.process:
            self.process.terminate()
            try: self.process.wait(timeout=2)
            except subprocess.TimeoutExpired: self.process.kill()
        self.process=None
    def _send(self,x):
        if not self.process or not self.process.stdin: raise MCPError("MCP process not running")
        self.process.stdin.write(json.dumps(x)+"\n"); self.process.stdin.flush()
    def _read(self):
        if not self.process or not self.process.stdout: raise MCPError("MCP process not running")
        line=self.process.stdout.readline()
        if not line: raise MCPError("MCP host closed stdout")
        try: return json.loads(line)
        except json.JSONDecodeError as e: raise MCPError("Invalid MCP JSON") from e
    def _request(self,method,params):
        self.request_id+=1; rid=self.request_id; self._send({"jsonrpc":"2.0","id":rid,"method":method,"params":params})
        while True:
            r=self._read()
            if r.get("id")==rid:
                if "error" in r: raise MCPError(str(r["error"]))
                return r.get("result")
    def _notify(self,method,params): self._send({"jsonrpc":"2.0","method":method,"params":params})
    def call_tool(self,name,arguments):
        if self.process is None: self.start()
        r=self._request("tools/call",{"name":name,"arguments":arguments})
        if isinstance(r,dict):
            if r.get("isError"): raise MCPError(str(r))
            if "structuredContent" in r: return r["structuredContent"]
            c=r.get("content")
            if isinstance(c,list):
                texts=[x.get("text") for x in c if isinstance(x,dict) and "text" in x]
                if len(texts)==1:
                    try:return json.loads(texts[0])
                    except (TypeError,json.JSONDecodeError):return texts[0]
                return texts
        return r
