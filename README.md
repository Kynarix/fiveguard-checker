<div align="center">

  <h1>🔒 FiveGuard Account Checker</h1>
  <p><strong>High-performance, multi-threaded account validation suite for FiveGuard services.</strong></p>

  <img src="https://img.shields.io/badge/Version-1.2-ff1744?style=for-the-badge&logo=semver&logoColor=white" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License">

  <br>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-project-structure">Project Structure</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-changelog">Changelog</a>
  </p>

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚡ **Multi-Threaded Engine** | Concurrent validation with 5 configurable worker threads |
| 📊 **Real-Time Dashboard** | Live Rich-powered terminal UI with progress tracking |
| 💰 **Auto Data Capture** | Extracts balance, owned products & active subscriptions |
| 🛡️ **Cloudflare Bypass** | Seamless anti-bot protection handling via cloudscraper |
| 📁 **Structured JSON Output** | Machine-readable results exported to `results/valid.json` |
| 🔄 **Auto-Retry Logic** | Intelligent retry mechanism for rate limits & server errors |
| 🎨 **Colored Logging** | Context-aware color-coded status indicators |

---

## 🚀 Installation

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) *(optional)*

### Clone & Setup

```bash
# Clone the repository
git clone https://github.com/Kynarix/fiveguard-checker.git

# Navigate to project directory
cd fiveguard-checker

# Install dependencies
pip install -r requirements.txt
```

> **Note:** Ensure `pip` is updated (`pip install --upgrade pip`) to avoid dependency conflicts.

---

## 📖 Usage

### 1. Prepare Account List

Create `accounts.txt` in the project root with the following format:

```text
email1@example.com:password1
email2@example.com:password2
email3@example.com:password3
```

> ⚠️ **One account per line.** Lines without a colon (`:`) separator are automatically skipped.

### 2. Run the Checker

```bash
python checker.py
```

### 3. View Results

Valid accounts are automatically saved to:

```
results/
└── valid.json
```

Sample `valid.json` output:

```json
[
  {
    "email": "user@example.com",
    "password": "password123",
    "username": "JohnDoe",
    "balance": "$150.00",
    "account_type": "Premium",
    "owned_products": [
      {
        "license": "FG-XXXX-XXXX",
        "ip": "192.168.1.1",
        "bought_date": "2024-01-15",
        "length": "30 Days"
      }
    ],
    "active_subscriptions": [
      {
        "license": "FG-YYYY-YYYY",
        "ip_address": "10.0.0.1",
        "time_remaining": "15 Days",
        "expires_on": "2026-05-18"
      }
    ],
    "checker": "PheXorA"
  }
]
```

---

## 🏗️ Project Structure

```
fiveguard-checker/
├── 📄 checker.py          # Core application logic
├── 📄 accounts.txt        # Input credentials list
├── 📄 requirements.txt    # Python dependencies
├── 📄 README.md           # Documentation
├── 📁 results/
│   └── 📄 valid.json      # Exported valid accounts
└── 📁 .git/               # Git metadata
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core runtime |
| **cloudscraper** | Cloudflare & anti-bot bypass |
| **requests** | HTTP session management |
| **Rich** | Terminal dashboard & UI rendering |
| **lxml** | HTML parsing & XPath extraction |
| **colorama** | Cross-platform ANSI color support |
| **concurrent.futures** | Multi-threaded execution |

---

## 📜 Changelog

### v1.2
- 🔁 Enhanced error handling for scraper initialization
- 🏷️ Rebranded checker identity to **PheXorA**
- 🐛 Fixed encoding issues on Windows (`UTF-8` support)

### v1.1
- 🎨 Initial Rich dashboard implementation
- ⚡ Multi-threaded account validation
- 📊 JSON result serialization

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/Kynarix/fiveguard-checker/issues).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.  
See the repository for full license details.

---

<div align="center">

  <p><strong>Crafted by <a href="https://github.com/Kynarix">PheXorA</a></strong></p>
  <p>
    <a href="https://github.com/Kynarix/fiveguard-checker">⭐ Star this repo</a> •
    <a href="https://github.com/Kynarix/fiveguard-checker/issues">🐛 Report Bug</a>
  </p>

</div>
