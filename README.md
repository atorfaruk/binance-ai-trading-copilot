# Binance AI Trading Copilot

Safety-first Binance MCP / Agent OS hackathon MVP.

Flow: Market Scan -> Features -> 0-100 Score -> Risk/Position Sizing -> Trade Proposal -> exact YES approval -> Spot firewall -> Monitoring -> JSONL Journal.

## Safety
- `ALLOW_LIVE_EXECUTION=false` by default.
- `--demo` uses synthetic data and a client that refuses every order.
- Spot tools only; Futures, Margin, withdrawals, transfers and deposits are blocked.
- Exact `YES` is required.
- Approval is bound to a SHA-256 fingerprint of execution-critical fields; changing them invalidates approval.
- Maximum risk is 1%; minimum R:R is 1:2.
- No Binance API keys are stored by this project.

## Components
Local Python: indicators, scoring, risk, sizing, proposal schema/fingerprint, approval, firewall, monitoring and journal.
MCP adapter: Binance market/account/order connectivity. The exact MCP host command is configured by you; this project does not invent a Binance package, credential flow, or undocumented API.

## Windows PowerShell
```powershell
cd .\binance-ai-trading-copilot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m app.main --demo
pytest -q
```
If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Optional MCP configuration:
```powershell
Copy-Item .env.example .env
```
Set `BINANCE_MCP_COMMAND` and `BINANCE_MCP_ARGS` to the actual MCP host used by your Binance environment. Do not put API keys here.

## Hackathon demo
Run `python -m app.main --demo`, show the scan, score, 1% risk calculation, proposal fingerprint, exact YES gate, then show that live execution remains blocked. Explain that the MCP adapter is isolated so the same deterministic safety layer can sit in front of the host's Binance Spot tools.

## Before any live test
Keep `ALLOW_LIVE_EXECUTION=false` for the hackathon demo unless you have reviewed the MCP host, account permissions and every tool exposed to the agent. This repository is not financial advice.
