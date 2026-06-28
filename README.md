# IP Blacklist Checker

A Python/Tkinter desktop application that checks whether an IP address is blacklisted, using both a **local file** and a **live DNSBL lookup**.

## Features

- IPv4 format validation (with regex)
- Local blacklist check (`ip_blacklist.txt`)
- Online check — Spamhaus DNSBL lookup (via the `socket` module, no API key required)
- History tracking (automatically saved to a JSON file)
- Clean and simple Tkinter interface

## Libraries Used

- `os`
- `re`
- `socket`
- `json`
- `datetime`
- `tkinter`

## Installation & Usage

```bash
git clone https://github.com/YusufKebabci/ip-blacklist-kontrol.git
cd ip-blacklist-kontrol
python ip_kontrol.py
```


## How It Works

1. The user enters an IP address.
2. The program validates the IP format.
3. The IP is checked against the local `ip_blacklist.txt` file.
4. The IP is reversed and queried against `zen.spamhaus.org` as a DNS lookup.
5. The result is displayed on screen and saved to `ip_gecmis.json`.

## Project Structure

```
ip-blacklist-kontrol/
├── ip_kontrol.py        # Main application
├── ip_blacklist.txt     # Sample local blacklist
├── README.md
└── .gitignore
```
