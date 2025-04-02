# 🔍 SQL Injection Scanner 

## 🛡️ Description  
An advanced tool to detect SQL injection vulnerabilities in web applications with multi-threading support, IP geolocation, and detailed reporting.

## ✨ Features  
- 🚀 Multi-threaded scanning for fast results  
- 🌍 IP address detection with geolocation (city, country, ISP)  
- 📊 HTML report generation  
- 🔄 User-agent rotation to avoid detection  
- 🔌 Proxy support for anonymity  
- 📋 Verbose output mode for debugging  
- 🛡️ 50+ built-in SQLi payloads  

## ⚙️ Requirements  
- 🐍 Python 3.6+  
- 📦 Required packages:  
  ```bash
  pip install requests beautifulsoup4 colorama

🚀 Installation

    Clone the repository:
    bash
    Copy

    git clone https://github.com/yourrepo/sql-scanner.git
    cd sql-scanner

    Install dependencies:
    bash
    Copy

    pip install -r requirements.txt

🛠️ Usage
bash
Copy

python sql_scanner.py [options]

Options:
  --urls FILE       📄 File containing target URLs  
  --url URL         🌐 Single URL to test  
  --payloads FILE   💉 Custom payloads file (default: payloads.txt)  
  --proxy PROXY     🔌 Proxy URL (e.g., http://127.0.0.1:8080)  
  --threads NUM     🧵 Number of threads (default: 10)  
  --verbose         📢 Show detailed scan results  
  --report FILE     📊 HTML report filename (default: report.html)  

💡 Examples

    Scan single URL:
    bash
    Copy

    python sql_scanner.py --url "http://example.com?id=1" --verbose

    Scan multiple URLs with proxy:
    bash
    Copy

    python sql_scanner.py --urls targets.txt --proxy "http://localhost:8080" --threads 20

    Full scan with custom payloads:
    bash
    Copy

    python sql_scanner.py --urls targets.txt --payloads my_payloads.txt --report scan_results.html

📊 Sample Report

HTML Report Preview
Includes:

    ✅ Vulnerable URLs

    💉 Successful payloads

    🖥️ Server IPs with geolocation

    📊 Response codes and error patterns

⚠️ Legal Disclaimer

This tool is for authorized security testing only. Unauthorized use against websites without permission is illegal. The developers assume no liability for misuse.
🤝 Contributing

Pull requests welcome! Please follow ethical guidelines and disclose vulnerabilities responsibly.
📜 License

MIT License - Use responsibly and ethically.
