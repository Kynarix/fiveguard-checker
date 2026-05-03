# FiveGuard Checker v1.2

Python-based account checker for **my.fiveguard.net**

## Author
- **Developer:** PheXorA
- **GitHub:** [https://github.com/Kynarix](https://github.com/Kynarix)
- **Repository:** [https://github.com/Kynarix/fiveguard-checker](https://github.com/Kynarix/fiveguard-checker)

## Features
- Multi-threaded checking (5 threads)
- Real-time dashboard with Rich
- Auto-capture balance, products & subscriptions
- JSON output for valid accounts
- Cloudflare bypass with cloudscraper

## Setup
```bash
pip install -r requirements.txt
```

## Usage
1. Put your accounts in `accounts.txt` (format: `email:password`)
2. Run the checker:
```bash
python checker.py
```

## Files
- `checker.py` - Main checker script
- `accounts.txt` - Account list (email:password format)
- `results/` - Output directory (`valid.json`)

## Requirements
- Python 3.8+
- cloudscraper
- requests
- colorama
- beautifulsoup4
- lxml
- rich

## Changelog
### v1.2
- Rebranded to PheXorA
- Version bump to v1.2
- Added error handling for scraper initialization
