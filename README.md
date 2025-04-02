SQL Injection Scanner
Description

An advanced SQL injection scanner that tests URLs for potential SQL injection vulnerabilities. The tool supports multi-threading, proxy configuration, and generates detailed HTML reports with IP information.
Features

    Tests multiple URLs with various SQL injection payloads

    Multi-threaded scanning for faster results

    Proxy support for anonymity

    IP address detection and geolocation details

    HTML report generation

    Verbose output mode for debugging

    User-agent rotation to avoid detection

Requirements

    Python 3.x

    Required Python packages:

        requests

        beautifulsoup4

        colorama

Installation

    Clone the repository or download the script

    Install required packages:
    bash
    Copy

    pip install requests beautifulsoup4 colorama

Usage
Copy

python sql_scanner.py [options]

Options:
  --urls FILE       Path to file containing URLs to test
  --url URL         Single URL to test
  --payloads FILE   Path to file containing SQL injection payloads (default: payloads.txt)
  --proxy PROXY     Proxy to use for requests (e.g., http://127.0.0.1:8080)
  --threads NUM     Number of threads to use (default: 10)
  --verbose         Enable verbose output
  --report FILE     Path to save the HTML report (default: report.html)

Examples

    Scan a single URL:
    bash
    Copy

    python sql_scanner.py --url "http://example.com/page.php?id=1"

    Scan multiple URLs from a file:
    bash
    Copy

    python sql_scanner.py --urls urls.txt --payloads custom_payloads.txt --threads 20

    Scan with proxy and verbose output:
    bash
    Copy

    python sql_scanner.py --urls urls.txt --proxy "http://127.0.0.1:8080" --verbose

Report

The tool generates an HTML report containing:

    Vulnerable URLs

    Payloads that triggered vulnerabilities

    Status codes

    Error messages

    IP addresses of vulnerable servers

    Geolocation information (city, region, country, ISP)

Disclaimer

This tool is for educational and authorized security testing purposes only. Unauthorized scanning of websites may violate laws and terms of service. Use responsibly and only on systems you have permission to test.
