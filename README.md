# Binance Futures Testnet Trading Bot

A Python application for placing Market, Limit, and Stop-Market orders on the Binance Futures Testnet (USDT-M). This project uses native `requests` for robust control over API requests, and provides a polished CLI interface using `argparse` and `rich`.

## Project Structur
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # API Client and HMAC-SHA256 Signature Logic
│   ├── logging_config.py  # Structured Logger config
│   ├── orders.py          # Order execution wrappers
│   └── validators.py      # Input Constraints and Validation
├── cli.py                 # Main CLI Entry point
├── .env.example           # Example environment file
├── requirements.txt       # Dependencies
└── README.md              # Project Documentation
```

## Setup Instructions

1. **Clone or Extract** the project folder.
2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   
   # For Linux/Mac:
   source venv/bin/activate  
   
   # For Windows:
   venv\Scripts\activate
   ```
3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your [Binance Futures Testnet](https://testnet.binancefuture.com) API credentials.
   ```bash
   cp .env.example .env
   ```
   Open `.env` and configure:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_secret_key
   ```

## Usage Examples

The bot is executed via `cli.py`. You can use `--help` to see all options:
```bash
python cli.py --help
```

### 1. Place a Market Order
Buys 0.001 BTCUSDT at the current market price.
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

### 2. Place a Limit Order
Places a Limit order to sell 0.005 BTCUSDT at a specific price (e.g., $95,000). Requires `--price`.
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.005 --price 95000
```

### 3. Place a Stop-Market Order (Bonus)
Places a Stop-Market order. Requires `--stop-price`.
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.001 --stop-price 60000
```

## Features & Assumptions

### Features
- **Structured Code**: Clear separation between API Logic (`client.py`), Validation (`validators.py`), Business Logic (`orders.py`) and Presentation (`cli.py`).
- **Enhanced CLI UX (Bonus)**: Uses `rich` for formatting beautiful tables, colorized errors, and layout execution details on the console.
- **Robust Exception Handling**: Cleanly captures and displays Binance API-specific errors, input validation errors, and raw network timeouts.
- **Detailed Logging**: All request endpoints, masked payloads, responses, and errors are appended with ISO timestamps natively in JSON strings to `bot.log`. 

### Assumptions
- **Futures Only**: This bot connects **only** to the Binance Futures Testnet (`https://testnet.binancefuture.com`). It does not target USD-S (Spot) endpoints.
- **Good-Till-Cancelled (GTC)**: Limit orders strictly default to the `GTC` time in force protocol, which is standard.
