#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  BLACK HAT HACKERS FORCE
  TAG     : BHHF
  Tool    : IP TO LOCATION
  Creator : Prime X Karlo
  Team    : BLACK HAT HACKERS FORCE
  Version : 1.0
  Note    : IP-ভিত্তিক আনুমানিক লোকেশন (শহর/এলাকা স্তর)
============================================================
"""

import os
import sys
import json
import socket
import urllib.request


# ---------- Colors ----------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"


# ---------- Banner ----------
def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{C.RED}{C.BOLD}
    ██████╗ ██╗  ██╗██╗  ██╗███████╗
    ██╔══██╗██║  ██║██║  ██║██╔════╝
    ██████╔╝███████║███████║█████╗
    ██╔══██╗██╔══██║██╔══██║██╔══╝
    ██████╔╝██║  ██║██║  ██║██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
{C.RESET}{C.WHITE}{C.BOLD}   BLACK HAT HACKERS FORCE{C.RESET}
{C.YELLOW}   ──────────────────────────────────────{C.RESET}
{C.MAGENTA}      TAG     : {C.BOLD}BHHF{C.RESET}
{C.GREEN}      Tool    : {C.BOLD}IP TO LOCATION{C.RESET}
{C.GREEN}      Creator : {C.BOLD}Prime X Karlo{C.RESET}
{C.GREEN}      Team    : {C.BOLD}BLACK HAT HACKERS FORCE{C.RESET}
{C.GREEN}      Version : {C.BOLD}1.0{C.RESET}
{C.YELLOW}   ──────────────────────────────────────{C.RESET}
""")


# ---------- Helper: domain → IP ----------
def resolve_host(target):
    """ডোমেইন দিলে IP বের করে, IP দিলে সেটাই ফেরত দেয়"""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


# ---------- Core: IP lookup ----------
def lookup_ip(ip):
    """ip-api.com থেকে তথ্য আনে"""
    url = f"http://ip-api.com/json/{ip}?fields=status,message,continent,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,query"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BHHF-IPTool/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"status": "fail", "message": str(e)}


# ---------- Print result ----------
def print_result(data, original=None):
    if data.get("status") != "success":
        print(f"{C.RED}[!]{C.RESET} Lookup failed: {data.get('message','unknown error')}")
        return

    lat = data.get("lat", 0)
    lon = data.get("lon", 0)
    maps = f"https://www.google.com/maps?q={lat},{lon}"

    print()
    print(f"  {C.YELLOW}┌──────────── IP INFORMATION ────────────┐{C.RESET}")
    if original and original != data.get("query"):
        print(f"  {C.CYAN}Host       :{C.RESET} {original}")
    print(f"  {C.CYAN}IP         :{C.RESET} {C.BOLD}{data.get('query','-')}{C.RESET}")
    print(f"  {C.CYAN}Continent  :{C.RESET} {data.get('continent','-')}")
    print(f"  {C.CYAN}Country    :{C.RESET} {data.get('country','-')} ({data.get('countryCode','-')})")
    print(f"  {C.CYAN}Region     :{C.RESET} {data.get('regionName','-')} [{data.get('region','-')}]")
    print(f"  {C.CYAN}District   :{C.RESET} {data.get('district','-') or '-'}")
    print(f"  {C.CYAN}City       :{C.RESET} {C.GREEN}{C.BOLD}{data.get('city','-')}{C.RESET}")
    print(f"  {C.CYAN}ZIP / Postal:{C.RESET} {data.get('zip','-') or '-'}")
    print(f"  {C.CYAN}Latitude   :{C.RESET} {lat}")
    print(f"  {C.CYAN}Longitude  :{C.RESET} {lon}")
    print(f"  {C.CYAN}Timezone   :{C.RESET} {data.get('timezone','-')}")
    print(f"  {C.CYAN}ISP        :{C.RESET} {data.get('isp','-')}")
    print(f"  {C.CYAN}Org        :{C.RESET} {data.get('org','-')}")
    print(f"  {C.CYAN}AS         :{C.RESET} {data.get('as','-')}")
    print(f"  {C.YELLOW}└─────────────────────────────────────────┘{C.RESET}")
    print()
    print(f"  {C.MAGENTA}Map Link   :{C.RESET} {C.BLUE}{maps}{C.RESET}")
    print()


# ---------- Main ----------
def main():
    banner()

    print(f"{C.WHITE}  Enter an IP address or a domain name.{C.RESET}")
    print(f"{C.WHITE}  Type {C.GREEN}'myip'{C.WHITE} to look up your own public IP.{C.RESET}")
    print(f"{C.WHITE}  Type {C.RED}'exit'{C.WHITE} to quit.{C.RESET}\n")

    while True:
        try:
            target = input(f"{C.CYAN}[?]{C.RESET} Target IP / Domain: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.RED}[!]{C.RESET} Exiting.")
            break

        if not target:
            print(f"{C.RED}[!]{C.RESET} Empty input.")
            continue

        if target.lower() in ("exit", "quit", "q"):
            print(f"\n{C.MAGENTA}  BHHF | Prime X Karlo | BLACK HAT HACKERS FORCE{C.RESET}")
            print(f"{C.YELLOW}  Goodbye.{C.RESET}\n")
            break

        # নিজের IP
        if target.lower() == "myip":
            data = lookup_ip("")
            print_result(data, "my public IP")
            continue

        # IP চেক
        ip_to_use = None
        if target.replace(".", "").isdigit() and target.count(".") == 3:
            ip_to_use = target
        else:
            ip_to_use = resolve_host(target)
            if not ip_to_use:
                print(f"{C.RED}[!]{C.RESET} Could not resolve: {target}")
                continue

        data = lookup_ip(ip_to_use)
        print_result(data, target if target != ip_to_use else None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.RED}[!]{C.RESET} Stopped.")
        sys.exit(0)