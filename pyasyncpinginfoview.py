import asyncio
from icmplib import async_ping
from icmplib import ping
from icmplib import ping
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.table import Table
import time
import argparse
import ipaddress
import socket
import asyncio


async def async_ping_host(host, results, ping_timeout):
    result = await async_ping(host, privileged=False, count=1, timeout=ping_timeout)
    update_results(host, result, results)


def is_ip_address(ip):
    try:
        ip_object = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def update_results(host, result, results):
    results[host]["is_alive"] = result.is_alive
    if result.is_alive:
        results[host]["history"].append(":white_check_mark:")
    else:
        results[host]["history"].append(":x:")
    results[host]["packets_sent"] += result.packets_sent
    results[host]["packets_received"] += result.packets_received
    results[host]["packet_loss"] = (
        results[host]["packets_sent"] - results[host]["packets_received"]
    ) / results[host]["packets_sent"]
    results[host]["rtts"].append(result.avg_rtt)
    results[host]["last_rtt"] = result.avg_rtt
    results[host]["average_rtt"] = sum(results[host]["rtts"]) / len(
        results[host]["rtts"]
    )
    return results


# Ping the host and update the results dict with result
def ping_host(host, results, ping_timeout):
    result = ping(host, count=1, privileged=False, timeout=ping_timeout)
    results = update_results(host, result, results)


def generate_table(hosts, results, ping_timeout) -> Table:
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
        table.add_row(
            f"[green]UP" if results[host]["is_alive"] else "[red]DOWN",
            f"{results[host]['ip_address']}",
            f"{results[host]['hostname']}",
            # history = ()
            f"{''.join(results[host]['history'][-10:])}",
            # result = ''.join(str(item) for item in list_of_integers)
            f"{results[host]['packet_loss'] * 100}%",
            f"{results[host]['packets_received']}",
            f"{results[host]['packets_sent']}",
            f"{round(results[host]['last_rtt'], 2)}",
            f"{round(results[host]['average_rtt'], 2)}",
        )
    return table


def setup(hosts):
    results = {}
    for host in hosts:
        results[host] = {}
        results[host]["is_alive"] = False
        try:
            if is_ip_address(host):
                results[host]["ip_address"] = host
                hostname = socket.gethostbyaddr(host)
                results[host]["hostname"] = hostname[0]
            else:
                results[host]["hostname"] = host
                ip_address = socket.gethostbyname(host)
                results[host]["ip_address"] = ip_address
        except Exception as e:
            # If the name/IP resolution doesn't work, set both as whatever input is given
            results[host]["ip_address"] = host
            results[host]["hostname"] = host
        results[host]["history"] = []
        results[host]["packets_sent"] = 0
        results[host]["packets_received"] = 0
        results[host]["packet_loss"] = 0
        results[host]["rtts"] = []
        results[host]["last_rtt"] = 0
        results[host]["average_rtt"] = 0
    return results


def process_hosts(file):
    with open(file, "r") as f:
        hosts = f.read().splitlines()
    return hosts


async def main(args):
    if args.hostfile:
        hosts = process_hosts(args.hostfile)
    else:
        hosts = [
            "1.1.1.1",
            "1.0.0.1",
            "8.8.8.8",
            "8.8.4.4",
            "canireachthe.net",
            "208.67.220.220",
            "208.67.222.222",
        ]
    results = setup(hosts)
    with Live(
        generate_table(hosts, results, args.timeout), refresh_per_second=2
    ) as live:
        i = 0
        while True:
            i += 1
            time.sleep(args.interval)
            #         results = ping_host(host, results, ping_timeout)
            for host in hosts:
                await asyncio.gather(async_ping_host(host, results, args.timeout))
            live.update(generate_table(hosts, results, args.timeout))
            if args.number > 0 and i > args.number:
                exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", type=int, default=1, help="ping interval")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="ping timeout")
    parser.add_argument(
        "-f", "--hostfile", type=str, help="file of hosts, one line per host"
    )
    args = parser.parse_args()
    # main(args)
    asyncio.run(main(args))
