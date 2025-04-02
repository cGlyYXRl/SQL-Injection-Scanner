import argparse
import random
import socket
import threading

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global variables
vulnerable_urls = []
lock = threading.Lock()

# List of user agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

# Function to load payloads from a file
def load_payloads(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Function to get IP details using ipinfo.io
def get_ip_details(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return None

# Function to test for SQL injection
def test_sql_injection(url, payload, proxy=None, verbose=False):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    test_url = f"{url}{payload}"
    try:
        response = requests.get(
            test_url,
            headers=headers,
            proxies=proxy,
            timeout=10,
        )
        if response.status_code == 200:
            error_messages = [
                "SQL syntax",
                "mysql_fetch",
                "syntax error",
                "unexpected end",
                "quoted string",
                "ORA-00933",
                "SQL command not properly ended",
            ]
            for error in error_messages:
                if error in response.text:
                    # Extract IP address from the URL
                    domain = test_url.split("/")[2]
                    ip = socket.gethostbyname(domain)
                    ip_details = get_ip_details(ip)

                    with lock:
                        vulnerable_urls.append({
                            "url": url,
                            "payload": payload,
                            "status_code": response.status_code,
                            "error": error,  # Ensure this key is used
                            "vulnerable_url": test_url,
                            "ip": ip,
                            "ip_details": ip_details,
                        })
                    if verbose:
                        print(f"{Fore.RED}[!] Potential SQL Injection vulnerability found!{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}Payload: {payload}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}Status Code: {response.status_code}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}Error Detected: {error}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}Vulnerable URL: {test_url}{Style.RESET_ALL}")
                        if ip_details:
                            print(f"{Fore.CYAN}IP Details: {ip_details}{Style.RESET_ALL}")
                    break
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

# Function to generate an HTML report
def generate_html_report(file_path):
    soup = BeautifulSoup("<html><head><title>SQL Injection Scan Report</title></head><body></body></html>", "html.parser")
    h1 = soup.new_tag("h1")
    h1.string = "SQL Injection Scan Report"
    soup.body.append(h1)

    table = soup.new_tag("table", border="1")
    headers = ["URL", "Payload", "Status Code", "Error", "Vulnerable URL", "IP", "IP Details"]
    header_row = soup.new_tag("tr")
    for header in headers:
        th = soup.new_tag("th")
        th.string = header
        header_row.append(th)
    table.append(header_row)

    for entry in vulnerable_urls:
        row = soup.new_tag("tr")
        for key in headers:
            td = soup.new_tag("td")
            if key == "IP Details" and entry["ip_details"]:
                td.string = f"{entry['ip_details'].get('city', 'N/A')}, {entry['ip_details'].get('region', 'N/A')}, {entry['ip_details'].get('country', 'N/A')}, ISP: {entry['ip_details'].get('org', 'N/A')}"
            else:
                # Map headers to dictionary keys
                if key == "Error":
                    td.string = str(entry.get("error", "N/A"))
                else:
                    td.string = str(entry.get(key.lower().replace(" ", "_"), "N/A"))
            row.append(td)
        table.append(row)

    soup.body.append(table)
    with open(file_path, "w") as file:
        file.write(soup.prettify())

# Main function
def main():
    parser = argparse.ArgumentParser(description="Advanced SQL Injection Scanner with IP Details")
    parser.add_argument("--urls", help="Path to the file containing URLs to test")
    parser.add_argument("--url", help="Single URL to test")
    parser.add_argument("--payloads", default="payloads.txt", help="Path to the file containing SQL injection payloads")
    parser.add_argument("--proxy", help="Proxy to use for requests (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--report", default="report.html", help="Path to save the HTML report")
    args = parser.parse_args()

    # Load URLs
    if args.url:
        urls = [args.url]
    elif args.urls:
        urls = load_payloads(args.urls)
    else:
        print(f"{Fore.RED}Error: Either --url or --urls must be specified.{Style.RESET_ALL}")
        return

    # Load payloads
    payloads = load_payloads(args.payloads)

    # Configure proxy
    proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    # Test URLs with payloads using multi-threading
    threads = []
    for url in urls:
        for payload in payloads:
            thread = threading.Thread(
                target=test_sql_injection,
                args=(url, payload, proxy, args.verbose),
            )
            threads.append(thread)
            thread.start()
            if len(threads) >= args.threads:
                for t in threads:
                    t.join()
                threads = []

    # Wait for remaining threads to complete
    for thread in threads:
        thread.join()

    # Generate HTML report
    generate_html_report(args.report)
    print(f"{Fore.GREEN}[+] Scan completed. Report saved to {args.report}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
