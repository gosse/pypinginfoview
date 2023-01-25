from icmplib import ping
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.table import Table
import time
import argparse
import ipaddress
import socket

hosts = [
    "1.1.1.1",
    "1.0.0.1",
    "8.8.8.8",
    "8.8.4.4",
    "canireachthe.net",
    "208.67.220.220",
    "208.67.222.222",
    "153.106.4.1"
]

results = {}

def is_ip_address(ip):
   try:
       ip_object = ipaddress.ip_address(ip)
       return True
   except ValueError:
       return False

def ping_host(host, ping_timeout):
    result = ping(host, count=1, privileged=False, timeout=ping_timeout)
    results[host]["is_alive"] = result.is_alive
    if result.is_alive:
        results[host]["history"].append(":white_check_mark:")
    else:
        results[host]["history"].append(":x:")
    results[host]["packets_sent"] += result.packets_sent
    results[host]["packets_received"] += result.packets_received
    results[host]["packet_loss"] = (
        (results[host]["packets_sent"] - results[host]["packets_received"])
        / results[host]["packets_sent"]
    ) * 100
    results[host]["rtts"].append(result.avg_rtt)
    # avg = sum(number_list)/len(number_list)
    results[host]["last_rtt"] = result.avg_rtt
    results[host]["average_rtt"] = sum(results[host]["rtts"]) / len(
        results[host]["rtts"]
    )
    # print(results)


def generate_table(ping_timeout) -> Table:
    # Make the table
    table = Table()
    table.add_column("Alive")
    table.add_column("IP Addr")
    table.add_column("Hostname")
    table.add_column("Last 10")
    table.add_column("Loss")
    table.add_column("Received")
    table.add_column("Sent")
    table.add_column("Last RTT")
    table.add_column("Mean RTT")

    # Working loop through the host list
    for host in hosts:
        ping_host(host, ping_timeout)
        table.add_row(
            f"[green]UP" if results[host]["is_alive"] else "[red]DOWN",
            f"{results[host]['ip_address']}",
            f"{results[host]['hostname']}",
            # history = ()
            f"{''.join(results[host]['history'][-10:])}",
            # result = ''.join(str(item) for item in list_of_integers)
            f"{results[host]['packet_loss']}%",
            f"{results[host]['packets_received']}",
            f"{results[host]['packets_sent']}",
            f"{round(results[host]['last_rtt'], 2)}",
            f"{round(results[host]['average_rtt'], 2)}",
        )
    return table

def setup():
    for host in hosts:
        results[host] = {}
        if is_ip_address(host):
            results[host]['ip_address'] = host
            hostname = socket.gethostbyaddr(host)
            results[host]['hostname'] = hostname[0]
        else:
            results[host]['hostname'] = host
            ip_address = socket.gethostbyname(host)
            results[host]['ip_address'] = ip_address
        results[host]["history"] = []
        results[host]["packets_sent"] = 0
        results[host]["packets_received"] = 0
        results[host]["rtts"] = []

def main(args):
    with Live(generate_table(args.timeout), refresh_per_second=2) as live:
        while True:
            time.sleep(args.interval)
            live.update(generate_table(args.timeout))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--interval", type=int, default=1, help="ping interval", metavar="i"
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=2, help="ping timeout", metavar="i"
    )
    args = parser.parse_args()
    setup()
    main(args)
