# SovrAI MCP (Management Control Program)

## Overview
SovrAI MCP is an advanced multi-strategy hedge fund management system that coordinates various AI agents to manage investments across multiple asset classes and platforms. The system employs a hierarchical architecture with a central Management Control Program (MCP) orchestrating specialized agents for different aspects of fund management.

## System Architecture

### Core Components

1. **Management Control Program (MCP)**
   - Central coordination system
   - Agent lifecycle management
   - Strategy allocation and risk management
   - System-wide monitoring and logging

2. **Market Intelligence Agents**
   - Daily market digest generation
   - Technical analysis
   - Fundamental analysis
   - News and sentiment analysis
   - Market data integration (yfinance, etc.)

3. **Trading Desk Agents**
   - ETF trading strategies
   - Stock trading strategies
   - Options trading (long positions)
   - Cryptocurrency trading
   - Order execution and management

4. **Risk Management Agents**
   - Portfolio risk analysis
   - Position sizing
   - Correlation analysis
   - Drawdown management
   - VaR calculations

5. **Accounting & Reporting Agents**
   - Performance tracking
   - NAV calculations
   - P&L reporting
   - Tax documentation
   - Compliance reporting

## Technology Stack

- **Programming Language**: Python 3.x
- **Data Sources**: 
  - yfinance for market data
  - Additional sources TBD
- **Database**: TBD
- **API Integration**: REST APIs for various trading platforms

## Getting Started

### Prerequisites
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Copy `config.example.yml` to `config.yml`
2. Add your API keys and credentials
3. Configure strategy parameters

### Running the System
```bash
python src/mcp.py
```

## Project Structure
```
sovrai_mcp/
├── src/
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── core.py
│   ├── agents/
│   │   ├── market_intelligence/
│   │   ├── trading/
│   │   ├── risk/
│   │   └── accounting/
│   ├── utils/
│   └── config/
├── tests/
├── docs/
├── config.example.yml
├── requirements.txt
└── README.md
```

## Development Status
- [x] Initial project setup
- [ ] MCP core implementation
- [ ] Market Intelligence Agent integration
- [ ] Trading Desk Agent implementation
- [ ] Risk Management System
- [ ] Accounting & Reporting System

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This software is for educational and research purposes only. Trading financial instruments carries significant risks. Always consult with financial and legal professionals before making investment decisions. 