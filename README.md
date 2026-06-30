# PythonSpeedScrape

# codee.py
codee.py is a small Python wrapper for masscan that performs fast ICMP host discovery against a list of IPv4 addresses and writes the results to CSV.

This kind of tool is used in network administration and security research to audit which hosts on a network quickly are responsive.

## ✨ Features

- **Blazing Fast**: Capable of sending 1.6M+ packets/sec on bare metal Linux.
- **Zero Python Dependencies**: Uses only the Python Standard Library.
- **Clean CSV Output**: Automatically parses `masscan`'s raw JSON output into a sorted, easy-to-read CSV file.
- **Pause & Resume**: Safely interrupt long scans with `Ctrl-C`. State is saved to `paused.conf` and can be resumed later.
- **Direct File Input**: Reads target IPs directly from a text file (no chunking or complex logic required).
- **Comprehensive Status**: Reports exactly which IPs responded and explicitly marks non-responding IPs as "dead".

## Installations

Install massacan
use any method suitable for your computer. Examples;
**Debian / Ubuntu:**
```bash
sudo apt update
sudo apt install masscan

## Usage

Creates a text file containing your target IPs (line by line). 
By default, the script looks for a file named v4.addrs.
# v4.addrs example
8.8.8.8
1.1.1.1
192.168.1.0/24
10.0.0.1

## Command-Line Arguments

--input
v4.addrs
Path to the input text file containing target IPs/CIDRs (one per line).
--output
results.csv
Path to the output CSV file where results will be saved.
--rate
5000
Packets per second to send. Increase with caution on metered/slow links.
--wait
10
Seconds to wait for late replies after all packets have been transmitted.
--resume
False
Resume a previously paused scan using the paused.conf file.

How the CSV file should look like:
ip,status
1.1.1.1,alive
8.8.8.8,alive
10.0.0.5,dead

At the end of the scan the terminal should give you:
Done!
Total scanned : 1,000,000
Alive         : 45,231  (4.5%)
Dead          : 954,769
Results       → results.csv

## Tips and trouble shooting

 Permission Denied: Ensure you are running the script with sudo. masscan will fail silently or throw an error if it cannot open raw sockets.
Network Congestion: If you set --rate too high (e.g., 100000) on a standard home/office connection, your router may drop packets, or your ISP may throttle/block your connection. Start at 5000 and increase gradually.
Firewalls: Remember that many hosts drop ICMP Echo Requests (ping) at the firewall level. "Dead" in this context means "Did not respond to ICMP", not necessarily "Powered off".
Missing masscan: If you get the ERROR: masscan not found message, ensure it is installed and available in your system's PATH.

## Warnings

Use this tool responsibly and ethically.
Scanning networks you do not own or do not have explicit, written permission to scan is illegal in many jurisdictions and violates the terms of service of most ISPs and cloud providers. The author of this script assumes no liability for how this tool is used. Always ensure you are authorized to perform host discovery on the target IP ranges.