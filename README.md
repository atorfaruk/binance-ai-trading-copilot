# Binance AI Trading Copilot

> The AI proposes. The risk engine validates. The human approves. The firewall executes.

A safety-first AI trading copilot built for the Binance Agent OS / MCP ecosystem.

## How It Works

Market Scan → Setup Score → Risk Check → Trade Proposal → Human YES Approval → Spot Execution Firewall

## Safety

- Live trading is OFF by default
- Exact YES approval is required
- SHA-256 fingerprint protects each proposal
- Maximum risk: 1%
- Minimum risk/reward: 1:2
- Spot trading only
- Futures and Margin are blocked
- Withdrawals, deposits and transfers are blocked
- Demo mode uses synthetic data
- Mock execution cannot place real orders
- No Binance API keys are stored

## Main Components

- Market Scanner
- Scoring Engine
- Risk Engine
- Trade Proposal
- Human Approval Gate
- Spot Execution Firewall
- Trade Monitoring
- Trade Journal
- Safety Tests

## Safe Demo

Run:

`python -m app.main --demo`

The demo uses synthetic data and cannot place a real Binance order.

## Tests

Run:

`pytest -q`

The project includes tests for approval, risk limits, proposal tampering, Spot-only restrictions and execution safety.

## Hackathon Vision

Most AI trading systems focus on giving agents more autonomy.

This project takes a safety-first approach:

**Give AI better analysis, but keep humans in control.**

## License

MIT
