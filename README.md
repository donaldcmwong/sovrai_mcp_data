# MCP Market Data Demo

A tiny **Model Context Protocol (MCP)** tool server with a matching async client.  
It exposes simple market-data utilities (price, OHLCV, summary) that an LLM can call.  
Built with Python, `fastmcp`, `yfinance`, and `pydantic`.

---

## ✨ Features
- **MCP Tool Server (`core.py`)**
  - `market_data(request)` → historical OHLCV via yfinance
  - `current_price(symbols)` → current prices
  - `market_summary(symbols)` → key metrics bundle

- **Async Client (`client.py`)**
  - Connects to the MCP server and calls tools
  - Pretty-prints JSON results

- **Deterministic Tests**
  - Mock `yfinance.Ticker` so CI runs without network flakiness
  - Run with `pytest -q`

- **Continuous Integration**
  - GitHub Actions workflow runs tests on push/PR
  - Green check shows reproducibility

---

## 🚀 Quickstart (macOS/Linux)

Clone and enter project:

```bash
git clone https://github.com/<your-username>/mcp-market-data-demo.git
cd mcp-market-data-demo
