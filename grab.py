import requests
import threading
import re
from queue import Queue
from colorama import init, Fore, Style

init(autoreset=True)  # Auto-reset color after each print

def print_banner():
    banner = f"""{Fore.CYAN}
  _______       ______ 
 |__   __|/\   |  ____|
    | |  /  \  | |__   
    | | / /\ \ |  __|  
    | |/ ____ \| |     
    |_/_/    \_\_|                         
    Team Anon Force
 
{Style.RESET_ALL}
{Fore.MAGENTA}         Coded by {Fore.YELLOW}http://t.me/Professor6T9
{Fore.MAGENTA}         GitHub   {Fore.YELLOW}https://github.com/Professor6T9{Style.RESET_ALL}
      Find Domains By Wordlist (Legal usage only)
"""
    print(banner)

def fetch_domains(word, output_file, lock):
    base_url = f"https://ipsniper.info/api/v1/domains_similar/{word}"
    urls_to_fetch = Queue()
    urls_to_fetch.put(base_url)
    first_request = True

    while not urls_to_fetch.empty():
        url = urls_to_fetch.get()
        try:
            response = requests.get(url)
            data = response.json()

            if first_request:
                print(f"\n{Fore.GREEN}[+] Word: {Fore.CYAN}{word}")
                print(f"{Fore.GREEN}[+] Results: {Fore.YELLOW}{data.get('results', 0)}")
                first_request = False

            domains = [entry["id"] for entry in data.get("data", [])]
            with lock:
                with open(output_file, "a", encoding="utf-8") as f:
                    for domain in domains:
                        print(f"{Fore.LIGHTWHITE_EX} - {domain}")
                        f.write(domain + "\n")

            next_page_match = re.search(r'"next_page"\s*:\s*"([^"]+)"', response.text)
            if next_page_match:
                next_page_url = next_page_match.group(1)
                if next_page_url != "*":
                    urls_to_fetch.put(next_page_url)

        except Exception as e:
            print(f"{Fore.RED}[!] May Be API Not Responding Properly")

def main():
    print_banner()
    input_file = input(f"{Fore.CYAN}Enter wordlist: ").strip()
    output_file = "domain.txt"
    num_threads = 5
    threads = []
    lock = threading.Lock()

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File '{input_file}' not found.")
        return

    print(f"\n{Fore.LIGHTGREEN_EX}[*] Starting with {len(words)} words using {num_threads} threads...\n")

    for word in words:
        t = threading.Thread(target=fetch_domains, args=(word, output_file, lock))
        threads.append(t)
        t.start()

        while threading.active_count() > num_threads:
            pass

    for t in threads:
        t.join()

    print(f"\n{Fore.LIGHTMAGENTA_EX}[+] Done! Domains saved in {Fore.YELLOW}{output_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
